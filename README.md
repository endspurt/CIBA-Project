# CIBA-Project
C.I.B.A. - Command Interface Bot Assistant 
The address book app for manage your contacts list with phone numbers, e-mails and personal data. 

# Installation
1. Install CIBA-Project-project with: $ pip install -e .
2. Enter via terminal: $ ciba_project

# Usage
Command list:
>>> help: show the list of all supported commands
>>> hello: start of the work with CIBA
>>> close or exit: quit the app
>>> all: show the whole address book
	- Contacts

>>> add <name> <phone>: add a new contact with a name and a phone number
>>> find <name>: search for contacts by name or phone number
>>> change <name> <new name>: change a name of an existing contact
>>> delete-contact <name>: delete a contact by name
	- Birthdays

>>> add-birthday <name> <date>: add a birthday to an existing contact
>>> show-birthday <name>: show a birthday for an existing contact
>>> birthdays <any digital>: show contacts with birthdays in the next <any digital> days
	- Emails

>>> add-email <name>: add an email address to an existing contact
>>> show-email <name>: show email for an existing contact
>>> delete-email <name>: delete an email address of an existing contact
	- Addresses

>>> add-address <name>: add an address to an existing contact
>>> show-address <name>: show an address to an existing contact
>>> delete-address <name>: delete an address of an existing contact
	- Notes

>>> add-note <title>: start creating process of a new note
>>> edit-note <title>: edit note content named <title>
>>> find-note <keyword>: searching by keyword in existing notes
>>> find-notes-by-tag <tags>: searching by tag in existing notes
>>> delete-note <title>: delete note by title
    
# Contact
@oleksandrsinitskyi alex.sinitskyi@gmail.com 
Project Link: https://github.com/Ol-Sin/CIBA-Project.git
