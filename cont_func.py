from decorators import * # Імпортуємо модуль який містить функцію-декоратор
from main import Record, AddressBook # Імпорт класів з головного модуля
import pickle # Імпортуємо модуль для серіалізації та десеріалізації даних

@input_error
def add_contact(args, book: AddressBook): # Функція для додавання контакту
    if len(args) != 2: # Перевірка наявності необхідної кількості аргументів для команди
        return "Invalid command. Format: add [name] [phone]"
    name, phone = args # Розділяємо аргументи вводу

    record = book.find(name) # Шукаємо запис в словнику за іменем
    if record: # Якщо запис знайдено використовуємо метод класу для додавання номеру
        record.add_phone(phone)
        return "Phone number added to existing contact."
    else: # Якщо запису немає в словнику - створюємо новий
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "New contact added."

@input_error # Огортаємо функцію оновлення номеру функцією-декоратором
def change_contact(args, book: AddressBook): # Функція оновлення номеру
    if len(args) != 2:
        return "Invalid command. Format: change [name] [new_phone]"
    name, new_phone = args
    record = book.find(name)
    if not record: # Виводимо повідомлення якщо контакту не існує
        return f"Contact '{name}' not found."
    # contacts[name] = new_phone # Оновлення номеру
    # save_contacts(contacts)
    old_phone = record.phones[0]
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error # Огортаємо функцію виводу номеру за ім'ям функцією-декоратором
def show_phone(args, book: AddressBook): # Функція виводу номеру за ім'ям
    if len(args) != 1:
        return "Invalid command. Format: phone [name]"
    name = args[0] # Задаємо ввід як аргумент для індексу при пошуку запису
    record = book.find(name)
    if not record: # Виводимо повідомлення якщо контакт не знайдено
        return f"Contact '{name}' not found."
    return ", ".join([phone.value for phone in record.phones])

def show_all(book: AddressBook): # Функція виводу записів з словника
    records = list(book.data.values())
    if not records: # Вивід повідомлення якщо список контактів порожній
        return "No contacts found."
    result = "\n".join([f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}" for record in records])
    return result

def save_data(book, filename="addressbook.pkl"): # Функція для збереження словника в файл
    with open(filename, "wb") as f: # Безпечне відкриття байтового файлу для запису
        pickle.dump(book, f) # Використовуємо pickle для серилізації словника в файл

def load_data(filename="addressbook.pkl"): # Функція 
    try:
        with open(filename, "rb") as f: # Безпечне відкриття байтового файлу для читання
            return pickle.load(f) # Використовуємо pickle для десерилізації словника з файлу
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
