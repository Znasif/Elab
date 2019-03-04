# -*- coding: utf-8 -*-


from keras.models import Sequential
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

with open("Data/diseases.json", "r") as f:
    a = f.read()
    diagnose = json.loads(a)

patient = {}
num = 0

for i in diagnose:
    j, k = diagnose[i]
    k = int(k)
    n = len(j)
    j = np.array(j)
    for r in range(k):
        p = rn.randint(n//2, n)
        c = rn.sample(range(n), p)
        patient[num] = [list(j[c]), i]
        num += 1

with open("Data/patient.json", 'w+') as f:
   json.dump(patient, f)


with open("Data/freq.json", "r") as f:
    a = f.read()
    symptom = json.loads(a)

with open("Data/patient.json", "r") as f:
    a = f.read()
    patient = json.loads(a)

inv_symp = {}
j = 0
symp_ = symptom.copy()
for i in symptom:
    symptom[i] = [j, i]
    inv_symp[j] = [j, i]
    j += 1

dataset = np.zeros((len(patient), len(symptom)+1))

r = 0
dist_dis = {}
inv_dis = {}

for i in patient:
    for j in patient[i][0]:
        dataset[int(i)][symptom[j][0]] = 1
    if(dist_dis.get(patient[i][1]) == None):
        dist_dis[patient[i][1]] = r
        inv_dis[r] = patient[i][1]
        r += 1
    dataset[int(i)][-1] = dist_dis[patient[i][1]]

#np.savetxt("dataset.txt", dataset, delimiter=',')
h5f = h5py.File('data.h5', 'w')
h5f.create_dataset('dataset_1', data=dataset)
h5f.close()

np.random.shuffle(dataset)

a = list(symp_.keys())
a.append("Disease")

df = pd.DataFrame(data=dataset)
df.columns = a

df.head(3)

def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]
np.random.seed(42)
train_set, test_set = split_train_test(df, 0.2)

print(len(train_set), len(test_set))

train=train_set.values
X=train[:,0:-1]
Y=train[:,-1]
dummy_y = np_utils.to_categorical(Y)
print(dummy_y[0].shape)

model = Sequential()
model.add(Dense(12, input_dim=401, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(134, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X, dummy_y, epochs=20, batch_size=10)

scores = model.evaluate(X, dummy_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

def ret(ls):
  ll = []
  for i in ls:
    ll.append(symptom[i][0])
  return sorted(ll)

def comp(ls, ll):
  ln = []
  i, j = 0, 0
  i_, j_ = len(ls), len(ll)
  while(i<i_ and j<j_):
    if(ls[i]==ll[j]):
      ln.append([inv_symp[ls[i]][1], symp_[inv_symp[ls[i]][1]]])
      i += 1
      j += 1
    elif(ls[i]<ll[j]):
      i += 1
    elif(ls[i]>ll[j]):
      j += 1
  return ln

print(comp(ret(['unsteady gait', 'withdraw', 'hyponatremia']), ret(['withdraw', 'hyponatremia'])))

test=test_set.values
X_test=test[:,0:-1]
Y_test=test[:,-1]
predictions = model.predict(X_test)
r = 0
cnt=0

for x in predictions:
  mx=-1
  idx=-1
  for j,i in enumerate(x):
    if(i>mx):
      mx=i
      idx=j
  
  #print("\n***********************", r, "***********************\n")
  if(idx!=Y_test[r]):
    print("Inferred --> ", inv_dis[idx])
    print("Actual --> ",inv_dis[int(Y_test[r])])
    ls, ll = ret(diagnose[inv_dis[idx]][0]), ret(diagnose[inv_dis[int(Y_test[r])]][0])
    ln = comp(ls, ll)
    ls_symp = []
    rn = X_test[r].shape[0]
    for j in range(rn):
      if(X_test[r][j] == 1):
        ls_symp.append(inv_symp[j])
    print(ls_symp)
    print(round(len(ln)/len(ls), 2), round(len(ln)/len(ll), 2))
    print(ln)
    cnt+=1
  else:
    pass
    #print(inv_dis[idx])
  r +=1
  #print(idx)
print("\n********\t",1-cnt/predictions.shape[0],"\t********")
#rounded = [max(x) for x in predictions]
#print(rounded)
#print(predictions.shape)

#test_ex = []#[["shortness of breath"]]#,"macerated skin","rest pain","myoclonus"]]

test_ex = [[i] for i in symp_.keys()]

test_ = np.zeros((len(test_ex), len(symptom)))

for i in range(len(test_ex)):
    for j in test_ex[i]:
        test_[i][symptom[j][0]] = 1
    test_[i][-1] = -1

y_ = ["peripheral vascular disease","epilepsy","hepatitis C"]

predictions_ex = model.predict(test_)

r=0

for x in predictions_ex:
  mx=-1
  idx=-1
  for j,i in enumerate(x):
    if(i>=mx):
      mx=i
      idx=j
  print(test_ex[r], inv_dis[idx], mx, symp_[test_ex[r][0]])
  r+=1

# %matplotlib inline
import matplotlib.pyplot as plt
plt.bar(symp_.keys(), symp_.values(), color='g')

import operator

sorted_x = sorted(symp_.items(), key=operator.itemgetter(1))

