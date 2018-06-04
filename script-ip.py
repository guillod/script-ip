#!/usr/bin/env python3

###################################################################################################
## Script python3 pour rentrer les notes sur IP (https://etu.math.upmc.fr/math/) automatiquement ##
## à partir d'un fichier CSV, par Julien Guillod (4 juin 2018)                                   ##
###################################################################################################

### Dépendances : ###
#   * firefox
#   * csv (installed by default on ubuntu otherwise execute "pip3 install csv")
#   * code (installed by default on ubuntu otherwise execute "pip3 install code")
#   * selenium (install the package python3-selenium on ubuntu or execute "pip3 install selenium")
#   * geckodriver (download the executable from https://github.com/mozilla/geckodriver/releases and add its location to $PATH)

# Testé sous ubuntu 16.04 avec firefox v60.0.1, selenium v3.8.1 et geckodriver v0.19.1

### Format de fichier CSV : ###
# doit contenir une colonne avec le numéro de l'étudiant (avec label id par exemple) et une autre avec la note (avec lable note par exemple),
# d'autres colonnes sont permises. Exemple de fichier notes.csv :
#   id,note,other
#   3409999,5,ert
#   3419999,5.6,rtt
#   3709999,5.8,rtz
#   3739999,Abs,rtz
#   3439999,AbsJ,ert

### Utilisation : ###
#   1. Lancer le script avec ./script-IP
#   2. Une fois que firefox a terminé de charger, procéder au login.
#   3. Naviguer jusqu'à la page du cours, cliquer sur "saisir les notes" et enfin sur la colonne correspondante aux notes à rentrer.
#   4. Taper la commande "upload('notes.csv', 'id', 'note')" pour remplir automatiquement les notes sur la page firefox depuis les colonnes 'id' et 'note' du fichier 'notes.csv'.
#   5. Contrôler que les notes sont rentrées correctement sur firefox et cliquer sur le bouton "Envoyer".
#   6. C'est terminé, taper quit() sur la ligne de commande pour quitter ou recommencer au point 3. pour remplir les notes d'un autre examen.

### Spécifications ###
# Le script remplit les notes de tout les étudiants affichés sur la page IP qui sont également présents dans le fichier CSV (i.e. l'intersection des deux). Les notes présentes dans le fichier csv et sur la page IP sont écrasées, les autres notes sont conservées.

import csv, code
from selenium import webdriver

# function to import CSV file to dict with notes['id'] = 'mark'
def load(filename, idd, mark):
    with open(filename) as file:
        notes = {}
        for row in csv.DictReader(file):
            notes[row[idd]] = row[mark]
    return notes

# function to fill the marks
def fill(notes):
    #iterate over the number of notes in html
    nb_notes = int(browser.find_element_by_id("nb_notes").get_attribute("value"))
    for i in range(nb_notes):
        # student's number corresponding to ith note
        no_etu = browser.find_element_by_id('dossier'+str(i)).get_attribute("value")
        # check if no_etu corresponds to a note in the csv
        if no_etu in notes.keys():
            # student's note
            note = notes[no_etu]
            # write note to html
            note_id = browser.find_element_by_id('note'+str(i))
            note_id.clear()
            note_id.send_keys(note)
            # execture onblur to update checkboxes and other verification checks
            #browser.execute_script("document.activeElement.onblur()")

# main function to upload csv
def upload(filename, idd, mark):
    # try to parse filename
    try:
        notes = load(filename, idd, mark)
        print("The file %s was parsed successfully." % filename)
    except:
        print("Error: unable to parse the file %. Please check the grammar of your CSV file." % filename)
        return
    
    # try to fill the marks
    try:
        fill(notes)
        print("Please check that the marks are correctly filled and click on the button Envoi to save the marks on IP.")
    except:
        print("Error: unable to fill the page with the marks. Please try again on the correct webpage or type quit() to exit.")

# exit firefox on quit
def quit():
    browser.quit()
    exit()

# main
if __name__ == '__main__':
    # open firefox
    print("Firefox is now loading...")
    browser = webdriver.Firefox()
    browser.get('https://etu.math.upmc.fr/math/')

    # wait until user browse to the correct page and wait for command to be executed
    print("Please login and browse to the page where you can enter the marks")
    print("Once you have reach the page, type upload('notes.csv', 'id', 'note') to upload the columns id and note of the file notes.csv.")
    print("Type quit() to exit. It is possible to run the command upload more than once.")
    code.interact(banner='', local=locals())

