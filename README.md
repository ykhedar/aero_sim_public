# Problem Statement
The drone flys over an area of 350m * 5m. It takes images continuously flying with a speed of 1.1m/s.
There are four cranes moving in the mapping area. The problem is that the images taken by the drone should 
not contain the cranes in the field of view.

This is seen in the video in the "output" folder. There are two videos for two difference strategies which are
explained in the next section. The video show the "Top View" of the Flying. The drone(marked in black color) 
moves along the Mission area long side and takes pictures. The surface of the black drone patch represents the 
ground coverage of the image. The cranes are represented in blue color. As soon as there is a conflict(overlap of 
the drone and cranes), this area is marked as "conflict slot" and needs to be re-flown in a next flight.

The objective of the simulation toolbox is to design a mission planning strategy which leads to the minimum number
and length of these "conflict slots".

There are two strategies implemented in the simulation toolbox:

1. Fly with constant speed of 1.1 m/s and mark the slots for a later re-fly mission.

2. Fly with a constant speed of 1.1 m/s and wait for a maximum of X seconds (one could parameterically define X to find the best value 
over large number of datasets.) when a crane is seen in a image (or when a conflict happens). 

In this thesis you would understand the problem and then implement one or more strategies which are hopefully better 
in comparision to the strategy A and B. Some ideas are as follows:

1. Use the information for crane next locations from the logs to do an intelligent planning, so that the crane is 
never in the images. 

2. Discover some other idea :)


## Description about the toolbox.
The toolbox is divided into the modules, "agents", "input", "output", "utils" and the main simulation file 
"simulation.py". 

First follow the steps below to install the necessary dependencies to run the toolbox.
### Installation steps
1. Install PyCharm IDE from the following website.

    [PyCharm Download Page](https://www.jetbrains.com/pycharm/download/#section=windows)

2. Download the git repository containing this code into a folder "aero_sim".

3. Run the PyCharm IDE. Open the git repository from Step 2 above by following the link:

[PyCharm Project Open](https://www.jetbrains.com/help/pycharm/opening-reopening-and-closing-projects.html#opening_projects)

4. Once the project is open, setup the "Project Interpretor" using the steps in the following website:

[PyCharm Python Interpretor Setup](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add_new_project_interpreter)

Create a new environment of type "Virtualenv Environment" with Python 3.6 or above. 

5. Once the setup is complete. Open up the "requirements.yml" from the "aero_sim" project. You will be prompted to install
the dependencies from this file. Install all the requirements. See the following image for the hints.

![Install Requirements Image](./images/install_requirements.PNG?raw=true)

6. Open up the "simulation.py" file, right click anywhere and then click on "Run". See the image below. 

![Run Simulation](./images/run_simulation.png?raw=true)

The script should take 10-20 seconds to complete and at the end you will see a video in the output folder.

### Information about functions needed to be modified in order to implement new strategy

The main function which does the time step update is the 
````python

    def update(self, time):
        
````
 method of the "Simulation" class of the "simulation.py" file.
 
 A new function stub is alread created in this file and is called the following.
 ````python
    def update_new_strategy(self, time):
````
You should implement your new strategy in this function.

These functions rely on the following methods from the "Drone" class of agents/drone.py file:

````python
    update_conflict_slot_list_no_wait()
````
or

````python
    update_conflict_slot_list_wait_x_seconds()
````

depending on the type of strategy to be used.

There is a new function stub already added to implement your new strategy in this class:

````python
    new_drone_strategy()
````

I believe you might not need to change anything else but if you need to then please go ahead. 

Since the code is already on github, if you have any doubts you could simply raise an issue there or 
write and email. 