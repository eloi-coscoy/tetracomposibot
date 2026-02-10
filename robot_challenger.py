# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : FRANCK MA 21316460
#  Prénom Nom No_étudiant/e : ELOI COSKOY 
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Team Rocket"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

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



        #rappel : si capte rien alors 1 

        if self.robot_id == 0:
            # vitesse max mais ralentit lors des murs pour eviter des situations de blocage contre le mur et recul ou ralenti lors des robots de même team
                        #avancement par defaut           si repère un enemie devant                                                          si repère un enemie derrière                                                            ralenti/recul si mur                     si robot allié alors recul/ralentit                                         
            translation = sensor_to_robot[sensor_front]*1 + (int(self.team!=sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*0.9) + (int(self.team!=sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*-0.85) + (1-sensor_to_wall[sensor_front])*-0.8  + ((int(self.team==sensor_team[sensor_front]))*(1-sensor_to_robot[sensor_front])*-1) + ((int(self.team==sensor_team[sensor_front_right]))*(1-sensor_to_robot[sensor_front_right])*-1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*-1) + ((int(self.team==sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*-1) + ((int(self.team==sensor_team[sensor_right]))*(1-sensor_to_robot[sensor_right])*-1) + ((int(self.team==sensor_team[sensor_rear]))*(1-sensor_to_robot[sensor_rear])*1) + ((int(self.team==sensor_team[sensor_rear_right]))*(1-sensor_to_robot[sensor_rear_right])*1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*1)# A MODIFIER
            # on va faire un robot qui suit les autres robots, mais dans un premier temps il va chercher par defaut sans trop coller au mur et essaye d'éviter les robots de même team (il évite les collisions) donc plus on a ce genre de robots plus il possède la capacité d'explorer tout en essayant de suivre les robots de l'équipe adverse
                        # devant gauche,                                                                             devant droite,                                                                                          gauche                                                                              doite                                                                                    arrière gauche                                                                             arrière droite                                                                               mouvement débloquage lors détection mur                   remarque: ici on a donné plus de priorité à la fornt_droite (cf front_gauche) pour être plus efficace par exemple dans l'arena 4 en prise de décision                                                                                                                       déblocage si robot de même team
            rotation =  (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*0.9) + (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_right])*-0.9) + (int(self.team!=(sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*0.9) + (int(self.team!=sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_right])*-0.9) + (int(self.team!=(sensor_team[sensor_rear_left]))*(1-sensor_to_robot[sensor_rear_left])*1) + (int(self.team!=sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*-1) + (1-sensor_to_wall[sensor_front])*random.choice([-1,1]) + (1-sensor_to_wall[sensor_front_right])*0.9 + (1-sensor_to_wall[sensor_right])*0.5 + (1-sensor_to_wall[sensor_rear_right])*0.5 + ((1-sensor_to_wall[sensor_front_left])*-1)*0.7 + ((1-sensor_to_wall[sensor_left])*-1)*0.5 +  ((1-sensor_to_wall[sensor_rear_left])*-1)*0.5 + (int(self.team==sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*random.choice([-1,1])) +  (int(self.team==sensor_team[sensor_front_right])*(1-sensor_to_robot[sensor_front_right])*1) + (int(self.team==sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_front_left])*-1) + (int(self.team==sensor_team[sensor_right])*(1-sensor_to_robot[sensor_right])*1) + (int(self.team==sensor_team[sensor_left])*(1-sensor_to_robot[sensor_left])*-1) + (int(self.team==sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*1) + (int(self.team==sensor_team[sensor_rear_left])*(1-sensor_to_robot[sensor_rear_left])*-1) + (int(self.team==sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*random.choice([-1,1]))
            #print((sensor_to_robot[sensor_left]),(sensor_to_robot[sensor_front_left]),sensor_to_robot[sensor_front],sensor_to_robot[sensor_front_right],sensor_to_robot[sensor_right])
        
        
        elif self.robot_id == 1:

            
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
            
        elif self.robot_id == 2:
            # vitesse max mais ralentit lors des murs pour eviter des situations de blocage contre le mur et recul ou ralenti lors des robots de même team
                        #avancement par defaut           si repère un enemie devant                                                          si repère un enemie derrière                                                              ralenti/recul si mur                     si robot allié alors recul/ralentit                                         
            translation = sensor_to_robot[sensor_front]*1 + (int(self.team!=sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*0.9) + (int(self.team!=sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*-0.85) + (1-sensor_to_wall[sensor_front])*-0.8  + ((int(self.team==sensor_team[sensor_front]))*(1-sensor_to_robot[sensor_front])*-1) + ((int(self.team==sensor_team[sensor_front_right]))*(1-sensor_to_robot[sensor_front_right])*-1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*-1) + ((int(self.team==sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*-1) + ((int(self.team==sensor_team[sensor_right]))*(1-sensor_to_robot[sensor_right])*-1) + ((int(self.team==sensor_team[sensor_rear]))*(1-sensor_to_robot[sensor_rear])*1) + ((int(self.team==sensor_team[sensor_rear_right]))*(1-sensor_to_robot[sensor_rear_right])*1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*1)# A MODIFIER
            # on va faire un robot qui suit les autres robots, mais dans un premier temps il va chercher par defaut sans trop coller au mur et essaye d'éviter les robots de même team (il évite les collisions) donc plus on a ce genre de robots plus il possède la capacité d'explorer tout en essayant de suivre les robots de l'équipe adverse
                        # devant gauche,                                                                             devant droite,                                                                                          gauche                                                                              doite                                                                                    arrière gauche                                                                             arrière droite                                                                               mouvement débloquage lors détection mur                   remarque: ici on a donné plus de priorité à la fornt_droite (cf front_gauche) pour être plus efficace par exemple dans l'arena 4 en prise de décision                                                                                                                       déblocage si robot de même team
            rotation =  (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*0.9) + (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_right])*-0.9) + (int(self.team!=(sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*0.9) + (int(self.team!=sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_right])*-0.9) + (int(self.team!=(sensor_team[sensor_rear_left]))*(1-sensor_to_robot[sensor_rear_left])*1) + (int(self.team!=sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*-1) + (1-sensor_to_wall[sensor_front])*random.choice([-1,1]) + (1-sensor_to_wall[sensor_front_right])*0.9 + (1-sensor_to_wall[sensor_right])*0.5 + (1-sensor_to_wall[sensor_rear_right])*0.5 + ((1-sensor_to_wall[sensor_front_left])*-1)*0.7 + ((1-sensor_to_wall[sensor_left])*-1)*0.5 +  ((1-sensor_to_wall[sensor_rear_left])*-1)*0.5 + (int(self.team==sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*random.choice([-1,1])) +  (int(self.team==sensor_team[sensor_front_right])*(1-sensor_to_robot[sensor_front_right])*1) + (int(self.team==sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_front_left])*-1) + (int(self.team==sensor_team[sensor_right])*(1-sensor_to_robot[sensor_right])*1) + (int(self.team==sensor_team[sensor_left])*(1-sensor_to_robot[sensor_left])*-1) + (int(self.team==sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*1) + (int(self.team==sensor_team[sensor_rear_left])*(1-sensor_to_robot[sensor_rear_left])*-1) + (int(self.team==sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*random.choice([-1,1]))
            #print((sensor_to_robot[sensor_left]),(sensor_to_robot[sensor_front_left]),sensor_to_robot[sensor_front],sensor_to_robot[sensor_front_right],sensor_to_robot[sensor_right])

        elif self.robot_id == 3:
            # vitesse max mais ralentit lors des murs pour eviter des situations de blocage contre le mur et recul ou ralenti lors des robots de même team
                        #avancement par defaut              si repère un enemie devant                                                          si repère un enemie derrière                                                         ralenti/recul si mur                     si robot allié alors recul/ralentit                                         
            translation = sensor_to_robot[sensor_front]*1 + (int(self.team!=sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*0.9) + (int(self.team!=sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*-0.85) + (1-sensor_to_wall[sensor_front])*-0.8  + ((int(self.team==sensor_team[sensor_front]))*(1-sensor_to_robot[sensor_front])*-1) + ((int(self.team==sensor_team[sensor_front_right]))*(1-sensor_to_robot[sensor_front_right])*-1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*-1) + ((int(self.team==sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*-1) + ((int(self.team==sensor_team[sensor_right]))*(1-sensor_to_robot[sensor_right])*-1) + ((int(self.team==sensor_team[sensor_rear]))*(1-sensor_to_robot[sensor_rear])*1) + ((int(self.team==sensor_team[sensor_rear_right]))*(1-sensor_to_robot[sensor_rear_right])*1) + ((int(self.team==sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*1)# A MODIFIER
            # on va faire un robot qui suit les autres robots, mais dans un premier temps il va chercher par defaut sans trop coller au mur et essaye d'éviter les robots de même team (il évite les collisions) donc plus on a ce genre de robots plus il possède la capacité d'explorer tout en essayant de suivre les robots de l'équipe adverse
                        # devant gauche,                                                                             devant droite,                                                                                          gauche                                                                              doite                                                                                    arrière gauche                                                                             arrière droite                                                                               mouvement débloquage lors détection mur                   remarque: ici on a donné plus de priorité à la fornt_droite (cf front_gauche) pour être plus efficace par exemple dans l'arena 4 en prise de décision                                                                                                                       déblocage si robot de même team
            rotation =  (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_left])*0.9) + (int(self.team!=(sensor_team[sensor_front_left]))*(1-sensor_to_robot[sensor_front_right])*-0.9) + (int(self.team!=(sensor_team[sensor_left]))*(1-sensor_to_robot[sensor_left])*0.9) + (int(self.team!=sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_right])*-0.9) + (int(self.team!=(sensor_team[sensor_rear_left]))*(1-sensor_to_robot[sensor_rear_left])*1) + (int(self.team!=sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*-1) + (1-sensor_to_wall[sensor_front])*random.choice([-1,1]) + (1-sensor_to_wall[sensor_front_right])*0.9 + (1-sensor_to_wall[sensor_right])*0.5 + (1-sensor_to_wall[sensor_rear_right])*0.5 + ((1-sensor_to_wall[sensor_front_left])*-1)*0.7 + ((1-sensor_to_wall[sensor_left])*-1)*0.5 +  ((1-sensor_to_wall[sensor_rear_left])*-1)*0.5 + (int(self.team==sensor_team[sensor_front])*(1-sensor_to_robot[sensor_front])*random.choice([-1,1])) +  (int(self.team==sensor_team[sensor_front_right])*(1-sensor_to_robot[sensor_front_right])*1) + (int(self.team==sensor_team[sensor_front_left])*(1-sensor_to_robot[sensor_front_left])*-1) + (int(self.team==sensor_team[sensor_right])*(1-sensor_to_robot[sensor_right])*1) + (int(self.team==sensor_team[sensor_left])*(1-sensor_to_robot[sensor_left])*-1) + (int(self.team==sensor_team[sensor_rear_right])*(1-sensor_to_robot[sensor_rear_right])*1) + (int(self.team==sensor_team[sensor_rear_left])*(1-sensor_to_robot[sensor_rear_left])*-1) + (int(self.team==sensor_team[sensor_rear])*(1-sensor_to_robot[sensor_rear])*random.choice([-1,1]))
            #print((sensor_to_robot[sensor_left]),(sensor_to_robot[sensor_front_left]),sensor_to_robot[sensor_front],sensor_to_robot[sensor_front_right],sensor_to_robot[sensor_right])
            
        return translation, rotation, False