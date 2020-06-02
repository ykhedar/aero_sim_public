def plot_log(file):
    data = pd.read_csv(file, dtype='float')
    x = data["X"] - 175
    x_grad = pd.DataFrame(np.gradient(x), columns=["x_grad"])
    x_grad.loc[x_grad["x_grad"].between(-0.5, 0.5), "x_grad"] = 0
    figsize = (30, 10)
    cols, rows = 1, 2

    fig1, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
    data["V"] = x_grad
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


def get_crane_stop_data(file):
    """:returns t, x, dT"""
    data = pd.read_csv(file)

    index_list = data[data["CRANESTOPPED"].diff() != 0].index.values
    new_index_list = np.append(index_list, data.index.values[-1])

    groups = []
    for el in range(0, len(new_index_list) - 1):
        groups.append([new_index_list[el], new_index_list[el + 1]])

    df_list = []
    for band in groups:
        df_list.append(data.iloc[band[0]:band[1]])

    crane_stop_data, crane_move_data = [], []
    for df in df_list:

        if df["CRANESTOPPED"].values[0] == 0:
            crane_stop_data.append([df["T"].values[0],
                                    df["X"].mean(),
                                    df["T"].values[-1] - df["T"].values[0]])

        if df["CRANESTOPPED"].values[0] == 1:
            crane_move_data.append([df["T"].values[0],
                                    df["V"].mean(),
                                    df["V"].abs().max(),
                                    df["T"].values[-1] - df["T"].values[0]])

    crane_stop_data_df = pd.DataFrame(crane_stop_data, columns=["t_start", "x_avg", "duration"])
    crane_stop_data_df.to_csv("input/crane_stop_data.csv", index=False)

    crane_move_data_df = pd.DataFrame(crane_move_data, columns=["t_start", "v_avg", "v_max", "duration"])
    crane_move_data_df.to_csv("input/crane_move_data.csv", index=False)

    print(" There are total bands: ", len(df_list), " Stop bands are: ", len(crane_stop_data),
          " Move bands are: ", len(crane_move_data))

    return True


def plot_crane_stop_data(crane_stop_file="input/crane_stop_data.csv",
                         crane_move_file="input/crane_move_data.csv"):
    data = pd.read_csv(crane_stop_file)
    data_move = pd.read_csv(crane_move_file)
    # plt.scatter(data["t_start"], data["duration"])
    plt.scatter(data["t_start"], data["x_avg"])
    # plt.scatter(data_move["t_start"], data_move["duration"])
    # plt.scatter(data_move["t_start"], data_move["v_max"])
    # plt.scatter(data["duration"], data_move["v_max"])
    # plt.scatter(data["duration"], data_move["duration"])
    plt.show()


plot_crane_stop_data()
# get_crane_stop_data(crane_log)

plot_log(crane_log)