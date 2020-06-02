import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


pd.options.display.precision = 8


def get_box_extent(box):
    x_bl, y_bl = box.xy
    x_br, y_br = (x_bl + box.get_width()), y_bl
    return [x_bl, x_br]


def detect_overlap(drone_, crane_):
    drone_xl, drone_xr = get_box_extent(drone_)
    crane_xl, crane_xr = get_box_extent(crane_)

    a = is_a_between(drone_xl, crane_xl, crane_xr) or is_a_between(drone_xr, crane_xl, crane_xr)
    b = is_a_between(crane_xl, drone_xl, drone_xr) or is_a_between(crane_xr, drone_xl, drone_xr)
    return a or b


def is_a_between(a, b, c):
    return b < a < c


# Original Logs contain only the X, Y columns without the headers
def read_log_and_process(log_file):
    data_df = pd.read_csv(log_file, dtype='float', header=0, names=["X", "Y"])
    #data_df["X"] = data_df["X"] - 175
    x_grad = pd.DataFrame(np.gradient(data_df["X"]), columns=["x_grad"])
    x_grad.loc[x_grad["x_grad"].between(-0.5, 0.5), "x_grad"] = 0
    data_df["V"] = x_grad
    data_df["T"] = data_df.index
    data_df['CRANESTOPPED'] = np.where(data_df['V'] == 0, 0, 1)
    data_df[["T", "X", "V", "CRANESTOPPED"]].to_csv(str(log_file).replace(".csv", "_processed.csv"), index=False)
    return data_df


def get_crane_stop_data(log_file):
    """:returns t, x, dT"""
    data = pd.read_csv(log_file)
    index_list = np.append(data[data["CRANESTOPPED"].diff() != 0].index.values, data.index.values[-1])

    crane_stop_data = []
    for el in range(0, len(index_list) - 1):
        df = data.iloc[index_list[el]:index_list[el + 1]]
        if df["CRANESTOPPED"].values[0] == 0:
            crane_stop_data.append([df["T"].values[0],
                                    df["X"].mean(),
                                    df["T"].values[-1] - df["T"].values[0]])
    crane_stop_data_df = pd.DataFrame(crane_stop_data, columns=["t_start", "x_avg", "duration"])
    filtered_data = crane_stop_data_df[crane_stop_data_df["duration"] > 10]
    filtered_data.to_csv(str(log_file).replace(".csv", "_stop_data.csv"), index=False)
    return filtered_data


def plot_log(file):
    data = pd.read_csv(file, dtype='float')
    x = data["X"] - 175

    figsize = (30, 10)
    cols, rows = 1, 2
    fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
    data_to_plot = [x, data["V"]]
    titles = ["Crane Position along the rail axis with time", "Crane Velocity with time"]
    ylabel = ["Crane Position (meter)", "Crane Velocity (m/s)"]
    index = 0

    for case in data_to_plot:
        axs.flat[index].set_title(titles[index])
        axs.flat[index].set_xlabel("Time (seconds)")
        axs.flat[index].set_ylabel(ylabel[index])
        axs.flat[index].plot(case, '.', ms=4)
        axs.flat[index].grid(True)
        index += 1
    plt.show()


def plot_stoppages(file):
    data = pd.read_csv(file, dtype='float')
    for index in [0, 900, 1800, 2700]:
        df_ = data[data["t_start"].between(index, index+900)]
        print(len(df_))
        df_["t_start"] = df_["t_start"] - index
        plt.scatter(df_["x_avg"], df_["t_start"])

    for time in range(0, 900, 150):
        continue
        plt.hlines(time, 0, 300)
    plt.xlabel("Location on the Track (meter)")
    plt.ylabel("Time (Seconds)")
    plt.yticks(np.arange(0, 901, 50))
    plt.xlim(0, 300)
    plt.ylim(0, 400)
    plt.grid(True)
    plt.hlines(120, 0, 120)
    plt.hlines(250, 150, 250)

    for drone_loc in range(0, 300, 1):
        print(drone_loc)
    plt.show()


if __name__ == '__main__':
    file_list = ["142.csv", "430.csv", "530.csv",
                 "560.csv", "570.csv", "650.csv",
                 "700.csv", "720.csv", "734.csv",
                 "1.csv", "2.csv", "3.csv", "4.csv"]
    for file in file_list:
        #file = "734.csv"
        crane_log = Path("./input/logs/" + file)
        crane_processed_log = Path("./input/logs/"+file.replace(".csv", "_processed.csv"))
        crane_stoppage_log = Path("./input/logs/"+file.replace(".csv", "_processed_stop_data.csv"))

        read_log_and_process(crane_log)
        get_crane_stop_data(crane_processed_log)
        plot_log(crane_processed_log)