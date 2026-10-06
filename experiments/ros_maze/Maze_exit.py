from robot_control_class import RobotControl
rc = RobotControl()
amiout = False
while amiout == False:
    rc.move_straight_time("forward", 0.3, 1)
    laser = rc.get_laser(360)

    if laser < 1:
        rc.stop_robot()
        lasersurround = rc.get_laser_full()
        if (lasersurround[0] > lasersurround[719]) and lasersurround[1] >= 2:
            rc.rotate(73)
            continue
        elif (lasersurround[0] < lasersurround[719]) and lasersurround[719] >= 2:
            rc.rotate(-73)
            continue
    lasersurround = rc.get_laser_full()
    for x in lasersurround:
        if x < 1:
            amiout == False
            break
        elif x > 1:
            amiout == True
            continue



