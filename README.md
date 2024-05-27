# CIBA-Project
C.I.B.A. - Command Interface Bot Assistant 
The address book app for manage your contacts list with phone numbers, e-mails and personal data. 

# Installation
1. Install CIBA-Project-project with: $ pip install -e .
2. Enter via terminal: $ ciba_project

# Usage
Command list:
>- help: show the list of all supported commands
>- hello: initial command
>- close or exit: quit the app
>- all: list of names and numbers from AddressBook

Contacts

>- add <name> <phone>: add new contact with name and phone number
>- find <name>: search for contacts by name or phone number
>- change <name> <new phone>: change by name a phone number for existing contact
>- delete-contact <name>: delete a contact by name

Birthdays

>- add-birthday <name> <date>: add birthday to contact
>- show-birthday <name>: show birthday for contact
>- birthdays <N>: show contacts with birthdays in the next <N> days

Emails

>- add-email <name>: add email to contact
>- show-email <name>: show email for contact
>- delete-email <name>: delete an email address of existing contact

Addresses

>- add-address <name>: add an address to a contact
>- show-address <name>: show an address for contact
>- delete-address <name>: delete an address of existing contact

Notes

>- add-note <title>: create a new note
>- edit-note <title>: edit note content named <title>
>- find-note <keyword>: searching by keyword in existing notes
>- find-notes-by-tag <tags>: searching by tag in existing notes
>- delete-note <title>: delete note by title
    
# Contact
@oleksandrsinitskyi alex.sinitskyi@gmail.com 
Project Link: https://github.com/Ol-Sin/CIBA-Project.git
