from imports import bot, ADMIN_ID
from db import *
import sheet
import admin_keyboard as ak

id = str(ADMIN_ID)

def admin_message(message):
    match message.text:
        case ak.track_number:
            bot.send_message(id, "Выберете из предложеных подрядчиков, того, кому хотите сгенерировать трек номер:", 
                             reply_markup= ak.get_set_contractors_inline())
        case ak.new_object:
            bot.send_message(id, "Введите название нового объекта:")
            bot.register_next_step_handler(message, get_new_object)

        case ak.delete_object:
            bot.send_message(id, 'Выберете объект, который вы хотите удалить:', 
                             reply_markup=ak.get_set_objects_inline())

def get_new_object(message):
    if message.text in ak.all_buttons:
        admin_message(message)
        return
    objects_names = sheet.get_set_objects_names()
    if message.text in objects_names:
        bot.send_message(id, "Данный объект уже есть в таблице")
        return
    bot.send_message(id, "Введите название подрядчика:")
    bot.register_next_step_handler(message, get_new_contractor, message.text)

def get_new_contractor(message, *kwargs):
    if message.text in ak.all_buttons:
        admin_message(message)
        return
    sheet.fill_new_object(str(*kwargs), message.text)
    bot.send_message(id, f'Новая строка со следующей информацией\nобъект - {str(*kwargs)}\nподрядчиком {message.text}\nБыла занесена в таблицу')


def make_token_for_contractor(call):
    cand_number = int(call.data.split()[1])
    cand_name = sheet.get_set_contractor_name_by_number(cand_number)
    mes_id = call.message.message_id
    result = add_new_cand(cand_name)
    bot.edit_message_reply_markup(id, mes_id, reply_markup=None)
    if result:
        bot.send_message(id, f'Токен для подрядчика {cand_name} - {result}')
    else:
        bot.send_message(id, f"Для подрядчика {cand_name} уже был выдан трек номер")
    bot.answer_callback_query(callback_query_id=call.id)

def delete_row_by_object(call):
    obj_number = int(call.data.split()[1])
    mes_id = call.message.message_id
    sheet.delete_object_by_number(obj_number)
    bot.edit_message_reply_markup(id, mes_id, reply_markup=None)
    bot.send_message(id, f"Объект был удален из таблицы")