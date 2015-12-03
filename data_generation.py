import random
# import ConfigParser

# Config = ConfigParser.ConfigParser()
# Config.read('config.cfg')

# N = int(Config.get('data size', 'Size'))
# Dim = int(Config.get('data size', 'Dim'))
# delta = float(Config.get('prob', 'delta'))

def data(N, Dim):
  
  if N >= 2**Dim:
      Data = [bin(i)[2:].zfill(Dim) for i in xrange(2**Dim)]
  else:
      Data = [bin(random.getrandbits(Dim))[2:].zfill(Dim) for i in xrange(N)]
  '''
  #ed = {}
  
  ed = numpy.zeros([N,N])
  
  for i in xrange(N):
    for j in xrange(i + 1, N):
      #key = '{}_{}'.format(i, j)
      ed[i,j] = editdistance.eval(Data[i], Data[j])
  pickle.dump(ed, open("ed.data", "wb"))
  '''
  return Data


if __name__ == '__main__':
    import time
    for N in [2,4,8,16]:
        for Dim in [1024,2048,4096,8192]:
            start_time = time.time()
            data()
            print N,Dim,time.time() - start_time