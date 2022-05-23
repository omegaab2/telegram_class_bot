from modules.subject_table import *


class MeetLinks(SubjectTable):

    def MeetLinksCall(self, call):

        if call.message.chat.id in self.admins:

            if call.data == "addMeetLinks" or call.data == "editMeetLinks" or call.data == "deleteMeetLinks":
                markup = types.InlineKeyboardMarkup()

                for subject in self.SUBJECTS:

                    if call.data == "addMeetLinks":
                        btn = types.InlineKeyboardButton(text=f"{subject[0]}",
                                                         callback_data=f"addMeetLinks:{subject[1]}:{subject[0]}")
                    elif call.data == "editMeetLinks":
                        btn = types.InlineKeyboardButton(text=f"{subject[0]}",
                                                         callback_data=f"editMeetLinks:{subject[1]}")
                    else:
                        btn = types.InlineKeyboardButton(text=f"{subject[0]}",
                                                         callback_data=f"deleteMeetLinks:{subject[1]}:{subject[0]}")

                    markup.add(btn)

                markup.add(self.goBack("MeetLinks"))
                self.bot.edit_message_text(text="اختر اسم المادة:", chat_id=call.message.chat.id,
                                           message_id=call.message.message_id, reply_markup=markup)

            elif "addMeetLinks:" in call.data or "editMeetLinks:" in call.data:

                self.bot.edit_message_text(text="رد على الرسالة و ارسل الرابط :", chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)
                self.meetLinksData = call.data.split(":")

                if self.meetLinksData[0] == "addMeetLinks":
                    self.bot.register_for_reply_by_message_id(message_id=call.message.message_id, callback=lambda msg : self.addMeetLinks(msg))

                else:
                    self.bot.register_for_reply_by_message_id(message_id=call.message.message_id,
                                                              callback=lambda msg: self.editMeetLinks(msg))

            elif "deleteMeetLinks:" in call.data:

                data = call.data.split(":")
                txt = f"هل تريد حذف الرابط الخاص ب {data[2]}"
                markup = types.InlineKeyboardMarkup()

                yes = types.InlineKeyboardButton(text="نعم", callback_data=f"deleteMeetLinksTrue:{data[1]}:{data[2]}")
                no = types.InlineKeyboardButton(text="لا", callback_data=f"deleteMeetLinksFalse:{data[1]}:{data[2]}")
                markup.add(yes, no)

                markup.add(self.goBack("deleteMeetLinks"))
                self.bot.edit_message_text(text=txt, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           reply_markup=markup)

            elif "deleteMeetLinksTrue" in call.data:
                data = call.data.split(":")
                try:
                    self.delete("meet_links" ,f"en_subject_name= '{data[1]}'")
                    self.bot.edit_message_text(text="تمت عملية الحذف ", chat_id=call.message.chat.id, message_id=call.message.message_id)
                    self.links = self.get("meet_links", ["*"])

                except Exception as e:
                    self.bot.send_message(text=f"error{e}", chat_id=call.message.chat.id)

            elif call.data == "showMeetLinks":
                markup = types.InlineKeyboardMarkup()

                if self.links:
                    for link in range(len(self.links)):
                        btn = types.InlineKeyboardButton(text=f"{self.links[link][0]}", url=self.links[link][1],
                                                         callback_data=f"MeetLinks:{self.links[link][2]}")
                        markup.add(btn)
                    markup.add(self.goBack("StartStudent"))

                    self.bot.edit_message_text(text="اختر من التالي : ", chat_id=call.message.chat.id,
                                               message_id=call.message.message_id, reply_markup=markup)

                else:
                    self.bot.send_message(chat_id=call.message.chat.id, text="there is no links")

        else:
            if call.data == "showMeetLinks":
                markup = types.InlineKeyboardMarkup()

                if self.links:
                    for link in range(len(self.links)):
                        btn = types.InlineKeyboardButton(text=f"{self.links[link][0]}", url=self.links[link][1],
                                                         callback_data=f"MeetLinks:{self.links[link][2]}")
                        markup.add(btn)
                    markup.add(self.goBack("StartStudent"))

                    self.bot.edit_message_text(text="اختر من التالي : ", chat_id=call.message.chat.id,
                                               message_id=call.message.message_id, reply_markup=markup)

                else:
                    self.bot.send_message(chat_id=call.message.chat.id, text="there is no links")

    def addMeetLinks(self, msg):

        try:
            self.insert("meet_links", ["subject_name", "en_subject_name", "subject_link"], [self.meetLinksData[2], self.meetLinksData[1], msg.text])
            self.links = self.get("meet_links", ["*"])
            self.bot.send_message(text="done", chat_id=msg.chat.id)

        except Exception as e:
            self.bot.send_message(text=f"error{e}", chat_id=msg.chat.id)

    def editMeetLinks(self, msg):
        try:
            self.update("meet_links", ["subject_link"], [msg.text], f"en_subject_name='{self.meetLinksData[1]}'")

            self.links = self.get("meet_links", ["*"])
            self.bot.send_message(text="done", chat_id=msg.chat.id)

        except Exception as e:
            self.bot.send_message(text=f"error{e}", chat_id=msg.chat.id)



