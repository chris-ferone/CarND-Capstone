from math import atan

# 1. Find radius of curvature of lane using vehicle longitudinal speed & vehicle angle velocity
# 2. Calculate steering angle to follow radius of curvature

class YawController(object):
    def __init__(self, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
        self.wheel_base = wheel_base
        self.steer_ratio = steer_ratio
        self.min_speed = min_speed
        self.max_lat_accel = max_lat_accel

        self.min_angle = -max_steer_angle
        self.max_angle = max_steer_angle


    def get_angle(self, radius):
	#given the radius of curvature of the lane, calculate the desired steering angle. This assumes ackerman steering
        angle = atan(self.wheel_base / radius) * self.steer_ratio
        return max(self.min_angle, min(self.max_angle, angle))

    def get_steering(self, linear_velocity, angular_velocity, current_velocity):
	#linear_velocity = desired speed from waypoints, agular velocity = desired yaw rate from waypoints, current velocity = current vehicle linear speed
        angular_velocity = current_velocity * angular_velocity / linear_velocity if abs(linear_velocity) > 0. else 0. #zero the angular velocity if vehicle is stopped

        if abs(current_velocity) > 0.1:
            max_yaw_rate = abs(self.max_lat_accel / current_velocity);
            angular_velocity = max(-max_yaw_rate, min(max_yaw_rate, angular_velocity))
	
	#Calculate the radius of curvature of the lane by dividing the current (longitudinal) speed by the angular speed (this is simply rearranging the formular v=w*r linear speed equals angular speed by radius)
        return self.get_angle(max(current_velocity, self.min_speed) / angular_velocity) if abs(angular_velocity) > 0. else 0.0; #zero the angular velocity if vehicle is stopped
