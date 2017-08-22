from gpiozero import DistanceSensor, AngularServo
from PID import pidController
from time import sleep

sensor = DistanceSensor(echo=24, trigger=23)
servo = AngularServo(25, min_angle=50, max_angle=0)
controller = pidController(P=0.5,D=0.4,I=0.00, noise_threshold=10)
SETPOINT = 25
MIN_COMMAND = 0
MAX_COMMAND = 50
balanced_count = 0
balanced_time = 30

while True:
    error = sensor.distance*100 - SETPOINT

    if abs(error) < 3:
        balanced_count += 1
        print('balanced for: {}'.format(balanced_count))
        if balanced_count > balanced_time:
            servo.detach()
            print('error: {}'.format(error))
            sleep(0.1)
            continue    

    if balanced_count >30:
        balanced_count = 0
        
    if abs(error) > 25:
        print('error: {}'.format(error))
        sleep(0.1)
        continue

    command = controller.update(error) + SETPOINT
    if command < MIN_COMMAND or command > MAX_COMMAND:
        command = MIN_COMMAND if command < MIN_COMMAND else MAX_COMMAND
        
    servo.angle = command

    print('error: {}, command: {}'.format(error, command)) 
    sleep(0.1)
