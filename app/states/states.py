
from aiogram.fsm.state import State, StatesGroup

# Create your states here.
# Состояние кросовок


class FSMSneakers(StatesGroup):
    rate_sneakers = State()

# Состояние пуховика


class FSMDownJacket(StatesGroup):
    rate_down_jacket = State()


# Состояние одежды
class FSMClothes(StatesGroup):
    rate_clothes = State()


# Состояние уход
class FSMCare(StatesGroup):
    rate_сare = State()

# Состояние добавления курса юаня


class FSMCourse(StatesGroup):
    course = State()

# Состояние файла


class FSMFile(StatesGroup):
    file = State()

# Состояние ФОТКИ


class FSMPhoto(StatesGroup):
    photo = State()


# Состояние рассылки
class FSMMailing(StatesGroup):
    mailing = State()
    mailing2 = State()


# Состояние гайд
class FSMGuide(StatesGroup):
    install_1 = State()
    install_2 = State()
    install_3 = State()
    search_1 = State()
    search_2 = State()
    size_1 = State()
    reference = State()


# Состояние заказ
class FSMOrders(StatesGroup):
    price_snecers = State()
    price_clothe = State()
    price_jacket = State()
    url = State()
    phone = State()
    name = State()
    adress = State()
    color = State()
    penza = State()
    penza2 = State()
    another = State()
    another2 = State()
    phone_modify = State()
    adress_modify = State()
    name_modify = State()

# Состояние заказ


class FSMAdress(StatesGroup):
    adress = State()
    adress2 = State()


# Состояние удаление заказа
class FSMDeleteorder(StatesGroup):
    delete = State()


class FSMConfirmation(StatesGroup):
    user_id = State()


class FSMImages(StatesGroup):
    image = State()
