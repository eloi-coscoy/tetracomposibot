from robot import * 
import math
import random

nb_robots = 0
debug = False

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
        
        # --- 1. LECTURE CAPTEURS ---
        # On garde les valeurs brutes (0=Mur, 1=Loin) car les puissances marchent mieux avec
        sl = max(0.0, sensors[sensor_left])
        sf = max(0.0, sensors[sensor_front])
        sr = max(0.0, sensors[sensor_right])

        # --- 2. MOUVEMENT DIRECT (FORMULE POLYNOMIALE) ---
        # Formule : Moteur = Somme( Poids * (Capteur ^ Puissance) )
        # On utilise abs() sur la puissance pour éviter les bugs mathématiques
        
        # A. Calcul Translation (Indices 0 à 5)
        # P[0]*G^P[1] + P[2]*F^P[3] + P[4]*D^P[5]
        raw_trans = (self.param[0] * sl ** abs(self.param[1]) + 
                     self.param[2] * sf ** abs(self.param[3]) + 
                     self.param[4] * sr ** abs(self.param[5]))

        # B. Calcul Rotation (Indices 6 à 11)
        raw_rot =   (self.param[6] * sl ** abs(self.param[7]) + 
                     self.param[8] * sf ** abs(self.param[9]) + 
                     self.param[10]* sr ** abs(self.param[11]))

        # C. Bornage (Clamping)
        translation = max(0, min(1, raw_trans)) # Force entre 0 et 1
        rotation = max(-1, min(1, raw_rot))     # Force entre -1 et 1

        # --- 3. GESTION GENETIQUE (RESET) ---
        change = False
        if self.iteration >= self.it_per_evaluation:
            
            # 1. On sauvegarde le score de CET essai dans le total
            self.cumulated_score += self.score
            self.trial += 1 # On passe à l'essai suivant (0 -> 1 -> 2 -> 3 -> 4)
            
            print(f"Fin essai {self.trial}/12 - Score essaie: {self.score:.2f} - Total: {self.cumulated_score:.2f}")
            
            # On demande TOUJOURS au simulateur de changer de terrain à la fin d'un essai
            change = (self.trial % 3 == 0)

            # 2. EST-CE LA FIN DE LA GÉNÉRATION ? (A-t-on fait les 4 terrains ?)
            if self.trial >= 12:
                self.eval += 1 # On incrémente le numéro de génération
                
                # C'est ICI qu'on compare le TOTAL des 4 terrains avec le meilleur record
                if self.cumulated_score > self.best_score:
                    self.best_score = self.cumulated_score
                    self.best_param = self.param[:] # On sauvegarde l'ADN du champion
                    self.write_best_param()
                    print(f"GEN {self.eval} TERMINÉE : NOUVEAU RECORD = {self.best_score:.2f}")
                else:
                    print(f"GEN {self.eval} Terminée : Pas d'amélioration ({self.cumulated_score:.2f})")

                # 3. PRÉPARATION DE LA PROCHAINE GÉNÉRATION (MUTATION)
                # On repart toujours du meilleur génome connu (best_param)
                self.param = self.best_param[:]
                
                # On applique la mutation pour créer le nouveau challenger
                for i in range(12):
                    if random.random() < 0.5: # 50% de chance de muter un gène
                        self.param[i] += random.gauss(0, 0.2)

                # On reset les compteurs de génération
                self.trial = 0
                self.cumulated_score = 0
            
            else:
                # Si on n'a pas fini les 4 essais, on ne fait RIEN aux paramètres.
                # Le robot garde le même cerveau pour le prochain terrain.
                pass

            # 4. RESET COMMUN (Pour le prochain run, que ce soit même gen ou nouvelle)
            self.tab_score = [[0 for _ in range(100)] for _ in range(100)] # Reset mémoire visite
            self.score = 0      # Reset score courant
            self.iteration = 0  # Reset chrono
            self.get_new_pos()  # Reset position physique
            
            # True = Reset du robot par le simu
            # change = True (calculé plus haut) = Changement de map par le simu
            return 0, 0, True, change

        # --- 4. CALCUL DU SCORE (NOUVELLE VERSION) ---
        
        ix = int(self.x)
        iy = int(self.y)
        
        # A. Bonus Case Inconnue
        if self.tab_score[ix][iy] == 0:
            self.score += 10.0 # Grosse récompense
            self.tab_score[ix][iy] = 1 # On marque la case
        
        # B. Bonus Distance Origine (Fuir le nid)
        dist_origine = math.sqrt((self.x - self.x0)**2 + (self.y - self.y0)**2)
        
        self.score += dist_origine * 0.1

        self.iteration += 1

        return translation, rotation, False, False