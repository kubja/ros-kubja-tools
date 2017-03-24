
# author: Jakub Tomasek  (jakub@tomasek.fr), www.jakubtomasek.cz
# license: MIT

import rosbag
import sys
import os
import string
import tf
import rospy
import matplotlib.pyplot as plt
import simplekml
import utm



if __name__ == '__main__':
	#did we get the arguments?
	if (len(sys.argv) > 4):
		file_name = sys.argv[1]
		utm_zone = sys.argv[2]
		reference_frame = sys.argv[3]
		target_frames = sys.argv[4:]
		n = len(target_frames)

		print "Reference frame: " + reference_frame
		for frame in target_frames:
			print "Target frame: " + frame


		if  utm_zone == '000' or not len(utm_zone) == 3:
			export_kml = False	
			print "Not exporting the KML file"
		else :
			utm_zone_number = int(utm_zone[0:2])
			utm_zone_letter = utm_zone[2]
			export_kml = True
			print "Exporting KML file. UTM zone " + str(utm_zone_number) + " " + utm_zone_letter
			


	else:
		print "bad argument(s): " + str(sys.argv)	
		print "Should be: [bag file name] [UTM zone] [reference frame] [target frame 1] ([target frame2]) ([target frame3]) ..."
		sys.exit(1)

	print "Reading ROSBUG...ehm, sorry, ROSBAG... " + file_name

	#open the bag file
	bag = rosbag.Bag(file_name)

	print "Bag loaded."

	if (os.stat(file_name).st_size > 2e8):
		print "Uff, it was heavy!"

	tfs = tf.Transformer(True, rospy.Duration(10.0))


	#loading positions into lists
	pos_x = [[] for i in range(n)]
	pos_y = [[] for i in range(n)]
	pos_t = [[] for i in range(n)]

	t0 =  0 #initial time
	first_flag = True

	have_map_flag = False




	for subtopic, msg, t in bag.read_messages("/tf"):	
		#we read data from /tf topic

		if first_flag :
			t0 = t.to_sec()
			first_flag = False


		for ms in msg.transforms:
			
			#updating transformer at point we receive update of the transform to our frame
			tfs.setTransform(ms)		

			if ms.child_frame_id == "map" and tfs.canTransform(reference_frame, "map",rospy.Time(0)) and not have_map_flag:
				#we detected receiving base_link transform
				utm_to_map = tfs.lookupTransform(reference_frame, "map",rospy.Time(0))
				pos_map_x = utm_to_map[0][0]
				pos_map_y = utm_to_map[0][1]
				pos_map_z = utm_to_map[0][2]
				have_map_flag = True

			i = 0
			for frame in target_frames:	

				if ms.child_frame_id == frame and tfs.canTransform(reference_frame, frame ,rospy.Time(0)):
					#we detected receiving base_link transform

					transform = tfs.lookupTransform(reference_frame, frame ,rospy.Time(0))
					pos_x[i].append(transform[0][0])
					pos_y[i].append(transform[0][1])
					pos_t[i].append(t.to_sec())

				i += 1

	bag.close()

	# create KML
	if export_kml :		
		kml = simplekml.Kml()

		if have_map_flag:
			pos_map = utm.to_latlon(pos_map_x, pos_map_y, utm_zone_number, utm_zone_letter)
			pnt = kml.newpoint(name="Map", coords = [(pos_map[1], pos_map[0])] ) 
		
		#add exported trajectories
		i = 0
		for frame in target_frames:	

			crds = []

			for x,y in zip (pos_x[i], pos_y[i]) :
				p = utm.to_latlon(x, y, utm_zone_number, utm_zone_letter) 
				crds.append( (p[1], p[0]) )
			i += 1
			lin = kml.newlinestring(name=frame, coords=crds)

		kml_file = string.rstrip(file_name, ".bag") + ".kml"
		kml.save(kml_file)	
		print "Exporting KML file: " + kml_file





	# visualization

	
	
	i = 0
	plot_x = []
	plot_y = []
	plot_t = []
	for frame in target_frames:	
		plt.figure(1)  
		plot_x[:] = [x - pos_x[0][0] for x in pos_x[i]]
		plot_y[:] = [y - pos_y[0][0] for y in pos_y[i]]
		plot_t[:] = [t - pos_t[0][0] for t in pos_t[i]]

		plt.plot(plot_x, plot_y, lw = 3, alpha = 0.8, label=frame)

		plt.figure(2)  
		plt.subplot(211)
		plt.plot(plot_t, plot_x, lw = 3, alpha = 1, label=frame)
		plt.subplot(212)
		plt.plot(plot_t, plot_y, lw = 3, alpha = 1, label=frame)

		i += 1

	plt.figure(1)  
	plt.grid(True)
	plt.xlabel("x [m]")
	plt.ylabel("y [m]")
	plt.legend()
	plt.axis('equal')

	plt.figure(2)  
	plt.subplot(211)
	plt.grid(True)
	plt.xlabel("t [s]")
	plt.ylabel("x [m]")
	plt.legend()

	plt.subplot(212)
	plt.grid(True)
	plt.xlabel("t [s]")
	plt.ylabel("y [m]")


	plt.show()




	
	print "Done."