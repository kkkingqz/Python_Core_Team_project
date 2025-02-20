from datetime import datetime, date, timedelta
from fields import Address, Birthday, Email, Name, Notes, Phone, Field

# from fields import *
# from assistant_bot.fields import *

class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.notes = {}
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_note(self, text, hashtag=''):
        self.notes.update({text: hashtag})

    def change_attr(self, attribute, old_value=None, new_value=None):
        if attribute not in ["name", "phones", "birthday", "email", "notes", "address"]:
            raise IndexError("You didn't write an attribute")
        self.attribute = getattr(self, attribute)
        if attribute == "phones":
            for item in self.phones:
                if item.value == old_value:
                    if new_value not in self.phones:
                        item.value = new_value
                        return True
        elif attribute == "notes":
            string_note = f"{old_value.strip()} {new_value}"
            list_note = string_note.split("->")
            old_value = list_note[0]
            new_value = "->".join(list_note[1:])
            if self.notes:
                find_note = []
                tags = []
                for note in self.notes.keys():
                    if note.startswith(old_value):
                        find_note.append(note)
                if len(find_note) == 1:
                    tags = self.notes.get(find_note[0],[])
                    self.notes.pop(find_note[0], None)
                    if not self.notes.get(new_value):
                        self.notes.update({new_value: tags})
                        return True
                else:
                    raise ValueError
            return True
        elif attribute == "birthday":
            self.birthday = Birthday(new_value)
            return True
        elif attribute == "address":
            self.address = Address(new_value)
            return True
        elif attribute == "email":
            self.email = Email(new_value)
            return True

    def delete_attribute(self, attribute, item=None):
        if attribute == "phones":
            for phone in self.phones:
                if phone.value == item:
                    self.phones.remove(phone)
                    return True
                else:
                    return "Contact hasn't such info"
        elif attribute == "notes":
            if self.notes:
                if item == "all":
                    self.notes = {}
                    return True
                else:
                    raise ValueError
        elif attribute == "note":
            if self.notes:
                find_note = []
                for note in self.notes.keys():
                    if note.startswith(item):
                        find_note.append(note)
                if len(find_note) == 1:
                    self.notes.pop(find_note[0], None)
                    return True
                else:
                    raise ValueError
        elif attribute == "birthday":
            self.birthday = None
            return True
        elif attribute == "address":
            self.address = None
            return True
        elif attribute == "email":
            self.email = None
            return True

    def get_info(self):
        birthday_info = ''
        email_info = ''
        notes_info = ''
        address_info = ''
        phones_info = [phone.value for phone in self.phones]

        if self.birthday:
            birthday_info = f'Burned: {self.birthday.value}'
        if self.email:
            email_info = f'Email: {self.email.value}'
        if self.notes:
            notes_list = []
            string_tags = ""
            for text, tags in self.notes.items():
                if tags:
                    string_tags = ", ".join(tags)
                notes_list.append(f"{text}, #{string_tags}")
                string_tags = ""
            notes_string = "; ".join(notes_list)
            notes_info = f"Notes: {notes_string}"
        if self.address:
            address_info = f'Lives: {self.address.value.capitalize()}'
        return f"Contact - {self.name.value.capitalize()} : phones: {', '.join(phones_info)} {birthday_info} {email_info} {notes_info} {address_info}"

    def day_to_birthday(self):
        if not self.birthday:
            return "The contact's birthday date not defined yet"
        current_date = datetime.now().date()
        birthday_date = datetime.strptime(
            self.birthday.value, '%d/%m/%Y').date()
        new_date_for_birthday = birthday_date.replace(year=current_date.year)

        if new_date_for_birthday < current_date:
            new_date_for_birthday = new_date_for_birthday.replace(
                year=current_date.year + 1)
        return (new_date_for_birthday - current_date).days

    def __str__(self):
        return f'{self.name, self.phones, self.birthday, self.email, self.notes, self.address}'

    def __repr__(self):
        return f'{self.name, self.phones, self.birthday, self.email, self.notes, self.address}'
