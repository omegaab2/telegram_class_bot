from modules.homework import *


class CustomUpload(Homework):

    def CustomUploadMeCall(self, call):

        if call.data == "StartCustomUpload":

            markup = types.InlineKeyboardMarkup()
            for index in range(len(self.courses)):
                btn = types.InlineKeyboardButton(text=str(self.courses[index]['name']), callback_data=f"CustomUploadSubject:{self.courses[index]['name']}")
                markup.add(btn)

            markup.add(self.goBack("AdminSetting"))

            self.bot.edit_message_text(text="اختر اسم المادة :", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, reply_markup=markup)

        elif "CustomUploadSubject:" in call.data:

            markup = types.InlineKeyboardMarkup()
            markup.add(self.goBack("StartCustomUpload"))

            self.__subject_name = call.data.split(":")[1]
            self.__my_msg = self.bot.edit_message_text(text="ارسل اسم الملف الذي تريد رفعه", chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, reply_markup=markup)

            self.bot.register_for_reply_by_message_id(message_id=call.message.message_id, callback=lambda msg: self.fileNameCustomUpload(msg))

    def fileNameCustomUpload(self, msg):
        self.__file_name = msg.text

        markup = types.InlineKeyboardMarkup()
        markup.add(self.goBack("CustomUploadSubject:"))

        self.__my_msg = self.bot.send_message(text="ارسل الملف الذي تريد رفعه", chat_id=msg.chat.id, reply_markup=markup)
        self.bot.register_for_reply_by_message_id(message_id=self.__my_msg.message_id,
                                                  callback=lambda mg: self.saveCustomUpload(mg))

    def saveCustomUpload(self, message):
        print("in message:")

        msg = self.bot.forward_message(chat_id=-1001670074369, from_chat_id=message.chat.id, message_id=message.message_id)
        self.saveIndexFile(self.__file_name, msg.message_id, self.__subject_name)
        self.bot.send_message(text="تم رفع الملف ورد", chat_id=self.__my_msg.chat.id)

