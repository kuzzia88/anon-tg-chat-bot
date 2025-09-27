"""
Telegram Bot: anon-tg-chat-bot
Copyright (c) 2025 kuzzia88
MIT License
"""

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from cfg import TOKEN
import asyncio
from utils import Anon, UserStates
from db import database as db

try:
    asyncio.run(db.create_default_db())
except:
    pass

bot = Bot(TOKEN)
dp = Dispatcher()
anon = Anon(bot)

@dp.message(UserStates.waiting_for_id)
async def userState_handler_check_psw(message: types.Message, state: FSMContext):
    await anon.userState_id_handler(message, state)

@dp.message(Command("start"))
async def start(message: types.Message):
    await anon.start(message)
    
@dp.message(Command("id"))
async def start(message: types.Message):
    await message.answer(f'<code>{await db.get_user_id(message)}</code>', parse_mode="HTML")
    
@dp.message(Command("changeid"))
async def changeID(message: types.Message):
    await db.change_ID(message)

@dp.message(Command("connect"))
async def connect(message: types.Message, state: FSMContext):
    await anon.connect(message, state)

@dp.message(Command("disconnect"))
async def disconnect(message: types.Message):
    await anon.disconnect(message)
    
@dp.message(F.text)
async def process_name(message: types.Message):
    await anon.text_handler(message)
    
@dp.callback_query(F.data)
async def callback_query(callback: types.CallbackQuery, state: FSMContext):
    await anon.callback_handler(callback, state)
    
async def main():
    print('[+] The bot has been launched successfully!')
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())