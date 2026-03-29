"""
Module de simulation de file d'attente M/M/c - VERSION ULTIME CORRIGÉE
"""

import numpy as np

class SimulationFileAttente:
    """Simulation d'une file d'attente M/M/c"""
    
    def __init__(self, lambda_, mu, c):
        if lambda_ <= 0 or mu <= 0 or c <= 0:
            raise ValueError("Les paramètres doivent être positifs")
        
        self.lambda_ = float(lambda_)
        self.mu = float(mu)
        self.c = int(c)
        self.rho = self.lambda_ / (self.c * self.mu) if (self.c * self.mu) > 0 else float('inf')
        self.rng = np.random.RandomState()
    
    def simuler(self, duree):
        """Simule le système pendant 'duree' minutes"""
        if duree <= 0:
            duree = 480
        
        print("\n=== DÉMARRAGE SIMULATION ===")
        print(f"λ={self.lambda_}, μ={self.mu}, c={self.c}, durée={duree}")
        
        # Initialisation
        temps_actuel = 0.0
        nb_clients = 0
        nb_clients_servis = 0
        caisses_libres = self.c
        file_attente = []
        temps_fin_service = []
        
        # Collecte des données
        temps_attente = []  # ← C'EST ICI QU'ON STOCKE LES TEMPS D'ATTENTE
        instants_changement = [0.0]
        nb_clients_instants = [0]
        
        # Première arrivée
        try:
            prochaine_arrivee = self.rng.exponential(1.0 / self.lambda_)
            print(f"Première arrivée à t={prochaine_arrivee:.3f} min")
        except:
            prochaine_arrivee = 1.0
            print("⚠️ Utilisation valeur par défaut pour première arrivée")
        
        max_iterations = 10000000
        iterations = 0
        
        while temps_actuel < duree and iterations < max_iterations:
            iterations += 1
            prochain_depart = min(temps_fin_service) if temps_fin_service else float('inf')
            
            if prochaine_arrivee < prochain_depart and prochaine_arrivee < duree:
                # ARRIVÉE d'un client
                temps_actuel = prochaine_arrivee
                nb_clients += 1
                instants_changement.append(temps_actuel)
                nb_clients_instants.append(nb_clients)
                
                # Planifier prochaine arrivée
                try:
                    prochaine_arrivee = temps_actuel + self.rng.exponential(1.0 / self.lambda_)
                except:
                    prochaine_arrivee = temps_actuel + 1.0
                
                if caisses_libres > 0:
                    # SERVICE IMMÉDIAT
                    caisses_libres -= 1
                    try:
                        duree_service = self.rng.exponential(1.0 / self.mu)
                    except:
                        duree_service = 1.0
                    temps_fin_service.append(temps_actuel + duree_service)
                    temps_attente.append(0.0)  # ← TEMPS D'ATTENTE = 0 (pas d'attente)
                else:
                    # MISE EN FILE D'ATTENTE
                    file_attente.append(temps_actuel)
                    # On n'ajoute pas encore le temps d'attente, il sera calculé au départ
            
            elif prochain_depart < duree:
                # DÉPART d'un client
                temps_actuel = prochain_depart
                temps_fin_service.remove(prochain_depart)
                caisses_libres += 1
                nb_clients -= 1
                nb_clients_servis += 1
                instants_changement.append(temps_actuel)
                nb_clients_instants.append(nb_clients)
                
                if file_attente:
                    # Un client de la file passe en service
                    temps_arrivee_file = file_attente.pop(0)
                    temps_attente_file = max(0.0, temps_actuel - temps_arrivee_file)
                    
                    # 🔴 C'EST ICI QU'ON AJOUTE LES TEMPS D'ATTENTE NON NULS
                    temps_attente.append(temps_attente_file)
                    
                    # Nouveau service
                    caisses_libres -= 1
                    try:
                        duree_service = self.rng.exponential(1.0 / self.mu)
                    except:
                        duree_service = 1.0
                    temps_fin_service.append(temps_actuel + duree_service)
            else:
                break
        
        # Ajouter l'instant final
        if temps_actuel < duree:
            instants_changement.append(duree)
            nb_clients_instants.append(nb_clients)
        
        # Calcul des moyennes temporelles
        nb_moyen_clients = 0.0
        nb_moyen_file = 0.0
        for i in range(len(instants_changement) - 1):
            intervalle = instants_changement[i+1] - instants_changement[i]
            nb_moyen_clients += nb_clients_instants[i] * intervalle
            nb_en_file = max(0, nb_clients_instants[i] - self.c)
            nb_moyen_file += nb_en_file * intervalle
        
        duree_effective = instants_changement[-1] if instants_changement else duree
        if duree_effective > 0:
            nb_moyen_clients /= duree_effective
            nb_moyen_file /= duree_effective
        
        # 🔍 DÉBOGAGE - Afficher ce qu'on a collecté
        print(f"\n=== RÉSULTATS DE LA SIMULATION ===")
        print(f"Clients servis: {nb_clients_servis}")
        print(f"Taille de temps_attente: {len(temps_attente)}")
        
        if temps_attente:
            print(f"Premiers temps: {temps_attente[:10]}")
            print(f"Moyenne calculée: {np.mean(temps_attente):.3f}")
            print(f"Min: {min(temps_attente):.3f}, Max: {max(temps_attente):.3f}")
            print(f"Nombre de clients avec attente > 0: {sum(1 for t in temps_attente if t > 0)}")
        else:
            print("⚠️ ATTENTION: temps_attente est VIDE !")
            print("   Vérifiez que des clients ont été mis en file d'attente.")
        
        return {
            'lambda': self.lambda_,
            'mu': self.mu,
            'c': self.c,
            'rho': self.rho,
            'duree_effective': float(duree_effective),
            'nb_clients_servis': int(nb_clients_servis),
            'temps_attente_moyen': float(np.mean(temps_attente)) if temps_attente else 0.0,
            'temps_attente_echantillon': [float(t) for t in temps_attente],  # ← CRITIQUE
            'nb_moyen_clients': float(nb_moyen_clients),
            'nb_moyen_file': float(nb_moyen_file)
        }