from collections import deque
class RunningSumQueue(deque):
    
    def __init__(self, length=30):
        deque.__init__(self)
        self._length = length
        self._sum = 0

    def push(self, *vals):
        for val in vals:
            self.appendleft(val)
            self._sum += val
            if len(self) > self._length:
                self._sum -= self.pop()

    def getSum(self):
        return self._sum
   
if __name__ == '__main__':
    testq = RunningSumQueue(3)
    testq.push(1,2,3)
    print('pass' if testq.getSum() == 6 else 'fail, sum is {} s/b 6'.format(testq.getSum()))
    testq.push(4)
    print('pass' if testq.getSum() == 9 else 'fail, sum is {} s/b 9'.format(testq.getSum()))
    testq.push(0,0,0)
    print('pass' if testq.getSum() == 0 else 'fail, sum is {} s/b 0'.format(testq.getSum()))
 
