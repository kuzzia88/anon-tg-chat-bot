"""
Telegram Bot: anon-tg-chat-bot
Copyright (c) 2025 kuzzia88
MIT License
"""

import sqlite3
import secrets
from aiogram import types

class database():
    async def get_user_id(message):
        id = message.from_user.id
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT bot_id FROM users WHERE id = ?", (id,))
        rez = cur.fetchall()
        return rez[0][0]
    async def create_default_db():
        db = sqlite3.connect('users.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id TEXT,
            bot_id TEXT,
            chat_id TEXT,
            connected TEXT,
            UNIQUE(id)
        )""")
        db.commit()
    async def user_started_bot_for_server(message: types.Message):
        print('________________________________')
        print('[+] New user:')
        print(f'    [ID] {message.from_user.id}')
        print(f'    [Chat ID] {message.chat.id}')
        print(f'    [username] {message.from_user.username}')
        print(f'    [Fname] {message.from_user.first_name}')
        print(f'    [Sname] {message.from_user.last_name}')
        print('________________________________')
        print()
    async def create_account(message: types.Message):
        id = message.from_user.id
        chat_id = message.chat.id
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (id,))
        rez = cur.fetchall()
        if not rez:
            db = sqlite3.connect('users.db')
            cur = db.cursor()
            usrlst = (id, secrets.token_hex(4), chat_id, '0')
            cur.execute("INSERT INTO users (id, bot_id, chat_id, connected) VALUES (?, ?, ?, ?)", usrlst)
            db.commit()
            await database.user_started_bot_for_server(message)
            return True
        else:
            return False
    async def change_ID(message: types.Message):
        id = message.from_user.id
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        nid = secrets.token_hex(4)
        cur.execute("UPDATE users SET bot_id = ? WHERE id = ?", (nid, id))
        db.commit()
        await message.answer(f'✅ ID успешно изменен на <code>{nid}</code>!', parse_mode="HTML")
        print(f'[INFO] user, with id - "{id}" changed his ID to - {nid}')
        return True
    async def check_connect_ur(message):
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT connected FROM users WHERE id = ?", (message.from_user.id,))
        rez = cur.fetchall()
        if rez[0][0] == '0':
            return False
        else:
            return rez[0][0]
    async def check_connect(message):
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT connected FROM users WHERE id = ?", (message.from_user.id,))
        rez = cur.fetchall()
        if rez[0][0] == '0':
            return False
        else:
            return rez[0][0]
    async def check_id(message, state):
        if message.text == 'e':
            await state.clear()
        else:
            db = sqlite3.connect("users.db")
            cur = db.cursor()
            cur.execute("SELECT id FROM users WHERE bot_id = ?", (message.text.strip(),))
            rez = cur.fetchall()
            if not rez: 
                await message.answer(f'🤷‍♂️ Что-то не так\n👍 Попробуйте перепроверьте ID\n❗ Чтобы выйти отправите "e"')
                return False
            else:
                await state.clear()
                return True
    async def get_chat_id(message):
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT chat_id FROM users WHERE bot_id = ?", (message.text.strip(),))
        rez = cur.fetchall()
        return rez[0][0]
    async def get_chat_id_by_bot_id(bot_id):
        try:
            db = sqlite3.connect("users.db")
            cur = db.cursor()
            cur.execute("SELECT chat_id FROM users WHERE bot_id = ?", (bot_id,))
            rez = cur.fetchall()
            return rez[0][0]
        except IndexError:
            pass
    async def get_id_by_bot_id(bot_id):
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        print(bot_id)
        cur.execute("SELECT id FROM users WHERE bot_id = ?", (bot_id,))
        rez = cur.fetchall()
        return rez[0][0]
    async def disconnect(message, bot):
        con = await database.check_connect(message)
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("UPDATE users SET connected = ? WHERE bot_id = ?", ('0', con))
        cur.execute("UPDATE users SET connected = ? WHERE id = ?", ('0', message.from_user.id))
        db.commit()
        await bot.send_message(chat_id=await database.get_chat_id_by_bot_id(con), text=f'🤷‍♂️ Собеседник отключился')
        await message.answer('✅ Вы успешно отключились!')
        return True
    async def connect(self, connector_id, connection_id):
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("UPDATE users SET connected = ? WHERE bot_id = ?", (connection_id, connector_id))
        db.commit()
        return True
    async def show_accounts():
        db = sqlite3.connect("users.db")
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        rez = cur.fetchall()
        return rez