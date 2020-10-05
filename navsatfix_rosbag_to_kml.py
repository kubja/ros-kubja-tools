
# author: Jakub Tomasek  (jakub@tomasek.fr), www.jakubtomasek.cz
# license: MIT

import rosbag
import sys
import os
import tf
import rospy
import matplotlib.pyplot as plt
import simplekml



if __name__ == '__main__':
	#did we get the arguments?
	if (len(sys.argv) > 2):
		file_name = sys.argv[1]
		topic_name = sys.argv[2]
	else:
		print ("bad argument(s): " + str(sys.argv))
		print ("Should be: [bag file name] [ROS topic name] [reference frame] [target frame 1] ([target frame2]) ([target frame3]) ...")
		sys.exit(1)

	print("Reading ROSBUG...ehm, sorry, ROSBAG... " + file_name)

	#open the bag file
	bag = rosbag.Bag(file_name)

	print("Bag loaded.")

	if (os.stat(file_name).st_size > 2e8):
		print("Uff, it was heavy!")


	kml = simplekml.Kml()
	coords = []
	for subtopic, msg, t in bag.read_messages("/ublox_gps/fix"):
		coords.append((msg.longitude,msg.latitude))

	lin = kml.newlinestring(name="Pathway", description="A pathway in Kirstenbosch", coords=coords)
	bag.close()

	kml_file = file_name.rstrip(".bag") + ".kml"
	kml.save(kml_file)
	print("Exporting KML file: " + kml_file)

	
	print("Done.")