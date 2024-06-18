from sqlalchemy import Column, Integer, Date, Float, String
from config.database import Base


class CourseModel(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date = Column(Date)


class BankModel(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True)
    phone = Column(String)
    bank = Column(String)


class ValidateInteger:
    def __init__(self):
        pass

    def validate(self, cost):
        if isinstance(cost, int):
            return True
        return False


validate = ValidateInteger()


class StringValue:
    def __init__(self, validator=None) -> None:
        self.validator = validator

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instanse, owner):
        return instanse.__dict__[self.name]

    def __set__(self, instanse, value):
        if self.validator == None:
            if validate.validate(value):
                instanse.__dict__[self.name] = value
        else:
            if self.validator.validate(value):
                instanse.__dict__[self.name] = value


class ShipingCost:
    def __init__(self):
        self.__closer = 1000
        self.__sneaker = 1200
        self.__jacket = 1000

    @property
    def sneaker(self):
        return self.__sneaker

    @sneaker.setter
    def sneaker(self, cost: int):
        self.__sneaker = cost

    @property
    def jacket(self):
        return self.__jacket

    @jacket.setter
    def jacket(self, cost: int):
        self.__jacket = cost

    @property
    def closer(self):
        return self.__closer

    @closer.setter
    def closer(self, cost: int):
        self.__closer = cost


cost_ships = ShipingCost()
