from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import h5py
import pandas as pd
import numpy as np
import random as rn
import json

class Data:
    symptom_name_to_id = {}
    symptom_id_to_name = {}
    disease_num_to_id = {}
    disease_id_to_num = {}
    symptom_pattern = {}

    @staticmethod
    def read_patient_data():
        with open("Data/patient.json", "r") as f:
            a = f.read()
            patient_data = json.loads(a)
        return patient_data
    
    @staticmethod
    def write_patient_data(patient_data):
        with open("Data/patient.json", 'w+') as f:
            json.dump(patient_data, f)

    @staticmethod
    def read_symptom_pattern():
        with open("Data/freq.json", "r") as f:
            a = f.read()
            Data.symptom_pattern = json.loads(a)
        return Data.symptom_pattern
    
    @staticmethod
    def write_symptom_pattern(symptom_pattern):
        with open("Data/symptom_pattern.json", 'w+') as f:
            json.dump(Data.symptom_pattern, f)

    @staticmethod
    def load_diagnostics():
        return load_model('Data/diagnostics.h5')
    
    @staticmethod
    def save_diagnostics(diagnostics_model):
        diagnostics_model.save('Data/diagnostics.h5')
        del diagnostics_model


class Report:
    @staticmethod
    def sort_symptom_ids(symptom_names):
        symptom_ids = [Data.symptom_name_to_id[i] for i in symptom_names]
        return sorted(symptom_ids)

    @staticmethod
    def find_symptom_overlap(symptom_ids_1, symptom_ids_2):
        symptom_ids = []
        i, j = 0, 0
        i_, j_ = len(symptom_ids_1), len(symptom_ids_2)
        while(i<i_ and j<j_):
            if(symptom_ids_1[i]==symptom_ids_2[j]):
                symptom_ids.append([Data.symptom_id_to_name[symptom_ids_1[i]][1], Data.symptom_pattern[Data.symptom_id_to_name[symptom_ids_1[i]][1]]])
                i += 1
                j += 1
            elif(symptom_ids_1[i]<symptom_ids_2[j]):
                i += 1
            elif(symptom_ids_1[i]>symptom_ids_2[j]):
                j += 1
        return symptom_ids

    @staticmethod
    def result(predictions):
        pass
        


class Train:
    @staticmethod
    def model_from_scratch():
        """
        This generates a model from scratch, ignoring the model available in disk
        """
        model = Sequential()
        model.add(Dense(12, input_dim=401, activation='relu'))
        model.add(Dense(20, activation='relu'))
        model.add(Dense(15, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(134, activation='softmax'))
        return model
    
    @staticmethod
    def split_train_test(data, test_ratio):
        """
        Divide data according to test_ratio
        """
        shuffled_indices = np.random.permutation(len(data))
        test_set_size = int(len(data) * test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        return data.iloc[train_indices], data.iloc[test_indices]
    
    @staticmethod
    def prepare_data(patient_data):
        """
        Process data for training
        """
        for j, i in enumerate(Data.symptom_pattern):
            Data.symptom_id_to_name[i] = [j, i]
            Data.symptom_name_to_id[j] = [j, i]

        dataset = np.zeros((len(patient_data), len(Data.symptom_pattern)+1))

        disease_num = 0

        for i in patient_data:
            for j in patient_data[i][0]:
                dataset[int(i)][Data.symptom_id_to_name[j][0]] = 1
            if(Data.disease_num_to_id.get(patient_data[i][1]) == None):
                Data.disease_num_to_id[patient_data[i][1]] = disease_num
                Data.disease_id_to_num[disease_num] = patient_data[i][1]
                disease_num += 1
            dataset[int(i)][-1] = Data.disease_num_to_id[patient_data[i][1]]
        
        # Shuffle dataset and convert to Dataframe
        np.random.shuffle(dataset)
        column_names = list(Data.symptom_id_to_name.keys())
        column_names.append("Disease")
        return pd.DataFrame(data=dataset)

    @staticmethod
    def train(new_patient, new_model=False):
        """
        
        """

        # Load and Update patient data
        patient_data = Data.read_patient_data()
        new_patient_ids = new_patient.keys()
        for id in new_patient_ids:
            patient_data[id] = new_patient[id]
        Data.write_patient_data(patient_data)
        Data.read_symptom_pattern()

        # process data for training
        np.random.seed(42)
        dataset = Train.prepare_data(patient_data)
        train_set, test_set = Train.split_train_test(dataset, 0.2)
        train = train_set.values
        X = train[:,0:-1]
        Y = train[:,-1]
        Y_ = np_utils.to_categorical(Y)
        
        if(new_model):
            model = Train.model_from_scratch()
        else:
            model = Data.load_diagnostics()

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, Y_, epochs=20, batch_size=10)

        scores = model.evaluate(X, Y_)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        
        Data.save_diagnostics(model)