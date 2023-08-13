from pymongo import MongoClient
import secrets
import string

cluster = MongoClient('mongodb+srv://rikgogs:U4pQ0cjr9fky7ooM@cluster0.eiptj34.mongodb.net/?retryWrites=true&w=majority')
db = cluster['bot']
users = db['contractors']
admin_data = db['admin']

alphabet = string.ascii_letters + string.digits

def add_new_contr(_id, name):
    if not is_contr_exist(_id):
        users.insert_one(
            {
                '_id': _id,
                'name': name,
            }
        )

def delete_contr(_id):
    if is_contr_exist(_id):
        users.delete_one({'_id' : _id})

def is_contr_exist(_id):
    return bool(users.find_one({'_id': _id}))

def get_contr_by_id(_id):
        return users.find_one({'_id': _id})['name']

def add_new_cand(name):
    if not is_cand_exist(name):
        token = generate_token()
        admin_data.insert_one(
            {
                'name': name,
                'token': token,
            }
        )
        return token
    return False

def is_cand_exist(name):
    return bool(admin_data.find_one({'name': name}))

def is_token_exist(token):
    return bool(admin_data.find_one({'token': token}))

def generate_token():
    while True:
        token = ''.join(secrets.choice(alphabet) for i in range(8))
        if not is_token_exist(token):
            return token
        
def get_cand_by_token(token):
    return admin_data.find_one({'token': token}) if is_token_exist(token) else False

def get_all_users():
    return users.find()

