import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from rapidfuzz import fuzz

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Data
students_data = {
    "Slimani Sarah": "3.5/7",
    "Talbi Wassila": "4/7",
    "Soufi Nabila": "3.5/7",
    "Said Alle Dine": "3.5/7",
    "Sekkak Aissa": "4.5/7",
    "Sebbouh Mehdi": "4.5/7",
    "Saim Sofiane": "3.5/7",
    "Hamel Aissa": "7/7",
    "Aicha Senhadji": "4/7",
    "Seddougui Chorouk": "4/7",
    "Seffehi Wissal": "4.5/7",
    "Stili Bekhta": "4/7",
    "Smahi Imene": "4/7",
    "Soummar Roumayssa": "4/7",
    "Tabet Hiba": "5/7",
    "Soltani Raouane": "3.5/7",
    "Selhami Meriem": "3.5/7",
    "Sahraoui" : "7777/7"
}

# Temporary state storage
awaiting_name = {}

# /note command
async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    awaiting_name[chat_id] = True
    await update.message.reply_text("Please provide your full name.")

# Name verification
async def check_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if awaiting_name.get(chat_id, False):
        user_input = update.message.text.strip().lower()
        best_match = None
        highest_score = 0

        # Find the closest matching name
        for student_name in students_data.keys():
            score = fuzz.ratio(user_input, student_name.lower())
            if score > highest_score:
                highest_score = score
                best_match = student_name

        # Respond based on the match
        if highest_score >= 50:  # Similarity threshold
            score = students_data[best_match]
            await update.message.reply_text(f"Welcome, {best_match}. Your score in Test 2 is {score}.")
        else:
            await update.message.reply_text("Sorry, the name you provided does not match our records.")
        
        awaiting_name[chat_id] = False
    else:
        await update.message.reply_text("Please type 'note' to start.")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("note", note_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_name))

    # Run the bot
    app.run_polling()

if __name__ == "__main__":
    main()
