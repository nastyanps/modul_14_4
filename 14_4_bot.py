from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions_14_4 import get_all_products

api = '7586673014:AAH_bwRR2F9R6tk53sgJwyvkygirofcz5sE'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_1 = ReplyKeyboardMarkup()
button_1_1 = KeyboardButton(text='Рассчитать')
button_1_2 = KeyboardButton(text='Информация')
button_1_3 = KeyboardButton(text='Купить')
kb_1.add(button_1_1)
kb_1.add(button_1_2)
kb_1.add(button_1_3)
kb_1.resize_keyboard = True

kb_2 = InlineKeyboardMarkup()
button_2_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_2_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_2.add(button_2_1)
kb_2.add(button_2_2)
kb_2.resize_keyboard = True

kb_3 = InlineKeyboardMarkup()
button_3_1 = InlineKeyboardButton(text='Мини', callback_data='product_buying')
button_3_2 = InlineKeyboardButton(text='База', callback_data='product_buying')
button_3_3 = InlineKeyboardButton(text='Опти', callback_data='product_buying')
button_3_4 = InlineKeyboardButton(text='Макси', callback_data='product_buying')
kb_3.add(button_3_1)
kb_3.add(button_3_2)
kb_3.add(button_3_3)
kb_3.add(button_3_4)
kb_3.resize_keyboard = True

all_products = get_all_products()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb_1)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for product in all_products:
        await message.answer(
            f"Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}")

        with open(product[4], 'rb') as photo:
            await message.answer_photo(photo)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_3)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


@dp.message_handler(state=None)
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
