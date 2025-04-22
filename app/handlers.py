from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.types import Message 
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery

from aiogram.fsm.state import State, StatesGroup #Машина состояния

import app.keyboard as kb 
import app.database.requests as rq
from app.database.requests import get_all_users

router = Router()

class Register(StatesGroup):
    noteName = State()
    noteText = State()

@router.message(CommandStart())
async def start(message: Message):
    chek = await rq.set_user(
        tg_id = message.from_user.id, 
        name = message.from_user.first_name,
        userId = message.from_user.username,
        data = datetime.now(timezone.utc).replace(microsecond=0)
        ) 
    
    if chek:
        await message.answer("✨ ")


    
    await message.answer(f'✨Добро пожаловать, {message.from_user.first_name}!'
                         '\n\n🔸Бот готов к использованию.'
                         '\n🔸Это бот для хранения заметок'
                         '\n🔸Чтобы открыть меню помощи /help', reply_markup=kb.newnote_menu)
    

    

    
    
@router.message(Command("users"))
async def cmd_users(message: Message):
    user_id = message.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    
    if chekadmin:
    
    
        users = await get_all_users()

        if not users:
            await message.answer("Пользователей пока нет.")
            return

        text = "👤 Список пользователей:\n\n"
        for user in users:
            name = user.name or "Без имени"
            username = f"@{user.userId}" if user.userId else "нет username"
            dataReg = user.data
            text += f"• {name} | {username} | userID: {user.tg_id} | Время рег-ии: {dataReg}\n\n"

        await message.answer(text, parse_mode='html')
    else:
        await message.answer("Эта команда вам не доступна...")
    

@router.message(Command("list"))
async def userNote(message: Message):
    notes = await rq.get_my_notes(user_id = message.from_user.id)

    if not notes:
        await message.answer("У вас еще нету заметок")
        return

    text = "📄    Вот список ваших заметок:\n\n\n"
    for note in notes:
        name = note.name
        noteText = note.text
        noteid = note.id
        text += f"<b>• Название заметки: </b> {name} \n<b>Id вашей замтеки:</b> {noteid} \n<b>Текст заметки: </b>\n <pre> {noteText} </pre>\n\n"

    await message.answer(text, reply_markup=kb.newNote_Clearall,parse_mode= 'HTML')
    

@router.callback_query(F.data == "listMenu")
async def userNote(callback: CallbackQuery):
    
    notes = await rq.get_my_notes(user_id = callback.from_user.id)

    if not notes:
        await callback.answer("У вас еще нету заметок...")
        return

    await callback.message.delete() 

    text = "📄    Вот список ваших заметок:\n\n\n"
    for note in notes:
        name = note.name
        noteText = note.text
        noteid = note.id
        text += f"<b>• Название заметки: </b> {name} \n<b>Id вашей замтеки:</b> {noteid} \n<b>Текст заметки: </b>\n <pre> {noteText} </pre>\n\n"

    await callback.message.answer(text,reply_markup=kb.newNote_Clearall,parse_mode= 'HTML')

    
@router.message(Command("giveapanel"))
async def giveapanel(message:Message):
    
    if message.from_user.id != "ADMIN ID":
        await message.reply("У тебя нет прав использовать эту команду.")
        return
    
    args = message.text.split(maxsplit=2)
    
    if len(args) < 3:
        await message.reply("Неверный формат команды. Используй: /apanel <user_id> <Данные>")
        return

    user_id = args[1]
    text = args[2]
    adminTag = 0
    
    if text.lower() in ['+', 'выдать', 'да', 'дать','админ','согласен', 'одобрить']:
        adminTag = 1
    
        extraditon = await rq.giveapanel(
            tg_id = user_id, 
            adminTag=adminTag
            )

        if extraditon: 
             await message.reply("Права обновлены.")
        else:
            await message.reply("Пользователь не найден.")
            
@router.message(Command("send"))
async def send(message: Message):
    user_id = message.from_user.id
    chekrules = await rq.chekAdmin(tg_id = user_id)
    
    if chekrules:
        args1 = message.text.split(maxsplit=2)
        
        if len(args1)<3:
            await message.reply("Неверный формат команды. Используй: /send <user_id> <Текст>")
            return
        
        user_id1 = args1[1]
        text1 = args1[2]
        
        try: 
            await message.bot.send_message(chat_id=user_id1, text= f'📨 У вас новое сообщение от администратора бота: \n\n <i>{text1}</i>', parse_mode='HTML')
        except:
            await message.reply('Не удалось отправить сообщение пользователю...')    
        
    else:
        await message.reply('Эта команда вам не досутпна')
        
        
@router.message(Command("clear"))
async def clear(message: Message):
    await message.answer("Вы действительно хотите удалить все заметки?", reply_markup= kb.delete_menu)
    
    
@router.callback_query(F.data == "deleteAll")
async def clearYes(callback: CallbackQuery):
    
    await callback.message.delete() 
    
    clear = await rq.clearAll(
        id = callback.from_user.id
    )
    
    if clear:
        await callback.message.answer("Ваши заметки успешно удалены!")
    else: 
        await callback.message.answer("Не удалось удалить ваши заметки...")
        
@router.message(Command("delete"))
async def delete(message: Message):
    delmess = message.text.split(maxsplit=2)
    
    if len(delmess) < 2:
        await message.reply("Неверный формат команды. Используй: /delete <id вашей заметки>", reply_markup=kb.list_menu)
        return

    note_id = delmess[1]
    userid = message.from_user.id
    
    dele = await rq.delete(
        userId = userid,
        noteId = note_id
    )
    
    if dele:
        await message.reply("Ваша заметка была успешна удалена.\n Посмотреть список заметок можно с помощью /list", reply_markup=kb.list_menu)
    else:
        await message.reply(f"Не удалось найти заметку с id {note_id} \n Используйте /list чтобы посмтреть ваши заметки", reply_markup=kb.list_menu)
        
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📝 *Бот для заметок*\n\n"
        "Вот список доступных команд:\n\n"
        "/start — приветственное сообщение и инструкция по использованию.\n\n"
        "/newnote — добавить новую заметку. Просто напиши название и текст заметки после команды.\n"
        "Пример: /newnote Купить молоко\n\n"
        "/list — показать все твои заметки.\n\n"
        "/delete — удалить заметку по номеру из списка.\n"
        "Пример: /delete <Id вашей заметки> | (Для удаления надо знать id вашей заметки)\n\n"
        "/edit — изменить текст заметки. "
        "| Будет вызвано меню изменения (Для изменения надо знать id вашей заметки)\n\n"
        "/clear — удалить все заметки сразу (будет запрос подтверждения).\n\n"
        "/help — показать это сообщение с описанием команд.",
        parse_mode="Markdown"
    )   
    
    
    
@router.message(Command("clearall"))
async def clearall(message: Message):
    user_id = message.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    
    if chekadmin:
        purge = await rq.clearall()
        if purge:
            await message.answer("Все заметки были успешно удалены.")
        else:
            await message.answer("Не удалось удалить заметки.")
    else:
        await message.answer("Эта команда вам не доступна...")