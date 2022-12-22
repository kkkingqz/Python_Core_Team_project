from fields.field import *

class Name(Field):

    @Field.value.setter
    def value(self, value):
        if value.isdigit():
            raise ValueError("Name cannot be a numbers")
        self._value = value