"""
private String comm_id #digit() = 4iEsmeg0tltskI7N4aw0
private String c_mail #mail=gmail.com
private String c_name
private boolean c_status #boolean
private List<String> b_array #list of uid of buildings
private List<String> c_array #split c_name
private List<String> address #list 0 house, 1 road, 2 area, 3 district

private String b_name;
private String b_flatformat; #A1, 1A, 101, 1001, SN
private String b_houseno;
private String b_roadno;
private String b_district;
private String b_area;
private String build_id;
private String comm_id;
private List<String> b_array; #split b_name
private List<String> f_array; #list of flats
"""
import numpy as np
import random
import json

s = [chr(i) for i in range(ord("a"), ord("z")+1)]
t = [chr(i) for i in range(ord("A"), ord("Z")+1)]
nums = [str(i) for i in range(10)]

def gen(nm):
    return ''.join(np.random.choice(s+t+nums, nm))

def gen_mail(nm):
    return nm.split(" ")[0]+"@gmail.com"

def all_s(nm):
    nm_ = nm.split(" ")
    s_ = ""
    p_ = []
    for i in nm_[::-1]:
        s_ = i+" "+s_
        for j in range(1, len(s_)):
            p_.append(s_[:j])
    return p_

def add_b(j, k):
    b_ = {}
    b_["b_houseno"] = k[0]
    b_["b_roadno"] = k[1]
    b_["b_district"] = k[3]
    b_["b_area"] = k[2]
    b_["b_name"] = gen(5)+" "+gen(3)
    b_["build_id"] = gen(20)
    b_["b_flatformat"] = np.random.choice(["A1", "1A", "101", "1001", "SN"])
    b_["comm_id"] = j
    b_["b_array"] = all_s(b_["b_name"])
    b_["b_tfloor"] = random.randint(5, 11)
    b_["b_tflat"] = random.randint(3, 6)
    b_["f_array"] = [gen(20) for i in range(b_["b_tflat"]*b_["b_tfloor"])]
    return b_

def add():
    return [''.join(np.random.choice(nums, random.randint(1, 3))), ''.join(np.random.choice(nums, random.randint(1, 3)))+np.random.choice(["/A", "/B"]), np.random.choice(house).replace("\n", ""), "Dhaka"]

def make_more():
    with open("com.txt", 'r') as f:
        comm = f.readlines()
        f1 = {}
        ff = {}
        comm = [i.replace("\n", "") for i in comm]
        with open("house.txt", 'r') as f:
            house = f.readlines()
            house = [i.replace("\n", "") for i in house]
        for i in comm:
            p = {}
            p["c_name"] = i
            p["comm_id"] = gen(20)
            p["c_status"] = True
            a = add()
            bf = []
            for j in range(random.randint(5, 8)):
                ab = add_b(p["comm_id"], a)
                ff[ab["build_id"]] = ab
                bf.append(ab["build_id"])
            p["b_array"] = bf
            p["c_array"] = all_s(i) + all_s(a[0])+ all_s(a[1])+ all_s(a[2])
            p["address"] = a
            p["c_mail"] = gen_mail(i)
            f1[p["comm_id"]] = p
        with open("build.json", "w") as p1:
            json.dump(ff, p1)
        with open("community.json", "w") as p1:
            json.dump(f1, p1)


def make_pond():
    with open("build.json", 'r') as f:
        b = f.read()
        b = json.loads(b)
        for i in b:
            print(b[i]["b_flatformat"], len(b[i]["f_array"]))

make_pond()