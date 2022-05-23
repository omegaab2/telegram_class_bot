from modules.custom_upload import *


class Student(CustomUpload):

    def StudentCall(self, call):
        print(call.message.chat.id)
        if "addStudent" in call.data:
            teleId = call.data.split(":")[2]
            name = call.data.split(":")[1]

            self.insert("student", ["name", "tele_id"], [name, teleId])

            self.StudentsTeleId = self.getStudentsTeleId()
            self.StudentsUsers = self.getStudentsUsers()
            admin_name = self.get("admin", ["admin_name"], f"tele_id = {call.message.chat.id}")

            for admin in self.admins:
                self.bot.send_message(text=f"تمت الموافقة على الحذف بواسطة الادمن {call.message.username}", chat_id=admin)
            print("save done")

        elif call.data == "DeleteMsg":
            self.bot.delete_message(call.message.chat.id, call.message.message_id)

        elif call.message.chat.id in self.admins:
            print("inside")
            if call.data == "showStudents":
                self.showStudent(call.message, "showAllStudentInfo")

            if "showAllStudentInfo" in call.data:

                data = self.get("student", ["*"], f"id={call.data.split(':')[1]}")
                txt = f"اسم الطالب: {data[0][1]}\nالتسلسل: {data[0][0]}\nمعرف التلي: {data[0][3]}\nايدي التليكرام : {data[0][2]}"

                markup = types.InlineKeyboardMarkup()
                markup.add(self.goBack("AdminSetting"))

                self.bot.edit_message_text(text=txt, chat_id=call.message.chat.id,
                                           message_id=call.message.message_id, reply_markup=markup)

            elif call.data == "deleteStudent":
                self.showStudent(call.message, "deleteStudent")

            elif "deleteStudent" in call.data:
                try:
                    self.delete("student", f"id={call.data.split(':')[1]}")

                except :
                    self.bot.send_message(text="there is Error in remove student")

    def showStudent(self, msg, callback):
        students = self.get("student", ["id", "name"], order='id')
        markup = types.InlineKeyboardMarkup()

        for stu in range(0, len(students)):

            btn1 = types.InlineKeyboardButton(text=f"{students[stu][1]}", callback_data=f"{callback}:{students[stu][0]}")
            markup.add(btn1)

        markup.add(self.goBack("AdminSetting"))
        self.bot.edit_message_text(text="اضغط على الطالب :", chat_id=msg.chat.id,
                                   message_id=msg.message_id, reply_markup=markup)
