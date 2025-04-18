from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = "8133255905:AAG9UNGZjeboL9ckvCCwb-wZx4tMlyoLmlY"

past_results = []
levels = [10, 20, 30, 60, 120, 250, 500]
user_data = {}

def get_prediction():
    if len(past_results) < 2:
        return "Big"
    return "Big" if past_results[-1] == past_results[-2] else "Small"

def format_prediction(user_id):
    level = user_data.get(user_id, 0)
    return (
        f"Period: {len(past_results)+1}\n"
        f"Prediction: {get_prediction()}\n"
        f"Level: {level + 1}\n"
        f"Bet: ₹{levels[level]}"
    )

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to Tashan Win Prediction Bot!\nSend /predict to get prediction.")

async def predict(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data[user_id] = user_data.get(user_id, 0)
    msg = format_prediction(user_id)
    buttons = [
        [InlineKeyboardButton("Winning", callback_data="win"),
         InlineKeyboardButton("Loss", callback_data="loss")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

async def result_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_data:
        user_data[user_id] = 0

    if query.data == "win":
        user_data[user_id] = 0
        past_results.append(get_prediction())
        await query.edit_message_text("Great! You won. Send /predict for next.")
    elif query.data == "loss":
        user_data[user_id] = min(user_data[user_id] + 1, len(levels) - 1)
        past_results.append(get_prediction())
        await query.edit_message_text("Sorry! You lost. Repeating prediction...\n\n" + format_prediction(user_id))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))
app.add_handler(CallbackQueryHandler(result_handler))

if __name__ == "__main__":
    app.run_polling()
