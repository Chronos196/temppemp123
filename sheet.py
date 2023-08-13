from main import spreadsheet_id, client

worksheet = client.open_by_key(spreadsheet_id).sheet1

def get_set_contractor_name_by_number(number):
    contractors = get_set_contractors_names()
    return contractors[number]

def get_set_contractors_names():
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    result = []
    contractors = [i for i in worksheet.col_values(3) if i != '' and i != 'Подрядчик']
    for i in contractors:
        if i not in result:
            result.append(i)
    return result

def get_set_objects_names():
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    result = []
    objects = [i for i in worksheet.col_values(2) if i != '' and i != 'Объект Строительства/реконструкции/ремонта']
    for i in objects:
        if i not in result:
            result.append(i)
    return objects

def fill_new_object(object_name, contractor_name):
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    empty_row = len(worksheet.get_all_values()) + 1
    worksheet.update(f'B{empty_row}', object_name)
    worksheet.update(f'C{empty_row}', contractor_name)

def delete_object_by_number(object_number):
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    object_name = get_set_objects_names()[object_number]
    obj_data = worksheet.col_values(2)
    for i in range(1,len(obj_data)):
        if obj_data[i] == '':
            obj_data[i] = obj_data[i - 1]
    rows_index = [j + 1 for j in range(len(obj_data)) if obj_data[j] == object_name]
    worksheet.delete_rows(rows_index[0], rows_index[-1])

def get_all_objects_list():
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    obj_data = worksheet.col_values(2)
    for i in range(1,len(obj_data)):
        if obj_data[i] == '':
            obj_data[i] = obj_data[i - 1]
    return obj_data


def get_all_contractors_list():
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    con_data = worksheet.col_values(3)
    return con_data

def get_value_by_cell(col, row):
    # worksheet = client.open_by_key(spreadsheet_id).sheet1
    return worksheet.acell(f'{col}{row}').value