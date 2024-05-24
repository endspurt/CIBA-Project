import re
from collections import UserDict  # Імпортуємо метод для роботи з словниками
from datetime import datetime, timedelta  # Імпортуємо метод для роботи з датою

class Field:  # Створюємо базовий клас для роботи з даними
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def to_dict(self):
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data):
        return cls(data['value'])

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

class Email(Field):
    def __init__(self, value):
        valid_email = self.validate_email(value)
        super().__init__(valid_email)

    @staticmethod
    def from_dict(data):
        return Email(data)

    @staticmethod
    def validate_email(value):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(regex, str(value))
        if match is not None:
            return value
        elif '@' not in value: # Поштова адреса має містити символ '@'
            raise ValueError("Email must contain '@' symbol")
        elif ' ' in value: # Поштова адреса не має містити пробілів
            raise ValueError("Email mustn't contain white spaces")
        else:
            raise ValueError("Email is invalid. Check the spelling of the email")

class Address(Field):
    pass

    @staticmethod
    def from_dict(data):
        return Address(data)

class Birthday(Field):  # Похідний клас для роботи з днями народження
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()  # Переводимо вміст рядкового запису дня народження та представляємо його у заданому форматі дати
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")  # Обробка виключення при хибному форматі

    def to_dict(self):
        return {"value": self.value.strftime("%d.%m.%Y")}

    @classmethod
    def from_dict(cls, data):
        return cls(data['value'])

class Record:  # Створюємо клас для обробки записів
    def __init__(self, name):
        self.name = Name(name)  # Визначаємо ім'я типом класу
        self.phones = []  # Ініціалізуємо номери як список для можливості зберігати декілька номерів
        self.email = None
        self.address = None
        self.birthday = None  # Ініціалізуємо необов'язковий атрибут для дня народження

    def __str__(self):  # Описуємо представлення рядка за допомогою магучного методу
        phone_numbers = '; '.join(p.value for p in self.phones)  # Створюємо атрибут для номерів як послідовності з використанням роздільника
        if self.email:
            email_info = f", email: {self.email}"
        if self.address:
            address_info = f", address: {self.address}"
        if self.birthday:  # Перевіряємо чи отримали значення для дня народження
            birthday_info = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"  # Атрибут для представлення дня народження у заданому форматі
        else:
            birthday_info = ""  # Якщо значення не отримали, робимо його порожнім
        return f"Contact name: {self.name.value}, phones: {phone_numbers}{email_info}{address_info}{birthday_info}"  # Повертаємо інформацію про запис у зручному форматі

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

    def add_email(self, email):
        self.email = Email(email)

    def delete_email(self):
        if self.email:
            self.email = None
            return f"Email removed."
        return f"Email not found."

    def add_address(self, address):
        self.address = Address(address)

    def delete_address(self):
        if self.address:
            self.address = None
            return f"Address removed."
        return f"Address not found."

    def add_birthday(self, birthday):  # Метод для додавання дня народження
        self.birthday = Birthday(birthday)  # Визначаємо атрибут як клас

    def to_dict(self):
        return {
            "name": self.name.to_dict(),
            "phones": [phone.to_dict() for phone in self.phones],
            "email": self.email.to_dict() if self.email else None,
            "address": self.address.to_dict() if self.address else None,
            "birthday": self.birthday.to_dict() if self.birthday else None
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data['name']['value'])
        record.phones = [Phone.from_dict(phone) for phone in data['phones']]
        email_data = data.get('email')
        address_data = data.get('address')
        if email_data:
            record.email = Email.from_dict(email_data['value'])
        if address_data:
            record.address = Address.from_dict(address_data['value'])
        if data['birthday']:
            record.birthday = Birthday.from_dict(data['birthday'])
        return record

class AddressBook(UserDict):  # Клас для словника адресної книги
    def __init__(self):
        self.data = {}  # Ініціалізація даних як словника

    def add_record(self, record):  # Метод для додавання запису в словник
        self.data[record.name.value] = record

    def find(self, name_or_phone):
        found_records = []
        for record in self.data.values():
            if record.name.value == name_or_phone:
                found_records.append(record)
            elif any(p.value == name_or_phone for p in record.phones):
                found_records.append(record)
        return found_records if found_records else None

    def find_by_name(self, name):
        return self.data.get(name)
    
    def find_by_phone(self, phone):
        found_records = []
        for record in self.data.values():
            if any(p.value == phone for p in record.phones):
                found_records.append(record)
        return found_records if found_records else None

    def delete(self, name):  # Метод для видалення запису з словника
        if name in self.data:
            del self.data[name]
            
    def get_upcoming_birthdays(self, days):  # Метод для отримання записів з найближчими днями народження
        current_day = datetime.today().date()  # Визначаємо поточну дату
        upcoming_birthdays = []  # Ініціалізація списку найближчих днів народження

        for name, record in self.data.items():  # Прохід по записам в словнику за атрибутами
            if record.birthday:  # Пошук наявності атрибуту дня народження
                birthday = record.birthday.value  # Отримуємо значення дня народження
                birthday = birthday.replace(year=current_day.year)  # Замінюємо рік в знайденому значенні на поточний
                
                if birthday < current_day:  # Перевірка чи день народження вже минув
                    birthday = birthday.replace(year=current_day.year + 1)  # Якщо так, збільшуємо рік для опрацювання цього запису в майбутньому

                if current_day <= birthday <= current_day + timedelta(days=days):  # Задаємо критерії для опрацювання, якщо день народження в найближчі N днів від поточної дати
                    congratulation_date = birthday  # Ініціалізуємо атрибут з датою привітання
                    formatted_congratulation_date = congratulation_date.strftime("%A, %d %B")  # Атрибут для представлення дати привітання з днем народження у заданому форматі
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": formatted_congratulation_date})  # Додаємо запис до списку

        upcoming_birthdays.sort(key=lambda x: datetime.strptime(x["congratulation_date"], "%A, %d %B"))  # Відсортовуємо список за датами привітання
        return upcoming_birthdays  # Виводимо список найближчих днів народження
    
    def to_dict(self):
        return {"records": [record.to_dict() for record in self.data.values()]}

    @classmethod
    def from_dict(cls, data):
        address_book = cls()
        for record_data in data['records']:
            record = Record.from_dict(record_data)
            address_book.add_record(record)
        return address_book

class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.tags = tags if tags else []

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}\nCreated at: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        note = cls(data['title'], data['content'], data['tags'])
        note.created_at = datetime.fromisoformat(data['created_at'])
        return note

class NotesBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_note(self, note):
        self.data[note.title] = note

    def find(self, keyword):
        found_notes = []
        for note in self.data.values():
            if keyword in note.title or keyword in note.content or keyword in note.tags:
                found_notes.append(note)
        return found_notes if found_notes else None

    def delete(self, title):
        if title in self.data:
            del self.data[title]

    def edit_note(self, title, new_content=None, new_tags=None):
        if title in self.data:
            note = self.data[title]
            if new_content:
                note.content = new_content
            if new_tags is not None:
                note.tags = new_tags
        else:
            return f"Note '{title}' not found."

    def find_by_tag(self, tag):
        found_notes = []
        for note in self.data.values():
            if tag in note.tags:
                found_notes.append(note)
        return found_notes if found_notes else None

    def to_dict(self):
        return {"notes": [note.to_dict() for note in self.data.values()]}

    @classmethod
    def from_dict(cls, data):
        notes_book = cls()
        for note_data in data['notes']:
            note = Note.from_dict(note_data)
            notes_book.add_note(note)
        return notes_book
    
