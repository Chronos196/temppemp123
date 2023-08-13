from imports import *
import sheet
import db
from datetime import datetime

def send_notification():
    print('dvdfvdvdfvdfv')
    obj_data = sheet.get_all_objects_list()
    con_data = sheet.get_all_contractors_list()
    for i_user in db.get_all_users():
        notify_objects = []
        for ind in range(len(con_data)):
            if i_user['name'] == con_data[ind]:
                fill_date = sheet.get_value_by_cell('S', ind + 1)
                try:
                    timedelta = datetime.now() - datetime.strptime(fill_date, "%Y-%m-%d %H:%M")
                    if timedelta.days > 0:
                        notify_objects.append(obj_data[ind])
                except:
                    notify_objects.append(obj_data[ind])
        if len(notify_objects):
            bot.send_message(str(i_user['_id']), "Не забудьте заполнить данные по следующим объектам\n" + '\n'.join(notify_objects))