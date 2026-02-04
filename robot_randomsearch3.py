
from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]
    score =0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation

        self.old_translation= 0
        self.old_rotation = 0
        self.old_x= x_0
        self.old_y = y_0
        self.best_param = [0 for i in range(8)]
        self.best_score = 0
        self.eval=0

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        reset = False
        
        if self.iteration % self.it_per_evaluation == 0:
            self.eval+=1


            if self.trial>=501:
                self.param=self.best_param
                reset= True
                if self.eval%3 == 0:
                    self.theta0 = random.random()*360
            else:
                if self.iteration > 0:
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                    print ("\tscore =",self.score)

                if self.eval%3 == 0:

                    if self.score > self.best_score:
                        print(self.score, self.best_score)
                        self.best_param = self.param.copy()
                        self.best_score = self.score
                    print(self.best_score, self.best_param)

                    self.param = self.best_param.copy()  

                    for _ in range(1):   #si on veut changer le nombre de parent a modifier               
                        indice = random.randint(0,7)
                        value= random.randint(0,1)
                        if self.param[indice] == 0:
                                if value == 0:
                                    value = -1
                        else:
                            value-=1

                        self.param[indice]=value
                    
                    self.score = 0
                else:
                    self.theta0 = random.random()*360

                self.trial = self.trial + 1
                print ("Trying strategy no.",self.trial)
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset
            


        if self.x == self.old_x and self.y == self.old_y:
            real_translation = 0
        else: 
            real_translation = self.old_translation

        self.score += real_translation*(1-abs(self.old_rotation))


        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)


        self.iteration = self.iteration + 1        
        

        self.old_x = self.x
        self.old_y = self.y

        self.old_translation = translation
        self.old_rotation = rotation

        return translation, rotation, reset
