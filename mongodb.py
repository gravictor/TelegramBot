from pymongo import MongoClient
from datetime import datetime
from additional.private_data import MONGODB_LINK, admin_chat_id

MONGO_DB = "baza"
mdb = MongoClient(MONGODB_LINK)[MONGO_DB]


def check_and_add_user(message):
    if mdb.users.find_one({'user_id': message.from_user.id}) == None:
        new_user = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_id': message.from_user.id,
            'nickname': message.from_user.username,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'старт'
        }
        mdb.users.insert_one(new_user)
    return


def get_all_users(message):
    if message.from_user.id == admin_chat_id:
        d = mdb.users.find({}, {"first_name": 1, "id": 1, "last_name": 1, "nickname": 1})
        c = "Доступны пользователи: "
        for i in d:
            a = str(i["first_name"] + " " + i["last_name"] + " @"+i["nickname"])
            c += "\n" + a
        return c
    else:
        return "Ти не хитруй, ти не адмін, самозванець!"