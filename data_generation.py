import random
import ConfigParser


Config = ConfigParser.ConfigParser()
Config.read('config.cfg')
a = Config.sections()[0]
b = Config.options(a)[0]
N = int(Config.get(a,b))

b = Config.options(a)[1]
Dim = int(Config.get(a,b))

Data = []

for i in range(N):
  Data.append(bin(random.getrandbits(Dim))[2:])

print Data[0]