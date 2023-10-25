import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
import json

# Fonction pour ajouter un nouveau mot de passe
def ajouter_mot_de_passe():
    nom_du_site = askstring("Ajouter un mot de passe", "Entrez le nom du site :")
    nom_utilisateur = askstring("Ajouter un mot de passe", f"Entrez le nom d'utilisateur pour {nom_du_site} :")
    mot_de_passe = askstring("Ajouter un mot de passe", f"Entrez le mot de passe pour {nom_utilisateur} :")
    if nom_du_site in mots_de_passe:
        print(f"Le site {nom_du_site} existe déjà dans la base de données.")
    else:
        mots_de_passe[nom_du_site] = {'utilisateur': nom_utilisateur, 'mot_de_passe': mot_de_passe}
        print(f"Le mot de passe pour {nom_du_site} a été ajouté avec succès.")
        sauvegarder_mots_de_passe()

# Fonction pour afficher les mots de passe
def afficher_mots_de_passe():
    onglet_affichage = ttk.Frame(onglets)
    onglets.add(onglet_affichage, text="Mots de passe")

    label_recherche = tk.Label(onglet_affichage, text="Recherche :")
    label_recherche.grid(row=0, column=0)
    champ_recherche = tk.Entry(onglet_affichage)
    champ_recherche.grid(row=0, column=1)
    bouton_recherche = tk.Button(onglet_affichage, text="Rechercher", command=lambda: rechercher_mot_de_passe(champ_recherche.get()))
    bouton_recherche.grid(row=0, column=2)

    tableau = ttk.Treeview(onglet_affichage, columns=("Site", "Utilisateur", "Mot de passe"))
    tableau.heading("#1", text="Site")
    tableau.heading("#2", text="Utilisateur")
    tableau.heading("#3", text="Mot de passe")

    tableau.grid(row=1, column=0, columnspan=3, sticky="nsew")
    tableau.column("#0", width=0)

    tableau.grid_rowconfigure(1, weight=1)
    tableau.grid_columnconfigure(0, weight=1)
    tableau.grid_columnconfigure(1, weight=1)
    tableau.grid_columnconfigure(2, weight=1)

    if not mots_de_passe:
        tableau.insert("", "end", values=("Aucun mot de passe n'a été enregistré", "", ""))
    else:
        for site, info in mots_de_passe.items():
            utilisateur = info.get('utilisateur', '')
            mot_de_passe = info.get('mot_de_passe', '')
            tableau.insert("", "end", values=(site, utilisateur, mot_de_passe))

# Fonction pour rechercher les mots de passe
def rechercher_mot_de_passe(terme_recherche):
    onglet_resultats = ttk.Frame(onglets)
    onglets.add(onglet_resultats, text="Résultats de la recherche")

    tableau = tk.Text(onglet_resultats, wrap=tk.WORD)
    tableau.pack()

    if not mots_de_passe:
        tableau.insert(tk.END, "Aucun mot de passe n'a été enregistré.")
    else:
        for site, info in mots_de_passe.items():
            ligne = f"{site} | {info['utilisateur']} | {info['mot_de_passe']}"
            if terme_recherche.lower() in site.lower() or terme_recherche.lower() in info['utilisateur'].lower():
                tableau.insert(tk.END, ligne + '\n')

# Fonction pour sauvegarder les mots de passe dans un fichier JSON
def sauvegarder_mots_de_passe():
    with open("password.json", "w") as fichier:
        json.dump(mots_de_passe, fichier)

def charger_mots_de_passe():
    try:
        with open("password.json", "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return {}

fenetre = tk.Tk()
fenetre.title("Gestionnaire de mots de passe")
fenetre.geometry("750x450")

mots_de_passe = charger_mots_de_passe()

onglets = ttk.Notebook(fenetre)
onglets.pack(fill="both", expand=True)

onglet_ajout = ttk.Frame(onglets)
onglets.add(onglet_ajout, text="Ajouter un mot de passe")

bouton_ajouter = tk.Button(onglet_ajout, text="Ajouter un mot de passe", command=ajouter_mot_de_passe)
bouton_ajouter.grid(row=0, column=0)

bouton_afficher = tk.Button(onglet_ajout, text="Afficher les mots de passe", command=afficher_mots_de_passe)
bouton_afficher.grid(row=0, column=1)

fenetre.mainloop()
