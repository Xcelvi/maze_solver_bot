"""distance_sensor_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#setup ps and enable all sensors
ps0 = robot.getDevice('ps0')
ps0.enable(timestep)

ps1 = robot.getDevice('ps1')
ps1.enable(timestep)
ps2 = robot.getDevice('ps2')
ps2.enable(timestep)
ps3 = robot.getDevice('ps3')
ps3.enable(timestep)
ps4 = robot.getDevice('ps4')
ps4.enable(timestep)
ps5 = robot.getDevice('ps5')
ps5.enable(timestep)
ps6 = robot.getDevice('ps6')
ps6.enable(timestep)
ps7 = robot.getDevice('ps7')
ps7.enable(timestep)
ps8 = robot.getDevice('ps8')
ps8.enable(timestep)
#setup motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
#set max speed
max_speed = 4

#set the motors to go
left_motor.setVelocity(max_speed)
right_motor.setVelocity(max_speed)

left_speed = max_speed
right_speed = max_speed

# Add a distance you want the robot from the wall
target_distance = 150
turn_aggression = .04

#Set max velo to not break
motor_limit = 6.28

while robot.step(timestep) != -1:
    
    forward0 = int(ps0.getValue())
    forward1 = int(ps8.getValue())
    forward2 = int(ps7.getValue())
    
    right0 = int(ps1.getValue())
    right1 = int(ps2.getValue())
    
    back0 = int(ps3.getValue())
    back1 = int(ps4.getValue())
    
    left0 = int(ps5.getValue())
    left1 = int(ps6.getValue())
    
    right_sensor = max(right0, right1)
    forward_sensor = max(forward0, forward1, forward2)
    left_sensor = max(left0, left1)
    back_sensor = max(back0, back1)
    
    # Turning amount and erros
    if forward_sensor > 200:
        left_motor.setVelocity(-4)
        right_motor.setVelocity(4)
        for i in range(30):
            robot.step(timestep)
        print("forward")
    else:    
        distance_from_ideal = target_distance - right_sensor
        if (abs(distance_from_ideal) < 80):
            distance_from_ideal = 0
        turn_correction = distance_from_ideal * turn_aggression
        
        left_speed = max_speed + turn_correction
        right_speed = max_speed - turn_correction
        
        left_speed = max(min(left_speed, motor_limit), -motor_limit)
        right_speed = max(min(right_speed, motor_limit), -motor_limit)
        print("Right", right_sensor, "left", left_sensor, "distance_from_ideal", distance_from_ideal)
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    
    pass

# Enter here exit cleanup code.
