"""
Telegram Bot: anon-tg-chat-bot
Copyright (c) 2025 kuzzia88
MIT License
"""

from aiogram import Bot, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import database as db

class UserStates(StatesGroup):
    waiting_for_id = State()

class Anon():
    def __init__(self, bot: Bot):
        self.bot = bot
    async def userState_id_handler(self, message, state):
        if await db.check_id(message, state):
            if not await db.check_connect_ur(message):
                if not await db.check_connect(message):
                    kb = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text=f"✅", callback_data=f"connect_{await db.get_user_id(message)}_{message.text}")
                            ]
                        ]
                    )
                    await self.bot.send_message(chat_id=await db.get_chat_id(message), text=f'{await db.get_user_id(message)} хочет пообщаться с вами!', reply_markup=kb)
                else:
                    await message.answer(f'{message.text} уже подключен к кому-то!')
            else:
                await message.answer(f'Ты уже подключен к кому-то!')
    async def start(self, message: types.Message):
        await db.create_account(message)
        lst = ['Халло', 'Дароу', 'Ку', 'Привет']
        if message.from_user.username != None:
            await message.answer(f'{random.choice(lst)}, {message.from_user.username}. Этот бот может связать любого человека с тобой анонимно!')
        else: 
            await message.answer(f'{random.choice(lst)}, {message.from_user.first_name}. Этот бот может связать любого человека с тобой анонимно!')
    async def connect(self, message: types.Message, state: FSMContext):
        await message.answer(f'Чтобы подключиться отправьте ID собеседника, ваш код - <code>{await db.get_user_id(message)}</code>', parse_mode="HTML")
        await state.set_state(UserStates.waiting_for_id)
    async def callback_handler(self, callback: types.CallbackQuery, state: FSMContext):
        parts = callback.data.split('_')
        if len(parts) >= 3:
            action = parts[0]
            connector_id = parts[1]
            connection_id = parts[2]
            
            if action == 'connect':
                await db.connect(self, connection_id, connector_id)
                await db.connect(self, connector_id, connection_id)
                await self.bot.send_message(chat_id=await db.get_chat_id_by_bot_id(connector_id), text='✅ Соединение успешно установлено!')
                await callback.message.answer('✅ Соединение успешно установлено!')
    async def disconnect(self, message):
        await db.disconnect(message, self.bot)
    async def text_handler(self, message: types.Message):
        connected = await db.check_connect(message)
        if not connected:
            pass
        else:
            await self.bot.send_message(chat_id=await db.get_chat_id_by_bot_id(connected), text=message.text)