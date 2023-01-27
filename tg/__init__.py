import logging
from telegram import MenuButtonWebApp, Update, WebAppInfo
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder
from pydantic import BaseSettings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class TGSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    TG_TOKEN: str


tg_settings = TGSettings()  # type: ignore


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat
    await context.bot.setChatMenuButton(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(
            text="Меню",
            web_app=WebAppInfo(url="https://stage-front.kittensanswers.ru/"),
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Для поиска открой меню"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(tg_settings.TG_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
