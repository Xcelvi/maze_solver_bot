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
max_speed = 6.28

#set the motors to go
left_motor.setVelocity(max_speed)
right_motor.setVelocity(max_speed)

left_speed = max_speed
right_speed = max_speed
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
    
    right_sensors = [right0, right1]
    forward_sensors = [forward0, forward1, forward2]
    left_sensors = [left0, left1]
    back_sensors = [back0, back1]
    
    # Process sensor data here.
    if (max(right_sensors) < 75):
        left_speed = max_speed
        right_speed = -4
        print("right")
    elif (max(forward_sensors) < 75):
        right_speed = max_speed
        left_speed = max_speed
        print("forward")
    else: 
        right_speed = max_speed
        left_speed = -4
        print("left")
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)    
    
    pass

# Enter here exit cleanup code.
