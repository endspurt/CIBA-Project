def input_error(func): # Створення функції-декоратора обробки помилок
    def inner(*args, **kwargs): # Створення вкладеної функції для опрацювання основних видів помилок
        try:
            return func(*args, **kwargs)
        except ValueError: # Опрацювання помилки відсутності аргументів
            return "Give me name and phone please."
        except KeyError: # Опрацювання помилки відсутності аргументу ключа
            return "Contact not found."
        except IndexError: # Опрацювання помилки відсутності відповідного індексу
            return "Invalid index."
        except Exception as e:
            return f"Error: {str(e)}"  # Опрацювання інших помилок

    return inner # Повернення результату роботи функції після опрацювання основних помилок
