#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from styx_msgs.msg import Lane, Waypoint

import math
import copy

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number


class WaypointUpdater(object):
    def __init__(self):
	#print("init")
	rospy.init_node('waypoint_updater')
	self.ego_pos = None
	self.wps = None
	self.final_wps = None
	self.first_pass = True	
        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)	       
	rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below
        self.final_waypoints_pub = rospy.Publisher('/final_waypoints', Lane, queue_size=1)
        rospy.spin()

    def pose_cb(self, msg):        
	self.ego_pos = msg.pose.position
	if self.wps is not None:	#Don't proceed until we have received waypoints
		#print('pose callback')
                #return the index of the closest waypoint, given our current position (pose)
		distances = []	
		find_dist = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)	
		wp_count = len(self.wps.waypoints)
                for i in range(wp_count):
			#find the distance between each waypoint and the current position
			distances.append(find_dist(self.wps.waypoints[i].pose.pose.position, self.ego_pos))
	
		#find index of waypoint closet to current position
		closest_wp = distances.index(min(distances))
                seconds = rospy.get_time() 
                print seconds, closest_wp, self.wps.waypoints[closest_wp].pose.pose.position.x, self.wps.waypoints[closest_wp].pose.pose.position.y, self.ego_pos.x, self.ego_pos.y, wp_count

		#final waypoints is a subset of original set of waypoints
                #print len(self.wps.waypoints)
		self.final_wps.waypoints = self.wps.waypoints[closest_wp+100:closest_wp+100+LOOKAHEAD_WPS]
                #print len(self.wps.waypoints)
		self.final_waypoints_pub.publish(self.final_wps)
	pass

    def waypoints_cb(self, waypoints):
      # Ensure we only get initial full list of waypoints as simulator keeps publishing
        # with patial list aftewards
        #print("got waypoints")        
	if self.wps is None:
            # We need to get a full copy as otherwise we just get a reference
            self.wps = copy.copy(waypoints)
            self.final_wps = copy.copy(waypoints)
            #print("copy waypoints")  
        pass

    def traffic_cb(self, msg):
        # TODO: Callback for /traffic_waypoint message. Implement
        pass

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x

    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
	WaypointUpdater()	
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')
