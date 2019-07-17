import psi4
import datetime
import time

t = datetime.datetime.fromtimestamp(time.time())
 
psi4.set_num_threads(nthread=2)
psi4.set_memory('2GB')
psi4.set_output_file('{}{}{}_{}{}.log'.format(t.year, t.month, t.day, t.hour, t.minute))

m_xylene = psi4.geometry('''
0 1
H          1.28968       -0.58485        2.54537
C          0.72665       -0.53821        1.60812
C         -0.66059       -0.63788        1.62278
H         -1.18866       -0.76325        2.57379
C         -1.38281       -0.57923        0.43824
H         -2.47598       -0.65808        0.46597
C         -0.70870       -0.41532       -0.78014
C         -1.44994       -0.24691       -1.99137
C          0.68999       -0.31852       -0.79417
H          1.23196       -0.19170       -1.73873
C          1.39668       -0.37916        0.39958
C          2.48879       -0.30069        0.38763
H         -2.49493       -0.35404       -1.78784
H         -1.14694       -0.98824       -2.70096
H         -1.26259        0.72757       -2.39162
H          2.86211       -0.36704        1.38820
H          2.77426        0.63858       -0.03801
H          2.89720       -1.09694       -0.19896
''')
 
psi4.optimize('b3lyp/6-311+g(d,p)', molecule=m_xylene)