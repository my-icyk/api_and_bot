import asyncio
import os
from fastapi import FastAPI
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import uvicorn
import httpx

# Configuration
BOT_TOKEN = "BOT_TOKEN"
CHAT_ID = -1
API_PORT = 8005

ALLOWED_CHAT_IDS = "-1"
if ALLOWED_CHAT_IDS:
    ALLOWED_CHAT_IDS = [int(x.strip()) for x in ALLOWED_CHAT_IDS.split(",")]

# FastAPI app
app = FastAPI()

# Global bot instance
bot = None


@app.on_event("startup")
async def startup():
    global bot
    bot = Bot(token=BOT_TOKEN)


@app.get("/")
async def hello_world():
    """Hello World endpoint"""
    return {"message": "Hello World!"}


@app.post("/notify")
async def notify(message: str = "API route was called!"):
    """Sends a message to Telegram when called"""
    if bot:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        return {"status": "Message sent", "message": message}
    return {"status": "error", "message": "Bot not initialized"}


# Telegram bot commands
def is_allowed_chat(chat_id: int) -> bool:
    """Check if the chat is allowed to use bot commands"""
    if ALLOWED_CHAT_IDS is None:
        return True
    return chat_id in ALLOWED_CHAT_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    chat_id = update.effective_chat.id

    if not is_allowed_chat(chat_id):
        await update.message.reply_text("⛔ This bot is not available in this chat.")
        return

    await update.message.reply_text(
        "Hello! I'm a bot that can:\n"
        "- Receive notifications from FastAPI\n"
        "- Call the API with /callapi command\n\n"
        f"Your chat ID is: {chat_id}"
    )


async def call_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calls the FastAPI hello world endpoint"""
    chat_id = update.effective_chat.id

    if not is_allowed_chat(chat_id):
        await update.message.reply_text("⛔ This bot is not available in this chat.")
        return

    await update.message.reply_text("Calling API...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:{API_PORT}/")
            data = response.json()
            await update.message.reply_text(f"API Response: {data['message']}")
        except Exception as e:
            await update.message.reply_text(f"Error calling API: {str(e)}")


async def run_telegram_bot():
    """Run the Telegram bot"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("callapi", call_api))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Keep running
    while True:
        await asyncio.sleep(1)


async def main():
    """Run both FastAPI and Telegram bot"""
    # Start FastAPI in a separate task
    config = uvicorn.Config(app, host="0.0.0.0", port=API_PORT, log_level="info")
    server = uvicorn.Server(config)

    # Run both concurrently
    await asyncio.gather(
        server.serve(),
        run_telegram_bot()
    )

if __name__ == "__main__":
    print(f"Starting FastAPI server on http://localhost:{API_PORT}")
    print("Starting Telegram bot...")
    print("\nMake sure to set BOT_TOKEN and CHAT_ID environment variables!")
    if ALLOWED_CHAT_IDS:
        print(f"Bot restricted to chat IDs: {ALLOWED_CHAT_IDS}")
    else:
        print("Bot will respond to all chats (no restrictions)")
    asyncio.run(main())
