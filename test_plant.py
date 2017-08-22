import PID
from time import sleep

controller = PID.PidController(P=0.3,I=0.01,D=9)
plant = PID.Plant(position=5, velocity=0, acceleration=0)   
position = 5
SETPOINT = 0

while True:
    angle = controller.update(position)
    position = plant.update(angle)
    print(position)
    sleep(0.1)
