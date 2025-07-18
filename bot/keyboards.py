from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = [
      [KeyboardButton(text="🃏Таро"), KeyboardButton(text="💘Совместимость")],
      [KeyboardButton(text="🔮Гороскоп")]
    ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_cancel_keyboard():
    keyboard = [
      [KeyboardButton(text="Отмена")]
    ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_taro_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="3 карты", callback_data="3_cards")],
            [InlineKeyboardButton(text="4 карты", callback_data="4_cards")],
            [InlineKeyboardButton(text="5 карт", callback_data="5_cards")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_sign_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Овен", callback_data="Овен"), InlineKeyboardButton(text="Телец", callback_data="Телец"), InlineKeyboardButton(text="Близнецы", callback_data="Близнецы")],
            [InlineKeyboardButton(text="Рак", callback_data="Рак"), InlineKeyboardButton(text="Лев", callback_data="Лев"), InlineKeyboardButton(text="Дева", callback_data="Дева")],
            [InlineKeyboardButton(text="Весы", callback_data="Весы"), InlineKeyboardButton(text="Скорпион", callback_data="Скорпион"), InlineKeyboardButton(text="Стрелец", callback_data="Стрелец")],
            [InlineKeyboardButton(text="Козерог", callback_data="Козерог"), InlineKeyboardButton(text="Водолей", callback_data="Водолей"), InlineKeyboardButton(text="Рыбы", callback_data="Рыбы")],
            [InlineKeyboardButton(text="Отмена", callback_data="Отмена")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_month_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Январь", callback_data="январь")],
            [InlineKeyboardButton(text="Февраль", callback_data="февраль")],
            [InlineKeyboardButton(text="Март", callback_data="март")],
            [InlineKeyboardButton(text="Апрель", callback_data="апрель")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_sex_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Мужской", callback_data="мужской")],
            [InlineKeyboardButton(text="Женский", callback_data="женский")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_subscribe_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Подписаться", callback_data="подписаться", url='https://t.me/astrologer77777')],
            [InlineKeyboardButton(text="Проверить Подписку", callback_data="проверка")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def remove():
        return ReplyKeyboardRemove() 
