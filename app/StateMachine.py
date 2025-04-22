from datetime import datetime


from aiogram import F, Router
from aiogram.types import Message 
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy import select


import app.keyboard as kb 
import app.database.requests as rq

router1 = Router()

class EditName(StatesGroup):
    noteid = State()
    newName = State()
    
    
class ReportMessage(StatesGroup):
    repMess = State()

class EditText(StatesGroup):
    noteid = State()
    newText = State()
    

class NewNote(StatesGroup):
    noteName = State()
    noteText = State()
    
class CategoryStates(StatesGroup):
    waiting_for_name = State()
    

@router1.message(Command("newnote")) # Машина состояния
async def newnote(message: Message, state: FSMContext):
    await state.set_state(NewNote.noteName)
    await message.answer('Укажите название для вашей заметки!')

@router1.callback_query(F.data == "newNote")
async def newnoteCall(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(NewNote.noteName)
    await callback.message.answer('Укажите название для вашей заметки!')
    
    
@router1.callback_query(F.data == "cancel")
async def newnoteCall(callback: CallbackQuery):
    await callback.message.delete()
    
@router1.message(NewNote.noteName)
async def notName(message: Message, state: FSMContext):
    await state.update_data(noteName=message.text)
    await state.set_state(NewNote.noteText)
    await message.answer('Укажите текст для вашей заметки!')
    
@router1.message(NewNote.noteText)
async def notText(message: Message, state: FSMContext):
    usId = message.from_user.id
    await state.update_data(noteText=message.text)
    await message.answer('✅ Ваша заметка успешно сохранена!',reply_markup=kb.list_menu)
    data = await state.get_data()
    # await message.answer(f"Название вашей заметки: {data['noteName']}\nТекст вашей заметки: {data['noteText']}")
    
    
      # Вызов правильной функции
    await rq.create_note(
            user_id= message.from_user.id,
            name=data["noteName"],
            text=data["noteText"],
            # category по умолчанию = 1
        )
    
    await state.clear()
    
    
    

    
@router1.message(Command("edit"))
async def editNote(message: Message, state: FSMContext):
    await message.answer("Выберите пункт, который хотите изменить!", reply_markup=kb.edit_menu)
    


@router1.callback_query(F.data == "editName")
async def choose_a(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы хотите изменить название вашей заметки!\n Сначала укажите ключ вашей заметки")
    await state.set_state(EditName.noteid)
    await callback.answer()

@router1.callback_query(F.data == "editText")
async def choose_a(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы хотите изменить текст вашей заметки!\n Сначала укажите ключ вашей заметки")
    await state.set_state(EditText.noteid)
    await callback.answer()
    
    
    
    
    
@router1.message(EditName.noteid)
async def handle_id(message: Message, state: FSMContext):
    await state.update_data(noteid=message.text)
    await state.set_state(EditName.newName)
    await message.answer('Укажите новое название для вашей заметки!')
    
@router1.message(EditName.newName)
async def handle_newNotetext(message: Message, state: FSMContext):
    await state.update_data(newName=message.text)
    dat = await state.get_data()
    # await message.answer(f"Название вашей заметки: {data['noteName']}\nТекст вашей заметки: {data['noteText']}")

    user = message.from_user.id

        # Вызов правильной функции
    test = await rq.changeNoteName(
            userId = message.from_user.id,
            id=dat["noteid"],
            name=dat["newName"],
            # category по умолчанию = 1
        )
    
    if test:
        await message.answer('✅ Ваша заметка успешно изменена! \n Посмотреть все заметки: /list')
    else: 
        await message.answer(' Не удалось изменить вашу заметку... \n Посмотреть id вашей заметки можно, с помощью /list')        

    await state.clear()
    
    
    
@router1.message(EditText.noteid)
async def handle_id(message: Message, state: FSMContext):
    await state.update_data(noteid=message.text)
    await state.set_state(EditText.newText)
    await message.answer('Укажите новый текст для вашей заметки!')
    
@router1.message(EditText.newText)
async def handle_newNotetext(message: Message, state: FSMContext):
    await state.update_data(newText=message.text)
    dat = await state.get_data()
    # await message.answer(f"Название вашей заметки: {data['noteName']}\nТекст вашей заметки: {data['noteText']}")

    user = message.from_user.id

        # Вызов правильной функции
    test = await rq.changeNoteText(
            userId = message.from_user.id,
            id=dat["noteid"],
            ntext=dat["newText"],
            # category по умолчанию = 1
        )
    
    if test:
        await message.answer('✅ Ваша заметка успешно изменена! \n Посмотреть все заметки: /list')
    else: 
        await message.answer(' Не удалось изменить вашу заметку... \n Посмотреть id вашей заметки можно, с помощью /list')        

    await state.clear()

    
    
    
    
@router1.message(Command("newcategory"))
async def cmd_new_category(message: Message, state: FSMContext):
    await message.answer("Введите название новой категории:")
    await state.set_state(CategoryStates.waiting_for_name)
    
@router1.message(CategoryStates.waiting_for_name)
async def add_category(message: Message, state: FSMContext):
    name = message.text.strip()

    await rq.new_category(name) 
    await message.answer(f"Категория '{name}' добавлена ✅")
    await state.clear()
    
    
@router1.message(Command("report"))
async def reportMessage(message: Message, state: FSMContext):
    await message.answer("Введите текст, который хотите отправить админу!")
    await state.set_state(ReportMessage.repMess)
    
    
@router1.message(ReportMessage.repMess)
async def handle_newNotetext(message: Message, state: FSMContext):
    await state.update_data(repMess=message.text)
    
    data = await state.get_data()

    text1 = data["repMess"]
    
    await message.bot.send_message(chat_id="ADMIN ID", text=text1)
    await state.clear()
