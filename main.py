import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


# df = df[df['Т150'] > 1000]
# print(df)

def prepare_data(filename: str) -> pd.DataFrame:
    df = pd.read_excel(filename, header=1)
    DZ = None
    DT = None
    DZ_list = []
    DT_list = []
    Vint_list = []
    wt_increment = 2000
    for i in df.itertuples():
        if DZ:
            cur_DZ = i[1] - DZ
            cur_DT = i[2] - DT
            cur_Vint = (cur_DZ / cur_DT) * wt_increment

            DZ_list.append(cur_DZ)
            DT_list.append(cur_DT)
            Vint_list.append(round(cur_Vint, 2))
            DZ, DT = None, None
        if not DZ:
            DZ = i[1]
            DT = i[2]
    DZ_list.insert(0, 0)
    DT_list.insert(0, 0)
    Vint_list.insert(0, 0)
    df['DZ'] = DZ_list
    df['DT'] = DT_list
    df['Vint'] = Vint_list
    return df


def data_filtering(df: pd.DataFrame) -> pd.DataFrame:
    df['smooth_3'] = df['Vint'].rolling(window=3).mean()
    df['smooth_5'] = df['Vint'].rolling(window=5).mean()
    df['exponential'] = df['Vint'].ewm(com=0.5).mean()  # to test more
    filter5 = np.convolve(np.ones(5), np.ones(5), mode='full')
    filter5 = filter5 / sum(filter5)
    filter7 = np.convolve(np.ones(7), np.ones(7), mode='full')
    filter7 = filter7 / sum(filter7)
    df['filtered'] = np.convolve(df['Vint'], filter7, mode='same')
    df['filtered_Time'] = np.convolve(df['T150'], filter7, mode='same')
    return df


def prepare_checkpoints(filename: str) -> pd.DataFrame:
    df = pd.read_excel("stratigraphy_Bairak35.xlsx")
    df = df.astype({'MD': 'int32'})
    return df


# time_increment = input('Please specify if time column is TWT format. Enter True/False')
# if time_increment = True:
#     wt_increment = 2000
# else:
#     wt_increment = 1000
def draw_plot(data_df: pd.DataFrame, checkpoint_df: pd.DataFrame):
    plt.plot(data_df['Vint'], data_df['Hкаб.'])
    markers_x = checkpoint_df['MD']
    markers_y = np.interp(markers_x, data_df['Hкаб.'], data_df['filtered'])
    plt.plot(data_df['filtered'], data_df['Hкаб.'])
    plt.scatter(markers_y, markers_x, color='red')
    plt.plot()
    plt.gca().invert_yaxis()
    for x, y, t in zip([0 for i in range(len(markers_y))], markers_x, checkpoint_df['Surface']):
        plt.text(x, y, t, fontfamily='monospace')
        print(x, y, t)
    plt.hlines(markers_x, 0, markers_y, color='red')
    plt.show()


# issues - use filter on OWT/TWT
# plot results for few wells
if __name__ == '__main__':
    data_df = prepare_data("Working_example.xlsx")
    data_checkpoint = prepare_checkpoints("stratigraphy_Bairak35.xlsx")
    data_df = data_filtering(data_df)
    draw_plot(data_df, data_checkpoint)
