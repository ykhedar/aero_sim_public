import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

import util


class Drone:
    def __init__(self, wait_time=None):
        #  Drone Visualisation related variables.
        self.length, self.width = 5, 5
        self.vis_rectangle = Rectangle((self.width, self.length), self.width, self.length, angle=0, lw=1,
                                       fc=mcolors.CSS4_COLORS['black'])
        self.drone_text = plt.text(0, 0, 'Drone')
        self.mission_counter_text = plt.text(150, 5.2, 'Mission Counter')

        # Drone Mission related variables.
        self.total_mission_duration = 350  # Seconds
        self.current_location = 0  # starting from zero meter
        self.slot_on = False
        self.slot_list = []
        self.wait_time = wait_time  # wait T seconds upon a collision detection.
        self.wait_counter = 0
        self.time_counter = 0
        self.wait_time_list = []
        self.velocity = 1.1  # m/s
        self.countdown_time = wait_time
        self.firstfly_mark = 1
        self.refly_mark = 0

    def get_location(self):
        return self.current_location

    def mission_end(self):
        return ((self.total_mission_duration - 2) == self.time_counter) or (self.get_location() > 300)

    def get_vis_patch(self):
        modified_coordinates = tuple(np.subtract((self.get_location(), 0), ((self.width), 0)))
        self.vis_rectangle.set_xy(modified_coordinates)
        return self.vis_rectangle

    def get_drone_text(self):
        left, bottom = self.get_vis_patch().get_xy()
        self.drone_text.set_x(left - 0.1)
        self.drone_text.set_y(bottom - 0.5)
        return self.drone_text

    def get_mission_counter_text(self):
        self.mission_counter_text.set_text('Mission Counter: ' + str(self.time_counter) + ' Seconds')
        return self.mission_counter_text

    def move_drone_one_step(self):
        self.current_location = self.current_location + self.velocity

    def get_slot_list(self):
        file_ = open(self.outfile, "w")
        length = []
        for slot in range(int(len(self.slot_list) / 2)):
            point_1 = (self.slot_list[2 * slot][0], self.slot_list[2 * slot][1])
            point_2 = (self.slot_list[2 * slot + 1][0], self.slot_list[2 * slot + 1][1])
            length.append(np.abs(np.subtract(point_1, point_2)))
            file_.write(str(self.slot_list[2 * slot][0]) + "," + str(self.slot_list[2 * slot][1]) + "," +
                        str(self.slot_list[2 * slot + 1][0]) + "," + str(self.slot_list[2 * slot + 1][1]) + "\n")
        file_.close()

        return self.slot_list, length, self.wait_time_list, self.time_counter

    def reset_wait_counter(self, conflicts):
        if not all(conflicts):  # if there is no conflict
            if not self.wait_counter == 0:
                self.wait_time_list.append(self.wait_counter)
            self.wait_counter = 0

    def do_wait_for_seconds(self):
        if self.wait_counter < self.wait_time:
            self.wait_counter += 1
            return True
        if self.wait_counter == self.wait_time:
            return False

    def update_conflict_slot_list_no_wait(self, conflicts):
        if any(conflicts) and not self.slot_on:  # Make the slot on.
            self.slot_on = True
            self.slot_list.append(self.get_location())

        if not (any(conflicts)) and self.slot_on:  # Make the slot off
            self.slot_on = False
            self.slot_list.append(self.get_location())

        self.time_counter += 1

        self.move_drone_one_step()

    def update_conflict_slot_list_wait_x_seconds(self, conflicts):
        if any(conflicts) and not self.slot_on:  # Make the conflict slot on.
            if self.do_wait_for_seconds():
                self.time_counter += 1
                return  # This will return out of the function. No further code will be executed.
            self.slot_on = True
            self.slot_list.append(self.get_location())

        if not (any(conflicts)) and self.slot_on:  # Make the slot off
            self.slot_on = False
            self.slot_list.append(self.get_location())

        self.reset_wait_counter(conflicts)

        self.time_counter += 1

        self.move_drone_one_step()

    def countdown(self):
        temp = self.countdown_time
        self.countdown_time -= 1
        return temp

    def reset_countdown(self):
        self.countdown_time = self.wait_time

    def update_conflict_slot_list_intelligent_wait(self, conflicts, is_wait):
        # TODO The new drone strategy should be implemented here.
        # if drone meets cranes, at first predict if the cranes move away in defined time
        # if yes, wait if not direct move through the cranes und mark the slot.
        if any(conflicts) and not self.slot_on:
            if any(is_wait):
                if self.do_wait_for_seconds():
                    # self.slot_on = True
                    # self.slot_list.append(self.getlocation())
                    self.time_counter += 1
                    print("is waiting")
                    return
            else:
                self.slot_on = True
                self.slot_list.append(self.get_location())
                print("is not waiting")

        if any(conflicts) and self.slot_on:
            self.slot_list.append(self.get_location())

        if not (any(conflicts)) and self.slot_on:  # Make the slot off
            self.slot_on = False
            print("no conflict")
            # self.slot_list.pop()

        self.reset_countdown()
        self.time_counter += 1
        self.reset_wait_counter(conflicts)
        self.speed_change(is_wait)
        self.move_drone_one_step()
        print("time_counter:", self.time_counter)

    def speed_change(self, is_waits):
        if not (any(is_waits)) and self.slot_on:
            self.velocity = 7
        else:
            self.velocity = 1.1

    def update_conflict_slot_list_no_wait_variant(self, conflicts, cranes, patches):
        if self.is_second_fly(cranes):
            self.firstfly_mark = 0
        if self.firstfly_mark:
            self.update_conflict_slot_list_no_wait(conflicts)
            return
        if self.refly_mark:
            # new strategy will be implemented hier
            if self.current_location <= 0:
                self.refly_mark = 0
                return
            self.time_counter += 1
            if not any(conflicts):
                for patch in patches:
                    if util.detect_overlap(self.get_vis_patch(), patch):
                        self.velocity = 1.1
                        # self.delete_slot(slot)
                        self.move_back_one_step()
                        print('is meeting')
                        return
            self.velocity = 7
            self.move_back_one_step()

    def delete_slot(self, slot):
        self.slot_list.remove(slot)

    def move_back_one_step(self):
        self.current_location = self.current_location - self.velocity

    def is_second_fly(self, cranes):
        if self.mission_end():
            if util.is_in_slots(cranes, self.slot_list):
                self.refly_mark = 1
                return True
            else:
                return False
        return False


def get_drone(wait_time):
    return Drone(wait_time=wait_time)
