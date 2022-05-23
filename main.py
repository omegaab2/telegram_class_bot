# import packages
import threading
import time

from modules import clock
from modules.intreface import Interface, types

# object from interface class
app = Interface()

# threading timers
t1 = threading.Thread(target=clock.examClock, args=(app,))
t1.start()

t2 = threading.Thread(target=clock.meetLinksClock, args=(app,))
t2.start()

t3 = threading.Thread(target=clock.homeworkClock, args=(app,))
t3.start()


# threading calls function
@app.bot.callback_query_handler(func=lambda call: True)
def tcall(call):
    tcall = threading.Thread(target=calls, args=(call,))
    tcall.start()


# calls function it's receive call as parameter
def calls(call):

    print(call.data)
    app.startCall(call)

    app.ExamCall(call)
    app.SubjectCall(call)

    app.InterfaceCall(call)
    app.HomeworkCall(call)

    app.MeetLinksCall(call)
    app.StudentCall(call)

    if call.message.chat.id in app.admins:
        app.AdminCall(call)
        app.CustomUploadMeCall(call)


# start command function...
@app.bot.message_handler(commands=["start"])
def tstart(msg):

    if msg.from_user.id in app.StudentsTeleId or msg.from_user.username in app.StudentsUsers:
        print(msg.from_user.id)

        ts = threading.Thread(target=startInterface, args=(msg,))
        ts.start()

    else:
        txt = f"يريد {msg.from_user.first_name} الانضمام الى البوت معرف الشخص : {msg.from_user.username}"
        markup = types.InlineKeyboardMarkup()

        yes = types.InlineKeyboardButton(text="موافق", callback_data=f"addStudent:{msg.from_user.first_name}:{msg.from_user.id}")
        no = types.InlineKeyboardButton(text="لا", callback_data=f"DeleteMsg")
        markup.add(yes, no)
        
        for adminId in app.admins:
            app.bot.send_message(chat_id=adminId, text=txt, reply_markup=markup)


# interface function...
def startInterface(msg):
    app.StudentInterface(msg)


# this function
@app.bot.message_handler(commands=["all"])
def tag_all(msg):

    if msg.from_user.id in app.StudentsTeleId or msg.from_user.username in app.StudentsUsers:
        stNum, init, ln = 4, 0, len(app.StudentsUsers)

        eq = int(ln / stNum) * stNum
        app.bot.send_message(text=f"this student:\n {msg.from_user.first_name} \nsend this tag", chat_id=msg.chat.id)

        for iuser in range(stNum, eq+1, stNum):
            print(init, iuser, eq)
            app.bot.send_message(text="@"+"\n@".join(app.StudentsUsers[init:iuser]), chat_id=msg.chat.id)

            time.sleep(0.1)
            init += stNum
        print(ln, eq, ln > eq)
        if eq < ln:
            app.bot.send_message(text="@"+"\n@".join(app.StudentsUsers[eq:ln]), chat_id=msg.chat.id)

    else:
        print("shit")
           

@app.bot.message_handler(commands=["id"])
def id_msg(msg):
    app.sendId(msg)


@app.bot.message_handler(commands=["admin"])
def sendAdmin(msg):
    if msg.chat.id in app.admins:
        app.adminSetting(msg)


def listener(messages):  # work same getUpdate() but code shorter and easy to write
    # app.bot.get_chat_member()
    for m in messages:
        M = m
        #pprint(str(m))
        # print(m.from_user.id)


print(50 * "*", "starting", 50 * "*")

while True:
    try:
        # bot.remove_webhook()
        app.bot.set_update_listener(listener)  # refreshTime
        app.bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        app.bot.send_message(chat_id=753033777,text=e)
