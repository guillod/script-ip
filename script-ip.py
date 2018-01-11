# import csv to dict with notes['id'] = 'note'
import csv
with open('notes.csv') as file:
    notes = {line[0]:line[1] for line in csv.reader(file)}
assert(notes['id'] == 'note')

# open firefox
from selenium import webdriver
browser = webdriver.Firefox()

# user browse to correct page

nb_notes = int(browser.find_element_by_id("nb_notes").get_attribute("value"))

for i in range(nb_notes):
    # student's number corresponding to ith note
    no_etu = browser.find_element_by_id('dossier'+str(i)).get_attribute("value")
    # check if no_etu corresponds to a note in the csv
    if no_etu in notes.keys():
        # student's note
        note = notes[no_etu]
        # write note to html
        browser.find_element_by_id('note'+str(i)).send_keys(note)

