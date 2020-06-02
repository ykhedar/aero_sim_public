import numpy as np
from matplotlib.patches import Rectangle
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


pd.options.display.precision = 8


class Crane:
    def __init__(self, fname_lcs=None, skiprows=None, crane_id=None, maxrows=900):
        # Has the format (T, X ,V)
        # self.logfile = np.loadtxt(fname_lcs, delimiter=',', skiprows=skiprows, max_rows=maxrows)
        self.log_file_path = fname_lcs
        self.log_data_df = pd.read_csv(fname_lcs, skiprows=skiprows, nrows=maxrows)
        # self.position = self.log_data_df["X"].values - 175  # this is because of the distance of the reference point from
        # the rail start point which is also the start point for the drone.
        self.position = self.log_data_df["X"].values
        length, width = 5, 5

        x_start = self.position[0]
        print("Start Time for Crane: ", str(crane_id), " is: ", x_start)
        self.vis_rectangle = Rectangle((x_start-width, 0), width, length, angle=0, lw=1, ec='b', fc='#6699ff')

        self.length = length
        self.width = width
        self.velocity = self.log_data_df["V"].values
        self.crane_text = plt.text(0, 0, 'Crane'+str(crane_id))

    def get_location(self, time):
        # Assuming the log file has the following structure: time, x, y
        x_pt = self.position[time]
        return x_pt

    def get_vis_patch(self, time):
        modified_coordinates = tuple(np.subtract((self.get_location(time), 0), (self.width, 0)))
        self.vis_rectangle.set_xy(modified_coordinates)
        return self.vis_rectangle

    def get_crane_text(self, time):
        left, bottom = self.get_vis_patch(time).get_xy()
        self.crane_text.set_x(left-0.1)
        self.crane_text.set_y(bottom - 0.5)
        return self.crane_text

    def is_crane_moving(self, time):
        if self.velocity[time] == 0:
            return False
        return True


def get_cranes(crane_logs_path):
    cranes = []
    index = 1
    for skiprows in [1, 900, 1800, 2700]:  # Box Ids on small cranes
        cranes.append(Crane(fname_lcs=crane_logs_path,
                            skiprows=skiprows,
                            crane_id=index,
                            maxrows=900))
        index = index + 1

    return cranes


def get_cranes_strategy_c(crane_logs_path):
    cranes = []
    for crane_id in [1, 2, 3, 4]:  # Box Ids on small cranes
        log_file = Path(crane_logs_path).joinpath(str(crane_id)+"_processed.csv")
        cranes.append(Crane(fname_lcs=log_file,
                            skiprows=0,
                            crane_id=crane_id,
                            maxrows=3600))
    return cranes