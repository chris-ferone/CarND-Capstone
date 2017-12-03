
MIN_NUM = float('-1')
MAX_NUM = float('1')


class PID(object):
    def __init__(self, kp, ki, kd, mn=MIN_NUM, mx=MAX_NUM):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min = mn
        self.max = mx

        self.int_val = self.last_int_val = self.last_error = 0.

    def reset(self):
        self.int_val = 0.0
        self.last_int_val = 0.0

    def step(self, error, sample_time):
        self.last_int_val = self.int_val

        integral = self.int_val + error * sample_time;
        derivative = (error - self.last_error) / sample_time;
	
        #limit contribution of integrator  	
        #self.int_val = max(-.1, min(self.int_val, .1))
	integrator = self.ki * self.int_val
        i = max(-.1, min(integrator, .1))
	p = self.kp * error
        y = p + i + self.kd * derivative;
        val = max(self.min, min(y, self.max))
	
	print p, i, 
	
        if val > self.max:
            val = self.max
        elif val < self.min:
            val = self.min
        else:
            self.int_val = integral
        self.last_error = error

        return val
