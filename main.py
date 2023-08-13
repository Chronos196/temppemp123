import keyboards as kb
from message import *
from state import State, CallBack
from imports import *
import admin_keyboard as ak
import admin
import contractor as ct
import sheet
import db
import schedule
from time import sleep
from threading import Thread
import notify

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, ADMIN_START_BOT, reply_markup= ak.ADMIN_KEYBOARD)
    else:
        db.delete_contr(message.chat.id)
        bot.send_message(message.chat.id, CONTRACTOR_START_BOT)



@bot.message_handler(content_types = CONTENT_TYPES)
def fill_form(message):
    id = message.chat.id
    if id == ADMIN_ID:
        admin.admin_message(message)
    else:
        ct.auth_message(message)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    id = call.message.chat.id
    mes_id = call.message.message_id

    if call.data in [CallBack.SEND.value, CallBack.CANCEL.value]:
        try:
            if call.data == CallBack.SEND.value : ct.senf_form(id)
            bot.send_message(id, SEND_DATA if call.data == CallBack.SEND.value else CANCEL_SEND_DATA, reply_markup = kb.START_FILLING)
        except:
             bot.send_message(id, SOMETHING_WRONG, reply_markup= kb.START_FILLING)
        bot.edit_message_reply_markup(id, mes_id, reply_markup=None)
        ct.clear_data(id)
    
    elif call.data.startswith(CallBack.OBJECT.value):
        ct.change_row(id, call.data.split()[1])
        data = sheet.get_all_objects_list()[int(call.data.split()[1])]
        bot.edit_message_text(chat_id=id, message_id=mes_id, text= USER_CHOICE.format(data))

        bot.send_message(id, PEOPLE_SELECT, reply_markup = kb.CANCEL_FILLING)
        ct.get_message(id, data, State.OBJECT.value, State.EQUIPMENT)

    elif call.data in [CallBack.YES.value, CallBack.NO.value]:
        bot.edit_message_reply_markup(id, mes_id, reply_markup=None)
        bot.send_message(id, PHOTO_SELECT, reply_markup= kb.CANCEL_FILLING)
        ct.get_message(id, PLAN_COMPLATE if call.data == CallBack.YES.value else PLAN_NOT_COMPLATE, State.WORK_PLAN.value, State.END)
    
    elif call.data.startswith('token'):
        admin.make_token_for_contractor(call)
    
    elif call.data.startswith('del_obj'):
        admin.delete_row_by_object(call)
    
    bot.answer_callback_query(callback_query_id=call.id)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == '__main__':
    schedule.every().day.at("08:00").do(notify.send_notification)
    Thread(target=schedule_checker).start()
    bot.polling()