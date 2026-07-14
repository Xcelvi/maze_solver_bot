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

#Setup cameras for finish
cam0 = robot.getDevice('cam0')
cam0.enable(timestep)
cam1 = robot.getDevice('cam1')
cam1.enable(timestep)
cam2 = robot.getDevice('cam2')
cam2.enable(timestep)
cam3 = robot.getDevice('cam3')
cam3.enable(timestep)

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

#Establish all states
FOLLOW_WALL = 0
TURN = 1

state = FOLLOW_WALL

#Follow wall state
def follow_wall(right_sensor):
    distance_from_ideal = target_distance - right_sensor
    if (abs(distance_from_ideal) < 80):
        distance_from_ideal = 0
    turn_correction = distance_from_ideal * turn_aggression
        
    left_speed = max_speed + turn_correction
    right_speed = max_speed - turn_correction
        
    left_speed = max(min(left_speed, motor_limit), -motor_limit)
    right_speed = max(min(right_speed, motor_limit), -motor_limit)
    return left_speed, right_speed
#wall in front state
def turn():
    left_speed = -4
    right_speed = 4
    return left_speed, right_speed
while robot.step(timestep) != -1:
    #Setup all distance sensors
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
    
    #Setup light sensors
    front_cam0 = cam0.getImage()
    front_cam1 = cam1.getImage()
    front_cam2 = cam2.getImage()
    front_cam3 = cam3.getImage()
    
    front_cam = [front_cam0, front_cam1, front_cam2, front_cam3]
    
    # Change and check states
    if state == FOLLOW_WALL:
        print("state == follow_wall")
        if forward_sensor > 200:
            print("state == turn")
            state = TURN
    elif state == TURN:
       left_speed, right_speed = turn()
       left_motor.setVelocity(left_speed)
       right_motor.setVelocity(right_speed)
       for i in range(8):
           robot.step(timestep)
       if forward_sensor < 100:
           state = FOLLOW_WALL
    if state == FOLLOW_WALL:
        left_speed, right_speed = follow_wall(right_sensor)
    
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
    #Setup camera and comparisons
    width = cam0.getWidth()
    height = cam0.getHeight()
    x = width //2
    y = height //2
    red0 = cam0.imageGetRed(front_cam0, width, x, y)
    green0 = cam0.imageGetGreen(front_cam0, width, x, y)    
    blue0 = cam0.imageGetBlue(front_cam0, width, x, y)  

    red1 = cam1.imageGetRed(front_cam1, width, x, y)
    green1 = cam1.imageGetGreen(front_cam1, width, x, y)    
    blue1 = cam1.imageGetBlue(front_cam1, width, x, y)  
    red2 = cam2.imageGetRed(front_cam2, width, x, y)
    green2 = cam2.imageGetGreen(front_cam2, width, x, y)    
    blue2 = cam2.imageGetBlue(front_cam2, width, x, y)  
    red3 = cam3.imageGetRed(front_cam3, width, x, y)
    green3 = cam3.imageGetGreen(front_cam3, width, x, y)    
    blue3 = cam3.imageGetBlue(front_cam3, width, x, y)  
    
    red_total = red0+red1+red2+red3
    green_blue_total = blue0 +blue1+blue2+blue3+green0+green1+green2+green3
    print(red_total, green_blue_total)
    if red_total > (green_blue_total):
        print("Total time", robot.getTime())
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
        break
    pass

# Enter here exit cleanup code.
