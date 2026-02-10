
from robot import * 
import math


nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Gen"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        self.memory = -2
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)


            if self.memory == -2: self.memory = -1
                
            cote = 1 if self.memory > 0 else -1
            
            valeur_absolue = abs(int(self.memory))
            state = valeur_absolue // 1000  
            timer = valeur_absolue % 1000   

            DURATION_4_CASES = 4
            TIME_TO_TURN_90 = 9
            
            wall_wide = (sensors[sensor_front] < 0.3) or (sensors[sensor_front_left] < 0.45) or (sensors[sensor_front_right] < 0.45)
            wall_front = (sensors[sensor_front] < 0.3)

            translation = 0
            rotation = 0

            
            if state == 0:
                translation = 1
                if wall_wide:
                    state = 1
                    timer = TIME_TO_TURN_90
            
            elif state == 1:
                rotation = 1.0 * cote
                timer -= 1
                if timer <= 0:
                    state = 2
                    timer = DURATION_4_CASES
            
            elif state == 2:
                if wall_front:
                    state = 4          
                    timer = TIME_TO_TURN_90
                    translation = 0
                else:
                    translation = 1.0
                    timer -= 1
                    if timer <= 0:
                        state = 3
                        timer = TIME_TO_TURN_90
            
            elif state == 3:
                rotation = 1 * cote
                timer -= 1
                if timer <= 0:
                    cote *= -1  
                    state = 0   
                    timer = 1   

            elif state == 4:
                rotation = 1 * cote
                timer -= 1
                if timer <= 0:
                    state = 2   
                    timer = DURATION_4_CASES

            self.memory = cote * (state * 1000 + timer)

            return translation, rotation, False