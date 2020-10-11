from pyrogram import Client
import json


with open('API.json', 'r') as API:
    API = json.load(API)


app = Client('MyBots',
             API['api_id'],
             API['api_hash'],
             bot_token = API['token'])

BOT = "MyTGbotsBot"

CREATOR = 0000000 # הכנס id יוצר
admins = [CREATOR, 00000000] #רשימת מנהלים


ER = '\n\n********************\n\n'

def log(name, e, m=None):
    try:
        m.reply("משהו נכשל. נסה שוב או שלח זה למפתח:\n`{}`".format(str(e)))
    except:
        pass
    with open('./log.txt', 'a', encoding='utf8') as log:
        log.write(name + '\n' + str(e), ER)

def return_command(m):
    try:
        with open('MSG.json', 'r', encoding='utf-8' ) as msg:
            msg = json.load( msg )
    except Exception as e:
        log('read commands',e,m)
    try:
        for com in msg:
            if com in m.text:
                m.reply( msg[com] )
    except Exception as e:
        log('return commends', e, m)