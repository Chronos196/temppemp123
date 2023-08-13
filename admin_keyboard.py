from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sheet import *

track_number = 'Выдать токен'
new_object = 'Добавить новый объект'
new_contractor = 'Добавить объекту нового подрядчика'
delete_contractor = 'Удалить подрядчика у определенного объекта'
delete_object = 'Удалить объект'

all_buttons = [track_number, new_object, new_contractor, delete_contractor, delete_object]

ADMIN_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    KeyboardButton(new_object),
    KeyboardButton(new_contractor),
    KeyboardButton(delete_contractor),
    KeyboardButton(delete_object),
    KeyboardButton(track_number))

def get_set_contractors_inline():
    contractors_names = get_set_contractors_names()
    contractors_keyboard = InlineKeyboardMarkup()
    contractors_keyboard.add(*[InlineKeyboardButton(i_data, 
                                                    callback_data = "token " + str(ind)) 
                                                    for ind, i_data in enumerate(contractors_names)])
    return contractors_keyboard

def get_set_objects_inline():
    objects_names = get_set_objects_names ()
    objects_keyboard = InlineKeyboardMarkup()
    objects_keyboard.add(*[InlineKeyboardButton(i_data, 
                                                    callback_data = "del_obj " + str(ind)) 
                                                    for ind, i_data in enumerate(objects_names)])
    return objects_keyboard