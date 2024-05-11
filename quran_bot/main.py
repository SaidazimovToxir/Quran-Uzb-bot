import os
import telebot
import logging
import requests
import replies
import json
from datetime import datetime
from database import Database
from buttons import (inline_keys, main_button, adminButtons, select_edition,
                        all_surah_buttons_1, all_surah_buttons_2,
                        all_surah_buttons_3, all_surah_buttons_4,
                        names_buttons, adminSelect_buttons, all_spell_button_1, all_spell_button_2,
                        spell_url_buttons, taqvim_buttons
                     )


class QuranBot:
    def __init__(self, api_token) -> None:
        self.API_TOKEN = api_token
        self.bot = telebot.TeleBot(api_token)
        logging.basicConfig(level=logging.INFO)

        self.surahCount = 1
        self.spell_number = None
        self.surah_number = None
        self.dataArabic = None
        self.dataUzbek = None
        self.surah_arabic = {}
        self.data_arabic_audio = {}
        self.surah_uzbek = {}
        self.admin_command_state = {}
        self.date_state = {}
        self.count = 1
        self.namesCount = 0
        self.spellCount = 1
        self.editions_name = ""
        self.check_allAudio = False

        self.register_handlers()
        self.db = Database()


    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_command)
        self.bot.message_handler(commands=['help'])(self.help_command)
        self.bot.message_handler(commands=['adminCommands'])(self.adminCommands)

        # main buttons
        self.bot.message_handler(func=lambda message: message.text == "Suralar ✨")(self.get_all_surah)
        self.bot.message_handler(func=lambda message: message.text == "Allohning 99 ismi 💫")(self.getAllNames)
        self.bot.message_handler(func=lambda message: message.text == "Duolar 🤲🏻")(self.get_all_spell)
        self.bot.message_handler(func=lambda message: message.text == "Taqvim 📅")(self.get_taqvim)

        # Admin buttons
        self.bot.message_handler(func=lambda message: message.text == 'Users info')(self.response_all_users)
        self.bot.message_handler(func=lambda message: message.text == 'Send message all users')(self.send_message_all_users)

        # send message all users buttons
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "for_text")(self.send_text_for_users)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "for_video_and_photo")(self.send_videoPhoto_for_users)

        # this inline buttons for ayahs
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'prev')(self.previous_ayahs)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'next')(self.next_ayahs)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'audio')(self.get_editon)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'allAudio')(self.get_editon_all_audios)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'surah_prev')(self.all_previous_surah)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'surah_next')(self.all_next_surah)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('surah_'))(self.get_selected_surah)


        # this inline buttons for spells
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "spell_prev")(self.spell_prev)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "spell_next")(self.spell_next)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('spell_'))(self.get_selected_spell)


        # Names next and prev
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "namePrev")(self.namesPrevious)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "nameNext")(self.namesNext)

        # Surah editions
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "alafasy")(self.alAfasy_button)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "abdulsamad")(self.abdulsamad_button)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "husary")(self.husary_button)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "minshawi")(self.minshawi_button)


        # Taqvim inline key buttons
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "now_and_hijri")(self.georgian_to_hijri)
        self.bot.callback_query_handler(func=lambda callback_query: callback_query.data == "hijri_and_now")(self.hijri_to_georgian)

        self.bot.message_handler(func=lambda message: True)(self.handle_user_response)
        self.bot.message_handler(content_types=['photo', 'video'])(self.handle_user_response)


    def runBot(self):
        print("Bot polling...")
        self.bot.polling(non_stop=True)

    ## COMMANDS
    def start_command(self, ms):
        try:
            fn = ms.from_user.first_name
            chatID = ms.chat.id
            reply = replies.start.format(firstName=fn)
            reply2 = replies.start2
            self.db.add_users(fn, ms.from_user.username, ms.from_user.id)

            self.bot.send_message(chatID, reply, parse_mode='html', reply_markup=main_button)
            self.bot.send_message(chatID, reply2, parse_mode='html')
        except Exception as e:
            print(f"ERROR ADD USER SECTION: {e}")

    def help_command(self, ms):
        chatID = ms.chat.id
        msID = ms.message_id
        reply = replies.help
        self.bot.send_message(chatID, reply, reply_to_message_id=msID)

    def adminCommands(self, message):
        try:
            reply = replies.adminCommands
            self.bot.send_message(message.chat.id, reply, parse_mode='html')

            self.admin_command_state[message.chat.id] = "waiting_for_text"
        except Exception as e:
            pass

    ## /COMMANDS

    ## ADMIN BUTTONS
    def handle_user_response(self, message):
        try:
            login = 'a'
            parol = 's'
            chat_id = message.chat.id
            reply = replies.admin
            lenght = len(self.db.users_info())
            if chat_id in self.admin_command_state and self.admin_command_state[chat_id] == "waiting_for_text":
                threat = message.text.split()
                if threat[0]==login and threat[1] == parol:
                    self.bot.send_message(chat_id, reply, reply_markup=adminButtons)
                else:
                    self.bot.send_message(chat_id, "Afsuski parol xato\nQayta urinib ko'rish uchun\n/adminCommands buyrug'ini yuboring")

                del self.admin_command_state[chat_id]



            if chat_id in self.admin_command_state and self.admin_command_state[chat_id] == 'waiting_for_all_users':
                msg = message.text
                for i in self.db.users_info():
                    try:
                        self.bot.send_message(i[2], msg)
                    except Exception as e:
                        pass

                del self.admin_command_state[chat_id]
                self.bot.send_message(message.chat.id, f"Text {lenght} ta foydalanuvchiga muaffaqiyatli yuborildi.")

            if chat_id in self.admin_command_state and self.admin_command_state[chat_id] == "waiting_video_photo_for_users":
                if message.photo:
                    photo_id = message.photo[-1].file_id
                    for i in self.db.users_info():
                        try:
                            self.bot.send_photo(i[2], photo_id, caption=message.caption)
                        except Exception as e:
                            pass

                elif message.video:
                    video_id = message.video.file_id
                    for i in self.db.users_info():
                        try:
                            self.bot.send_video(i[2], video_id, caption=message.caption)
                        except Exception as e:
                            pass

                del self.admin_command_state[chat_id]
                self.bot.send_message(chat_id, f"{'Photo' if message.photo else 'Video'} {lenght} ta foydalanuvchiga yuborildi.")

            if chat_id in self.date_state and self.date_state[chat_id] == "waiting_user_input_to_hijri":
                message_textToH = message.text
                georgToHijri = f"http://api.aladhan.com/v1/gToH/{message_textToH}"
                response = requests.get(georgToHijri)
                date = response.json()
                # print(date)

                n = date['data']['hijri']
                holiday = "Ushbu sanada muhim kun mavjud emas!" if n['holidays'] == [] else ', '.join(n['holidays'])
                reply = replies.hijri_.format(DATE=n['date'], WeEN=n['weekday']['en'], WeAR=n['weekday']['ar'],
                                            MoNUM=n['month']['number'], MoEN=n['month']['en'], MoAR=n['month']['ar'], HOLIDAY=holiday)
                self.bot.send_message(chat_id, reply, parse_mode='html')
                del self.date_state[chat_id]

            if chat_id in self.date_state and self.date_state[chat_id] == "waiting_user_input_to_georgian":
                message_textToG = message.text
                hijriToGeorg = f"http://api.aladhan.com/v1/hToG/{message_textToG}"
                response = requests.get(hijriToGeorg)
                data = response.json()

                g = data['data']['gregorian']
                reply2 = replies.georgian_.format(DATE=g['date'], WeEN=g['weekday']['en'], MoNUM=g['month']['number'], MoEN=g['month']['en'])
                self.bot.send_message(chat_id, reply2, parse_mode='html')
                del self.date_state[chat_id]

        except Exception as e:
            self.bot.send_message(message.chat.id, f"ERROR: {e}")


    def response_all_users(self, message):
        try:
            self.bot.send_message(message.chat.id, f"Umumiy userlar soni {len(self.db.users_info())}")
            for user in self.db.users_info():
                reply = replies.user_info.format(ID=user[2], FN=user[0], USERNM=user[1], DATE=user[3])
                self.bot.send_message(message.chat.id, reply, parse_mode='html')
        except Exception as e:
            self.bot.send_message(message.chat.id, f"ERROR: barcha userlarni chiqarishda xatolik bor {e}")

    def send_message_all_users(self, message):
        self.bot.send_message(message.chat.id, "Qanday turda xabar yubormoqchisiz ?\n\nTanlang:", reply_markup=adminSelect_buttons)

    def send_text_for_users(self, callback_query):
        self.bot.send_message(callback_query.message.chat.id, "Foydalanuvchilarga yubormoqchi bo'lgan matn: ")

        self.admin_command_state[callback_query.message.chat.id] = "waiting_for_all_users"

    def send_videoPhoto_for_users(self, callback_query):
        self.bot.send_message(callback_query.message.chat.id, "video toki rasm yuboring\n❗️ Iltimos <b><u>Caption</u></b> qo'shib yuboring:", parse_mode='html')

        self.admin_command_state[callback_query.message.chat.id] = "waiting_video_photo_for_users"

    # all surah buttons
    def get_all_surah(self, message):
        self.bot.send_message(message.chat.id, "Quyidagi suralardan birini tanlang: ", reply_markup=all_surah_buttons_1)

    ## NEXT BUTTON FOR ALL SURAH
    def all_next_surah(self, callback_query):
        try:
            if self.surahCount == 4:
                self.surahCount = 0
            if self.surahCount < 4:
                self.surahCount += 1
                markup = None
                if self.surahCount == 1:
                    markup = all_surah_buttons_1
                elif self.surahCount == 2:
                    markup = all_surah_buttons_2
                elif self.surahCount == 3:
                    markup = all_surah_buttons_3
                elif self.surahCount == 4:
                    markup = all_surah_buttons_4
                if markup:
                    self.bot.edit_message_text("Quyidagi suralardan birini tanlang: ",
                                            chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=markup)

        except Exception as e:
            print(f"Surah Next ERROR: {e}")

    ## PREVIOUS BUTTON FOR ALL SURAH
    def all_previous_surah(self, callback_query):
        try:
            if self.surahCount > 1:
                self.surahCount -= 1
                markup = None
                if self.surahCount == 3:
                    markup = all_surah_buttons_3
                elif self.surahCount == 2:
                    markup = all_surah_buttons_2
                elif self.surahCount == 1:
                    markup = all_surah_buttons_1
                if markup:
                    self.bot.edit_message_text("Quyidagi suralardan birini tanlang: ",
                                            chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=markup)

        except Exception as e:
            print(f"Surah Previous ERROR: {e}")

        ## GET THE SURAH NUMBER AFTER INLINE BUTTONS CLICKED

    def get_selected_surah(self, callback_query):
        self.surah_number = int(callback_query.data.split('_')[1])
        self.get_valid_surah(callback_query.message)

        ## ALL SURAH SAVED IN DICT SECTION

    def get_valid_surah(self, message):
        try:
            url = f"http://api.alquran.cloud/v1/surah/{self.surah_number}/quran-simple"
            urlUz = f"http://api.alquran.cloud/v1/surah/{self.surah_number}/uz.sodik"

            response = requests.get(url)
            self.dataArabic = response.json()

            respons = requests.get(urlUz)
            self.dataUzbek = respons.json()

            self.surah_arabic = {i['numberInSurah']: i['text'] for i in self.dataArabic['data']['ayahs']}
            self.surah_uzbek = {i['numberInSurah']: i['text'] for i in self.dataUzbek['data']['ayahs']}

            chat_id = message.chat.id
            message_id = message.message_id
            self.bot.delete_message(chat_id, message_id)

            self.count = 1
            mes = f"""
<b>Sura nomi:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Umumiy oyatlar soni:</b> {len(self.surah_arabic.keys())} : {self.count}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "Error"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "Xatolik"}</blockquote>
        """
            self.bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=inline_keys)

        except Exception as e:
            print(f"Get Valid Surah ERROR: {e}")


        ## NEXT BUTTON SECTION
    def next_ayahs(self, callback_query):
        try:
            self.count += 1

            if self.count > 0 and self.count <= len(self.surah_arabic.keys()):
                mes = f"""
<b>Sura nomi:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Umumiy oyatlar soni:</b> {len(self.surah_arabic.keys())} : {self.count}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "NimaduAr"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "NimaduUz"}</blockquote>
            """
                self.bot.edit_message_text(mes, chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        parse_mode='html',
                                        reply_markup=inline_keys)
            else:
                self.count -= 1

        except Exception as e:
            print(f"Ayahs Next Button ERROR: {e}")

        ## PREVIOUS BUTTON SECTION
    def previous_ayahs(self, callback_query):
        try:
            self.count -= 1

            if self.count > 0 and self.count <= len(self.surah_arabic.keys()):
                mes = f"""
<b>Sura nomi:</b> {self.dataArabic['data']['englishName']} ({self.dataArabic['data']['number']})
<b>Umumiy oyatlar soni:</b> {len(self.surah_arabic.keys())} : {self.count}

<u><b>Arabic:</b></u> <blockquote>{self.surah_arabic[self.count] if self.count in self.surah_arabic else "NimaduAr"}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{self.surah_uzbek[self.count] if self.count in self.surah_uzbek else "NimaduUz"}</blockquote>
            """
                self.bot.edit_message_text(mes, chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        parse_mode='html',
                                        reply_markup=inline_keys)
            else:
                self.count += 1

        except Exception as e:
            print(f"Ayahs previous button ERROR: {e}")


        ## AUDIOS SECTION

    # Select Edition
    def get_editon(self, callback_query):
        self.bot.send_message(callback_query.message.chat.id, "Quyidagi o'zingizga yoqqan qorilardan birini tanlang:",reply_markup=select_edition)

    def get_editon_all_audios(self, callback_query):
        self.check_allAudio = True
        self.bot.send_message(callback_query.message.chat.id, "Quyidagi o'zingizga yoqqan qorilardan birini tanlang:",reply_markup=select_edition)


    def alAfasy_button(self, callback_query):
        try:
            if self.check_allAudio == True:
                channel_id = -1002122176215
                chanel_message_id = self.surah_number + 1
                self.bot.copy_message(callback_query.message.chat.id, channel_id, chanel_message_id, parse_mode='html')
                self.check_allAudio = False

                chat_id = callback_query.message.chat.id
                message_id = callback_query.message.message_id
                self.bot.delete_message(chat_id, message_id)

            else:
                self.editions_name = "ar.alafasy"
                self.get_valid_ahays_audios(callback_query.message)
        except Exception as e:
            print(f"Alafasy button ERROR: {e}")

    def abdulsamad_button(self, callback_query):
        try:
            if self.check_allAudio == True:
                channel_id = -1002065837739
                chanel_message_id = self.surah_number + 1
                self.bot.copy_message(callback_query.message.chat.id, channel_id, chanel_message_id, parse_mode='html')
                self.check_allAudio = False

                chat_id = callback_query.message.chat.id
                message_id = callback_query.message.message_id
                self.bot.delete_message(chat_id, message_id)
            else:
                self.editions_name = "ar.abdulsamad"
                self.get_valid_ahays_audios(callback_query.message)
        except Exception as e:
            print(f"Abdulsamad button ERROR: {e}")

    def husary_button(self, callback_query):
        try:
            if self.check_allAudio == True:
                channel_id = -1002076500176
                chanel_message_id = self.surah_number + 1
                self.bot.copy_message(callback_query.message.chat.id, channel_id, chanel_message_id, parse_mode='html')
                self.check_allAudio = False

                chat_id = callback_query.message.chat.id
                message_id = callback_query.message.message_id
                self.bot.delete_message(chat_id, message_id)
            else:
                self.editions_name = "ar.husary"
                self.get_valid_ahays_audios(callback_query.message)
        except Exception as e:
            print(f"Husary button ERROR: {e}")

    def minshawi_button(self, callback_query):
        try:
            if self.check_allAudio == True:
                channel_id = -1002090285210
                chanel_message_id = self.surah_number + 1
                self.bot.copy_message(callback_query.message.chat.id, channel_id, chanel_message_id, parse_mode='html')
                self.check_allAudio = False

                chat_id = callback_query.message.chat.id
                message_id = callback_query.message.message_id
                self.bot.delete_message(chat_id, message_id)
            else:
                self.editions_name = "ar.minshawi"
                self.get_valid_ahays_audios(callback_query.message)
        except Exception as e:
            print(f"minshawi button ERROR: {e}")

    def get_valid_ahays_audios(self, callback_query):
        try:
            chat_id = callback_query.chat.id
            message_id = callback_query.message_id
            self.bot.delete_message(chat_id, message_id)

            url = f"http://api.alquran.cloud/v1/surah/{self.surah_number}/{self.editions_name}"
            response = requests.get(url)
            self.data_arabic_audio = response.json()

            for i in self.data_arabic_audio['data']['ayahs']:
                if self.count == i['numberInSurah']:
                    self.bot.send_audio(callback_query.chat.id, i['audio'])
                    break
        except Exception as e:
            print(f"Ayahs Audio button ERROR: {e}")

    # NAMES SECTION
    def getAllNames(self, message):
        try:
            self.namesCount = 0
            with open("99names.json", 'r') as f:
                self.data = json.load(f)
                arabic = self.data['allNames'][self.namesCount]['Arabic']
                name = self.data['allNames'][self.namesCount]['Name']
                meaning = self.data['allNames'][self.namesCount]['Meaning']
        except Exception as e:
            print(f"Names json fayl ERROR: {e}")
        try:
            pass
            reply = replies.allNames.format(COUNT=self.namesCount + 1,ARABIC=arabic, UZBEK=name, MEANING=meaning)

            self.bot.send_message(message.chat.id, reply, reply_markup=names_buttons, parse_mode='html')

        except Exception as e:
            print(f"Names button ERROR: {e}")

    def namesNext(self, callback_query):
        try:
            self.namesCount += 1
            if self.namesCount > 0 and self.namesCount < 99:
                arabic = self.data['allNames'][self.namesCount]['Arabic']
                name = self.data['allNames'][self.namesCount]['Name']
                meaning = self.data['allNames'][self.namesCount]['Meaning']

                reply = replies.allNames.format(COUNT=self.namesCount + 1, ARABIC=arabic, UZBEK=name, MEANING=meaning)

                self.bot.edit_message_text(reply, chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        parse_mode='html',
                                        reply_markup=names_buttons)
            else:
                self.namesCount -= 1

        except Exception as e:
            print(f"names next button ERROR: {e}")

    def namesPrevious(self, callback_query):
        try:
            self.namesCount -= 1
            if self.namesCount >= 0 and self.namesCount < 99:
                arabic = self.data['allNames'][self.namesCount]['Arabic']
                name = self.data['allNames'][self.namesCount]['Name']
                meaning = self.data['allNames'][self.namesCount]['Meaning']

                reply = replies.allNames.format(COUNT=self.namesCount + 1, ARABIC=arabic, UZBEK=name, MEANING=meaning)

                self.bot.edit_message_text(reply, chat_id=callback_query.message.chat.id,
                                           message_id=callback_query.message.message_id,
                                           parse_mode='html',
                                           reply_markup=names_buttons)

            else:
                self.namesCount += 1

        except Exception as e:
            print(f"previuos button ERROR: {e}")
    # /NAMES SECTION

    # SPELL (DUOLAR) SECTION
    def get_all_spell(self, message):
        reply = replies.main_spell
        self.bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=all_spell_button_1)
    def spell_next(self, callback_query):
        try:
            self.spellCount += 1
            reply = replies.main_spell
            if self.spellCount == 2:
                self.bot.edit_message_text(reply, chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=all_spell_button_2, parse_mode='html')
            else:
                self.spellCount -= 1
        except Exception as e:
            print(f"spell nexrt ERROR: {e}")
    def spell_prev(self, callback_query):
        try:
            self.spellCount -= 1
            reply = replies.main_spell
            if self.spellCount == 1:
                self.bot.edit_message_text(reply, chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=all_spell_button_1, parse_mode='html')

            else:
                self.spellCount += 1
        except Exception as e:
            print(f"spell prev ERROR: {e}")

    # get selected spells
    def get_selected_spell(self, callback_query):
        self.spell_number = int(callback_query.data.split("_")[1])
        self.get_valid_spell(callback_query.message)

    def get_valid_spell(self, message):
        try:
            with open('duolar.json', 'r') as f:
                spell_data = json.load(f)

            chat_id = message.chat.id
            message_id = message.message_id
            self.bot.delete_message(chat_id, message_id)

            for i in spell_data['duolar']:
                if self.spell_number == i['number']:
                    reply = replies.spell_.format(NAME = i['name'], TEXT = i['text'], ARABIC = i['arabic'], MEANING = i['meaning'], TEXT2 = i['text2'])
                    self.bot.send_message(chat_id, reply, parse_mode='html', reply_markup=spell_url_buttons)
        except Exception as e:
            print(f"get valid spell ERROR: {e}")
    # /get selected spells

    # get Hijriy and Georgian Date
    def get_taqvim(self, message):
        try:
            current_date = datetime.now()
            formatted = current_date.strftime("%d-%m-%Y")

            urlToCurr = f"http://api.aladhan.com/v1/gToH/{formatted}"

            response = requests.get(urlToCurr)

            data = response.json()

            all_date = data['data']['hijri']

            reply = replies.date_main.format(CurrDate=formatted, DATE=all_date['date'])

            self.bot.send_message(message.chat.id, reply, parse_mode='html', reply_markup=taqvim_buttons)
        except Exception as e:
            print(f"Get taqvim ERROR: {e}")

    def georgian_to_hijri(self, callback_query):
        chat_id = callback_query.message.chat.id

        reply = replies.for_user_input_to_hijri
        self.bot.send_message(chat_id, reply, parse_mode='html')

        self.date_state[chat_id] = "waiting_user_input_to_hijri"

    def hijri_to_georgian(self, callback_query):
        chat_id = callback_query.message.chat.id

        reply = replies.for_user_input_to_georigan
        self.bot.send_message(chat_id, reply, parse_mode='html')

        self.date_state[chat_id] = "waiting_user_input_to_georgian"




if __name__ == '__main__':
    bot = QuranBot("6966475696:AAFSKj66T4ciD6jGz8Rk1krbdI_AM7fPdFE")
    bot.runBot()
