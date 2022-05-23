from modules.admin_setting import *


class Interface(AdminSetting):

    def StudentInterface(self, msg, call=False):
        markup = types.InlineKeyboardMarkup()

        courses = types.InlineKeyboardButton(text="ملازم", callback_data="sendCourses")
        exams = types.InlineKeyboardButton(text="الامتحانات", callback_data="showExams")
        homeworks = types.InlineKeyboardButton(text="الواجبات", callback_data="showHomework")
        # table = types.InlineKeyboardButton(text="الجدول", callback_data="showSubjectTable")
        links = types.InlineKeyboardButton(text="روابط المحاضرات الإلكترونية", callback_data="showMeetLinks")

        markup.add(courses, exams, homeworks, links, self.goBack("Exit", "خروج"), row_width=1)

        if not call:
            self.bot.send_message(text="اختر من القائمة", chat_id=msg.chat.id, reply_markup=markup)

        else:
            self.bot.edit_message_text(text="اختر من القائمة", chat_id=msg.chat.id,
                                       message_id=msg.message_id, reply_markup=markup)

    def InterfaceCall(self, call):

        if call.data == "StartStudent":
            self.StudentInterface(call.message, call=True)
