import telebot
from telebot import types
import os
import threading
from flask import Flask

# ========== ТОКЕН И НАСТРОЙКИ ==========
# Рендер сам подставит токен из переменной окружения, если ты её добавил.
# Если нет — он возьмёт токен, который в коде.
TOKEN = os.getenv('TOKEN', '8910906044:AAHFxhSOe3LBudK2V3jayLA6kFx8I18ib4Y')

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# ========== СЧЁТЧИК ДЛЯ /terms (18 раз) ==========
user_terms_counter = {}

# ========== ВЕБ-СЕРВЕР ДЛЯ ПИНГА (ЧТОБЫ НЕ ЗАСЫПАЛ) ==========
app = Flask(__name__)

@app.route('/')
def health():
    return "FLASH KUPYRY is alive ✅", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

# Запускаем Flask в фоновом потоке
threading.Thread(target=run_flask, daemon=True).start()

# ========== ГЛАВНОЕ МЕНЮ (ВНИЗУ ЭКРАНА) ==========
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn1 = types.KeyboardButton("📄 Прайс цен")
    btn2 = types.KeyboardButton("❓ Почему продаем")
    btn3 = types.KeyboardButton("🚕 Такси и клады")
    btn4 = types.KeyboardButton("🙌 Отзывы")
    btn5 = types.KeyboardButton("🇺🇦 Фото гривны")
    btn6 = types.KeyboardButton("🇺🇸 Фото USD")
    btn7 = types.KeyboardButton("💳 Банковские Карты")
    btn8 = types.KeyboardButton("📋 Инструкция по отмыву")
    btn9 = types.KeyboardButton("📱 Заказать")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    markup.add(btn9)
    return markup

# ========== СТАРТ ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 FLASH_KUPYRY\n\nВыберите раздел:",
        reply_markup=main_menu(),
        protect_content=True
    )

# ========== КОМАНДА /terms (18 раз подряд) ==========
@bot.message_handler(commands=['terms'])
def terms_command(message):
    user_id = message.chat.id
    
    if user_id in user_terms_counter:
        user_terms_counter[user_id] += 1
    else:
        user_terms_counter[user_id] = 1
    
    if user_terms_counter[user_id] >= 18:
        bot.send_message(
            user_id,
            "📄 Пользовательское соглашение:\nhttps://telegra.ph/Legal-Terms-FLASH-KUPYRY-2026-07-17",
            reply_markup=main_menu(),
            protect_content=True
        )
        del user_terms_counter[user_id]

# ========== ОБРАБОТЧИК ВСЕХ СООБЩЕНИЙ (КНОПКИ) ==========
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.chat.id

    # Сброс счётчика для /terms, если написал что-то другое
    if user_id in user_terms_counter:
        if not text.startswith('/terms'):
            del user_terms_counter[user_id]

    # ========== ПРАЙС ==========
    if text == "📄 Прайс цен":
        response = """🔥 АКЦИОННЫЙ ПРАЙС НА ЛУЧШИЕ ФАЛЬШ КУПЮРЫ В 2026 🔥

🇺🇦 Гривна UAH
Платите → Получаете:

1 000 грн    →    <s>3 500 грн</s> <b>4 400 грн</b> (+25%)
1 500 грн    →    <s>6 500 грн</s> <b>8 100 грн</b> (+25%)
2 500 грн    →    <s>10 500 грн</s> <b>13 100 грн</b> (+25%)
5 000 грн    →    <s>21 000 грн</s> <b>26 300 грн</b> (+25%)
10 000 грн   →    <s>42 000 грн</s> <b>52 500 грн</b> (+25%)
14 000 грн   →    <s>63 000 грн</s> <b>78 800 грн</b> (+25%)

💵 DOLLAR USA (USD)
Платите:          Получаете:
100$        →     400$
200$        →     900$
500$        →    2400$

💥 Акция действует ограниченное время!"""

    # ========== ПОЧЕМУ ПРОДАЕМ ==========
    elif text == "❓ Почему продаем":
        response = """📍Почему мы сами не избавляемся от подделок, а продаем их?

⚜️Нам часто задают этот вопрос. Но это очевидно: если товар будет продаваться нами только в одном регионе страны — это будет подозрительно, нужно, чтобы товар равномерно расходился по всем регионам, и в этом вы — наши помощники и партнеры🤝

⚜️В данный момент подделок большое количество, а деньги, как говорится, способны приносить прибыль, мы продаем и снова пускаем в оборот. Так и растет дело⬆️

⚜️Для нашей и вашей безопасности нужно, чтобы купюры равномерно распределялись по стране, конечно, мы тоже отмываем нашу продукцию, но другими способами и в больших количествах. 

⚜️Нам гораздо выгоднее делиться с вами и зарабатывать вместе, что выгодно всем 💯

⚜️ Начни зарабатывать вместе с нами и забудь о работе на начальника, ты сам будешь регулировать свой доход💹💵💵

🙏 Партнеры и новички, убедительная просьба: если вы стали нашим покупателем, не нужно рассказывать близким и друзьям, откуда у вас такие большие суммы, ведите обычную жизнь, не нужно бежать в магазин за креветками, икрой и Хеннесси (я понимаю, что хочется, но будьте мудрее🙏)
1️⃣ Сомневаюсь, что этот заработок ваши близкие оценят по достоинству.
2️⃣ Зависть... (последствие...)
✅ Нас уже много, мы не бросаемся во все тяжкие! Работаем спокойно 😌

Для заказа обращайтесь к оператору: 👇
@FLASH_KUPYRY"""

    # ========== ТАКСИ И КЛАДЫ ==========
    elif text == "🚕 Такси и клады":
        response = """🚕 Города в которых делаем клады:

📍 Киев
📍 Харьков
📍 Одесса
📍 Днепр
📍 Львов
📍 Запорожье
📍 Кривой Рог
📍 Николаев
📍 Мариуполь
📍 Винница
📍 Херсон
📍 Полтава
📍 Чернигов
📍 Черкассы
📍 Житомир
📍 Сумы
📍 Ровно
📍 Ивано-Франковск
📍 Тернополь
📍 Луцк
📍 Ужгород
📍 Хмельницкий
📍 Кропивницкий
📍 Черновцы
📍 Белая Церковь
📍 Каменское
📍 Кременчуг
📍 Северодонецк
📍 Бровары
📍 Дрогобыч
📍 Борисполь

Свяжитесь с оператором для уточнения деталей 👇
@FLASH_KUPYRY"""

    # ========== ОТЗЫВЫ ==========
    elif text == "🙌 Отзывы":
        response = """🙌 Отзывы

В связи с блокировкой отзывы временно не доступны. Новый канал будет добавлен, и мы вас оповестим.

Приносим извинения за временные неудобства 🙏

@FLASH_KUPYRY"""

    # ========== ФОТО ГРИВНЫ ==========
    elif text == "🇺🇦 Фото гривны":
        photos = ['grivna1.jpg', 'grivna2.jpg', 'grivna3.jpg', 'grivna4.jpg']
        for photo_file in photos:
            try:
                with open(photo_file, 'rb') as f:
                    bot.send_photo(chat_id, f, protect_content=True)
            except:
                pass
        bot.send_message(
            chat_id,
            "🇺🇦 Фото гривны (лучшие фальш купюры)",
            reply_markup=main_menu(),
            protect_content=True
        )
        return

    # ========== ФОТО USD ==========
    elif text == "🇺🇸 Фото USD":
        response = """🇺🇸 Фото USD

⏳ Раздел в разработке. Скоро добавим фото!"""

    # ========== БАНКОВСКИЕ КАРТЫ ==========
    elif text == "💳 Банковские Карты":
        response = """❗ Для удобства и анонимности работы вы можете приобрести у нас банковские карты, оформленные на «дропа» (человека, не имеющего к вам никакого отношения)

♻ Вы сможете анонимно пополнять и снимать деньги в терминалах самообслуживания и банкоматах.

В комплект входит:
1⃣ Карта
2⃣ PIN-код
3⃣ SIM-карта
4⃣ Кодовое слово
5⃣ Адрес электронной почты, к которому привязана карта, и доступ в личный кабинет
6⃣ Сканы документов дропа

🏧 Используя этот комплект, вы легко можете установить себе приложения банков на телефон и пользоваться картой как своей, но анонимно, так как она оформлена на подставного лица.

Цена карт от 2000 грн до 6000 грн, зависит от банка, класса карты и лимитов.

👉 @FLASH_KUPYRY 👈"""
        
        try:
            with open('card.jpg', 'rb') as photo:
                bot.send_photo(
                    chat_id,
                    photo,
                    caption=response,
                    reply_markup=main_menu(),
                    protect_content=True
                )
        except:
            bot.send_message(
                chat_id,
                response,
                reply_markup=main_menu(),
                protect_content=True
            )
        return

    # ========== ИНСТРУКЦИЯ ==========
    elif text == "📋 Инструкция по отмыву":
        response = """📋 Инструкция по безопасной работе

Подробная инструкция: https://telegra.ph/INSTRUKCIYA-PO-BEZOPASNOJ-RABOTE-FLASH-KUPYRY-07-17

@FLASH_KUPYRY"""

    # ========== ЗАКАЗАТЬ ==========
    elif text == "📱 Заказать":
        response = """📱 Для оформления заказа пишите нашему оператору:

👇 @FLASH_KUPYRY 👇

Быстро, качественно, конфиденциально! ✅"""

    else:
        return

    # Отправляем ответ
    bot.send_message(
        chat_id,
        response,
        reply_markup=main_menu(),
        protect_content=True
    )

# ========== ЗАПУСК БОТА ==========
if __name__ == '__main__':
    print("🚀 Бот FLASH_KUPYRY запущен...")
    bot.infinity_polling()
