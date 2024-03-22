personnage = {
    "PV": 100,
    "Age": None,
    "Nom": None,
    "Techniques": {},
    "Etage": 1,
    "Points": 5,
    "Badges": 0,
    "KaiokenUtilise": False,
    "DeplacementInstantaneUtilise": False,
    "Plats": []
}

techniques = {
    "Son Goku": {
        "Kaméhaméha": 40,
        "Genkidama": 40,
        "Kaioken": 1.5,
        "Déplacement instantané": None
    },
    "Vegeta": {
        "Rayon Garric": 40,
        "Final Flash": 40,
        "Boost de Puissance": 1.5,
        "Déplacement instantané": None
    }
}

ennemis = {
    1: ("Soldat", 70, 10),
    2: ("Super Soldat", 100, 15),
    4: ("Le Gardien", 150, 20),
}

plats = {
    "Ramen": 25,
    "Onigiri": 25,
    "Udon": 25,
    "Curry": 25
}

def initialisation_jeu():
    print("Bienvenue dans le vaisseau de Babidi ! Vous êtes dans le Hall du 1er étage.")
    age = int(input("Quel est votre âge ? "))
    if age < 12:
        print("Désolé, vous n'avez pas l'âge requis pour jouer.")
        return
    choix_personnage = input("Souhaitez-vous jouer Son Goku ou Vegeta ? ")
    if choix_personnage.lower() in ["son goku", "goku"]:
        personnage["Nom"] = "Son Goku"
        personnage["Techniques"] = techniques["Son Goku"]
    elif choix_personnage.lower() in ["vegeta"]:
        personnage["Nom"] = "Vegeta"
        personnage["Techniques"] = techniques["Vegeta"]
    else:
        print("Choix non valide. Veuillez recommencer.")
        initialisation_jeu()
    print(f"\nVous avez choisi {personnage['Nom']} ! Préparez-vous pour l'aventure.\n")
    navigation()

def navigation():
    lieu_actuel = "Hall"
    while True:
        if lieu_actuel == "Hall":
            action = input("Où souhaitez-vous aller ? (Couloir/Quitter): ")
            if action == "Couloir":
                lieu_actuel = "Couloir"
            elif action == "Quitter":
                print("Merci d'avoir joué. À bientôt !")
                break
        elif lieu_actuel == "Couloir":
            action = input("Où souhaitez-vous aller ? (Hall/Escalier): ")
            if action == "Hall":
                lieu_actuel = "Hall"
            elif action == "Escalier":
                gestion_escalier()

def gestion_escalier():
    print(f"Vous êtes à l'escalier de l'étage {personnage['Etage']}.")
    choix = input("Souhaitez-vous monter ou descendre ? (Monter/Descendre/Retour): ").lower()
    if choix == "descendre" and personnage["Etage"] < 5:
        personnage["Etage"] += 1
        if personnage["Etage"] in [1, 2, 4]:
            lieu_combat_etage()
        elif personnage["Etage"] == 3:
            lieu_cafeteria()
    elif choix == "monter" and personnage["Etage"] > 1:
        personnage["Etage"] -= 1
    else:
        print("Action non valide ou impossible.")

def lieu_combat_etage():
    ennemi, ennemi_pv, ennemi_degats = ennemis.get(personnage["Etage"], (None, 0, 0))
    if ennemi:
        print(f"Vous entrez dans l'Arène de Combat pour affronter un {ennemi} !")
        combat_tour_par_tour(ennemi, ennemi_pv, ennemi_degats)

def combat_tour_par_tour(ennemi, ennemi_pv, ennemi_degats):
    while ennemi_pv > 0 and personnage["PV"] > 0:
        choix_action = input("Choisissez votre action (Attaquer/Consommer un plat): ")
        if choix_action == "Attaquer":
            print("Choisissez une technique :")
            for nom, effet in personnage["Techniques"].items():
                print(f"- {nom}")
            technique = input("> ")
            if technique in personnage["Techniques"]:
                if technique == "Kaioken" and not personnage["KaiokenUtilise"]:
                    personnage["KaiokenUtilise"] = True
                    print("Kaioken activé pour le prochain tour !")
                elif technique == "Déplacement instantané" and not personnage["DeplacementInstantaneUtilise"]:
                    personnage["DeplacementInstantaneUtilise"] = True
                    print("Vous esquivez l'attaque de l'ennemi.")
                    continue
                else:
                    degats = personnage["Techniques"][technique]
                    ennemi_pv -= degats
                    print(f"Vous utilisez {technique} et infligez {degats} points de dégâts à l'ennemi.")
            else:
                print("Technique non reconnue.")
        elif choix_action == "Consommer un plat" and personnage["Plats"]:
            pass
        else:
            print("Action non reconnue ou impossible.")
        
        if ennemi_pv > 0:
            personnage["PV"] -= ennemi_degats
            print(f"{ennemi} attaque et vous inflige {ennemi_degats} points de dégâts.")
        
        if personnage["PV"] <= 0:
            print("Vous avez été vaincu... Le jeu est terminé.")
            break
        
        if ennemi_pv <= 0:
            print(f"Vous avez vaincu {ennemi} et gagné un badge !")
            personnage["Badges"] += 1
            if personnage["Etage"] < 5:
                print("Vous pouvez maintenant descendre au prochain étage.")
            else:
                print("Félicitations, vous avez atteint le dernier étage et trouvé le Cocon de Buu !")
                break

def lieu_cafeteria():
    print("Vous êtes dans la cafétéria. Voici les plats disponibles (2 points chacun) :")
    for nom, pv in plats.items():
        print(f"{nom}: +{pv} PV")
    choix = input("Quel plat souhaitez-vous acheter ? (Entrez le nom du plat ou 'Retour' pour revenir) : ")
    if choix in plats and personnage["Points"] >= 2:
        personnage["Plats"].append(choix)
        personnage["Points"] -= 2
        print(f"Vous avez acheté {choix}. Vous pouvez le consommer pendant un combat.")
    elif choix == 'Retour':
        print("Retour au couloir.")
    else:
        print("Choix invalide ou points insuffisants.")

def consommer_plat():
    if not personnage["Plats"]:
        print("Vous n'avez pas de plats à mmanger.")
        return
    print("Quel plat souhaitez-vous manger ?")
    for i, plat in enumerate(personnage["Plats"], start=1):
        print(f"{i}. {plat}")
    choix = int(input("> ")) - 1
    if 0 <= choix < len(personnage["Plats"]):
        plat_choisi = personnage["Plats"].pop(choix)
        pv_gagnes = plats[plat_choisi]
        personnage["PV"] += pv_gagnes
        print(f"Vous avez consommé {plat_choisi} et gagné {pv_gagnes} PV.")
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    initialisation_jeu()
