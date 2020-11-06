from db import db
from enum import IntEnum


class UserDialog(IntEnum):
    NO_DIALOG = 0
    ASK_FOR_PROBLEM = 1,
    CONFIGURE_HANDLE = 2,


class AskForProblemDialog(IntEnum):
    START = 0,
    LOWER_DF = 1,
    UPPER_DF = 2,
    EXCLUDE_SOLVED = 3,
    INLINE_HANDLE_CONFIG = 4,
    TAGS = 5,
    QUANTITY = 6


class ConfigureHandleDialog(IntEnum):
    START = 0,
    SEND_HANDLE = 1


userdata = {}


def save_udata(uid):
    ref = db.collection('userdata').document(str(uid))
    try:
        ref.set(userdata[str(uid)])
    except:
        print("Database error")
        return


def load_udata(uid):
    doc = db.collection('userdata').document(str(uid)).get()
    if not doc.exists:
        try:
            doc = db.collection('userdata').document(str(uid)).create(init_udata())
        except:
            print('Database creation error')
        doc = db.collection('userdata').document(str(uid)).get()
    userdata[str(uid)] = doc.to_dict()


def get_udata(uid):
    if str(uid) not in userdata:
        load_udata(uid)
    return userdata[str(uid)]


def set_udata(uid, _data):
    userdata[str(uid)] = _data


def update_dialog(uid, dialog):
    userdata[str(uid)]['dialog'] = dialog
    update_dialog_state(uid, 0)


def update_dialog_state(uid, dialog_state):
    userdata[str(uid)]['dialog_state'] = dialog_state


def put_into_cache(uid, field, data):
    userdata[str(uid)]['cache'][field] = data


def get_cache(uid):
    return userdata[str(uid)]['cache']


def clear_cache(uid):
    userdata[str(uid)]['cache'] = {}


def change_handle(uid, handle):
    userdata[str(uid)]['handle'] = handle
    save_udata(uid)


def get_handle(uid):
    return userdata[str(uid)]['handle']


def init_udata():
    return {
        'dialog': UserDialog.NO_DIALOG,
        'dialog_state': 0,
        'cache': {},
        'handle': None
    }


def init_load():
    ref = db.collection('userdata')
    for doc_ref in ref.get():
        try:
            userdata[str(doc_ref.id)] = doc_ref.to_dict()
            update_dialog(str(doc_ref.id), 0)
        except:
            continue
    print(userdata)