"""
Module de simulation de file d'attente M/M/c - VERSION AVEC VARIABLE DISCRÈTE
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
        self.debug = False  # Désactiver le débogage par défaut
    
    def set_seed(self, seed):
        """Fixer la graine aléatoire pour reproductibilité"""
        self.rng = np.random.RandomState(seed)
    
    def set_debug(self, enabled):
        """Activer/désactiver les messages de débogage"""
        self.debug = enabled
    
    def simuler(self, duree):
        """Simule le système pendant 'duree' minutes"""
        if duree <= 0:
            duree = 480
        
        if self.debug:
            print("\n" + "="*50)
            print("DÉMARRAGE SIMULATION")
            print("="*50)
            print(f"λ = {self.lambda_} clients/min")
            print(f"μ = {self.mu} clients/min")
            print(f"c = {self.c} caisses")
            print(f"ρ = {self.rho:.4f} ({'STABLE' if self.rho < 1 else 'INSTABLE'})")
            print(f"Durée = {duree} minutes")
            print("="*50)
        
        # Initialisation
        temps_actuel = 0.0
        nb_clients = 0
        nb_clients_servis = 0
        caisses_libres = self.c
        file_attente = []
        temps_fin_service = []
        
        # Variables continues
        temps_attente = []
        instants_changement = [0.0]
        nb_clients_instants = [0]
        
        # 🔴 NOUVEAU : Variables discrètes (nombre de clients en file)
        nb_file_instants = [0]          # Valeurs du nombre en file
        nb_file_instants_temps = [0.0]  # Temps correspondants
        
        # Compteurs pour statistiques
        nb_arrivees = 0
        nb_departs = 0
        nb_service_immediat = 0
        nb_mis_en_file = 0
        nb_sortie_file = 0
        
        # Première arrivée
        prochaine_arrivee = self.rng.exponential(1.0 / self.lambda_)
        
        if self.debug:
            print(f"\n[INIT] Première arrivée programmée à t = {prochaine_arrivee:.3f} min")
            print(f"[INIT] {self.c} caisses libres")
        
        max_iterations = 10000000
        iterations = 0
        
        while temps_actuel < duree and iterations < max_iterations:
            iterations += 1
            prochain_depart = min(temps_fin_service) if temps_fin_service else float('inf')
            
            if prochaine_arrivee < prochain_depart and prochaine_arrivee < duree:
                # ===== ARRIVÉE d'un client =====
                temps_actuel = prochaine_arrivee
                nb_arrivees += 1
                nb_clients += 1
                instants_changement.append(temps_actuel)
                nb_clients_instants.append(nb_clients)
                
                # 🔴 Enregistrer le nombre de clients en file à l'arrivée
                nb_file = max(0, nb_clients - self.c)
                nb_file_instants.append(nb_file)
                nb_file_instants_temps.append(temps_actuel)
                
                if self.debug and nb_arrivees <= 20:
                    print(f"\n[ARRIVÉE #{nb_arrivees}] t = {temps_actuel:.3f} min")
                    print(f"   → Clients dans système: {nb_clients}")
                    print(f"   → Caisses libres: {caisses_libres}/{self.c}")
                    print(f"   → File d'attente: {len(file_attente)} clients")
                
                # Planifier prochaine arrivée
                inter_arrivee = self.rng.exponential(1.0 / self.lambda_)
                prochaine_arrivee = temps_actuel + inter_arrivee
                
                if caisses_libres > 0:
                    # SERVICE IMMÉDIAT
                    caisses_libres -= 1
                    nb_service_immediat += 1
                    duree_service = self.rng.exponential(1.0 / self.mu)
                    temps_fin = temps_actuel + duree_service
                    temps_fin_service.append(temps_fin)
                    temps_attente.append(0.0)  # Pas d'attente
                    
                    if self.debug and nb_arrivees <= 20:
                        print(f"   → ✅ SERVICE IMMÉDIAT (caisse libre)")
                        print(f"      Durée service = {duree_service:.3f} min")
                        print(f"      Fin service à t = {temps_fin:.3f} min")
                else:
                    # MISE EN FILE D'ATTENTE
                    nb_mis_en_file += 1
                    file_attente.append(temps_actuel)
                    
                    if self.debug and nb_arrivees <= 20:
                        print(f"   → ⏳ MISE EN FILE (toutes caisses occupées)")
                        print(f"      File d'attente: {len(file_attente)} clients")
                        print(f"      Temps d'arrivée enregistré: {temps_actuel:.3f}")
            
            elif prochain_depart < duree:
                # ===== DÉPART d'un client =====
                temps_actuel = prochain_depart
                nb_departs += 1
                temps_fin_service.remove(prochain_depart)
                caisses_libres += 1
                nb_clients -= 1
                nb_clients_servis += 1
                instants_changement.append(temps_actuel)
                nb_clients_instants.append(nb_clients)
                
                # 🔴 Enregistrer le nombre de clients en file au départ
                nb_file = max(0, nb_clients - self.c)
                nb_file_instants.append(nb_file)
                nb_file_instants_temps.append(temps_actuel)
                
                if self.debug and nb_departs <= 20:
                    print(f"\n[DÉPART #{nb_departs}] t = {temps_actuel:.3f} min")
                    print(f"   → Clients restants: {nb_clients}")
                    print(f"   → Caisses libres: {caisses_libres}/{self.c}")
                    print(f"   → File d'attente: {len(file_attente)} clients")
                
                if file_attente:
                    # Un client de la file passe en service
                    temps_arrivee_file = file_attente.pop(0)
                    nb_sortie_file += 1
                    temps_attente_file = max(0.0, temps_actuel - temps_arrivee_file)
                    temps_attente.append(temps_attente_file)
                    
                    if self.debug and nb_departs <= 20:
                        print(f"   → 🚪 SORTIE DE FILE")
                        print(f"      Client arrivé à t = {temps_arrivee_file:.3f}")
                        print(f"      Temps d'attente = {temps_attente_file:.3f} min")
                    
                    # Nouveau service
                    caisses_libres -= 1
                    duree_service = self.rng.exponential(1.0 / self.mu)
                    temps_fin = temps_actuel + duree_service
                    temps_fin_service.append(temps_fin)
                    
                    if self.debug and nb_departs <= 20:
                        print(f"      Nouvelle durée service = {duree_service:.3f} min")
                        print(f"      Fin service à t = {temps_fin:.3f} min")
                else:
                    if self.debug and nb_departs <= 20:
                        print(f"   → File vide, caisse libérée")
            else:
                break
        
        # Ajouter l'instant final
        if temps_actuel < duree:
            instants_changement.append(duree)
            nb_clients_instants.append(nb_clients)
            
            # 🔴 Ajouter l'état final de la file
            nb_file = max(0, nb_clients - self.c)
            nb_file_instants.append(nb_file)
            nb_file_instants_temps.append(duree)
        
        # Calcul des moyennes temporelles (continues)
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
        
        # ===== 🔴 CALCUL DE LA DISTRIBUTION DISCRÈTE =====
        distribution_file = {}
        total_temps = 0
        
        for i in range(len(nb_file_instants_temps) - 1):
            duree_etat = nb_file_instants_temps[i+1] - nb_file_instants_temps[i]
            nb_file = nb_file_instants[i]
            distribution_file[nb_file] = distribution_file.get(nb_file, 0) + duree_etat
            total_temps += duree_etat
        
        # Convertir en probabilités
        for k in distribution_file:
            distribution_file[k] /= total_temps if total_temps > 0 else 1
        
        # Trier par clé
        distribution_file = dict(sorted(distribution_file.items()))
        
        # 🔴 Calcul des statistiques discrètes
        nb_file_values = list(distribution_file.keys())
        nb_file_probas = list(distribution_file.values())
        
        # Moyenne de la file
        moyenne_file = sum(k * p for k, p in zip(nb_file_values, nb_file_probas))
        
        # Variance
        variance_file = sum((k - moyenne_file) ** 2 * p for k, p in zip(nb_file_values, nb_file_probas))
        
        # Probabilité que la file soit vide
        proba_file_vide = distribution_file.get(0, 0)
        
        # Probabilité file > 5 clients
        proba_file_grande = sum(p for k, p in zip(nb_file_values, nb_file_probas) if k > 5)
        
        # ===== AFFICHAGE DES RÉSULTATS =====
        if self.debug:
            print("\n" + "="*50)
            print("RÉSUMÉ DE LA SIMULATION")
            print("="*50)
            print(f"Événements traités: {iterations}")
            print(f"Arrivées: {nb_arrivees}")
            print(f"Départs: {nb_departs}")
            print(f"Clients servis: {nb_clients_servis}")
            print(f"Services immédiats: {nb_service_immediat}")
            print(f"Mises en file: {nb_mis_en_file}")
            print(f"Sorties de file: {nb_sortie_file}")
            print(f"File restante à la fin: {len(file_attente)}")
            print(f"Caisses occupées à la fin: {self.c - caisses_libres}")
            print("-"*50)
            print(f"Taille échantillon temps d'attente: {len(temps_attente)}")
            
            if temps_attente:
                print(f"Premiers temps d'attente: {temps_attente[:10]}")
                print(f"Moyenne: {np.mean(temps_attente):.3f} min")
                print(f"Min: {min(temps_attente):.3f} min")
                print(f"Max: {max(temps_attente):.3f} min")
                attente_positive = sum(1 for t in temps_attente if t > 0)
                print(f"Clients avec attente > 0: {attente_positive} ({attente_positive/len(temps_attente)*100:.1f}%)")
            else:
                print("⚠️ Aucun temps d'attente enregistré !")
            
            print("-"*50)
            print("🔴 STATISTIQUES DISCRÈTES (Nombre de clients en file)")
            print(f"Moyenne: {moyenne_file:.3f} clients")
            print(f"Variance: {variance_file:.3f}")
            print(f"Écart-type: {np.sqrt(variance_file):.3f}")
            print(f"P(file vide) = {proba_file_vide:.3f}")
            print(f"P(file > 5) = {proba_file_grande:.3f}")
            print("="*50)
        
        # Retourner tous les résultats
        return {
            # Paramètres
            'lambda': self.lambda_,
            'mu': self.mu,
            'c': self.c,
            'rho': self.rho,
            'duree_effective': float(duree_effective),
            'nb_clients_servis': int(nb_clients_servis),
            
            # Variables continues
            'temps_attente_moyen': float(np.mean(temps_attente)) if temps_attente else 0.0,
            'temps_attente_echantillon': [float(t) for t in temps_attente],
            'nb_moyen_clients': float(nb_moyen_clients),
            'nb_moyen_file': float(nb_moyen_file),
            
            # 🔴 NOUVELLES VARIABLES DISCRÈTES
            'distribution_file': distribution_file,
            'moyenne_file_discrete': float(moyenne_file),
            'variance_file': float(variance_file),
            'proba_file_vide': float(proba_file_vide),
            'proba_file_grande': float(proba_file_grande),
            'nb_file_instants': nb_file_instants,
            'nb_file_instants_temps': nb_file_instants_temps,
            
            # Données de débogage
            'debug': {
                'nb_arrivees': nb_arrivees,
                'nb_departs': nb_departs,
                'nb_service_immediat': nb_service_immediat,
                'nb_mis_en_file': nb_mis_en_file,
                'nb_sortie_file': nb_sortie_file
            }
        }