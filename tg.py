from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Данные меню буфета (можно расширить)
MENU = """
🍽️ Меню буфета на сегодня:

1. Салат овощной — 80руб.
2. Суп гороховый — 120руб.
3. Котлета с пюре — 150руб.
4. Компот — 50руб.
5. Булочка с маком — 40руб.
"""

# Список для хранения пожеланий
wishes = []

# Команда /start и /menu — показываем меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Меню буфета")],
        [KeyboardButton("Оставить пожелание")],
        [KeyboardButton("Пожелания")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я бот буфета. Выбери действие:",
        reply_markup=reply_markup
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU, parse_mode='Markdown')

# Обработка текста «Пожелания»
async def show_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if wishes:
        wishes_text = "📋 **Все пожелания:**\n\n" + "\n".join(f"• {w}" for w in wishes)
    else:
        wishes_text = "Пока нет пожеланий."
    await update.message.reply_text(wishes_text, parse_mode='Markdown')

# Приём пожеланий
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Меню буфета":
        await show_menu(update, context)
    elif text == "Пожелания":
        await show_wishes(update, context)
    elif text == "Оставить пожелание":
        await update.message.reply_text("Напишите ваше пожелание:")
    else:
        # Сохраняем любое другое сообщение как пожелание
        wishes.append(f"{update.message.from_user.first_name}: {text}")
        await update.message.reply_text("Спасибо! Ваше пожелание записано.")

def main():
    # Замените 'YOUR_TOKEN' на токен вашего бота от @BotFather
    TOKEN = "8509695347:AAGbIr7LY_tCkVSkFVqaGV8kxVqMd4DLZaI"

    application = Application.builder().token(TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()