from datetime import datetime
from modules.start import *


class Exam(START):

    def __init__(self):
        super().__init__()
        self.subjects = self.get("subject", ["subject_name", "en_subject_name"])

    def addExam(self, msg):
        markup = types.InlineKeyboardMarkup()

        for subject in self.subjects:
            button = types.InlineKeyboardButton(text=subject[0], callback_data=f"addExam:subject:{subject[0]}:{subject[1]}")
            markup.add(button)

        self.bot.edit_message_text(text="اختر المادة",
                                   message_id=msg.message_id,
                                   chat_id=msg.chat.id,
                                   reply_markup=markup)

    def ExamCall(self, call):

        if call.message.chat.id in self.admins:
            if "addExam:subject" in call.data:

                self.__subject_name = call.data.split(":")[2]
                self.__en_subject_name = call.data.split(":")[3]
                markup = types.InlineKeyboardMarkup()

                for i in range(1, 13, 2):
                    btn1 = types.InlineKeyboardButton(text=f"{i}", callback_data=f"addExam:month:{i}")
                    btn2 = types.InlineKeyboardButton(text=f"{i+1}", callback_data=f"addExam:month:{i+1}")
                    markup.add(btn1, btn2, row_width=2)

                self.bot.edit_message_text(text="اختر الشهر :",
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           reply_markup=markup)

            elif "addExam:month" in call.data:

                self.__month = call.data.split(":")[2]

                markup = types.InlineKeyboardMarkup()

                for i in range(1, 32, 3):
                    if i != 31:
                        btn1 = types.InlineKeyboardButton(text=f"{i}", callback_data=f"addExam:day:{i}")
                        btn2 = types.InlineKeyboardButton(text=f"{i+1}", callback_data=f"addExam:day:{i+1}")
                        btn3 = types.InlineKeyboardButton(text=f"{i+2}", callback_data=f"addExam:day:{i+2}")
                        markup.add(btn1, btn2, btn3, row_width=3)
                    else:
                        btn1 = types.InlineKeyboardButton(text=f"{i}", callback_data=f"addExam:day:{i}")
                        markup.add(btn1)

                self.bot.edit_message_text(text="اختر اليوم :",
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           reply_markup=markup)

            elif "addExam:day" in call.data:
                self.__day = call.data.split(":")[2]

                self.bot.edit_message_text(text="ادخل الملاحظات :",
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
                self.bot.register_for_reply_by_message_id(message_id=call.message.message_id,
                                                          callback=lambda msg : self.saveExam(msg))

            elif call.data == "deleteExam":
                txt = self.showExams() + "\n\n\n" + "ادخل id الامتحان(رد على الرسالة)"
                self.bot.edit_message_text(text=txt, chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
                self.bot.register_for_reply_by_message_id(message_id=call.message.message_id,
                                                          callback=lambda msg: self.deleteExam(msg))
            elif call.data == "showExams":

                self.showExams(call)

        elif call.data == "showExams":
            self.showExams(call)

        elif call.data == "Exit":
            self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    def saveExam(self, msg):

        if len(self.__day) == 1:
            self.day = f"0{self.__day}"

        if len(self.__month) == 1:
            self.month = f"0{self.__month}"

        year = datetime.now().year
        if datetime.now().month > int(self.__month):
            year += 1

        date = f"{year}-{self.__month}-{self.__day}"

        print("date", date)
        self.insert("exam", ["subject_name", "exam_date", "exam_note", "en_subject_name"],
                            [self.__subject_name, date, msg.text, self.__en_subject_name])

        self.bot.send_message(chat_id=msg.chat.id, text="تم إضافة الامتحان بنجاح")
        self.showExams(msg=msg)

    def showExams(self, call=False, msg=False):
        exams = self.get("exam", ["*"], "homework=false")
        form = ""

        if exams:
            for exam in exams:
                form += f'''🔥😳🔥😳🔥🔥😳🔥😳
التسلسل: {exam[0]}
 اسم المادة:{exam[1]}\n
التاريخ : {exam[2]}\n
الملاحظات : {exam[3]}\n🔥😳🔥😳🔥🔥😳🔥😳\n\n'''
            if call:
                self.bot.send_message(text=form, chat_id=call.message.chat.id)
            elif msg:
                self.bot.send_message(text=form, chat_id=msg.chat.id)

        else:
            if call:
                self.bot.send_message(text="لا توجد امتحانات", chat_id=call.message.chat.id)
            elif msg:
                self.bot.send_message(text="لا توجد امتحانات", chat_id=msg.chat.id)

        return form

    def deleteExam(self, msg):

        try :
            self.delete("exam", f"(exam_id = {msg.text} and homework=false)")
            self.bot.send_message(chat_id=msg.chat.id,
                                  text="تم حذف الامتحان بنجاح")

        except:
            self.bot.send_message(chat_id=msg.chat.id,
                                  text="error in delete exam")










