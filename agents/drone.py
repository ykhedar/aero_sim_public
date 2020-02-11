import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


class Drone:
    def __init__(self, wait_time=None):
        self.total_mission_duration = 350  # Seconds

        length, width = 5, 5
        x_start = 0
        self.current_location = x_start
        self.vis_rectangle = Rectangle((width, length), width, length, angle=0, lw=1, fc=mcolors.CSS4_COLORS['black'])
        self.drone_text = plt.text(0, 0, 'Drone')

        self.length = length
        self.width = width

        self.slot_on = False
        self.slot_list = []
        self.wait_time = wait_time  # wait T seconds upon a collision detection.
        self.wait_counter = 0
        self.time_counter = 0
        self.wait_time_list = []
        self.velocity = 1.1    # m/s

    def get_location(self):
        return self.current_location

    def sim_end(self):
        if (self.total_mission_duration - 2) == self.time_counter or self.get_location() > 300:
            return True
        else:
            return False

    def get_vis_patch(self):
        modified_coordinates = tuple(np.subtract((self.get_location(), 0), ((self.width), 0)))
        self.vis_rectangle.set_xy(modified_coordinates)
        return self.vis_rectangle

    def get_drone_text(self):
        left, bottom = self.get_vis_patch().get_xy()
        self.drone_text.set_x(left-0.1)
        self.drone_text.set_y(bottom - 0.5)
        return self.drone_text

    def move_one_step(self):
        self.current_location = self.current_location + self.velocity

    def add_to_slot_list(self, conflicts):
        #TODO add move_one_step somewhere for moving the drone.
        if any(conflicts) and not self.slot_on:
            should_wait = self.wait_seconds()
            if should_wait:
                return
            self.slot_on = True
            self.slot_list.append(self.get_location())

        if not (any(conflicts)) and self.slot_on:
            self.slot_on = False
            self.slot_list.append(self.get_location())

        if not all(conflicts):  # if there is no conflict
            if not self.wait_counter == 0:
                self.wait_time_list.append(self.wait_counter)
            self.wait_counter = 0
        self.time_counter += 1

    def wait_seconds(self):
        if self.wait_counter < self.wait_time:
            self.wait_counter += 1
            return True
        if self.wait_counter == self.wait_time:
            return False


def get_drone(wait_time):
    return Drone(wait_time=wait_time)

