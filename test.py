import requests
import json

BASE = "http://127.0.0.1:5000/"

def join_ep(ep):
    return BASE + ep


def initdb():
    print('#################### initdb ####################')
    r = requests.get(join_ep('initdb'))
    print(r.status_code)
    print(r.json())
    return r.json()

def register():
    print('#################### register ####################')
    r = requests.post(join_ep('register'), {
        "username": 'user',
        "password": 'aaa'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def login():
    print('#################### login ####################')
    r = requests.post(join_ep('login'), {
        "username": 'user',
        "password": 'aaa'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def notes_list(token):
    print('#################### notes list ####################')
    r = requests.get(join_ep('notes'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def notes_create(token):
    print('#################### notes create ####################')
    r = requests.post(join_ep('notes'), {
        'title': 'Test note',
        'body': 'Some note body'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def note_get(token, id):
    print('#################### note get ####################')
    r = requests.get(join_ep(f'note/{id}'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def note_del(token, id):
    print('#################### note del ####################')
    r = requests.delete(join_ep(f'note/{id}'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def note_put(token, id):
    print('#################### note put ####################')
    r = requests.put(join_ep(f'note/{id}'), {
        'title': 'New title',
        'body': 'New body'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def refresh(token):
    print('#################### refresh ####################')
    r = requests.post(join_ep('refresh'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def otp_list(token):
    print('#################### OTP list ####################')
    r = requests.get(join_ep('otp'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def otp_get_one(token, id):
    print('#################### OTP get one ####################')
    r = requests.get(join_ep(f'otp/{id}'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def otp_add(token):
    print('#################### OTP add ####################')
    r = requests.put(join_ep('otp'), {
        'name': 'andrej.paskalev@gmail.com',
        'issuer': 'google',
        'secret': 'sjy3rq4zyjhwzfpuomikxdpmyw52zr3l'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

def otp_remove(token, id):
    print('#################### OTP remove ####################')
    r = requests.delete(join_ep(f'otp/{id}'), headers={
        'Authorization': f'Bearer {token}'
    })
    print(r.status_code)
    print(r.json())
    return r.json()

initdb()
register()
login = login()
token = login['data']['access']
new_note = notes_create(token)
note_get(token, new_note['data']['id'])
note_put(token, new_note['data']['id'])
note_put(token, 'random id')
note_del(token, new_note['data']['id'])
note_del(token, 'random id')
notes_list(token)
new_otp = otp_add(token)
otp_get_one(token, new_otp['data']['id'])
otp_list(token)
otp_remove(token, new_otp['data']['id'])
otp_list(token)
refresh(login['data']['refresh'])

