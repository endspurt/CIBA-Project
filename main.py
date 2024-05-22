from cont_func import *  # Імпортуємо модуль, який містить функції обробки контактів та читання/збереження файлу
from decorators import *  # Імпортуємо модуль, який містить функцію-декоратор
from collections import UserDict  # Імпортуємо метод для роботи з словниками
from datetime import datetime, timedelta  # Імпортуємо метод для роботи з датою

class Field:  # Створюємо базовий клас для роботи з даними
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):  # Похідний клас для роботи з іменами
    pass

class Phone(Field):  # Похідний клас для роботи з телефонами
    def __init__(self, value):
        if not self.validate_phone(value):  # Перевірка номеру
            raise ValueError("Invalid phone number format.")
        super().__init__(value)

    @staticmethod  # Використовуємо декоратор для доповнення класу валідацією номера
    def validate_phone(value):  # Валідація формату номеру
        return len(value) == 10 and value.isdigit()

class Birthday(Field):  # Похідний клас для роботи з днями народження
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()  # Переводимо вміст рядкового запису дня народження та представляємо його у заданому форматі дати
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")  # Обробка виключення при хибному форматі

class Record:  # Створюємо клас для обробки записів
    def __init__(self, name):
        self.name = Name(name)  # Визначаємо ім'я типом класу
        self.phones = []  # Ініціалізуємо номери як список для можливості зберігати декілька номерів
        self.birthday = None  # Ініціалізуємо необов'язковий атрибут для дня народження

    def __str__(self):  # Описуємо представлення рядка за допомогою магучного методу
        phone_numbers = '; '.join(p.value for p in self.phones)  # Створюємо атрибут для номерів як послідовності з використанням роздільника
        if self.birthday:  # Перевіряємо чи отримали значення для дня народження
            birthday_info = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"  # Атрибут для представлення дня народження у заданому форматі
        else:
            birthday_info = ""  # Якщо значення не отримали, робимо його порожнім
        return f"Contact name: {self.name.value}, phones: {phone_numbers}{birthday_info}"  # Повертаємо інформацію про запис у зручному форматі

    def add_phone(self, phone):  # Метод для додавання номеру до списку
        existing_phones = [p.value for p in self.phones] # Отримуємо значення наявних номерів
        if phone not in existing_phones: # Якщо в списку такого номеру немає, то додаємо
            self.phones.append(Phone(phone))
        else:
            print("Phone number already exists for this contact.") # Вивід якщо спробуємо додати номер, який вже є у списку

    def remove_phone(self, phone):  # Метод для видалення (насправді перезапису) номерів у списку
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):  # Метод для оновлення номеру
        if not Phone.validate_phone(new_phone):  # Використання класу для валідації номеру
            raise ValueError("Invalid phone number format.")
        for phone in self.phones:  # Перевіряємо відповідність старого номеру при оновлені на новий
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):  # Метод для пошуку номера в записі
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):  # Метод для додавання дня народження
        self.birthday = Birthday(birthday)  # Визначаємо атрибут як клас

class AddressBook(UserDict):  # Клас для словника адресної книги
    def __init__(self):
        self.data = {}  # Ініціалізація даних як словника

    def add_record(self, record):  # Метод для додавання запису в словник
        self.data[record.name.value] = record

    def find(self, name):  # Метод для пошуку запису в словнику
        return self.data.get(name)

    def delete(self, name):  # Метод для видалення запису з словника
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):  # Метод для отримання записів з найближчими днями народження
        current_day = datetime.today().date()  # Визначаємо поточну дату
        upcoming_birthdays = []  # Ініціалізація списку найближчих днів народження

        for name, record in self.data.items():  # Прохід по записам в словнику за атрибутами
            if record.birthday:  # Пошук наявності атрибуту дня народження
                birthday = record.birthday.value  # Отримуємо значення дня народження
                birthday = birthday.replace(year=current_day.year)  # Замінюємо рік в знайденому значенні на поточний
                if birthday < current_day:  # Перевірка чи день народження вже минув
                    birthday = birthday.replace(year=current_day.year + 1)  # Якщо так, збільшуємо рік для опрацювання цього запису в майбутньому

                if current_day <= birthday <= current_day + timedelta(days=7):  # Задаємо критерії для опрацювання, якщо день народження в найближчі 7 днів від поточної дати
                    if current_day.weekday() < 5 and birthday.weekday() < 5:  # Перевіряємо чи днь народження в межах робочих днів на цьому тижні
                        congratulation_date = birthday  # Якщо попередні умови виконано - ініціалізуємо атрибут з датою привітання
                        formatted_congratulation_date = congratulation_date.strftime("%A, %d %B")  # Атрибут для представлення дати привітання з днем народження у заданому форматі
                        upcoming_birthdays.append({"name": record.name.value, "congratulation_date": formatted_congratulation_date})  # Додаємо запис до списку

        upcoming_birthdays.sort(key=lambda x: datetime.strptime(x["congratulation_date"], "%A, %d %B"))  # Відсортовуємо список за датами привітання
        return upcoming_birthdays  # Виводимо список найближчих днів народження

def parse_input(user_input):  # Метод для обробки вводу користувача
    cmd, *args = user_input.split()  # Розділяємо ввід користувача, як команду та параметри
    cmd = cmd.strip().lower()  # Прибираємо зайві пробіли та зводимо введену команду до нижнього регістру щоб мінімізувати похибку введених даних
    return cmd, args
	
@input_error
def add_birthday(args, book): # Метод для додавання дня народження до словника
    name, birthday = args # Ініціалізуємо введені аргументи
    record = book.find(name) # Пошук в словнику за іменем
    if record:
        record.add_birthday(birthday) # Якщо отримали результат пошуку, то викликаємо метод додавання дня народження у словник
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book): # Метод для відображення дня народження
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
    upcoming_birthdays = book.get_upcoming_birthdays() # Агрумент запускає метод з класу
    if upcoming_birthdays: # Якщо попередній метод повернув результат - виводимо в заданому форматі
        return "\n".join([f"{birthday['name']}'s birthday is on {birthday['congratulation_date']}." for birthday in upcoming_birthdays])
    else: # Вивід якщо метод не повернув результатом запис
        return "No upcoming birthdays."


@input_error  # Огортаємо основну функцію функцією-декоратором
def main(book: AddressBook):  # Головна функція бота
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
                - phone (show phone by name),
                - all (print all contacts I know),
                - add-birthday (add birthday for contact),
                - show-birthday (show birthday for contact),
                - birthdays (show upcoming birthdays),
                - help (print this message),
                - close or exit (end of work)""")

        else:
            cmd, args = parse_input(command)  # Визначаєто яку функцію ініціює користувач
            if cmd == "add":
                print(add_contact(args, book))
            elif cmd == "change":
                print(change_contact(args, book))
            elif cmd == "phone":
                print(show_phone(args, book))
            elif cmd == "all":
                print(show_all(book))
            elif cmd == "add-birthday":
                print(add_birthday(args, book))
            elif cmd == "show-birthday":
                print(show_birthday(args, book))
            elif cmd == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")  # Вивід повідомлення коли команда не відповідає поточному функціоналу

if __name__ == "__main__":  # Перевіряємо, чи запущено цей файл як основний скрипт
    book = load_data() # Виклик функції для перевірки наявності файлу з контактами
    main(book)  # Запускаємо основну функцію
    save_data(book)  # ВВиклик функції для збереження перед виходом з програми
