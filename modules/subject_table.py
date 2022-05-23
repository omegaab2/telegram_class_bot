from modules.exam import *


class SubjectTable(Exam):

    def emptyBtn(self):
        return types.InlineKeyboardButton(text=f" ", callback_data="nothing")

    def SubjectCall(self, call):

        if call.message.chat.id in self.admins:
            # add subject name step
            if call.data == "addSubjectTable":

                markup = types.InlineKeyboardMarkup()

                for subject in self.SUBJECTS:
                    btn = types.InlineKeyboardButton(text=f"{subject[0]}", callback_data=f"SubjectTableName:{subject[1]}")
                    markup.add(btn)
                markup.add(self.goBack("SubjectTable"))

                self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                           message_id=call.message.message_id, reply_markup=markup)

            # add day step
            elif "SubjectTableName:" in call.data:
                subject = call.data.split(":")[1]

                markup = types.InlineKeyboardMarkup()
                for day in self.week:
                    btn = types.InlineKeyboardButton(text=f"{self.week[day]}", callback_data=f"SubjectTableDay:{subject}:{day}")
                    markup.add(btn)

                markup.add(self.goBack("addSubjectTable"))

                self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                           message_id=call.message.message_id, reply_markup=markup)

            # add time step
            elif "SubjectTableDay:" in call.data:
                subject = call.data.split(":")[1]
                day = call.data.split(":")[2]

                markup = types.InlineKeyboardMarkup()
                for tm in self.times:
                    btn = types.InlineKeyboardButton(text=f"{tm}",
                                                     callback_data=f"SubjectTableTimes-{subject}-{day}-{tm}")
                    markup.add(btn)

                markup.add(self.goBack("SubjectTableName:"))

                self.bot.edit_message_text(text="اختر من التالي :", chat_id=call.message.chat.id,
                                           message_id=call.message.message_id, reply_markup=markup)

            # save subject step
            elif "SubjectTableTimes" in call.data:
                en_subject = call.data.split("-")[1]
                day = call.data.split("-")[2]
                time = call.data.split("-")[3]
                subject = self.get("subject", ["subject_name"], f"en_subject_name = '{en_subject}'")[0][0]

                try:
                    self.insert("subjects_table", ["subject_name", "subject_day", "subject_time", "en_subject_name"], [subject, day, time, en_subject])
                    self.bot.edit_message_text(text="subject added to the table", message_id=call.message.message_id,
                                               chat_id=call.message.chat.id)

                except Exception as e:
                    self.bot.send_message(text=f"Error: \n {e}", chat_id=call.message.chat.id)
                    print(e)

            elif call.data == 'deleteSubjectTable':
                markup = self.showSubject(for_delete=True)

                self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           text="اضغط على المادة التي تريد حذفها من الجدول", reply_markup=markup)

            elif "delete_subject:" in call.data:
                self.delete("subjects_table", f"id={call.data.split(':')[2]}")
                markup = self.showSubject(for_delete=True)
                self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           message_id=call.message.message_id,
                                           text="اضغط على المادة التي تريد حذفها من الجدول", reply_markup=markup)

        # show subjects
        elif call.data == "showSubjectTable":
            markup = self.showSubject()
            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       text="الجدول :", reply_markup=markup)

    def showSubject(self, for_delete=False):

        ls = []
        table = self.get("subjects_table", ["*"], order='subject_time')
        markup = types.InlineKeyboardMarkup()

        ls.append(self.emptyBtn())

        for t in self.times[:-1]:
            btn = types.InlineKeyboardButton(text=f"{t}", callback_data="nothing")
            ls.append(btn)

        markup.add(ls)
        ls = []

        for i in range(len(self.days)):
            ls.append(types.InlineKeyboardButton(text=f"{self.days[i]}", callback_data=f"nothing"))

            for j in range(len(table)):
                if table[j][1] == self.days[i]:

                    if not for_delete:
                        btn = types.InlineKeyboardButton(text=f"{table[j][3]}", callback_data=f"fullInfo:{table[j][3]}:{table[j][4]}")

                    else:
                        btn = types.InlineKeyboardButton(text=f"{table[j][3]}",
                                                         callback_data=f"delete_subject:{table[j][3]}:{table[j][4]}")

                    index = self.times.index(table[j][2].strftime("%H:%M"))
                    ran = index + (len(ls) % 4) - len(ls)

                    print("ran", ran, "index", index, "len", len(ls), "mod", (len(ls) % 4), table[j][0])

                    if ran < 1:
                        ls.append(btn)

                    else:
                        for n in range(index-1):

                            if len(ls) < 4:
                                print("len : ", len(ls))
                                ls.append(self.emptyBtn())

                            elif len(ls) >= 4:
                                break

                        ls.append(btn)

                elif len(ls) < 5:
                    continue

            while len(ls) < 5:
                ls.append(self.emptyBtn())

            markup.add(ls)
            ls = []

        if for_delete:
            markup.add(self.goBack("SubjectTable"))

        else:
            markup.add(self.goBack("StartStudent"))

        return markup

