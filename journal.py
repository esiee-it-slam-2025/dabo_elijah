"""
Cours "Advanced 2" - Exercice "Journal"
Réalisé par Xxxxx XXXXX
"""

import argparse
import random
from donnees import articles, interviews

class ElementJournal:
    def __init__(self, date, edition, auteur, titre, contenu, **kwargs):
        self.date = date
        self.edition = edition
        self.auteur = auteur
        self.titre = titre
        self.contenu = contenu

        for key, value in kwargs.items():
            setattr(self, key, value)

class Article(ElementJournal):
    def __init__(self, date, edition, auteur, titre, contenu, **kwargs):
        super().__init__(date, edition, auteur, titre, contenu, **kwargs)

class Interview(ElementJournal):
    def __init__(self, date, edition, auteur, invite, contenu, **kwargs):
        super().__init__(date, edition, auteur, invite, contenu, **kwargs)

class Generateur:
    def __init__(self, date, edition):
        self.date = date
        self.edition = edition

    def importer(self):

        elements = [Article(**article) for article in articles if article['date'] == self.date and (article['edition'] == self.edition or article['edition'] == 'national')]
        elements += [Interview(**interview) for interview in interviews if interview['date'] == self.date and (interview['edition'] == self.edition or interview['edition'] == 'national')]
        random.shuffle(elements)
        return elements

    def afficher(self, elements):
        print("==================================")
        print("*-*-*-*-*-* LeLutécien *-*-*-*-*-*")
        print("==================================")
        for element in elements:
            print(f"Type: {'Article' if isinstance(element, Article) else 'Interview'}")
            print(f"Titre: {element.titre}")
            print(f"Édition: {element.edition}")
            print(f"Contenu: {element.contenu}")
            print("---------------")
        with open('credits.txt', 'r', encoding='utf-8') as file:
            credits = file.read()
            print("\nCrédits:\n" + credits)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère le journal du jour qui dépend d'une date et d'une région.")
    parser.add_argument("date", help="Génerer une Date du journal, sous le format 'annee-mois-jour'")
    parser.add_argument("edition", help="Édition du journal à générer", choices=["national", "idf", "paca"])
    args = parser.parse_args()

    generateur = Generateur(args.date, args.edition)
    elements = generateur.importer()
    generateur.afficher(elements)