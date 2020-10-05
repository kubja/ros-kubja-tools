# ros-kubja-tools
Repo with my tools for ROS. 

## navsattfix_rosbag_to_kml.py

--> Visualize ROS `sensor_msgs/NavSatFix` in Google Earth.

This script takes rosbag with `sensor_msgs/NavSatFix` topic as an input and exports kml file. The kml file can be visualized in Google Earth.

### Usage

```
python navsattfix_rosbag_to_kml.py [absolute/relative bag file path] [topic_name]
```

---

## tf_visualize.py
Script to visualize the robots' trajectories recorded in ROSBAG of the transformations (*/tf* topic). Plots arbitrary number of trajetories (either you can have multiple robots or the ground truth reference) of specified frames and exports the .kml with the trajectories and origin of the map frame. For export in .kml assumes the [reference_frame] to be the origin of the utm frame

### Installation

You need Python packages: 
* utm : https://pypi.python.org/pypi/utm
* simplekml : http://simplekml.com/en/latest/

And of course installed ROS.

### Usage:

```
python tf_visualize.py \[bag file name\] \[UTM zone\] \[reference_frame\]  \[target_frame1\] \(\[target_frame2\] \[target_frame3\] ...\)
```

Visualizes position of \[target_frames\] with respect to the \[reference_frame\] . 
\[UTM zone\] in format XXY where XX is the zone number ranging from 01 to 60, Y for letter, if 000 then .kml file is not exported and data are only visualized

### Example:

python tf_visualize.py 30T utm base_link gt



---


## License 
The code is available at github under [MIT licence].
