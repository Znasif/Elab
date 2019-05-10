import os, sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import np_utils
from keras import backend as K
import tensorflow as tf
import pandas as pd
import numpy as np
import random as rn
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import collections
sys.stderr = stderr

#####################
CLOUD_SETUP = False
#####################

def exit_tf():
    K.clear_session()
    return

def cloud_setup(folder="Data/"):
    if CLOUD_SETUP!=True:
        return False
    cred = credentials.Certificate(folder+'elabCre.json')
    firebase_admin.initialize_app(cred,  {'storageBucket': 'elab-237906.appspot.com'})
    Data.bucket = storage.bucket()
    if "Data" not in os.listdir():
        os.mkdir(folder)
    for i in Data.listfiles:
        if down(folder+i):
            continue
        exit(0)

def sort_dict(x):
    sorted_x = sorted(x.items(), key=lambda kv: kv[1])[::-1]
    return dict(collections.OrderedDict(sorted_x))

def down(filepath):
    if CLOUD_SETUP!=True:
        return False
    try:
        blob = Data.bucket.blob(filepath)
        blob.download_to_filename(filepath)
        return True
    except:
        return False

def up(filepath):
    if CLOUD_SETUP!=True:
        return False
    try:
        blob = Data.bucket.blob(filepath)
        blob.upload_from_filename(filepath)
        print(filepath)
        return True
    except:
        return False

class Data:
    symptom_name_to_id = {}
    symptom_id_to_name = {}
    disease_name_to_id = {}
    disease_id_to_name = {}
    symptom_pattern = {}
    diseases = {}
    bucket = None
    listfiles = ["diagnostics.h5", "diseases.json", "patient.json", "symptom_pattern.json"]
    folder_ = "Data/"
    log_folder = "Logs/"
    prepared = None

    @staticmethod
    def read_patient_data():
        with open(Data.folder_+"patient.json", "r") as f:
            a = f.read()
            patient_data = json.loads(a)
        return patient_data
    
    @staticmethod
    def write_patient_data(patient_data):
        with open(Data.folder_+"patient.json", 'w+') as f:
            json.dump(patient_data, f)
        return up(Data.folder_+"patient.json")

    @staticmethod
    def read_disease_data():
        with open(Data.folder_+"diseases.json", "r") as f:
            a = f.read()
            Data.diseases = json.loads(a)

    @staticmethod
    def write_disease_data(diseases):
        with open(Data.folder_+"diseases.json", 'w+') as f:
            json.dump(diseases, f)
        return up(Data.folder_+"diseases.json")

    @staticmethod
    def read_symptom_pattern():
        with open(Data.folder_+"symptom_pattern.json", "r") as f:
            a = f.read()
            Data.symptom_pattern = json.loads(a)
        return Data.symptom_pattern
    
    @staticmethod
    def write_symptom_pattern(symptom_pattern):
        with open(Data.folder_+"symptom_pattern.json", 'w+') as f:
            json.dump(symptom_pattern, f)
        return up(Data.folder_+"symptom_pattern.json")

    @staticmethod
    def load_diagnostics():
        return load_model(Data.folder_+'diagnostics.h5')

    @staticmethod
    def save_diagnostics(diagnostics_model):
        diagnostics_model.save(Data.folder_+'diagnostics.h5')
        del diagnostics_model
        return up(Data.folder_+"diagnostics.h5")

    @staticmethod
    def write_log():
        time_ = time.asctime( time.localtime(time.time()))
        time_ = time_.replace(':', '-')
        with open(Data.log_folder+time_+".txt", "w+") as f:
            f.write(Report.log)
        return up(Data.log_folder+time_+".txt")

    @staticmethod
    def prepare_keys():
        Data.read_disease_data()
        Data.read_symptom_pattern()

        for j, i in enumerate(Data.symptom_pattern):
            Data.symptom_id_to_name[j] = i
            Data.symptom_name_to_id[i] = j

        disease_num = 0

        for i in Data.diseases.keys():
            if(Data.disease_name_to_id.get(i) == None):
                Data.disease_name_to_id[i] = disease_num
                Data.disease_id_to_name[disease_num] = i
                disease_num += 1


class Report:
    toLog = True
    log = ""
    @staticmethod
    def print(str_, *argv):
        if(Report.toLog):
            Report.log += str(str_) + "\n"
        else:
            print(str_)

    @staticmethod
    def sort_symptom_ids(symptom_names):
        symptom_ids = [Data.symptom_name_to_id[i] for i in symptom_names]
        return sorted(symptom_ids)

    @staticmethod
    def find_symptom_overlap(symptom_ids_1, symptom_ids_2):
        symptom_properties = []
        symptom_ids = []
        i, j = 0, 0
        i_, j_ = len(symptom_ids_1), len(symptom_ids_2)
        while(i<i_ and j<j_):
            if(symptom_ids_1[i]==symptom_ids_2[j]):
                symptom_name = Data.symptom_id_to_name[symptom_ids_1[i]]
                symptom_properties.append([symptom_name, Data.symptom_pattern[symptom_name]])
                symptom_ids.append(symptom_ids_1[i])
                i += 1
                j += 1
            elif(symptom_ids_1[i]<symptom_ids_2[j]):
                i += 1
            elif(symptom_ids_1[i]>symptom_ids_2[j]):
                j += 1
        return symptom_properties, symptom_ids

    @staticmethod
    def result(predictions, x_test, y_test=None):
        r = 0
        false_cnt = 0
        diagnosed_patient = []
        Report.log = ""
        for x in predictions:
            mx = -1
            idx = -1
            
            all_ = {}

            for j, i in enumerate(x):
                all_[Data.disease_id_to_name[j]] = i
            
            diagnosed_ = sort_dict(all_)
            diagnosed_patient.append(diagnosed_)
            
            idx = Data.disease_name_to_id[list(diagnosed_.keys())[0]]
            Report.print("\n***********************"+ str(r)+ "***********************\n")
            Report.print("Inferred --> "+ Data.disease_id_to_name[idx])

            symptoms_list = []
            given_symptom_ids = []
            rn = x_test[r].shape[0]

            for j in range(rn):
                if (x_test[r][j] == 1):
                    symptoms_list.append(Data.symptom_id_to_name[j])
                    given_symptom_ids.append(j)
            Report.print(str(symptoms_list))
            inferred_symptom_ids = Report.sort_symptom_ids(Data.diseases[Data.disease_id_to_name[idx]][0])
            symptom_properties, aid = Report.find_symptom_overlap(inferred_symptom_ids, given_symptom_ids)

            # The percentage of given symptoms that is also present in Inferred Disease
            Report.print(str(round(len(aid) / len(inferred_symptom_ids), 2)))

            if (y_test is not None and idx != y_test[r]):
                Report.print("Actual --> "+ Data.disease_id_to_name[int(y_test[r])])
                actual_symptom_ids = Report.sort_symptom_ids(Data.diseases[Data.disease_id_to_name[int(y_test[r])]][0])

                _, bid = Report.find_symptom_overlap(actual_symptom_ids, given_symptom_ids)
                cnames, _ = Report.find_symptom_overlap(aid, bid)

                # The percentage of given symptoms that is also present in Actual Disease
                Report.print(str(round(len(bid) / len(actual_symptom_ids), 2)))

                # The symptoms that are present in both Inferred and Actual Diseases
                Report.print("Overlapping Symptoms "+ str(cnames))
                false_cnt += 1
            else:
                pass
                # Report.print(disease_id_to_name[idx])
            r += 1

            # The percentage of given symptoms that actually contributed to the inference of the disease
            Report.print("Actual Contribution Factor -> "+ str(round(len(aid) / (len(given_symptom_ids)+ 0.000001), 2)))

            # The portion of given symptoms that is also present in Inferred Disease
            Report.print(symptom_properties)

        if (y_test is not None):
            Report.print("\n********\t"+str(1 - false_cnt / predictions.shape[0])+ "\t********")
        Data.write_log()
        
        return diagnosed_patient
        

class Train:
    def model_from_scratch(self):
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
    
    def split_train_test(self, data, test_ratio):
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
    
    def prepare_data(self, patient_data):
        """
        Process data for training
        :param patient_data:
        :return:
        """
        Data.prepare_keys()

        dataset = np.zeros((len(patient_data), len(Data.symptom_pattern)+1))

        for k, i in enumerate(patient_data):
            for j in patient_data[i][0]:
                dataset[k][Data.symptom_name_to_id[j]] = 1
            dataset[k][-1] = Data.disease_name_to_id[patient_data[i][1]]
        
        # Shuffle dataset and convert to Dataframe
        np.random.shuffle(dataset)
        column_names = list(Data.symptom_id_to_name.keys())
        column_names.append("Disease")
        return pd.DataFrame(data=dataset)

    def __init__(self, new_patient, new_model=False):
        """

        :param new_patient:
        :param new_model:
        :return:
        """

        # Load and Update patient data
        Data.prepare_keys()
        patient_data = Data.read_patient_data()
        for id in new_patient:
            to_ids = [Data.symptom_id_to_name[int(i)] for i in new_patient[id]["symptomid"].split(",")]
            patient_data[id] = [to_ids, Data.disease_id_to_name[new_patient[id]["diagnosis"]]]
        Data.write_patient_data(patient_data)
        Data.read_symptom_pattern()

        # process data for training
        np.random.seed(42)
        dataset = self.prepare_data(patient_data)
        train_set, test_set = self.split_train_test(dataset, 0.2)
        train = train_set.values
        x = train[:,0:-1]
        y = train[:,-1]
        y_ = np_utils.to_categorical(y)
        
        if(new_model):
            model = self.model_from_scratch()
        else:
            model = Data.load_diagnostics()

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(x, y_, epochs=2, batch_size=10)

        scores = model.evaluate(x, y_)
        print(f"\n{model.metrics_names[1]}: {scores[1]*100:2f}%")
        
        Data.save_diagnostics(model)

        test = test_set.values
        x_test = test[:, 0:-1]
        y_test = test[:, -1]
        predictions = model.predict(x_test)
        res = Report.result(predictions, x_test, y_test)
        for j, id in enumerate(new_patient):
            new_patient[id]["prediction"] = trim_data(res[j])

        self.prediction = new_patient

class Diagnose:
    count = 0

    def __init__(self, symptom_list):
        """

        :param symptom_list:
        :return:
        """
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        if Diagnose.count == 0:
            Data.prepare_keys()
        
        Diagnose.count += 1
        #print("*************FIRST TIME***********************")

        test_ex = [[Data.symptom_id_to_name[int(i)] for i in symptom_list["symptomid"].split(",")]]
        test_ = np.zeros((len(test_ex), len(Data.symptom_pattern)))

        for i in range(len(test_ex)):
            for j in test_ex[i]:
                test_[i][Data.symptom_name_to_id[j]] = 1
            test_[i][-1] = -1

        # for some reason in a flask app the graph/session needs to be used in the init else it hangs on other threads
        with self.graph.as_default():
            with self.session.as_default():
                self.session.run(tf.global_variables_initializer())
                self.model = Data.load_diagnostics()
                predictions = self.model.predict(test_)
                results = Report.result(predictions, test_)
                self.diagnosis = trim_data(results[0])
        '''
        for j, i in enumerate(symptom_list):
            symptom_list[i] = [symptom_list[i], results[j]]
        '''
        
def rand_():
    s = ""
    for i in range(rn.randint(1, 5)):
        s += str(rn.randint(1, 401))+","
    return s[:-1]

def trim_data(dct):
  thresh_ = .01
  res = {}
  for i in dct:
    if dct[i]>thresh_:
      res[i] = float(f'{dct[i]:.3}')
  return res

def cloud_reply():
    Data.prepare_keys()
    ls_ = [[i.lower(), Data.symptom_name_to_id[i]] for i in Data.symptom_name_to_id.keys()]
    ret = {}
    for i in sorted(sorted(ls_)):
      j = {}
      k, l = i
      j["name"] = k
      j["id"] = l
      ret[l]=j
    return ret

if __name__ == "__main__":
    #symptom_list_ = {'33724': [['syncope', 'vertigo'], 'incontinence'], '33725': [['polyuria', 'polydypsia'], 'diabetes'], '33726': [['tremor', 'intoxication'], 'decubitus ulcer']}
    #print(Train.train(symptom_list_))
    #msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}
    #print(Diagnose.diagnose(msg_))
    # while True:
    #     msg_ = {'symptomid': rand_(), "age": "40", "gender": "male"}
    #     print(msg_)
    #     a = input()
    #     if a== "0":
    #         exit(0)
    #     #msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}
    #     print(Diagnose.diagnose(msg_))
    cloud_setup()
    Data.folder_ = "../Data/"
    Data.log_folder = "../Logs/"
    # for i in range(7):
    #     msg_ = {'symptomid': rand_(), "age": "40", "gender": "male"}
    #     d = Diagnose(msg_)
    #     print(d.diagnosis)
    
    # symptom_list_ = {}
    # ln = len(Data.read_patient_data())
    # for i in range(rn.randint(1, 5)):
    #     symptom_list_[str(ln+i)] = {"symptomid": rand_(), "age": "40", "gender": "male", "diagnosis":rn.randint(0, 20)}
    # print(symptom_list_)
    # t = Train(symptom_list_)
    # print(t.prediction)
    # Data.save_diagnostics(Data.load_diagnostics())

