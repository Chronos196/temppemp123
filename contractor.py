from imports import *
from db import *
import keyboards as kb
from message import *
from state import State
from datetime import datetime


user_state = {}
user_data = {}
user_row = {}

def auth_message(message):
    id = message.chat.id
    text = message.text

    if not is_contr_exist(id):
        result = get_cand_by_token(text)
        if result == False:
            bot.send_message(id, WRONG_TOKEN)
        else:
            contr_name = result['name']
            add_new_contr(id, contr_name)
            bot.send_message(id, SUCCESSFUL_AUTH.format(contr_name), reply_markup= kb.START_FILLING)
            user_data[message.chat.id] = {}
    else:
        contractor_message(message)


def contractor_message(message):
    id = message.chat.id
    if message.text == kb.start_filling:
        bot.send_message(id, START_FILL_FORM, reply_markup= kb.CANCEL_FILLING)
        user_state[id] = State.OBJECT
        user_data[id] = {}
        user_data[id][State.CONTRACTOR.value] = get_contr_by_id(id)
    elif message.text == kb.cancel_filling:
        bot.send_message(message.chat.id, CANCEL_FILL_FORM, reply_markup= kb.START_FILLING)
        user_state[id], user_data[id], user_row[id] = None, None, None
        return
    match user_state.get(message.chat.id):
            case State.OBJECT:
                bot.send_message(id, OBJECT_SELECT, reply_markup= kb.get_objects_list_by_contr_name(user_data[id][State.CONTRACTOR.value], client, spreadsheet_id))
                user_state[id] = State.PEOPLE
            case State.EQUIPMENT:
                bot.send_message(id, EQUIPMENT_SELECT, reply_markup= kb.CANCEL_FILLING)
                get_message(id, message.text, State.PEOPLE.value, State.REPORT_DATE)
            case State.REPORT_DATE:
                bot.send_message(id, REPORT_DATE_SELECT, reply_markup= kb.CANCEL_FILLING)
                get_message(id, message.text, State.EQUIPMENT.value, State.NOTES)
            case State.NOTES:
                bot.send_message(id, NOTES_SELECT, reply_markup = kb.CANCEL_FILLING)
                get_message(id, message.text, State.REPORT_DATE.value, State.WORK_PLAN)
            case State.WORK_PLAN:
                bot.send_message(id, PLAN_SELECT, reply_markup= kb.PLAN_CHOICE)
                get_message(id, message.text, State.NOTES.value, State.END)
            case State.END:
                try:
                    user_data[id][State.WORK_PLAN.value]
                    bot.send_message(str(ADMIN_ID), PHOTO_TEXT.format(user_data[id][State.CONTRACTOR.value],user_data[id][State.OBJECT.value]))
                    bot.forward_message(str(ADMIN_ID), message.chat.id, message.message_id)
                    get_final_data(id)
                except:
                    bot.send_message(id, WORK_PLAN_NO_SELECT, reply_markup= kb.CANCEL_FILLING)
            case _:
                bot.send_message(id, WRONG_COMAND)

def get_message(_id, user_message, cur_key, state):
    user_data[_id][cur_key] = user_message
    user_state[_id] = state

def get_final_data(id):
    data_array = [
        f"<b>Объект:</b> {user_data[id][State.OBJECT.value]}",
        f"<b>Подрядчик:</b> {user_data[id][State.CONTRACTOR.value]}",
        f"<b>Количество людей:</b> {user_data[id][State.PEOPLE.value]}",
        f"<b>Информация о спецтехнике:</b> {user_data[id][State.EQUIPMENT.value]}",
        f"<b>План работы на отчетную дату:</b> {user_data[id][State.REPORT_DATE.value]}",
        f"<b>Примечания/проблемы:</b> {user_data[id][State.NOTES.value]}",
        f"<b>Выполнение плана за предыдущий день:</b> {user_data[id][State.WORK_PLAN.value]}",
    ]
    bot.send_message(id, DATA_GENERATE.format('\n'.join(data_array)), reply_markup= kb.FINAL_CHOICE)


def senf_form(_id):
    worksheet = client.open_by_key(spreadsheet_id).sheet1
    worksheet.update(f'D{int(user_row[_id]) + 1}', user_data[_id][State.PEOPLE.value])
    worksheet.update(f'E{int(user_row[_id]) + 1}', user_data[_id][State.PEOPLE.value])
    worksheet.update(f'I{int(user_row[_id]) + 1}', user_data[_id][State.EQUIPMENT.value])
    worksheet.update(f'J{int(user_row[_id]) + 1}', user_data[_id][State.EQUIPMENT.value])
    worksheet.update(f'M{int(user_row[_id]) + 1}', user_data[_id][State.WORK_PLAN.value])
    worksheet.update(f'P{int(user_row[_id]) + 1}', user_data[_id][State.NOTES.value])
    worksheet.update(f'L{int(user_row[_id]) + 1}', user_data[_id][State.REPORT_DATE.value])
    worksheet.update(f'S{int(user_row[_id]) + 1}', datetime.now().strftime("%Y-%m-%d %H:%M"))

def clear_data(id):
    user_state[id], user_data[id], user_row[id] = None, None, None

def change_row(id, new_row):
    user_row[id] = new_row