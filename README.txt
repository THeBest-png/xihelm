A ROS (Robot Operating System) package for a simulation of a C-beam linear actuator in Gazebo with a front-facing camera has been created. 
The detection of blue color is done using cv2 in Python3. 
A threshold percentage is set to determine the amount of blue required to trigger a stop in the actuator's movement, which is controlled by ROS Actions.


python3 package required.
    cv2


Instruction running the package.

$cd ~/xihelm
$catkin_make
$source devel/setup.bash

"change threshold to set percentage of blue required to trigger a stop"
$roslaunch colour_linear gazebo.launch threshhold:=10 

"on a seperate terminial"
$rosrun colour_linear action_client.py 

