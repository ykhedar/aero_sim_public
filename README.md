# Problem Statement
The drone flys over an area of 350m * 5m. It takes images continuosly every 1.76meters flying with a speed of 1.1m/s
There are four cranes moving in the mapping area. The problem is that the images taken should not contain the cranes in the.
Since one wants to only map the rails in the area. 

## Image of the mission area, with and without cranes. and 

There are two strategies implemented in the simulation toolbox:

A. Mark the slots for a later refly
B. Wait when a crane is seen to be in image for X seconds (one could paramterically define X to find the best value 
over large number of datasets.)

In this thesis you would understand the problem and then implement one or more strategies which are hopefully better 
in comparision to the strategy A and B. Some ideas are as follows:

C. Use the information for crane next locations from the logs to do an intelligent planning, so that the crane is 
never in the images. 
D. Discover some other idea :)


## Description about the toolbox.
The toolbox is divided into the modules, "agents", "input", "output", "utils" and the main simulation file 
"simulation.py". 

First follow the steps below to install the necessary dependencies to run the toolbox.
## Installation steps
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

![Install Requirements Image](https://github.com/ykhedar/aero_sim_public/images/install_requirements.PNG)

6. Open up the "simulation.py" file, right click anywhere and then click on "Run". See the image below. 

![Run Simulation](https://github.com/ykhedar/aero_sim_public/images/run_simulation.png)

The script should take 10-20 seconds to complete and at the end you will see a video in the output folder.
