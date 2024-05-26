from src.func import *  # Імпортуємо модуль, який містить функції обробки контактів та читання/збереження файлу
from src.dec import *  # Імпортуємо модуль, який містить функцію-декоратор
from src.clas import AddressBook, NotesBook

def parse_input(user_input):  # Метод для обробки вводу користувача
    cmd, *args = user_input.split()  # Розділяємо ввід користувача, як команду та параметри
    cmd = cmd.strip().lower()  # Прибираємо зайві пробіли та зводимо введену команду до нижнього регістру щоб мінімізувати похибку введених даних
    return cmd, args

def main_bot():
    book = load_data()  # Виклик функції для перевірки наявності файлу з контактами
    notes_book = load_notes()  # Завантажуємо нотатки з файлу
    main(book, notes_book)  # Запускаємо основну функцію
    save_data(book)  # Виклик функції для збереження перед виходом з програми
    save_notes(notes_book)  # Збереження нотаток перед виходом з програми
	
@input_error  # Огортаємо основну функцію функцією-декоратором
def main(book: AddressBook, notes_book: NotesBook):  # Головна функція бота
    print("Hello! Welcome to the assistant bot!")  # Виводимо привітання від бота

    while True:
        command = input("Enter a command: ").strip().lower()  # Отримання вводу від користувача

        if command in ["close", "exit"]:  # Обробка виходу з боту
            print("Good bye!")
            break

        elif command == "hello":  # Ініціація привітання
            print("How can I help you?")

        elif command == "help":  # Вивід довідки по поточним можливостям боту
            print("""This is what I can help you with working with contacts:
                - add (add new contact),
                - change (change existing contact),
                - find (find phone by name or name by phone),
                - all (print all contacts I know),
                - delete-contact (delete existing contact),
                - add-email (add email for contact),
                - show-email (show email for contact),
                - delete-email (delete email for contact),
                - add-address (add address for contact),
                - show-address (show address for contact),
                - delete-address (delete address for contact),
                - add-birthday (add birthday for contact),
                - show-birthday (show birthday for contact),
                - birthdays (show upcoming birthdays),
            
                For notes:
                - add-note (add a new note),
                - find-note (find note by keyword),
                - delete-note (delete note by title),
                - edit-note (edit note by title),
                - find-notes-by-tag (find notes by tag)
                  
                - help (print this message),
                - close or exit (end of work)""")

        else:
            cmd, args = parse_input(command)  # Визначаємо яку функцію ініціює користувач
            if cmd == "add":
                print(add_contact(args, book))
            elif cmd == "change":
                print(change_contact(args, book))
            elif cmd == "find":
                print(find(args, book))
            elif cmd == "all":
                print(show_all(book))
            elif cmd == "delete-contact":
                print(delete_contact(args, book)) 
            elif cmd == "add-email":
                print(add_contact_info(args, book, "email"))
            elif cmd == "show-email":
                print(show_contact_info(args, book, "email"))
            elif cmd == "delete-email":
                print(delete_contact_info(args, book, "email"))
            elif cmd == "add-address":
                print(add_contact_info(args, book, "address"))
            elif cmd == "show-address":
                print(show_contact_info(args, book, "address"))
            elif cmd == "delete-address":
                print(delete_contact_info(args, book, "address"))
            elif cmd == "add-birthday":
                print(add_birthday(args, book))
            elif cmd == "show-birthday":
                print(show_birthday(args, book))
            elif cmd == "birthdays":
                print(birthdays(args, book))
            elif cmd == "add-note":
                print(add_note(args, notes_book))
            elif cmd == "find-note":
                print(find_note_by_keyword(args, notes_book))
            elif cmd == "delete-note":
                print(delete_note(args, notes_book))
            elif cmd == "edit-note":
                print(edit_note(args, notes_book))
            elif cmd == "find-notes-by-tag":
                print(find_notes_by_tag(args, notes_book))
            else:
                print("Invalid command.")  # Вивід повідомлення коли команда не відповідає поточному функціоналу

if __name__ == "__main__":  # Перевіряємо, чи запущено цей файл як основний скрипт
    book = load_data()  # Виклик функції для перевірки наявності файлу з контактами
    notes_book = load_notes()  # Завантажуємо нотатки з файлу
    main(book, notes_book)  # Запускаємо основну функцію
    save_data(book)  # Виклик функції для збереження перед виходом з програми
    save_notes(notes_book)  # Збереження нотаток перед виходом з програми

