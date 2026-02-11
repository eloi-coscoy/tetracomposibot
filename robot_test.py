from robot import * 
import math
import random

nb_robots = 0
debug = False

poidmap= [1,2,1,2]
class Robot_player(Robot):
    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    it_per_evaluation = 400
    
    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.theta_0 = theta_0
        
        self.param = [random.uniform(-1, 1) for i in range(34)]
        self.best_param = self.param[:] 
        
        self.best_score = -1000 
        self.score = 0
        self.cumulated_score = 0
        self.eval = 0
        self.trial = 0
        self.cur_map = 0
        
        self.tab_score = [[0 for _ in range(100)] for _ in range(100)]
        
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        if it_per_evaluation > 0:
            self.it_per_evaluation = it_per_evaluation

    def write_best_param(self):
        with open('result.txt', 'w') as f:
            res = ",".join(map(str, self.best_param))
            f.write(res)
            
    def get_new_pos(self):
        self.x0 = random.randint(2, 97)
        self.y0 = random.randint(2, 97)
        self.theta0 = random.randint(0, 359)

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
        change = False
        if self.iteration >= self.it_per_evaluation:

            self.cumulated_score += self.score*poidmap[self.cur_map]
            self.trial += 1 
            
            print(f"Fin essai {self.trial}/12 - Score essaie: {self.score:.2f} - Total: {self.cumulated_score:.2f}") 


            if self.trial %3 == 0:
                change = True
                self.cur_map = (self.cur_map+1)%4
                print(self.cur_map)


            if self.trial >= 12:
                self.eval += 1
                
                if self.cumulated_score > self.best_score:
                    self.best_score = self.cumulated_score
                    self.best_param = self.param[:]
                    self.write_best_param()
                    print(f"GEN {self.eval} TERMINÉE : NOUVEAU RECORD = {self.best_score:.2f}")
                else:
                    print(f"GEN {self.eval} Terminée : Pas d'amélioration ({self.cumulated_score:.2f})")

                self.param = self.best_param[:]
                
                for i in range(12):
                    if random.random() < 0.5: 
                        self.param[i] += random.gauss(0, 0.2)

                self.trial = 0
                self.cumulated_score = 0
                self.cur_map = 0
            
            else:
                pass

            self.tab_score = [[0 for _ in range(100)] for _ in range(100)]
            self.score = 0    
            self.iteration = 0 
            self.get_new_pos()  
            
            return 0, 0, True, change

        
        ix = int(self.x)
        iy = int(self.y)
        
        if self.tab_score[ix][iy] == 0:
            self.score += 10.0 
            self.tab_score[ix][iy] = 1 
        
        dist_origine = math.sqrt((self.x - self.x0)**2 + (self.y - self.y0)**2)*2
        
        self.score += dist_origine * 0.1


        self.iteration += 1

        return translation, rotation, False, False