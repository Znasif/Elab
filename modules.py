from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import np_utils
import pandas as pd
import numpy as np
import random as rn
import json


class Data:
    symptom_name_to_id = {}
    symptom_id_to_name = {}
    disease_name_to_id = {}
    disease_id_to_name = {}
    symptom_pattern = {}
    diseases = {}

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
    def read_disease_data():
        with open("Data/diseases.json", "r") as f:
            a = f.read()
            patient_data = json.loads(a)
        return patient_data

    @staticmethod
    def write_disease_data(diseases):
        with open("Data/diseases.json", 'w+') as f:
            json.dump(diseases, f)

    @staticmethod
    def read_symptom_pattern():
        with open("Data/freq.json", "r") as f:
            a = f.read()
            Data.symptom_pattern = json.loads(a)
        return Data.symptom_pattern
    
    @staticmethod
    def write_symptom_pattern(symptom_pattern):
        with open("Data/symptom_pattern.json", 'w+') as f:
            json.dump(symptom_pattern, f)

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
    def result(predictions, x_test, y_test=None):
        r = 0
        false_cnt = 0
        diagnosed_ = []

        for x in predictions:
            mx = -1
            idx = -1
            for j, i in enumerate(x):
                if (i > mx):
                    mx = i
                    idx = j
            diagnosed_.append(Data.disease_id_to_name[idx])
            # print("\n***********************", r, "***********************\n")
            if (y_test != None and idx != y_test[r]):
                print("Inferred --> ", Data.disease_id_to_name[idx])
                print("Actual --> ", Data.disease_id_to_name[int(y_test[r])])
                inferred_symptom_ids = Report.sort_symptom_ids(Data.diseases[Data.disease_id_to_name[idx]][0])
                actual_symptom_ids = Report.sort_symptom_ids(Data.diseases[Data.disease_id_to_name[int(y_test[r])]][0])
                symptom_ids = Report.find_symptom_overlap(inferred_symptom_ids, actual_symptom_ids)
                symptoms_list = []
                rn = x_test[r].shape[0]
                for j in range(rn):
                    if (x_test[r][j] == 1):
                        symptoms_list.append(Data.symptom_id_to_name[j])
                print(symptoms_list)
                print(round(len(symptom_ids) / len(inferred_symptom_ids), 2), round(len(symptom_ids) / len(actual_symptom_ids), 2))
                print(symptom_ids)
                false_cnt += 1
            else:
                pass
                # print(disease_id_to_name[idx])
            r += 1

        if (y_test != None):
            print("\n********\t", 1 - false_cnt / predictions.shape[0], "\t********")
        return diagnosed_
        

class Train:
    @staticmethod
    def model_from_scratch():
        """
        This generates a model from scratch, ignoring the model available in disk
        :return:
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
        :param data:
        :param test_ratio:
        :return:
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
        :param patient_data:
        :return:
        """
        for j, i in enumerate(Data.symptom_pattern):
            Data.symptom_id_to_name[i] = [j, i]
            Data.symptom_name_to_id[j] = [j, i]

        dataset = np.zeros((len(patient_data), len(Data.symptom_pattern)+1))

        disease_num = 0

        for i in patient_data:
            for j in patient_data[i][0]:
                dataset[int(i)][Data.symptom_id_to_name[j][0]] = 1
            if(Data.disease_name_to_id.get(patient_data[i][1]) == None):
                Data.disease_name_to_id[patient_data[i][1]] = disease_num
                Data.disease_id_to_name[disease_num] = patient_data[i][1]
                disease_num += 1
            dataset[int(i)][-1] = Data.disease_name_to_id[patient_data[i][1]]
        
        # Shuffle dataset and convert to Dataframe
        np.random.shuffle(dataset)
        column_names = list(Data.symptom_id_to_name.keys())
        column_names.append("Disease")
        return pd.DataFrame(data=dataset)

    @staticmethod
    def train(new_patient, new_model=False):
        """

        :param new_patient:
        :param new_model:
        :return:
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
        x = train[:,0:-1]
        y = train[:,-1]
        y_ = np_utils.to_categorical(y)
        
        if(new_model):
            model = Train.model_from_scratch()
        else:
            model = Data.load_diagnostics()

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(x, y_, epochs=20, batch_size=10)

        scores = model.evaluate(x, y_)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        
        Data.save_diagnostics(model)

        test = test_set.values
        x_test = test[:, 0:-1]
        y_test = test[:, -1]
        predictions = model.predict(x_test)
        Report.result(predictions, x_test, y_test)


class Diagnose:
    @staticmethod
    def diagnose(symptom_list):
        """

        :param symptom_list:
        :return:
        """
        model = Data.load_diagnostics()
        test_ex = [symptom_list[i] for i in symptom_list.keys()]

        test_ = np.zeros((len(test_ex), len(Data.symptom_pattern)))

        for i in range(len(test_ex)):
            for j in test_ex[i]:
                test_[i][Data.symptom_name_to_id[j][0]] = 1
            test_[i][-1] = -1
        predictions = model.predict(test_)
        results = Report.result(predictions, test_)
        for j, i in enumerate(symptom_list):
            symptom_list[i] = [symptom_list[i], results[j]]

        return symptom_list


if __name__ == "__main__":
    symptom_list_ = {"60000":["syncope", "vertigo"]}
    Diagnose.diagnose(symptom_list_)
