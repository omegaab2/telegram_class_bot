from modules.student import *


class AdminSetting(Student):

    def adminSetting(self, msg, call=False):
        txt = 'اختر من الإعدادات'
        markup = types.InlineKeyboardMarkup()

        customUpload = types.InlineKeyboardButton(text="رفع ملفات يدويا", callback_data="StartCustomUpload")

        examSetting = types.InlineKeyboardButton(text="الامتحان", callback_data="ExamSetting")
        homeworkSetting = types.InlineKeyboardButton(text="الواجبات", callback_data="HomeworkSetting")

        subjectSetting = types.InlineKeyboardButton(text="الجدول", callback_data="SubjectTable")
        students = types.InlineKeyboardButton(text="الطلاب", callback_data="Students")
        addLinks = types.InlineKeyboardButton(text="روابط المحاضرات", callback_data="MeetLinks")

        markup.add(downloadFiles, customUpload, examSetting, homeworkSetting,students,
                   subjectSetting, addLinks, self.goBack("Exit", "خروج"), row_width=1)

        if not call:
            self.bot.send_message(text=txt, chat_id=msg.chat.id, reply_markup=markup)

        else:
            self.bot.edit_message_text(text=txt, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=markup)

    def AdminCall(self, call):


        if call.data == "ExamSetting":

            markup = types.InlineKeyboardMarkup()
            addExam = types.InlineKeyboardButton(text="أضافه امتحان", callback_data="addExam")

            deleteExam = types.InlineKeyboardButton(text="حذف الامتحان", callback_data="deleteExam")
            markup.add(deleteExam, addExam, self.goBack("AdminSetting"), row_width=1)

            self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=markup)

        elif call.data == "addExam":
            self.addExam(call.message)

        elif call.data == "SubjectTable":
            markup = types.InlineKeyboardMarkup()

            addSubject = types.InlineKeyboardButton(text="أضافه الى الجدول", callback_data="addSubjectTable")
            deleteSubject = types.InlineKeyboardButton(text="حذف من الجدول", callback_data="deleteSubjectTable")

            markup.add(addSubject, deleteSubject, self.goBack("AdminSetting"), row_width=1)
            self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=markup)

        elif call.data == "MeetLinks":
            markup = types.InlineKeyboardMarkup()

            addLinks = types.InlineKeyboardButton(text="أضافه رابط", callback_data="addMeetLinks")
            editLinks = types.InlineKeyboardButton(text="تعديل رابط", callback_data="editMeetLinks")
            deleteLinks = types.InlineKeyboardButton(text="حذف رابط", callback_data="deleteMeetLinks")

            markup.add(addLinks, editLinks, deleteLinks, self.goBack("AdminSetting"), row_width=1)
            self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=markup)

        elif call.data == "HomeworkSetting":
            markup = types.InlineKeyboardMarkup()
            addHomework = types.InlineKeyboardButton(text="أضافه واجب", callback_data="addHomework")

            deleteHomework = types.InlineKeyboardButton(text="حذف واجب", callback_data="deleteHomework")
            markup.add(deleteHomework, addHomework, self.goBack("AdminSetting"), row_width=1)

            self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=markup)

        elif call.data == "Exit":
            self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        elif call.data == "AdminSetting":
            self.adminSetting(call.message, call=True)

        elif call.data == "Students":
            markup = types.InlineKeyboardMarkup()
            addStudent = types.InlineKeyboardButton(text="أضافه طالب", callback_data="addStudent")
            showStudents = types.InlineKeyboardButton(text="عرض الطلاب", callback_data="showStudents")

            deleteStudent = types.InlineKeyboardButton(text="حذف طالب", callback_data="deleteStudent")
            markup.add(addStudent, showStudents, deleteStudent, self.goBack("AdminSetting"), row_width=1)

            self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       reply_markup=markup)








