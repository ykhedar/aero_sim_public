import util
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib import animation
from agents import crane, drone
from pathlib import Path
import matplotlib.colors as mcolors
plt.rcParams['animation.ffmpeg_path'] = 'E:\\ffmpeg\\ffmpeg-win64-static\\bin\\ffmpeg.exe'

crane_log_path = Path("input\\crane_log.csv")
drone_max_wait_time = 12  # Only used in the update_conflict_slot_list_wait_x_seconds() strategy.


def frame_gen(drone_):
    b = 0
    while not drone_.mission_end():
        b += 1
        yield b


class Simulation:
    def __init__(self):
        self.fig = plt.figure(figsize=(20, 3))
        self.ax = plt.axes()

        # Initialisation of the plot canvas
        plt.title('Simulation of drone movement for the mapping mission. (VIEW FROM THE TOP)')
        plt.xlabel('Distance Parallel to the Tracks (meter)')
        plt.ylabel('Width of the Mapping Area (meter)')
        plt.xlim(0, 360)
        plt.ylim(-1, 6)

        # Initialise the cranes and drone class
        self.cranes = crane.get_cranes(crane_log_path)
        self.drone_ = drone.get_drone(drone_max_wait_time)

        # Initialisation of the crane and drone patches for visualisation in the simulation
        self.patches_list = []
        self.ax.add_patch(Rectangle((5, 0), 350, 5, angle=0, lw=1, ec='b', fc=mcolors.CSS4_COLORS['lightgray']))
        plt.text(5, 5.2, 'Mission Area')
        [self.ax.add_patch(crane_.get_vis_patch(0)) for crane_ in self.cranes]
        self.ax.add_patch(self.drone_.get_vis_patch())
        plt.tight_layout()

    def get_patches_list(self, time):
        # Add the patches to the list for visualisation.
        self.patches_list = []
        self.patches_list = [crane.get_vis_patch(time) for crane in self.cranes]
        self.patches_list.append(self.drone_.get_vis_patch())
        self.patches_list.append(self.drone_.get_drone_text())
        self.patches_list.append(self.drone_.get_mission_counter_text())
        [self.patches_list.append(crane_.get_crane_text(time)) for crane_ in self.cranes]

    def add_conflict_patch(self):
        conflict_patch = Rectangle((self.drone_.get_location(), 0), 5, 5, lw=2, fc=mcolors.CSS4_COLORS['red'])
        self.ax.add_patch(conflict_patch)
        self.patches_list.append(conflict_patch)

    def update(self, time):
        self.get_patches_list(time)

        # Check for conflicts.
        conflicts = [util.detect_overlap(self.drone_.get_vis_patch(), crane_.get_vis_patch(time))
                     for crane_ in self.cranes]

        if any(conflicts):  # Mark it for re-fly mission.
            self.add_conflict_patch()

        # Strategy A: Just mark the conflict slots for a later re-fly mission
        #self.drone_.update_conflict_slot_list_no_wait(conflicts)

        # Strategy B: Wait for 10 Seconds on a conflict before moving on.
        self.drone_.update_conflict_slot_list_wait_x_seconds(conflicts)
        return self.patches_list


    def update_new_strategy(self, time):
        # TODO Implement the new update strategy here.
        self.get_patches_list(time)
        conflicts = [util.detect_overlap(self.drone_.get_vis_patch(), crane_.get_vis_patch(time))
                     for crane_ in self.cranes]

        # self.get_patches_list(time)
        is_waits = []
        if any(conflicts):
            is_waits = [util.is_wait(self.drone_, crane_, time, self.drone_.countdown())
                    for crane_ in self.cranes]
        self.drone_.update_conflict_slot_list_intelligent_wait(conflicts, is_waits)
        if not (any(is_waits)) and any(conflicts):
            self.add_conflict_patch()
            print("slot_location:", self.drone_.get_location())
        return self.patches_list


    def animate(self):
        gen = frame_gen(self.drone_)
        anim2 = animation.FuncAnimation(self.fig, self.update_new_strategy, fargs=(), frames=gen,
                                        interval=1, blit=True, save_count=1000)
        anim_name = 'output/anim_with_intelligent_wait.mp4'
        anim2.save(anim_name, fps=10, extra_args=['-vcodec', 'libx264'])


sim = Simulation()
sim.animate()
# print(crane_log_path)
# cranes_ = crane.get_cranes(crane_log_path)
# crane1 = cranes_[0]
# drone1 = drone.get_drone(drone_max_wait_time)
# wait_time = 10
# current_time = 5
# conflicts = [util.detect_overlap(drone1.get_vis_patch(), crane_.get_vis_patch(current_time))
#                      for crane_ in cranes_]
#
# print(crane1.get_location(current_time))
# print(crane1.get_location(current_time+wait_time))
# print(drone1.get_location())
# print(util.is_wait(drone1, crane1, current_time, wait_time))
# drone1.update_conflict_slot_list_intelligent_wait(conflicts, False)
