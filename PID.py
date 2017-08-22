from sumq import RunningSumQueue
from collections import namedtuple

PrevState =  namedtuple('PrevState', ['err','command','noise_count']) 

class pidController:

    def __init__(self, P=0, I=0, D=0, queue_len=30, noise_threshold=None):
        self.P = P
        self.I = I
        self.D = D
        self.iqueue = RunningSumQueue(queue_len)
        self.noise_threshold = noise_threshold
        self.prevState = PrevState(0,0,0) 

    def update(self, err):
        if self.noise_threshold and abs(self.prevState.err-err) > self.noise_threshold:
            if self.prevState.noise_count < 3:
                self.prevState = PrevState(self.prevState.err, self.prevState.command, self.prevState.noise_count + 1)
                return self.prevState.command

        command = 0
        if self.P:
            command += self.P*err
        if self.I:
            self.iqueue.push(err)
            command += self.I*self.iqueue.getSum()
        if self.D:
            command += self.D*(err-self.prevState.err)
            
        self.prevState = PrevState(err, command, 0)
        return command 
