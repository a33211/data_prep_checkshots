import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("Working_example.xlsx", header=1)
df2 = pd.read_excel("stratigraphy_Bairak35.xlsx")
#df = df[df['Т150'] > 1000]
#print(df)

DZ = None
DT = None
DZ_list = []
DT_list = []
Vint_list = []
#Vint = DZ/DT*2000
wt_increment = 2000

#time_increment = input('Please specify if time column is TWT format. Enter True/False')
# if time_increment = True:
#     wt_increment = 2000
# else:
#     wt_increment = 1000


for i in df.itertuples():
    if DZ:
        cur_DZ = i[1] - DZ
        cur_DT = i[2] - DT
        cur_Vint = (cur_DZ/cur_DT)*wt_increment

        DZ_list.append(cur_DZ)
        DT_list.append(cur_DT)
        Vint_list.append(round(cur_Vint,2))
        DZ, DT = None, None
    if not DZ:
        DZ = i[1]
        DT = i[2]
#print(DZ_list,DT_list, Vint_list, sep = '\n')
DZ_list.insert(0,0)
DT_list.insert(0,0)
Vint_list.insert(0,0)
df['DZ'] = DZ_list
df['DT'] = DT_list
df['Vint'] = Vint_list
df['smooth_3'] = df['Vint'].rolling(window=3).mean()
df['smooth_5'] = df['Vint'].rolling(window=5).mean()
df['exponential'] = df['Vint'].ewm(com=0.5).mean()#to test more
filter5 = np.convolve(np.ones(5), np.ones(5), mode='full')
filter5 = filter5/sum(filter5)
filter7 = np.convolve(np.ones(7), np.ones(7), mode='full')
filter7 = filter7/sum(filter7)
df['filtered'] = np.convolve(df['Vint'], filter7, mode='same')
print(df2)
#df.to_excel('test.xlsx')

#smoothing x3, x5, triangular filtring




plt.plot(df['Vint'],df['Hкаб.'])
# plt.plot(df['smooth_3'],df['Hкаб.'])
# plt.plot(df['smooth_5'],df['Hкаб.'])
plt.plot(df['filtered'],df['Hкаб.'])
plt.plot(df2['MD'])
plt.gca().invert_yaxis()
plt.show()
