import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as mcolors
from matplotlib import animation
from agents import crane, drone
from matplotlib.patches import Rectangle
import util
import numpy as np


def frame_gen(drone_):
    b = 0
    while not drone_.mission_end():
        b += 1
        yield b


class Simulation:
    def __init__(self, crane_log_path="input/logs/", drone_max_wait_time=10):
        self.fig = plt.figure(figsize=(20, 3))
        self.ax = plt.axes()

        # Initialisation of the plot canvas
        plt.title('Simulation of drone movement for the mapping mission. (VIEW FROM THE TOP)')
        plt.xlabel('Distance Parallel to the Tracks (meter)')
        plt.ylabel('Width of the Mapping Area (meter)')
        plt.xlim(0, 360)
        plt.ylim(-1, 6)

        # Initialise the cranes and drone class
        self.cranes = crane.get_cranes_strategy_c(crane_log_path)
        self.drone_ = drone.get_drone(drone_max_wait_time)

        # Initialisation of the crane and drone patches for visualisation in the simulation
        self.patches_list = []
        self.ax.add_patch(Rectangle((5, 0), 350, 5, angle=0, lw=1, ec='b', fc=mcolors.CSS4_COLORS['lightgray']))
        plt.text(5, 5.2, 'Mission Area')
        [self.ax.add_patch(crane_.get_vis_patch(0)) for crane_ in self.cranes]
        self.ax.add_patch(self.drone_.get_vis_patch())
        plt.tight_layout()

        self.crane_stoppages_list = []

    def get_patches_list(self, time):
        self.patches_list = []
        self.patches_list = [crane.get_vis_patch(time) for crane in self.cranes]
        self.patches_list.append(self.drone_.get_vis_patch())
        self.patches_list.append(self.drone_.get_drone_text())
        self.patches_list.append(self.drone_.get_mission_counter_text())
        [self.patches_list.append(crane_.get_crane_text(time)) for crane_ in self.cranes]

    def update(self, time):
        # Get the current patches list.
        self.get_patches_list(time)
        print(time)

        # Move the Drone one time step in this function:
        # A: Divide the
        # Assess the situation now for the next time window.
        # assess_time_window()

        return self.patches_list

    def animate(self):
        gen = frame_gen(self.drone_)
        anim2 = animation.FuncAnimation(self.fig, self.update, fargs=(), frames=gen,
                                        interval=1, blit=True, save_count=1000)
        anim_name = 'output/anim_new.mp4'
        anim2.save(anim_name, fps=10, extra_args=['-vcodec', 'libx264'])

    def get_cranes_stoppages(self):
        for crane in self.cranes:
            df_ = util.get_crane_stop_data(crane.log_file_path)
            self.crane_stoppages_list.append(df_)

    def plot_crane_stoppages(self, size_):
            figure = plt.figure(num=2, figsize=size_)
            y_min, y_max = 0, 300
            for item in self.crane_stoppages_list:
                item_new = item[item["t_start"].between(y_min, y_max)]
                time = item_new["t_start"].values
                position = item_new["x_avg"].values
                duration = item_new["duration"].values
                yerr_min = [0 for el in duration]
                #print(len(duration), type(yerr_array), yerr_array.shape)
                plt.errorbar(position, time, yerr=[yerr_min, duration], fmt='o')
                #plt.scatter(position, time)
            plt.xlim(0, 300)
            plt.ylim(y_min, y_max)
            plt.xlabel("Distance Along X (meter)")
            plt.ylabel("Time (Seconds)")
            #plt.show()
            plt.savefig("test.png")

    def create_data_matrix(self):
        y_min, y_max = 900, 1200
        data_list = []
        for item in self.crane_stoppages_list:
            item = item[item["t_start"] < 300]
            print("crane: ")
            # position, time
            matrix = np.zeros((301, 301))
            for index, row in item.iterrows():
                time_start = row["t_start"]
                time_end = time_start + row["duration"]
                if time_end >= 301:
                    time_end = 301
                current_location = row["x_avg"]
                print(time_start, time_end, int(current_location))
                for time in range(int(time_start), int(time_end), 1):
                    #print(time)
                    matrix[time][int(current_location)] = 1
            print(matrix.shape)
            data_list.append(matrix)

        # combine the data from all the crane matrices:
        comb_matrix = np.zeros((301, 301))
        for row in range(0, 301):
            for col in range(0, 301):
                cell_value_list = [mat[row][col] for mat in data_list]
                if any(cell_value_list):
                    dat = 1
                else:
                    dat = 0
                comb_matrix[row][col] = dat
        return data_list, comb_matrix

    def plt_color_mesh(self, data, size_):
        fig, ax0 = plt.subplots(1, 1)
        fig.set_size_inches(size_)

        c = ax0.pcolormesh(data, cmap="Wistia")
        ax0.set_title('default: no edges')

        fig.tight_layout()
        plt.show()

    def get_drone_naive_motion(self):
        distance = 0
        data = []
        time = 0
        while distance < 300:
            distance += 1.1
            time += 1
            data.append([time, distance])


if __name__ == '__main__':
    crane_log_path_folder = Path("input/logs/")
    sim = Simulation(crane_log_path=crane_log_path_folder, drone_max_wait_time=10)
    #sim.animate()
    size_ = (15, 5)
    sim.get_cranes_stoppages()
    sim.plot_crane_stoppages(size_)
    data_list_, comb_matrix = sim.create_data_matrix()
    sim.plt_color_mesh(comb_matrix, size_)