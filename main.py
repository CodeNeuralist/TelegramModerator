import config
import logging
from filters import isAdminFilter
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(isAdminFilter)

# Чтение нецензурных слов из файла
censored_words_file = "censored_words.txt"
with open(censored_words_file, "r", encoding="utf-8") as file:
    censored_words = [word.strip().lower() for word in file.readlines()]

@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Эта команды должна быть ответов на сообщение!")
        return
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    # Delete the original message
    await message.delete()

    # Greet the new chat member
    new_member = message.new_chat_members[0]
    await message.answer(f"Hello, {new_member.first_name}!")


@dp.message_handler(content_types=["text"])
async def check_for_censored_words(message: types.Message):
    words = message.text.lower().split()
    for word in censored_words:
        if word in words:
            await bot.delete_message(message.chat.id, message.message_id)
            return
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)