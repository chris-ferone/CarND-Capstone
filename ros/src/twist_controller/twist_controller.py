
GAS_DENSITY = 2.858
ONE_MPH = 0.44704
from pid import PID
from yaw_controller import YawController
import rospy

class Controller(object):
    def __init__(self, *args, **kwargs):
        # TODO: Implement
	self.pidCntlr = PID(kp = .1, ki = .01, kd = 0)
	self.yc = YawController(*args)
        self.DBW_enabled_last = False
        pass

    def control(self, speed_setpoint, current_speed, yawrate_setpoint, angular_velocity, DBW_enabled):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
	if DBW_enabled is True and self.DBW_enabled_last is False:
            self.pidCntlr.reset()

	error = speed_setpoint - current_speed
	
	steadystate_ff = speed_setpoint*.28/11 #.3 throttle is needed to maintain 11mps
        print steadystate_ff, 
        throttle_command_pre = steadystate_ff + self.pidCntlr.step(error, sample_time=.02)
        throttle_command = max(0, min(throttle_command_pre, 1))
	#print "sp", speed_setpoint, "act",current_speed, "e", error, "cmd", throttle_command
		
	brake_command = 0;
        #brake_deadband 
	#switch between throttle and brake
	
	#feedforward: we can calcualte steady state torque required for vehicle to maintain speed
	#forces acting on vehicle
		#weight force due to grade (not considered. It is assumed vehicle is operating on level surface)
		#aerodynamic drag
		#rolling resistance
		#driveline drag
	#can consider equivalent mass of tires
	#need a table to map throttle to torque

	steer_command = self.yc.get_steering(speed_setpoint, yawrate_setpoint, current_speed)
        #rospy.loginfo("SpdStPnt: %.2f | CrntSpd: %.2f | Err: %.2f | ThrtllCmd: %.2f | StrCmd: %.2f | YwRtStPnt: %.3f", speed_setpoint, current_speed, error, throttle_command, steer_command, yawrate_setpoint)
	seconds = rospy.get_time()        
	print seconds, speed_setpoint, current_speed, error, throttle_command, steer_command, yawrate_setpoint, angular_velocity, int(DBW_enabled)
        self.DBW_enabled_last = DBW_enabled	
        return throttle_command, brake_command, steer_command
