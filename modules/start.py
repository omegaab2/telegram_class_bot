from modules.room import *


class START(OmegaRoom):

    def __init__(self):
        super().__init__()
        self.courses = self.getCourses(12)

        self.SUBJECTS = self.get("subject", ["subject_name", "en_subject_name"])
        self.dataTimes = self.get("subjects_table", ["subject_time"], group_by="subject_time")

        for s in range(len(self.dataTimes)):
            self.dataTimes[s] = self.dataTimes[s][0]

        self.week = {"sun": "الأحد", 'mon': "الاثنين", 'tue': "الثلاثاء", 'wed': "الأربعاء", 'thu': "الخميس"}
        self.days = list(self.week.keys())
        self.times = ["08:30", "10:30", "11:30", "12:30", "another"]

        self.STAGE = 'third'
        self.links = self.get("meet_links", ["*"])
        self.getAdminsTeleId()
        self.StudentsTeleId = self.getStudentsTeleId()
        self.StudentsUsers = self.getStudentsUsers()

    def getStudentsTeleId(self):
        var = self.get("student", ["tele_id"])
        for teleId in range(len(var)):
            var[teleId] = var[teleId][0]

        return var

    def getStudentsUsers(self):
        var = self.get("student", ["tele_user"], condition=f"tele_user is not null")
        r = len(var)

        for teleUser in range(r):
                var[teleUser] = var[teleUser][0]
        return var

    def getAdminsTeleId(self):
        self.admins = self.get("admin", ["tele_id"])

        for teleId in range(len(self.admins)):
            self.admins[teleId] = self.admins[teleId][0]

        return self.admins

    def sendId(self, msg):
        txt = f"الرقم التعريفي الخاص بك هو {msg.chat.id}"
        message = self.bot.send_message(chat_id=msg.chat.id,
                             text=txt)

        print("message id :", message.message_id)

    def send_courses(self, msg):

        markup = types.InlineKeyboardMarkup()

        for index in range(1, len(self.courses)):
            button = types.InlineKeyboardButton(text=self.courses[index]['name'],
                                                callback_data=f"getCourses:{index}")
            markup.add(button)

        markup.add(self.goBack("StartStudent"))

        self.bot.edit_message_text(chat_id=msg.chat.id,
                                   message_id=msg.message_id,
                                   text="اختر المادة الدراسية",
                                   reply_markup=markup)

    def startCall(self, call):

        if "getCourses" in call.data:
            courseIndex = call.data.split(":")[1]
            works = self.get("clscontent", ["*"], condition=f"(class_name='{self.courses[int(courseIndex)]['name']}' and stage = '{self.STAGE}')", order="post_id")

            if works:
                markup = types.InlineKeyboardMarkup()
                for index in range(len(works)):
                    button = types.InlineKeyboardButton(text=works[index][2],
                                                        callback_data=f"getWorks:{works[index][0]}")
                    markup.add(button)
                markup.add(self.goBack("StartStudent"))

                self.bot.edit_message_text(text="اختر الملف الذي تريده",
                                           message_id= call.message.message_id,
                                           chat_id=call.message.chat.id,
                                           reply_markup=markup)
            else:
                self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           text="there is no files here")

        elif "getWorks" in call.data:
            msg_id = int(call.data.split(':')[1])

            try :

                self.bot.forward_message(chat_id=call.message.chat.id,
                                         from_chat_id=-605543900,
                                         message_id=msg_id)
            except:
                self.bot.forward_message(chat_id=call.message.chat.id,
                                         from_chat_id=-1001670074369,
                                         message_id=msg_id)

        elif call.data == "sendCourses":
            self.send_courses(call.message)

    def goBack(self, callback, txt="رجوع"):
        btn = types.InlineKeyboardButton(text=txt, callback_data=callback)
        return btn

