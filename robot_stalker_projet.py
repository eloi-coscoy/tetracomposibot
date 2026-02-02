
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Gen"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
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

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        #rappel : si capte rien alors 1

        #### Problème : comment on fait pour repérer les teams, pcq là ils essayent juste de suivre les robots qu'ils voient 

        # vitesse max mais ralentit lors des murs pour eviter des situations de blocage contre le mur et recul ou ralenti lors des robots de même team
                        #avancement par defaut           si repère un enemie devant                                                          si repère un enemie                                                                ralenti/recul si mur                     si robot allié alors recul/ralentit                                         
        translation = sensor_to_robot[sensor_front]*1 + (int(self.team!=sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*0.6) + (int(self.team!=sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*-0.8) + (1-sensor_to_wall[sensor_front])*-0.7  + ((int(self.team==sensor_team[sensor_front]))*(1-sensor_to_robot[sensor_front])*-1) + ((int(self.team==sensor_team[sensor_front_right]))*(1-sensor_to_robot[sensor_front_right])*-1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*-1) + ((int(self.team==sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*-1) + ((int(self.team==sensor_team[sensor_right]))*(1-sensor_to_robot[sensor_right])*-1) + ((int(self.team==sensor_team[sensor_rear]))*(1-sensor_to_robot[sensor_rear])*1) + ((int(self.team==sensor_team[sensor_rear_right]))*(1-sensor_to_robot[sensor_rear_right])*1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*1)# A MODIFIER

        # on va faire un robot qui suit les autres robots, mais dans un premier temps il va chercher par defaut sans trop coller au mur et essaye d'éviter les robots de même team (il évite les collisions) donc plus on a ce genre de robots plus il possède la capacité d'explorer tout en essayant de suivre les robots de l'équipe adverse

                    # devant gauche,                                                                             devant droite,                                                                                          gauche                                                                              doite                                                                                    arrière gauche                                                                             arrière droite                                                                               mouvement débloquage lors détection mur                   remarque: ici on a donné plus de priorité à la fornt_droite (cf front_gauche) pour être plus efficace par exemple dans l'arena 4 en prise de décision                                                                                                                       déblocage si robot de même team
        rotation =  (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*0.9) + (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_right])*-0.9) + (int(self.team!=(sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*0.9) + (int(self.team!=sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_right])*-0.9) + (int(self.team!=(sensor_team[sensor_rear_left]))*(1-sensor_to_robot[sensor_rear_left])*1) + (int(self.team!=sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*-1) + (1-sensor_to_wall[sensor_front])*random.choice([-1,1]) + (1-sensor_to_wall[sensor_front_right])*0.9 + (1-sensor_to_wall[sensor_right])*0.5 + (1-sensor_to_wall[sensor_rear_right])*0.5 + ((1-sensor_to_wall[sensor_front_left])*-1)*0.7 + ((1-sensor_to_wall[sensor_left])*-1)*0.5 +  ((1-sensor_to_wall[sensor_rear_left])*-1)*0.5 + (int(self.team==sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*random.choice([-1,1])) +  (int(self.team==sensor_team[sensor_front_right])*(1-sensor_to_robot[sensor_front_right])*1) + (int(self.team==sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_front_left])*-1) + (int(self.team==sensor_team[sensor_right])*(1-sensor_to_robot[sensor_right])*1) + (int(self.team==sensor_team[sensor_left])*(1-sensor_to_robot[sensor_left])*-1) + (int(self.team==sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*0.5) + (int(self.team==sensor_team[sensor_rear_left])*(1-sensor_to_robot[sensor_rear_left])*-0.5) + (int(self.team==sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*random.choice([-1,1]))
        print((sensor_to_robot[sensor_left]),(sensor_to_robot[sensor_front_left]),sensor_to_robot[sensor_front],sensor_to_robot[sensor_front_right],sensor_to_robot[sensor_right])
        
        self.iteration = self.iteration + 1        
        return translation, rotation, False
