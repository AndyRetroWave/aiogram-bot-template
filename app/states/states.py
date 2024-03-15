from aiogram.fsm.context import FSMContext
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

