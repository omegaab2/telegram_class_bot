from telebot import types
import datetime
import time


def examClock(app):

    while True:

        today = datetime.datetime.now().date()
        delta = today + datetime.timedelta(2)

        tm = datetime.datetime.now() - datetime.timedelta(hours=4)
        # print("time :===> ", tm.strftime("%H:%M:%S"))

        if tm.strftime("%H:%M:%S") == "13:10:00":
            exams = app.get("exam", ["*"], "homework=false")

            for i in range(len(exams)):
                if today < exams[i][2] < delta:

                    txt = f'''يوجد امتحان {exams[i][1]} 
    الملاحظات : {exams[i][3]}'''

                    msg = app.bot.send_message(chat_id=-1001433698786, text=txt)
                    app.bot.pin_chat_message(chat_id=-1001433698786, message_id=msg.message_id)

        time.sleep(1)


def meetLinksClock(app):

    while True:

        today = datetime.datetime.now() + datetime.timedelta(hours=2)
        tm = today.strftime("%H:%M:%S")
        day = str(today.strftime("%A"))[:3].lower()
        # print("today: ", today, "tm: ", tm, "day: ", day)

        if day in app.week.keys() and tm in app.times:

            subject_info = app.get("subjects_table", ["en_subject_name"], f"(subject_day='{day}' and subject_time = '{tm}')")

            print(subject_info)
            try:
                link = app.get("meet_links", ["*"], f"en_subject_name='{subject_info[0][0]}'")
            except:
                continue

            if link:

                link = link[0]
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text=link[0], url=link[1], callback_data=f"StartMeet:{link[2]}")
                markup.add(btn)

                txt = f"انظر الى هذه الرسالة التي تحتوي على معاني عميقة جدا لا جذب بس اكو محاضرة {link[0]} هسة"
                app.bot.send_message(text=txt, chat_id=-1001433698786, reply_markup=markup)

        time.sleep(1)


def homeworkClock(app):
    while True:

        today = datetime.datetime.now().date()
        delta = today + datetime.timedelta(2)

        tm = datetime.datetime.now() - datetime.timedelta(hours=4)
        if tm.strftime("%H:%M:%S") == "13:10:00":

            exams = app.get("exam", ["*"], "homework=true")
            for i in range(len(exams)):

                if today < exams[i][2] < delta:
                    txt = f'''يوجد امتحان {exams[i][1]} بعد يومين من الان
        الملاحظات : {exams[i][3]}'''

                    msg = app.bot.send_message(chat_id=-1001433698786, text=txt)
                    app.bot.pin_chat_message(chat_id=-1001433698786, message_id=msg.message_id)

        time.sleep(1)

