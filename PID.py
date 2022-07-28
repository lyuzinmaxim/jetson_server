class PID:
    # https://stackoverflow.com/questions/12569018/why-is-adding-attributes-to-an-already-instantiated-object-allowed
    def __init__(self, dt=0.1, kp=1.4, ki=0.01, kd=0.15, min_angle=-60, max_angle=60):
        self.dt = dt
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral_error = 0
        self.instantaneous_error = 0
        self.derivative = 0
        self.p_out = 0
        self.i_out = 0
        self.d_out = 0

    def calculate(self, angle, target=0):

        self.instantaneous_error = target - angle
        # Proportional
        self.p_out = self.kp * self.instantaneous_error
        # Integral
        self.integral_error += self.instantaneous_error * self.dt
        self.i_out = self.ki * self.integral_error
        # Derivative
        self.derivative = (self.instantaneous_error - self.previous_error) / self.dt
        self.d_out = self.kd * self.derivative

        output = self.p_out + self.i_out + self.d_out

        if output > self.max_angle:
            output = self.max_angle
        elif output < self.min_angle:
            output = self.min_angle

        self.previous_error = self.instantaneous_error

        return output
