from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

editName = InlineKeyboardButton(text='✏️ Название заметки', callback_data="editName")
editText = InlineKeyboardButton(text='✏️ Текст заметки', callback_data="editText")
listbtn = InlineKeyboardButton(text='🗓 Список моих заметок', callback_data="listMenu")

yes = InlineKeyboardButton(text='🗑 Очистить список заметок', callback_data="deleteAll")
no = InlineKeyboardButton(text='↩️ Отменить', callback_data="cancel")

newNote = InlineKeyboardButton(text='✏️ Создать новую заметку', callback_data="newNote")

edit_menu = InlineKeyboardMarkup(inline_keyboard=[
    [editName],[editText]
])

delete_menu = InlineKeyboardMarkup(inline_keyboard=[
    [yes],[no]
])

list_menu = InlineKeyboardMarkup(inline_keyboard=[[listbtn]])
newNote_Clearall = InlineKeyboardMarkup(inline_keyboard=[[newNote],
                                                         [yes]])
newnote_menu = InlineKeyboardMarkup(inline_keyboard=[[newNote]])