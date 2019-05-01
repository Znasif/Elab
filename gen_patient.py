import json
import numpy as np
import random

s = [chr(i) for i in range(ord("a"), ord("z")+1)]
t = [chr(i) for i in range(ord("A"), ord("Z")+1)]
nums = [str(i) for i in range(10)]

with open("Data/patient.json", "r") as f:
    a = f.read()
    history = json.loads(a)

with open("extras/m.json", "r") as f:
    a = f.read()
    med = json.loads(a)

with open("extras/u.json", "r") as f:
    a = f.read()
    lab = json.loads(a)

def gen(nm):
    return ''.join(np.random.choice(s+t+nums, nm))

def randig(nm):
    return ''.join(np.random.choice(nums, nm))

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
m_num = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
year = 2019
tm_hr = 8
th_min = 60
th_sec = 60
endst = [" AM UTC+6", " PM UTC+6"]

carriers_ = ["017", "013", "019", "018", "016", "015"]
gender = ["male", "female", "others"]
marital_status = ["married", "unmarried", "divorced", "widowed"]

last_names = []
male_names = []
female_names = []

class Date_:
    @staticmethod
    def add_time():
        tm = ""
        tm_ = random.randint(0, 11)
        tm += month[tm_]+" "+str(random.randint(1, m_num[tm_]))+", "+str(random.randint(2011, year))+" at "
        tm += str(random.randint(1,tm_hr))+":"+str(random.randint(0, 5))+str(random.randint(0, 9))
        tm += ":"+str(random.randint(0, 5))+str(random.randint(0, 9))
        tm += str(endst[random.randint(0, 1)])
        return tm
    
    @staticmethod
    def age():
        return ''.join(np.random.choice(nums, 2))
    
class Phone_:
    st_ = "+88"
    phn_nums = []

    @staticmethod
    def add_phone():
        ph_ = Phone_.st_+np.random.choice(carriers_)+randig(8)
        if ph_ not in Phone_.phn_nums:
            Phone_.phn_nums.append(ph_)
            return ph_
        return Phone_.add_phone()

class Name_:
    @staticmethod
    def add_name(flag):
        i_ = np.random.choice(last_names)
        if(flag==0):
            j_ = np.random.choice(male_names)
        else:
            j_ = np.random.choice(female_names)
        return j_+" "+i_


with open("extras/last.txt", "r") as f:
    a = f.readlines()
    for i in a:
        last_names.append(i.split("\"")[1])
with open("extras/female.txt", "r") as f:
    a = f.readlines()
    for i in a:
        female_names.append(i.split("\"")[1])
with open("extras/male.txt", "r") as f:
    a = f.readlines()
    for i in a:
        male_names.append(i.split("\"")[1])


# print(Date_.add_time())
# print(Phone_.add_phone())
# print(Name_.add_name(random.randint(0,1)))

patient = {}

def pat(ns):
    for i in range(ns):
        id = gen(20)
        patient[id] = {}
        patient[id]["ID"] = id
        patient[id]["Phone"] = Phone_.add_phone()
        gn = random.randint(0, 1)
        patient[id]["Gender"] = gender[gn]
        patient[id]["MaritalStatus"] = marital_status[random.randint(0, 3)]
        patient[id]["Age"] = Date_.age()
        patient[id]["Name"] = Name_.add_name(gn)
    return patient

def hist(ns):
    cnt = 0
    pt = pat(ns)
    pl = list(pt.keys())
    ml = list(med.keys())
    ll = list(lab.keys())

    his_data = {}

    for i in history:
        if (cnt >= ns):
            break
        cnt += 1
        # print(history[i][0], history[i][1])
        # print(pl[cnt-1], ml[cnt-1], ll[cnt-1])

        id = gen(20)
        his_data[id] = {}
        his_data[id]["patient_ID"] = pl[cnt-1]
        his_data[id]["medicine_ID"] = list(np.random.choice(ml, random.randint(0, 3)))
        his_data[id]["labtest_ID"] = list(np.random.choice(ll, random.randint(0, 3)))
        his_data[id]["symptom_ID"] = history[i][0]
        his_data[id]["doctor_ID"] = gen(20)
        his_data[id]["visit_time"] = Date_.add_time()
    
    with open("history.json", 'w+') as f:
        json.dump(his_data, f)
    
    with open("patient_ids.json", 'w+') as f:
        json.dump(pt, f)

    return his_data, pt

# pat(2)
print(hist(2))