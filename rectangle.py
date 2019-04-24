# -*- coding: utf-8 -*-
import json
m=set()
with open("extras/e.json", "r") as f:
  a = f.read()
  l = json.loads(a)
  print(len(l))


# with open("extras/multiple.json", "r") as f:
#   a = f.read()
#   rl = json.loads(a)
#   m = {}
#   for i in l:
#     m[rl[i]] = l[i]

# with open("extras/diseases.json", "w+") as f:
#   json.dump(m, f)