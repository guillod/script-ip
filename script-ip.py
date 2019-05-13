#!/usr/bin/env python3

###################################################################################
## Script python3 pour rentrer les notes sur IP (https://etu.math.upmc.fr/math/) ##
## automatiquement à partir d'un fichier CSV, par Julien Guillod                 ##
## Instructions d'installation et d'utilisation : https://guillod.org/script-ip/ ##
###################################################################################

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
    # list of student number on IP
    list_no_etu = set()
    for i in range(nb_notes):
        # try if student's note can be filled on IP
        try:
            # student's number corresponding to ith note
            no_etu = browser.find_element_by_id('dossier'+str(i)).get_attribute("value")
            # add to set of student number
            list_no_etu.add(no_etu)
        # otherwise go to next line on IP
        except:
            continue
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
    return list_no_etu

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
        list_no_etu = fill(notes)
        print("Please check that the marks are correctly filled and click on the button Envoi to save the marks on IP.")
    except:
        print("Error: unable to fill the page with the marks. Please try again on the correct webpage or type quit() to exit.")

    # return the differences between csv file and IP
    notinCSV = list_no_etu - notes.keys()
    notinIP = notes.keys() - list_no_etu
    print("Students in IP but not in CSV file: %s" % notinCSV)
    print("Students in CSV but not on IP: %s" % notinIP)

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

