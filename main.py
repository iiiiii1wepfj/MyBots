import json
from pyrogram import filters, types
from pyrogram.types import *

from MyBots.MyBots.bot import Client
from MyBots.MyBots.bot.Client import log, return_command, CREATOR, admins
from MyBots.MyBots.bot.msg import *

# ----------------הגדרות פיירוגרם----------------
app = Client.app

disable_web_page_preview = True  # תצוגה מקדימה של קישורים. אם ברצונכם שתפעל - החליפו את /True/ ב /False/
parse_mode = "md"  # פורמט טקסט = Marksown
resize_keyboard = True

bot = Client.BOT
#--------------------מנהלים---------------------


# -----------------הודעת פתיחה-------------------
@app.on_message(filters.command('start'))
def start_func(c, m):
    fid, fnm  = '' , ''
    # שמירת משתמש
    try:
        fid = m.from_user.id
        fnm = m.from_user.first_name
        with open( 'members.json', 'r', encoding='utf8' ) as Jmembers:
            members = json.load( Jmembers )
        if fid not in members:
            members[str( fid )] = fnm
            members = json.dumps( members )
            with open( 'members.json', 'w', encoding='utf8' ) as mem2:
                mem2.write( members )
    except Exception as e:
        log( 'save member', e, m )
    # הודעת ברוכים הבאים
    if len( m.text ) == 6:

        if fid in admins:
            m.reply( START_MESSAGE.format( fnm, fid )
                     , reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton( "רשימת הפקודות", callback_data='list' )]] ) )
        else:
            m.reply( START_USER.format( fnm, fid, bot )
                     , reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton( "רשימת הפקודות", callback_data='list' )]] ) )

    # פקודות /start אחרות
    else:
        try:
            start = m.text.strip( '/start ' )
            if start == "md":
                m.reply( MARKDOWN, disable_web_page_preview=False )
            if start == "info":
                pass
            if m.text == "/start format":
                m.reply( HELP_COMMANSD )
        except Exception as e:
            m.reply( "אירעה שגיאה. שלח זה למפתח:\n`{}`".format( str( e ) ) )
            log( 'deep link', e, m )


# -----------------------תפריט עזרה------------------
@app.on_message(filters.command('עזרה') & filters.chat(admins))
def help_func(c, m):
    try:
        m.reply( HELP, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton( "הוספת פקודות", callback_data='adds' )]] ) )
    except Exception as e:
        log( 'help user', e, m )

# -----------------ניהול משתמשים----------------
@app.on_message(filters.chat(admins) & filters.command('משתמשים'))
def get_members(c, m):
    try:
        with open( './members.json', 'r' ) as members_j:
            members = json.load( members_j )
            list_members = ""
            for member in members:
                list_members += f'✅ [{members[member]}](tg://user?id={member})\n'
            m.reply( '**רשימת המשתמשים**' + list_members )
    except Exception as e:
        log( 'iter members', e, m )

#-------------------ניהול מנהלים--------------------
@app.on_message(filters.chat(CREATOR) & filters.command('הוסף מנהל'))
def add_admin(c,m):
    admin = m.text[10:].strip()
    if len(admin):
        print(admins)
        if admin not in admins:
            with open('./admins.json', 'w') as add:
                add = json.dumps(admins + [int(admin)])
            m.reply("המנהל נוסף בהצלחה.\nרשימת המנהלים: {}".format(admins))

# ------------------בדיקת סטטוס------------------
@app.on_message(filters.command( 'סטטוס' ) & filters.chat( admins ))
def chekc_status(c, m):
    if stat == 1:
        m.reply( 'אתה בתפריט ניהול' )
    elif stat == 0:
        m.reply( 'אתה בתפריט משתמש' )

# --------------------כניסה לתפריט ניהול-----------------
stat = 0
admin_commands = ['ניהול', "סגור תפריט ניהול"]
start_admin = '/' + admin_commands[0]
stop_admin = '/' + admin_commands[1]


@app.on_message( filters.chat( admins ) & filters.command( admin_commands ) )
def admin_stat(c, m):
    global stat

    if m.text == start_admin:
        if stat == 0:
            try:
                m.reply( "אתה בתפריט ניהול", reply_markup=ReplyKeyboardMarkup( [
                    [KeyboardButton( 'הוספת פקודה' )],
                    [KeyboardButton( stop_admin )]], resize_keyboard=True ) )
                stat = 1
            except Exception as e:
                m.reply( f"אירעה שגיאה. נסה להכנס מחדש לתפריט ניהול.\n`{str( e )}`" )
                log( 'menu admin', e, m )
    if m.text == stop_admin:
        if stat == 1:
            m.reply( "יצאת מתפריט ניהול", reply_markup=ReplyKeyboardRemove() )
            stat = 0

# -----------------תפריט הוספת פקודות--------------------
@app.on_message( filters.chat( admins ) )
def add_commands(c, m):
    try:
        with open( './MSG.json', 'r', encoding='utf8' ) as MSG_old:
            MSG = json.load( MSG_old )
    except:
        try:
            with open( './MSG.json', 'w', encoding='utf8' ) as first:
                first.write('{"קרדיט":"מקליד תמיד"}')
        except Exception as e:
            log( 'load hold commends', e, m )
    text = f"שלח את הטקסט בפורמט פקודה. לקריאה מפורטת [לחץ כאן](http://t.me/{bot}?start=format)"
    if stat == 1:
        if m.text == "הוספת פקודה":
            m.reply( text, reply_markup=types.ForceReply() )
        if m.reply_to_message:
            try:
                if m['reply_to_message']['text'] == text:
                    text_commend = m.text.split( "\n" )
                    if len( text_commend ) == 2:
                        command = text_commend[0]
                        comment = text_commend[1]
                        if command in MSG:
                            m.reply( "הפקודה קיימת כבר.\nהשיבו על ההודעה הקודמת שלי עם פקודה חדשה." )
                        else:
                            try:
                                MSG[comment] = comment
                                MSG = json.dumps( MSG )
                                try:
                                    with open( './MSG.json', 'w', encoding='utf8' ) as MSG_NEW:
                                        MSG_NEW.write( str( MSG ) )
                                except Exception as e:
                                    log( 'save command', e, m )
                                m.reply( "מעולה! נשמרה פקודה חדשה."
                                         f"שם הפקודה: **{command}**. תגובה: **{comment}**" )
                            except Exception as e:
                                log( 'sub add command', e, m )
                    else:
                        m.reply( "מצטערים, לא הוספתם פקודה תקינה. שלחו /עזרה להסבר על פורמט הפקודה" )
            except Exception as e:
                log( 'super add comman', e, m )

    # הצגת פקודות רגילה למנהלים
    else:
        return_command( m )


# --------------פקודות לכל המשתמשים----------------
@app.on_message()
def commands_func(c, m):
    return_command( m )


# -----------------callback_query---------------
@app.on_callback_query()
def list_commends(client, callback_query):
    cald = callback_query.data
    if cald == 'list':
        try:
            list_text = "**רשימת הפקודות:**\n"
            try:
                with open( 'MSG.json', 'r', encoding='utf-8' ) as list_j:
                    list_p = json.load( list_j )
            except Exception as e:
                log( 'open callback list', e, callback_query )
            for key in list_p:
                list_text += '💠' + key + '\n'
            callback_query.edit_message_text( list_text )
        except Exception as e:
            log( 'callback list', e, callback_query )
    if cald == 'adds':
        try:
            callback_query.edit_message_text( HELP_COMMANSD.format( bot ) )
        except Exception as e:
            log( 'callback help', e, callback_query )


# ---------------------------------------------------------------------------------
app.run()

