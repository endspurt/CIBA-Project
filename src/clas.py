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

    def to_dict(self):
        return {
            "name": self.name.to_dict(),
            "phones": [phone.to_dict() for phone in self.phones],
            "birthday": self.birthday.to_dict() if self.birthday else None
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data['name']['value'])
        record.phones = [Phone.from_dict(phone) for phone in data['phones']]
        if data['birthday']:
            record.birthday = Birthday.from_dict(data['birthday'])
        return record

class AddressBook(UserDict):  # Клас для словника адресної книги
    def __init__(self):
        self.data = {}  # Ініціалізація даних як словника

    def add_record(self, record):  # Метод для додавання запису в словник
        self.data[record.name.value] = record

    # def find(self, name):
    #     for record in self.data.values():
    #         if record.name.value == name:
    #             return record
    #     return None

    def find(self, name):
        return self.data.get(name)
    
    def find_by_phone(self, phone):
        for record in self.data.values():
            if any(p.value == phone for p in record.phones):
                return record
        return None

    def delete(self, name):  # Метод для видалення запису з словника
        if name in self.data:
            del self.data[name]

    # def get_upcoming_birthdays(self):  # Метод для отримання записів з найближчими днями народження
    #     current_day = datetime.today().date()  # Визначаємо поточну дату
    #     upcoming_birthdays = []  # Ініціалізація списку найближчих днів народження

    #     for name, record in self.data.items():  # Прохід по записам в словнику за атрибутами
    #         if record.birthday:  # Пошук наявності атрибуту дня народження
    #             birthday = record.birthday.value  # Отримуємо значення дня народження
    #             birthday = birthday.replace(year=current_day.year)  # Замінюємо рік в знайденому значенні на поточний
    #             if birthday < current_day:  # Перевірка чи день народження вже минув
    #                 birthday = birthday.replace(year=current_day.year + 1)  # Якщо так, збільшуємо рік для опрацювання цього запису в майбутньому

    #             if current_day <= birthday <= current_day + timedelta(days=7):  # Задаємо критерії для опрацювання, якщо день народження в найближчі 7 днів від поточної дати
    #                 if current_day.weekday() < 5 and birthday.weekday() < 5:  # Перевіряємо чи днь народження в межах робочих днів на цьому тижні
    #                     congratulation_date = birthday  # Якщо попередні умови виконано - ініціалізуємо атрибут з датою привітання
    #                     formatted_congratulation_date = congratulation_date.strftime("%A, %d %B")  # Атрибут для представлення дати привітання з днем народження у заданому форматі
    #                     upcoming_birthdays.append({"name": record.name.value, "congratulation_date": formatted_congratulation_date})  # Додаємо запис до списку

    #     upcoming_birthdays.sort(key=lambda x: datetime.strptime(x["congratulation_date"], "%A, %d %B"))  # Відсортовуємо список за датами привітання
    #     return upcoming_birthdays  # Виводимо список найближчих днів народження

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
    