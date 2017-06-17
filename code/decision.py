import numpy as np
import random

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    
    # Decide which angle to use, nav_angles or rock_angels
    valid_angle = None
    valid_go = None
    valid_stop = None
    if Rover.rock_exist:
        valid_angle = Rover.rock_angles
        valid_go = Rover.rock_go
        valid_stop = Rover.rock_stop     
    else:
        valid_angle = Rover.nav_angles
        valid_go = Rover.go_forward
        valid_stop = Rover.stop_forward
        

    # Example:
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and not Rover.picking_up:
        if Rover.vel != 0:
            Rover.throttle = 0
            Rover.brake = Rover.brake_set * 2
        else:
            Rover.send_pickup = True
            Rover.rock_exist = False
    
    # Check if we have vision data to make decisions with
    elif valid_angle is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # if stuck
            if Rover.vel == 0 and Rover.throttle > 0:
                Rover.throttle = -1
                Rover.brake = 0
                Rover.mode = 'stuck'
            
            # Check the extent of navigable terrain
            elif len(valid_angle) >= valid_stop:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(valid_angle * 180/np.pi), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(valid_angle) < valid_stop:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(valid_angle) < valid_go:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                elif len(valid_angle) >= valid_go:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(valid_angle * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
        elif Rover.mode == "stuck":
            Rover.brake = 0
            if Rover.throttle == 0:
                Rover.throttle = -1
                Rover.steer = -15 if random.randint(0,1) else 15
            elif Rover.throttle < -0.1:
                Rover.throttle = Rover.throttle + 0.07
            else:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.mode = 'forward'

    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    return Rover

