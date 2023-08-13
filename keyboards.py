from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import sheet

start_filling = 'Внести данные'
cancel_filling = 'Отмена'

final_choice_yes = InlineKeyboardButton(text = 'Да', callback_data = "send")
final_choice_no = InlineKeyboardButton(text = 'Нет', callback_data = "cancel")

plan_choice_yes = InlineKeyboardButton(text = '✅', callback_data = "yes")
plan_choice_no = InlineKeyboardButton(text = '❌', callback_data = "no")

START_FILLING = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton(start_filling))

CANCEL_FILLING = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton(cancel_filling))

FINAL_CHOICE = InlineKeyboardMarkup(row_width = 2).add(final_choice_yes, final_choice_no)

PLAN_CHOICE = InlineKeyboardMarkup(row_width = 2).add(plan_choice_yes, plan_choice_no)

def get_objects_list_by_contr_name(contr_name, client, spreadsheet_id):
    con_keyboard = InlineKeyboardMarkup(row_width= 1)
    obj_data = sheet.get_all_objects_list()
    con_data = sheet.get_all_contractors_list()
    for i in range(len(obj_data)):
        try:
            if con_data[i] == contr_name:
                con_keyboard.add(InlineKeyboardButton(obj_data[i], callback_data="obj " + str(i)))
        except:
            continue
    return con_keyboard