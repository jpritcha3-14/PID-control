from sumq import RunningSumQueue
from collections import namedtuple
import math

PrevStateC =  namedtuple('PrevStateC', ['err','command','noise_count']) 
PrevStateP =  namedtuple('PrevStateP', ['acc', 'vel', 'pos']) 

class PidController:

    def __init__(self, P=0, I=0, D=0, queue_len=30, noise_threshold=None):
        self.P = P
        self.I = I
        self.D = D
        self.iqueue = RunningSumQueue(queue_len)
        self.noise_threshold = noise_threshold
        self.prevState = PrevStateC(0,0,0) 

    def update(self, err):
        if self.noise_threshold and abs(self.prevState.err-err) > self.noise_threshold:
            if self.prevState.noise_count < 3:
                self.prevState = PrevStateC(self.prevState.err, self.prevState.command, self.prevState.noise_count + 1)
                return self.prevState.command

        command = 0
        if self.P:
            command += self.P*err
        if self.I:
            self.iqueue.push(err)
            command += self.I*self.iqueue.getSum()
        if self.D:
            command += self.D*(err-self.prevState.err)
            
        self.prevState = PrevStateC(err, command, 0)
        return command 

class Plant:

    def __init__(self, position=0, velocity=0, acceleration=0, angle=0, time_step=0.1, max_position=25):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.angle = angle
        self.time_step = time_step
        self.max_position = max_position
        self.prevState = PrevStateP(position, velocity, acceleration)

    def update(self, angle):
        rad_angle = (angle*math.pi)/180.0
        self.acceleration = -9.8*math.sin(rad_angle)
        self.velocity += self.acceleration*self.time_step
        self.position += ((self.velocity + self.prevState.vel)/2.0)*self.time_step
        if abs(self.position) > self.max_position:
            self.position = self.max_position if self.position > 0 else -self.max_position
            self.velocity = 0
        self.prevState = PrevStateP(self.acceleration, self.velocity, self.position)
        return self.position
