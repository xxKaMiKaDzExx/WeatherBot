from aiogram import Bot, Dispatcher
from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import  F, types



import requests
import asyncio



bot = Bot(token='YOUR TOKEN BOT')
dp = Dispatcher()



###################################################################################################
# КЛАВИАТУРЫ
###################################################################################################



inline_start_msg_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✉️ Рассылка ✉️', callback_data='message_weather')],
    [InlineKeyboardButton(text='❓ Источники данных ❓', callback_data='link')],
    [InlineKeyboardButton(text='⚙️ Доп. возможности ⚙️', callback_data='dp')],
    [InlineKeyboardButton(text='🌎 Самые популярные города 🌎', callback_data='popular')]
])

inline_information_weather_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🌇 Более подробный прогноз погоды 🌇', callback_data='dop_info')],
    [InlineKeyboardButton(text='👔 Что надеть на улицу?  👔', callback_data='cloth_info')]
])


subscription_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ежедневно", callback_data="daily")],
    [InlineKeyboardButton(text="Раз в неделю", callback_data="weekly")],
    [InlineKeyboardButton(text="Раз в месяц", callback_data="monthly")],
    [InlineKeyboardButton(text="Тест (раз в 1 минуту)", callback_data="test")]
])

most_popular_city_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Москва'),
        KeyboardButton(text='Минск'),
        KeyboardButton(text='Питер'),
        KeyboardButton(text='Берлин')
    ],
    [
        KeyboardButton(text='Афины'),
        KeyboardButton(text='Париж'),
        KeyboardButton(text='Лондон'),
        KeyboardButton(text='Стамбул')
    ],
    [
        KeyboardButton(text='Лиссабон'),
        KeyboardButton(text='Мадрид')
    ]
], resize_keyboard=True, one_time_keyboard=True)

###################################################################################################
# ОСНОВНОЙ ФУНКЦИОНАЛ
###################################################################################################



class WeatherState(StatesGroup):
    city = State()
    temperature = State()
    temperature_feels = State()
    wind_speed = State()
    cloud_cover = State()
    humidity = State()




@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f'<b>Приветсвую тебя {message.from_user.first_name} 👋</b>\n\n<em>Я</em> - <b>бот-прогнозчик</b> погоды.\nМогу стать твоим личным <em>аналитиком</em> погоды!\nЗдесь ты сможеш узнать <b>прогноз погоды</b> в самых разных <em>точках планеты</em>! Для того чтобы <b>начать</b> - <em>введи название города или выбери один из предложенных ниже!</em>', parse_mode="HTML", reply_markup=inline_start_msg_kb)
    
    



@dp.message(F.text)
async def get_weather(message: types.Message, state: FSMContext):
    city = message.text
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()

        temperature = weather_data['main']['temp']
        temperature_feels = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        cloud_cover = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

      
        await state.update_data(city=city)
        await state.update_data(temperature=temperature)
        await state.update_data(temperature_feels=temperature_feels)
        await state.update_data(wind_speed=wind_speed)
        await state.update_data(cloud_cover=cloud_cover)
        await state.update_data(humidity=humidity)

        # await message.answer(f'Температура воздуха: {temperature}°C\n'
        #                      f'Ощущается как: {temperature_feels}°C\n'
        #                      f'Ветер: {wind_speed} м/с\n'
        #                      f'Облачность: {cloud_cover}\n'
        #                      f'Влажность: {humidity}%')
        await message.reply(f'<em>{message.from_user.first_name}</em>, данные о городе <b>{city}</b> были успешно найдены ✅.\n\n'
                            f'<b>📩 Итого краткая сводка по погоде 📩</b>\n'
                            f'<b>🌡Температура воздуха: {temperature}°C 🌡</b>\n'
                            f'<b>🚶‍♂️ Ощущается как: {temperature_feels}°C 🚶‍♂️</b>\n\n'
                            f'<em>Если вам нужны более точные сводки и погоде вы можете обратится к ниже предоставленным кнопкам:</em>', parse_mode='HTML', reply_markup=inline_information_weather_kb)
        

        
    except KeyError:
        await message.reply(f'<b>{message.from_user.first_name}</b>, к сожелению нам не удалось найти информацию о городе {city} ❌.\n\n'
                             f'Произошла <b>ошибка</b> и мы <em>не смогли найти</em> город <b>{city}</b>, попробуйте <b>еще раз</b> ввести его или используйте другие названия!', parse_mode="HTML")
    

                    

        


@dp.callback_query(F.data == 'dop_info')
async def dop_info_weather_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get('city')
    temperature = data.get('temperature')
    temperature_feels = data.get('temperature_feels')
    wind_speed = data.get('wind_speed')
    cloud_cover = data.get('cloud_cover')
    humidity = data.get('humidity')

    await callback.answer('')
    await callback.message.reply(f'<em>Ваш запрос на подробную сводку погоды был успешен ✅.</em>\n\n'
                            f'<b>📩 Итоговая полная сводка по погоде в городе {city} 📩</b>\n\n'
                            f'<b>🌡Температура воздуха: {temperature}°C 🌡</b>\n'
                            f'<b>🚶‍♂️ Ощущается как: {temperature_feels}°C 🚶‍♂️</b>\n'
                            f'<b>💨 Скорость ветра: {wind_speed}м/c 💨</b>\n'
                            f'<b>☁️ Облачность: {cloud_cover} ☁️</b>\n'
                            f'<b>☔️ Процент влажности: {humidity}% ☔️</b>\n', parse_mode='HTML')
    
    

@dp.callback_query(F.data == 'cloth_info')
async def cloth_info_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    temperature = data.get('temperature')
    await callback.answer('')
    if temperature >= 20:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>На улице довольно жарко, вы можете обойтись футболкой и шортами и кепкой.</b>'
                                    f'<b>Запасайтесь холодным мороженным и напитками и наслаждайтесь жарким деньком ☀️.</b>', parse_mode='HTML')
    if 20 > temperature >= 15:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>На улице тепло, однако при ветренной погоде может стать немного прохладно ❄️.</b>\n'
                                    f'<b>Советуем взять с собой кофту и штаны на всякий случай изменения погодных условий 🥶.</b>', parse_mode='HTML')
    if 15 > temperature >= 10:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>На улице довольно прохладно, уж точно время не для шорт с майкой 😄.</b>\n'
                                    f'<b>Советуем надеть штаны и легкую куртку-ветровку а также легкую шапку!</b>\n', parse_mode='HTML')
    if 10 > temperature >= 0:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>На улице холоднее чем обычно, погода весьма обманчива ☹️.</b>\n'
                                    f'<b>Советуем надеть штаны и шапку потеплее а также плотную куртку во избежании обморожения.</b>\n'
                                    f'<b>Возможно пришло время достать бабушкины варешки 😅.</b>', parse_mode='HTML')
    if 0 > temperature >= -19:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>На улице явная зима ☃️.</b>\n'
                                    f'<b>Одевайтесь очень хорошо, теплые штаны, шапка и варежки - ваши лучшие друзья!</b>\n', parse_mode='HTML')
    if -20 > temperature >= -30:
        await callback.message.reply(f'<em>Ваш запрос на совет по одежде был успешно выполнен ✅.</em>\n\n'
                                    f'<b>За окном полная тундра 🥶.</b>\n'
                                    f'<b>Советуем воздержатся от длительных выходов на улицу во избежании обморожений!</b>\n'
                                    f'<b>Лучше будет остатся дома, смотреть любимые видосики и греться попивая чаек ☕️.</b>', parse_mode='HTML')
    


###################################################################################################
# ОБРАБОТКА КНОПОК КОМАНДЫ START
###################################################################################################


@dp.callback_query(F.data == 'popular')
async def popular_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(f'Ниже клавиатурой вам представлен выбор городов:', reply_markup=most_popular_city_kb)

@dp.callback_query(F.data == 'link')
async def link_callback(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.reply(f'Уважаемый наш <b>пользователь</b>, в <em>нашем боте</em> информация о погоде берется с источника <a href="https://openweathermap.org">OpenWeatherMap</a> ⛅️.\nС их <b>API</b> мы получаем <em>самые точные сводки</em> о <b>погоде</b> радуя вас точными прогнозами 😘.', parse_mode='HTML')


@dp.callback_query(F.data == 'dp')
async def dp_callback(callback: CallbackQuery):
    # await callback.answer('')
    await callback.answer('В разработке...', show_alert=True)



@dp.callback_query(F.data == 'message_weather')
async def start_subscription(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Временно недоступно...', show_alert=True)



###################################################################################################
# КОД ЗАПУСКА БОТА
###################################################################################################

async def main():
    

    print("Бот запускается...")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота приостановлена...')