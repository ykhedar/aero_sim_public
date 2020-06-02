import util
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib import animation
from agents import crane, drone
from pathlib import Path
import matplotlib.colors as mcolors


crane_log_path = Path("input\\crane_log.csv")


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

        plt.xlabel('Distance Parallel to the Tracks (meter)')
        plt.ylabel('Width of the Mapping Area (meter)')
        plt.xlim(0, 360)
        plt.ylim(-1, 6)

        # Initialise the cranes and drone class
        self.cranes = crane.get_cranes(crane_log_path)
        self.drone_ = drone.get_drone(10)

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
        self.drone_.update_conflict_slot_list_no_wait(conflicts)

        # Strategy B: Wait for 10 Seconds on a conflict before moving on.
        # self.drone_.update_conflict_slot_list_wait_x_seconds(conflicts)
        return self.patches_list

    def update_new_strategy(self, time):
        # TODO Implement the new update strategy here.
        print("Hello World")

    def animate(self):
        gen = frame_gen(self.drone_)
        anim2 = animation.FuncAnimation(self.fig, self.update, fargs=(), frames=gen,
                                        interval=1, blit=True, save_count=1000)
        anim_name = 'output/anim.mp4'
        anim2.save(anim_name, fps=10, extra_args=['-vcodec', 'libx264'])


sim = Simulation()
sim.animate()
