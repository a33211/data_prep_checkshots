import pandas as pd

df = pd.read_excel("Working_example.xlsx", header=1)
df2 = pd.read_excel("stratigraphy_Bairak35.xlsx", header=1)
#df = df[df['Т150'] > 1000]
#print(df)

DZ = None
DT = None
DZ_list = []
DT_list = []
Vint_list = []
#Vint = DZ/DT*2000
wt_increment = 2000

#time_increment = input('Please specify if time column is TWT format. Entrer True/False')
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
print(df2.describe())
#df.to_excel('test.xlsx')

#smoothing x3, x5, triangular filtring
#structure hints for solo work



