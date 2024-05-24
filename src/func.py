from src.dec import input_error # Імпортуємо модуль який містить функцію-декоратор
from src.clas import Record, AddressBook, Note, NotesBook # Імпорт класів з головного модуля
import json # Імпортуємо модуль для серіалізації та десеріалізації даних
import os

@input_error
def add_contact(args, book: AddressBook): # Функція для додавання контакту
    if len(args) != 2: # Перевірка наявності необхідної кількості аргументів для команди
        return "Invalid command. Format: add [name] [phone]"
    name, phone = args # Розділяємо аргументи вводу

    records = book.find(name) # Шукаємо запис в словнику за іменем
    if records: # Якщо запис знайдено використовуємо метод класу для додавання номеру
        if len(records) > 1:
            return f"Multiple contacts found for {name}. Please refine your search."
        record = records[0]
        record.add_phone(phone)
        return "Phone number added to existing contact."
    else: # Якщо запису немає в словнику - створюємо новий
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "New contact added."

@input_error
def change_contact(args, book: AddressBook): # Функція оновлення номеру
    if len(args) != 2:
        return "Invalid command. Format: change [name] [new_phone]"
    name, new_phone = args
    records = book.find(name)
    if not records: # Виводимо повідомлення якщо контакту не існує
        return f"Contact '{name}' not found."
    if len(records) > 1:
        return f"Multiple contacts found for {name}. Please refine your search."
    record = records[0]
    old_phone = record.phones[0].value if record.phones else None
    if old_phone:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return f"No phone number found for contact '{name}'."


@input_error # Огортаємо функцію виводу номеру за ім'ям функцією-декоратором
def find(args, book: AddressBook):
    if len(args) != 1:
        return "Invalid command. Format: find [name or phone]"
    
    query = args[0]
    if query.isdigit():
        found_records = book.find_by_phone(query)
    else:
        found_records = book.find(query)
    
    if not found_records:
        return f"Contact '{query}' not found."

    result = []
    for record in found_records:
        phones_info = ", ".join([phone.value for phone in record.phones])
        result.append(f"{record.name.value}: {phones_info}")
    return "\n".join(result)

def show_all(book: AddressBook): # Функція виводу записів з словника
    records = list(book.data.values())
    if not records: # Вивід повідомлення якщо список контактів порожній
        return "No contacts found."
    result = "\n".join([f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}" for record in records])
    return result

def save_data(book, filename="usr/addressbook.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(book.to_dict(), f, ensure_ascii=False, indent=4)

def load_data(filename="usr/addressbook.json"):
    try:
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
            return AddressBook.from_dict(data)
    except FileNotFoundError:
        return AddressBook()

@input_error
def add_birthday(args, book): # Метод для додавання дня народження до словника
    if len(args) != 2:
        return "Invalid command. Format: add-birthday [name] [birthday]"
    name, birthday = args # Ініціалізуємо введені аргументи
    record = book.find(name) # Пошук в словнику за іменем
    if record:
        record.add_birthday(birthday) # Якщо отримали результат пошуку, то викликаємо метод додавання дня народження у словник
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book): # Метод для відображення дня народження
    if len(args) != 1:
        return "Invalid command. Format: show-birthday [name]"
    name, = args # Ініціалізуємо отриманий аргумент як ім'я
    record = book.find(name) # Пошук в словнику за іменем
    if record and record.birthday: # Якщо ім'я є в словнику і має запис про день народження, то виводимо у заданому форматі дати
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    elif record:  # Вивід якщо ім'я не має запис про день народження
        return f"{name} has no birthday set."
    else: # Вивід якщо ім'я не знайдено
        return f"Contact {name} not found."

@input_error
def birthdays(args, book): # Метод для ініціалізації пошуку записів з найближчими днями народження 
    days = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthdays(days) # Агрумент запускає метод з класу
    if upcoming_birthdays: # Якщо попередній метод повернув результат - виводимо в заданому форматі
        return "\n".join([f"{birthday['name']}'s birthday is on {birthday['congratulation_date']}." for birthday in upcoming_birthdays])
    else: # Вивід якщо метод не повернув результатом запис
        return "No upcoming birthdays."

@input_error
def add_note(args, notes_book: NotesBook):
    if len(args) < 1:
        return "Invalid command. Format: add_note [title]"
    title = args[0]
    content = input("Enter note content: ").strip()
    tags_input = input("Enter comma-separated tags (optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    return add_note_with_details(title, content, tags, notes_book)

def add_note_with_details(title, content, tags, notes_book: NotesBook):
    if title in notes_book.data:
        return f"Note with title '{title}' already exists."
    note = Note(title=title, content=content, tags=tags)
    notes_book.add_note(note)
    return f"Note '{title}' added successfully."

@input_error
def find_note_by_keyword(args, notes_book: NotesBook):
    if len(args) != 1:
        return "Invalid command. Format: find_note [keyword]"
    keyword = args[0]
    found_notes = notes_book.find(keyword)
    if not found_notes:
        return f"No notes found with keyword '{keyword}'."
    
    result = "\n\n".join(str(note) for note in found_notes)
    return result

@input_error
def delete_note(args, notes_book: NotesBook):
    if len(args) != 1:
        return "Invalid command. Format: delete_note [title]"
    title = args[0]
    notes_book.delete(title)
    return f"Note '{title}' deleted."

@input_error
def edit_note(args, notes_book: NotesBook):
    if len(args) < 2:
        return "Invalid command. Format: edit_note [title] [new_content] [new_tag1] [new_tag2] ..."
    title = args[0]
    new_content = args[1]
    new_tags = args[2:]
    
    result = notes_book.edit_note(title, new_content, new_tags)
    if result:
        return result
    return f"Note '{title}' updated."

@input_error
def find_notes_by_tag(args, notes_book: NotesBook):
    if len(args) != 1:
        return "Invalid command. Format: find_notes_by_tag [tag]"
    tag = args[0]
    found_notes = notes_book.find_by_tag(tag)
    if not found_notes:
        return f"No notes found with tag '{tag}'."
    
    result = "\n\n".join(str(note) for note in found_notes)
    return result

def save_notes(notes_book, filename="usr/notesbook.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(notes_book.to_dict(), f, ensure_ascii=False, indent=4)

def load_notes(filename="usr/notesbook.json"):
    try:
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
            return NotesBook.from_dict(data)
    except FileNotFoundError:
        return NotesBook()
    
