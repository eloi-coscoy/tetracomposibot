from robot import * 
import math

nb_robots = 0
debug = True


class Robot_player(Robot):
    team_name = "Gen Result"
    robot_id = -1
    iteration = 0
    
    tab_score = [[0 for _ in range(100)] for _ in range(100)]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        
        try:
            with open('result.txt', 'r') as f:
                contenu = f.read() 
            self.param = [float(x) for x in contenu.split(',')]
        except:
            self.param = [0.0] * 12

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        sl = max(0.0, sensors[sensor_left])
        sf = max(0.0, sensors[sensor_front])
        sr = max(0.0, sensors[sensor_right])
        
        raw_trans = (self.param[0] * sl ** abs(self.param[1]) + 
                     self.param[2] * sf ** abs(self.param[3]) + 
                     self.param[4] * sr ** abs(self.param[5]))

        raw_rot =   (self.param[6] * sl ** abs(self.param[7]) + 
                     self.param[8] * sf ** abs(self.param[9]) + 
                     self.param[10]* sr ** abs(self.param[11]))
        
        translation = max(0, min(1, raw_trans)) 
        rotation = max(-1, min(1, raw_rot))

        self.iteration += 1
        

        return translation, rotation, False