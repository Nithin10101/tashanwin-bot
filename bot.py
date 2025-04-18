from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

TOKEN = "8133255905:AAG9UNGZjeboL9ckvCCwb-wZx4tMlyoLmlY"

past_results = []
levels = [10, 20, 30, 60, 120, 250, 500]
user_data = {}
user_period = {}

def get_prediction():
    if len(past_results) < 2:
        return "Big"
    return "Big" if past_results[-1] == past_results[-2] else "Small"

def format_prediction(user_id):
    level = user_data.get(user_id, 0)
    period = user_period.get(user_id, "Unknown")
    return (
        "TASHAN WIN 💥\n\n"
        f"**Period:** {period}\n"
        f"**Prediction:** {get_prediction()}\n"
        f"**Level:** {level + 1}\n"
        f"**Bet:** ₹{levels[level]}"
    )

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to Tashan Win Prediction Bot!\nSend Period Number to get prediction.")

async def handle_period(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Enter Period Number")
        return

    user_data[user_id] = user_data.get(user_id, 0)
    user_period[user_id] = text

    msg = format_prediction(user_id)
    buttons = [
        [InlineKeyboardButton("Won", callback_data="won"),
         InlineKeyboardButton("Loss", callback_data="loss")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

async def result_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_data:
        user_data[user_id] = 0

    if query.data == "won":
        user_data[user_id] = 0
        past_results.append(get_prediction())
        await query.edit_message_text("Great! You Won. Send next Period Number.")
    elif query.data == "loss":
        user_data[user_id] = min(user_data[user_id] + 1, len(levels) - 1)
        past_results.append(get_prediction())
        msg = format_prediction(user_id)
        buttons = [
            [InlineKeyboardButton("Won", callback_data="won"),
             InlineKeyboardButton("Loss", callback_data="loss")]
        ]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_period))
app.add_handler(CallbackQueryHandler(result_handler))

if __name__ == "__main__":
    app.run_polling()
