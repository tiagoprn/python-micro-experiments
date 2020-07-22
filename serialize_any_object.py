import json

from datetime import date, datetime


class Address:
    def __init__(self, street, number, cep):
        self.street = street
        self.number = number
        self.cep = cep


class SampleClass:
    def __init__(self, name, surname, email, address,
                 date_field, datetime_field):
        self.name = name
        self.surname = surname
        self.email = email
        self.address = address
        self.date_field = date_field
        self.datetime_field = datetime_field

    def __repr__(self):
        representation = {}
        for key in self.__dict__:
            if isinstance(self.__dict__[key], (datetime, date, )):
                representation[key] = self.__dict__[key].isoformat()
            elif isinstance(self.__dict__[key], (str, int, float, complex,
                                               tuple, list, dict, set, )):
                representation[key] = str(self.__dict__[key])
            else:
                representation[key] = self.__dict__[key].__dict__
        return representation

    def __str__(self):
        return json.dumps(self.__repr__())


instance = SampleClass(name = 'tiago',
                       surname = 'paranhos',
                       email = 'tiago@tiagoprnl.me',
                       address = Address(
                           street='blablabla',
                           number=15,
                           cep='44'),
                       date_field = date(2017, 12, 25),
                       datetime_field = datetime(2017, 12, 25, 5, 59, 0))

print(f'Representation: {instance}')
