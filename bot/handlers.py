from functools import wraps
from aiogram import F
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import keyboards
from config import GROUP_ID, CHANNEL_ID
from datetime import datetime, time #для проверки
import http_requests
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMember

router = Router()


#ежедневный гороскоп
user_clicks = {}
def can_click(user_id):
    now = datetime.now()
    if user_id in user_clicks:
        last_click_time = user_clicks[user_id]
        # Получаем полночь сегодняшнего дня
        midnight = datetime.combine(now.date(), time.min)

        if last_click_time >= midnight: #если последнее нажатие было сегодня
            return False
        else:
            return True
    else:
        return True
    

class TaroState(StatesGroup):
    name = State()
    quest = State()
    cards = State()

class SovmesState(StatesGroup):
    name = State()
    name2 = State()
    sign = State()
    sign2 = State()

class GoroskopState(StatesGroup):
    sign = State()


def get_date():
    current_date = datetime.now().strftime('%Y-%m-%d')
    return current_date


async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Проверяем статус. Важно, чтобы пользователь был не 'left' или 'kicked'.
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR, ChatMemberStatus.RESTRICTED)
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")  # Логируем ошибку
        return False  # Обрабатываем ошибки, возвращаем False




@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = keyboards.get_main_keyboard()
    photo = FSInputFile("photos/cards.jpg")
    await message.answer_photo(caption="🤬 Эй, ты, чего застыл? Я – Вещун Залупный, и я не люблю ждать!\n 😠 Готов узнать горькую правду о себе? Выбирай, на что ты сегодня отважишься: гороскоп, совместимость, или Таро? 😈", photo=photo, reply_markup=keyboard)


#ДЕКОРАТОР ДЛЯ ПОДПИСОК
def check_subscription_decorator():
        def decorator(func):
            @wraps(func)
            async def wrapper(message: types.Message, *args, **kwargs):
                user_id = message.from_user.id
                is_subscribed = await check_subscription(message.bot, user_id)
                if is_subscribed:
                    return await func(message, *args, **kwargs)
                else:
                    keyboard = keyboards.get_subscribe_keyboard()
                    await message.answer(
                        "Слышь! 👀 Вещун Залупный не для всех! 🤫 Хочешь заглянуть в будущее? 🔮 Подпишись на канал – получи VIP-пропуск в мир тайн! 🗝 Иначе будешь гадать на кофейной гуще! ☕️",
                        reply_markup=keyboard,
                    )

            return wrapper

        return decorator

#ДЕКОРАТОР ДЛЯ ПОДПИСОК КАЛБЕК
def check_subscription_callback_decorator():
    def decorator(func):
        @wraps(func)
        async def wrapper(callback: types.CallbackQuery, *args, **kwargs):
            user_id = callback.from_user.id
            is_subscribed = await check_subscription(callback.message.bot, user_id)
            if is_subscribed:
                return await func(callback, *args, **kwargs)
            else:
                keyboard = keyboards.get_subscribe_keyboard()
                await callback.message.answer(
                    "Слышь! 👀 Вещун Залупный не для всех! 🤫 Хочешь заглянуть в будущее? 🔮 Подпишись на канал – получи VIP-пропуск в мир тайн! 🗝 Иначе будешь гадать на кофейной гуще! ☕️",
                    reply_markup=keyboard,
                )
                await callback.answer()  # Важно ответить на callback, чтобы убрать "часики"

        return wrapper

    return decorator


#ОТМЕНА
@router.callback_query(GoroskopState.sign, F.data.in_({"Отмена"}))
async def callback_cancel(callback: types.CallbackQuery, state: FSMContext, bot:Bot):
    await state.clear()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 
    keyboard = keyboards.get_main_keyboard()
    await callback.message.answer("🤬 Эй, ты, чего застыл? Я – Вещун Залупный, и я не люблю ждать!\n 😠 Готов узнать горькую правду о себе? Выбирай, на что ты сегодня отважишься: гороскоп, совместимость, или Таро? 😈", reply_markup=keyboard)

#ПРОВЕРКА ПОДПИСКИ
@router.callback_query( F.data.in_({"проверка"}))
async def callback_cancel(callback: types.CallbackQuery, state: FSMContext, bot:Bot):
    await state.clear()
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(callback.message.bot, user_id)

    if is_subscribed:
        await callback.message.answer("Ага! 😎 Подписка есть – ты в теме! 👍 Готов к правде? 😈 Выбирай, что нагадать! 🔮")
    else:
        keyboard = keyboards.get_subscribe_keyboard()
        await callback.message.answer("Э, нет! 🙅‍♂️ Думал, проскочишь? Вещун Залупный всё видит! 👁️ Не подписался – нет и предсказаний! 🚫 Подпишись, и будет тебе счастье! ✨", reply_markup=keyboard)
    await callback.answer()  # Важно ответить на callback, чтобы убрать "часики"

@router.message(F.text == "Отмена")
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = keyboards.get_main_keyboard()
    await message.answer("🤬 Эй, ты, чего застыл? Я – Вещун Залупный, и я не люблю ждать!\n 😠 Готов узнать горькую правду о себе? Выбирай, на что ты сегодня отважишься: гороскоп, совместимость, или Таро? 😈", reply_markup=keyboard)

#ТАРО
@router.message(F.text == "🃏Таро")
@check_subscription_decorator()
async def start(message: types.Message, state: FSMContext):
    await state.set_state(TaroState.name)
    keyboard = keyboards.get_cancel_keyboard()
    await message.answer("🖤 Хочешь узнать своё будущее, через карты Таро?\n Ну, ладно, Вещун Залупный поможет. 🔮 Для начала, введи свое имя, чтобы я знал, с кем имею дело. 😏", reply_markup=keyboard)
    await message.answer("Введите ваше имя:")
@router.message(TaroState.name)
async def start(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(TaroState.quest)
    await message.answer("🤨 Так, имя есть. Теперь изложи, что у тебя там за беда приключилась? \n🙄 Опиши свою ситуацию, Вещуну Залупному всё можно рассказать. 🤫")
    await message.answer("Введите ваш вопрос/ситуацию:")

@router.message(TaroState.quest)
async def start(message: types.Message, state: FSMContext):
    await state.update_data(quest=message.text)
    await state.set_state(TaroState.cards)
    keyboard = keyboards.get_taro_keyboard()
    await message.answer("🤔 Ага, ясно-понятно. Теперь, сколько карт Таро хочешь вытянуть? 🔮", reply_markup=keyboard)

@router.callback_query(TaroState.cards, F.data.in_({"3_cards", "4_cards", "5_cards"}))
async def callback_taro(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "3_cards":
        await state.update_data(cards="3")
    elif callback.data == "4_cards":
        await state.update_data(cards="4")
    elif callback.data == "5_cards":
        await state.update_data(cards="5")

    await bot.send_message(chat_id=callback.message.chat.id, text="Вещун колдует...") # Отправляем сообщение "Запрос отправлен"
    data = await state.get_data()

    await state.clear()
    keyboard = keyboards.get_main_keyboard()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 
    bot_mes = await http_requests.getTaro(data["name"], data["quest"], data["cards"])
    await bot.send_message(chat_id=callback.message.chat.id, text=bot_mes, reply_markup=keyboard)
    await bot.send_message(
        chat_id=GROUP_ID,
        text=f'Юз: @{callback.from_user.username}\n Запрос:ТАРО \n Имя: {data["name"]}\n Запрос: {data["quest"]}\n Карт: {data["cards"]} \n \n {bot_mes}'
    )


#СОВМЕСТИМОСТЬ
@router.message(F.text == "💘Совместимость")
@check_subscription_decorator()
async def sovm1(message: types.Message, state: FSMContext):
    await state.set_state(SovmesState.name)
    keyboard = keyboards.get_cancel_keyboard()
    await message.answer("😈 Ну что, красавчик(ца), раз решил(а) узнать правду, то давай начнем с простого! \n🤪 Введи своё имя, чтобы я, Вещун Залупный, не путался, когда буду рассказывать про твою совместимость. 🖕", reply_markup=keyboard)
    await message.answer("Введите ваше имя:")

@router.message(SovmesState.name)
async def sovm2(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SovmesState.name2)
    await message.answer("🤬 Окей, твоё имя у меня. Теперь введи имя того бедолаги, с кем ты хочешь узнать совместимость. \n😈 Ну, давай, не тупи, Вещун Залупный ждёт! ⏳")
    await message.answer("Введите второе имя:")

@router.message(SovmesState.name2)
async def sovm3(message: types.Message, state: FSMContext):
    await state.update_data(name2=message.text)
    await state.set_state(SovmesState.sign)
    keyboard = keyboards.get_sign_keyboard()
    await message.answer(" Отлично, с именами разобрались. Теперь, какой ты там по гороскопу? Выбери свой знак зодиака, чтобы я мог дальше мудрить. 👇", reply_markup=keyboard)

@router.callback_query(SovmesState.sign, F.data.in_({"Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Козерог", "Водолей", "Рыбы", "Стрелец"}))
async def callback_sovmes1(callback: types.CallbackQuery, state: FSMContext):
    sign = callback.data
    await state.update_data(sign=sign)
    await state.set_state(SovmesState.sign2)
    keyboard = keyboards.get_sign_keyboard()
    await callback.message.answer("И последний шаг: какой знак зодиака у твоего партнера? 😈 Выбирай! Вещун Залупный почти готов раскрыть всю правду. 🔮", reply_markup=keyboard)

@router.callback_query(SovmesState.sign2, F.data.in_({"Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Козерог", "Водолей", "Рыбы", "Стрелец"}))
async def callback_sovmes2(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    sign = callback.data
    await state.update_data(sign2=sign)
    await state.set_state(SovmesState.sign2)

    data = await state.get_data()
    await state.clear()
    await callback.answer()
    keyboard = keyboards.get_main_keyboard()
    await bot.send_message(chat_id=callback.message.chat.id, text="Вещун колдует...", reply_markup=keyboard) # Отправляем сообщение "Запрос отправлен"
    bot_mes = await http_requests.getCompatibility(data["name"], data["name2"], data["sign"], data["sign2"])
    await bot.send_message(chat_id=callback.message.chat.id, text=bot_mes, reply_markup=keyboard)
    await bot.send_message(
        chat_id=GROUP_ID,
        text=f'Юз: @{callback.from_user.username}\n Запрос:СОВМЕСТИМОСТЬ \n Имя: {data["name"]}\n Имя2: {data["name2"]}\n Знак Зодиака1: {data["sign"]}\n Знак Зодиака2: {data["sign2"]} \n \n {bot_mes}'
    )

#ГОРОСКОП
@router.message(F.text == "🔮Гороскоп")
@check_subscription_decorator()
async def goroskop(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if can_click(user_id):
        user_clicks[user_id] = datetime.now()
        await state.set_state(GoroskopState.sign)
        keyboard = keyboards.get_sign_keyboard()
        await message.answer("🔮Давай, не стесняйся, выбери свой значок среди этого зоопарка. \nВещун Залупный готов тебе выдать самую правдивую (и смешную) предсказашку. 🤪", reply_markup=keyboard)
    else:
        await message.answer("🙄 Ну вот, опять ты! Я, 🔮Вещун Залупный, не попка-дурак повторять одно и то же. \n😒 Приходи завтра, если терпения хватит. ⏳")
    
@router.callback_query(GoroskopState.sign, F.data.in_({"Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Козерог", "Водолей", "Рыбы", "Стрелец"}))
async def callback_goroskop(callback: types.CallbackQuery, state: FSMContext, bot:Bot):
    sign = callback.data
    await state.update_data(sign=sign)
    data = await state.get_data()
    await state.clear()
    await callback.answer()
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 
    await bot.send_message(chat_id=callback.message.chat.id, text="Вещун колдует...") # Отправляем сообщение "Запрос отправлен"
    bot_mes = await http_requests.getHoroscope(data["sign"])
    await bot.send_message(chat_id=callback.message.chat.id, text=bot_mes)
    await bot.send_message(
        chat_id=GROUP_ID,
        text=f'Юз: @{callback.from_user.username}\n Запрос:ГОРОСКОП \n Знак зодиака: {data["sign"]} \n Дата: {get_date()} \n \n {bot_mes}'
        )







#если пользотель ввел что то не то
@router.message()
async def unknown_message(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GoroskopState.sign:
          await message.answer("🤨 Это что вообще такое? Ты, случаем, не перепутал кнопки? 🙄 Я просил выбрать знак зодиака, а не придумывать новые. Выбирай, давай!")
    else:
        await message.answer("😈 Не понял тебя. Я, Вещун Залупный, жду твоих внятных действий, а не этой ахинеи. 🖕 Введи команду /start, и тогда поговорим. 😒")

