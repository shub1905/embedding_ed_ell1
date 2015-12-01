import random
import ConfigParser
import pickle
import editdistance

Config = ConfigParser.ConfigParser()
Config.read('config.cfg')
a = Config.sections()[0]
b = Config.options(a)[0]
N = int(Config.get(a, b))

b = Config.options(a)[1]
Dim = int(Config.get(a, b))

Data = []


def data():
  for i in range(N):
    x = bin(random.getrandbits(Dim))[2:]
    Data.append(x.zfill(Dim))

  ed = {}

  for i in range(N):
    for j in range(i + 1, N):
      key = '{}_{}'.format(i, j)
      ed[key] = editdistance(Data[i], Data[j])

  pickle.dump(ed, open("ed.data", "wb"))
  return Data
