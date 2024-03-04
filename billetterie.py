"""
Cours "Introduction 1" - Exercice "Billetterie"
"""

# Variables
stations = {
    "Meinohama": 1.5,
    "Muromi": 0.8,
    "Fujisaki": 1.1,
    "Nishijin": 1.2,
    "Tojinmachi": 0.8,
    "Ohorikoen (Ohori Park)": 1.1,
    "Akasaka": 0.8,
    "Tenjin": 0.8,
    "Nakasu-Kawabata": 1.0,
    "Gion": 0.7,
    "Hakata": 1.2,
    "Higashi-Hie": 2.1,
    "Fukuokakuko (Airport)": 0.0,
}
stations_names = list(stations.keys())
stations_distances = list(stations.values())
nb_billets_adulte = 0
has_reduit = False

# Introduction
print("           /////// ")
print("         ///       ")
print("  //////////////   ")
print("      ///          ")
print("///////            ")
print("\nBienvenue sur la billetterie du métro municipal de Fukuoka.")

# Questions à l'utilisateur

# Calculs de l'itinéraire

# Choix de la bonne zone tarifaire

# Calcul du coût total

# Affichage des détails du voyage et du tarif

# Affichage de la voie du train à emprunter


#Début de l'éxercice
print("           /////// ")
print("         ///       ")
print("  //////////////   ")
print("      ///          ")
print("///////            ")
print("\nBienvenue sur la billetterie du métro municipal de Fukuoka.")

#Les différentes stations et distances entre (stations)
stations = {
    "Meinohama": 1.5,
    "Muromi": 0.8,
    "Fujisaki": 1.1,
    "Nishijin": 1.2,
    "Tojinmachi": 0.8,
    "Ohorikoen (Ohori Park)": 1.1,
    "Akasaka": 0.8,
    "Tenjin": 0.8,
    "Nakasu-Kawabata": 1.0,
    "Gion": 0.7,
    "Hakata": 1.2,
    "Higashi-Hie": 2.1,
    "Fukuokakuko (Airport)": 0.0,
}

stations_names = list(stations.keys())
stations_distances = list(stations.values())
nb_billets_adulte = 0
has_reduit = False
   
#Demander le nombre de billets adulte voulu
def demander_nombre_billets(message):
    while True:
        try:
            nombre = int(input(message))
            if nombre < 0:
                print("Veuillez entrer un nombre positif.")
            else:
                return nombre
        except ValueError:
            print("Veuillez entrer un nombre entier.")

nb_billets_adulte = demander_nombre_billets("Combien de billets adulte voulez-vous ? ")

#Demander si il veut des billets à tarif réduit
reponse = input("Voulez-vous un ou des billets tarif réduit (Oui/Non) ? ")
if reponse.lower() == "oui":
    has_reduit = True
    nb_billets_reduit = demander_nombre_billets("Combien de billets à tarif réduit voulez-vous ? ")
else:
    nb_billets_reduit = 0

#Demande des stations de départ et d'arrivée
def demander_station(message):
    print("\nStations :")
    for i, station in enumerate(stations_names, 1):
        print(f"{i}. {station}")
    while True:
        try:
            choix = int(input(message))
            if choix < 1 or choix > len(stations):
                print("Veuillez entrer un numéro de station.")
            else:
                return stations_names[choix - 1]
        except ValueError:
            print("Veuillez entrer un numéro de station.")

depart = demander_station("Entrez le numéro de la station de départ : ")
arrivee = demander_station("Entrez le numéro de la station d'arrivée : ")

#Calcul de la zone tarifaire
def calculer_zone_tarifaire(depart, arrivee):
    distance = abs(stations_distances[stations_names.index(depart)] - stations_distances[stations_names.index(arrivee)])
    if distance <= 3:
        return 1
    elif 3 < distance <= 7:
        return 2
    elif 7 < distance <= 11:
        return 3
    elif 11 < distance <= 15:
        return 4

zone = calculer_zone_tarifaire(depart, arrivee)

#Calcul du prix unitaire
def calculer_prix(zone, is_reduit):
    tarifs = {
        1: (210, 110),
        2: (260, 130),
        3: (300, 150),
        4: (340, 170),
    }
    prix_plein, prix_reduit = tarifs[zone]
    return prix_reduit if is_reduit else prix_plein

prix_unitaire = calculer_prix(zone, has_reduit)

#Afficher les informations finales
def afficher_details(depart, arrivee, nb_billets_adulte, nb_billets_reduit, zone, prix_unitaire):
    print("\nDétails du voyage :")
    print(f"De {depart} à {arrivee}")
    print(f"Nombre de billets adulte : {nb_billets_adulte}")
    print(f"Nombre de billets à tarif réduit : {nb_billets_reduit}")
    print(f"Zone tarifaire : {zone}")
    print(f"Prix unitaire : {prix_unitaire} yen")

afficher_details(depart, arrivee, nb_billets_adulte, nb_billets_reduit, zone, prix_unitaire)

def afficher_cout_total(nb_billets_adulte, nb_billets_reduit, prix_unitaire):
    total = (nb_billets_adulte + nb_billets_reduit) * prix_unitaire
    print(f"\nCoût total : {total} yen")

afficher_cout_total(nb_billets_adulte, nb_billets_reduit, prix_unitaire)

def afficher_voie(depart, arrivee):
    if stations_distances[stations_names.index(depart)] < stations_distances[stations_names.index(arrivee)]:
        print("\nVoie à emprunter : Voie 2 (Fukuokakuko (Airport) -> Meinohama)")
    else:
        print("\nVoie à emprunter : Voie 1 (Meinohama -> Fukuokakuko (Airport)")

afficher_voie(depart, arrivee)