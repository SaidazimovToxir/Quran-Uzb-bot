from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

class BotButtons:
    @staticmethod
    def main_button():
        """Returns the main reply keyboard markup."""
        return ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            KeyboardButton("Suralar ✨"),
            KeyboardButton("Allohning 99 ismi 💫"),
            KeyboardButton("Duolar 🤲🏻"),
            KeyboardButton("Taqvim 📅")
        )

    @staticmethod
    def namesButtons():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Oldingi isim", callback_data="namePrev"),
            InlineKeyboardButton(text="Keyingi isim", callback_data="nameNext"),
            InlineKeyboardButton(text="O'qish kerak", url="https://telegra.ph/Paygambarimiz-Muhammad-sollallohu-alayhi-vasallam-aytdilar-03-21"),
            InlineKeyboardButton(text="Rabbiyning isimlari", url="https://telegra.ph/Rabbiyning-mohiyatini-bildiruvchi-ismlar-03-21")
        )

    @staticmethod
    def select_edition():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Alafasy 🇦🇪", callback_data='alafasy'),
            InlineKeyboardButton(text="Abdul Samad 🇪🇬", callback_data='abdulsamad'),
            InlineKeyboardButton(text="Husary 🇪🇬", callback_data='husary'),
            InlineKeyboardButton(text="Minshawi 🇪🇬", callback_data='minshawi')
        )

    @staticmethod
    def surah_inline_keys():
        """Returns the inline keyboard markup for surah navigation."""
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Oldingi oyat", callback_data='prev'),
            InlineKeyboardButton(text="Keyingi oyat", callback_data='next'),
            InlineKeyboardButton(text="Oyat audiosi", callback_data='audio'),
            InlineKeyboardButton(text="To'liq audio", callback_data='allAudio')
        )

    # buttons for surahs
    @staticmethod
    def all_surah_buttons(surah_names, start_index):
        """Returns inline keyboard markup for displaying surahs."""
        markup = InlineKeyboardMarkup()
        row = []
        for i, name in enumerate(surah_names, start=start_index):
            callback_data = f"surah_{i}"
            button = InlineKeyboardButton(text=f"{i} {name}", callback_data=callback_data)
            row.append(button)
            if len(row) == 3:
                markup.row(*row)
                row = []
        if row:
            markup.row(*row)
        markup.row(
            InlineKeyboardButton(text="Oldingi suralar", callback_data="surah_prev"),
            InlineKeyboardButton(text="Keyingi suralar", callback_data="surah_next")
        )
        return markup

    # spell
    @staticmethod
    def all_spell_buttons(spell_names, start_index):
        markub = InlineKeyboardMarkup()
        row = []

        for i, name in enumerate(spell_names, start=start_index):
            callback_data = f"spell_{i}"
            button = InlineKeyboardButton(text=f"{name}", callback_data=callback_data)
            row.append(button)
            if len(row) == 2:
                markub.row(*row)
                row = []
        if row:
            markub.row(*row)

        markub.row(
            InlineKeyboardButton(text="Oldingi duolar", callback_data="spell_prev"),
            InlineKeyboardButton(text="Keyingi duolar", callback_data='spell_next'),
        )
        return markub

    @staticmethod
    def spell_url_buttons():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Kirish 😇", url="https://telegra.ph/Kirish-03-24"),
            InlineKeyboardButton(text="Oyatal kursi ", url="https://telegra.ph/Oyatal-kursi-03-24"),
            InlineKeyboardButton(text="Salovat, Istig'for", url="https://telegra.ph/Salovotlar-Istigfor-duolari-03-24"),
            InlineKeyboardButton(text="Duoyim qabul bo'lsin desangiz", url="https://telegra.ph/Duoyim-qabul-bolsin-desangiz-03-24")
        )

    @staticmethod
    def adminButtons():
        return ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("Users info"),
            KeyboardButton("Send message all users")
        )

    @staticmethod
    def video_and_photo():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Photo and Video", callback_data="for_video_and_photo"),
            InlineKeyboardButton(text="Text", callback_data="for_text")
        )

    # taqvim buttons
    @staticmethod
    def date_methods():
        return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text="Hozirgi 🔁 Hijriy", callback_data="now_and_hijri"),
            InlineKeyboardButton(text="Hijriy 🔁 Hozirgi", callback_data="hijri_and_now")
        )




main_button = BotButtons.main_button()
inline_keys = BotButtons.surah_inline_keys()
adminButtons = BotButtons.adminButtons()
adminSelect_buttons = BotButtons.video_and_photo()
select_edition = BotButtons.select_edition()
names_buttons = BotButtons.namesButtons()
spell_url_buttons = BotButtons.spell_url_buttons()
taqvim_buttons = BotButtons.date_methods()



all_surah_names_1 = ["Al-Fatihah", "Al-Baqarah", "Ali 'Imran", "An-Nisa", "Al-Ma'idah", "Al-An'am", "Al-A'raf", "Al-Anfal", "At-Tawbah", "Yunus", "Hud", "Yusuf", "Ar-Ra'd", "Ibrahim", "Al-Hijr", "An-Nahl", "Al-Isra", "Al-Kahf", "Maryam", "Taha", "Al-Anbya", "Al-Hajj", "Al-Mu'minun", "An-Nur", "Al-Furqan", "Ash-Shu'ara", "An-Naml", "Al-Qasas", "Al-'Ankabut", "Ar-Rum", "Luqman", "As-Sajdah", "Al-Ahzab"]
all_surah_names_2 = ["Saba", "Fatir", "Ya-Sin", "As-Saffat", "Sad", "Az-Zumar", "Ghafir", "Fussilat", "Ash-Shuraa", "Az-Zukhruf", "Ad-Dukhan", "Al-Jathiyah", "Al-Ahqaf", "Muhammad", "Al-Fath", "Al-Hujurat", "Qaf", "Adh-Dhariyat", "At-Tur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi'ah", "Al-Hadid", "Al-Mujadila", "Al-Hashr", "Al-Mumtahanah", "As-Saf", "Al-Jumu'ah", "Al-Munafiqun", "At-Taghabun", "At-Talaq", "At-Tahrim"]
all_surah_names_3 = ["Al-Mulk", "Al-Qalam", "Al-Haqqah", "Al-Ma'arij", "Nuh", "Al-Jinn", "Al-Muzzammil", "Al-Muddaththir", "Al-Qiyamah", "Al-Insan", "Al-Mursalat", "An-Naba", "An-Nazi'at", "'Abasa", "At-Takwir", "Al-Infitar", "Al-Mutaffifin", "Al-Inshiqaq", "Al-Buruj", "At-Tariq", "Al-A'la", "Al-Ghashiyah", "Al-Fajr", "Al-Balad", "Ash-Shams", "Al-Layl", "Ad-Duhaa", "Ash-Sharh", "At-Tin", "Al-'Alaq", "Al-Qadr", "Al-Bayyinah", "Az-Zalzalah"]
all_surah_names_4 = ["Al-'Adiyat", "Al-Qari'ah", "At-Takathur", "Al-'Asr", "Al-Humazah", "Al-Fil", "Quraysh", "Al-Ma'un", "Al-Kawthar", "Al-Kafirun", "An-Nasr", "Al-Masad", "Al-Ikhlas", "Al-Falaq", "An-Nas"]

all_surah_buttons_1 = BotButtons.all_surah_buttons(all_surah_names_1, start_index=1)
all_surah_buttons_2 = BotButtons.all_surah_buttons(all_surah_names_2, start_index=34)
all_surah_buttons_3 = BotButtons.all_surah_buttons(all_surah_names_3, start_index=67)
all_surah_buttons_4 = BotButtons.all_surah_buttons(all_surah_names_4, start_index=100)



all_spell_names_1 = ['Sajda paytida', "Ruku'da bosh ko'targanda", "Namozda Ruku'da", "Namoz boshlaganda", "Azon va iqomatni eshitganda", "Masjidga kirishda", "Masjiddan chiqishda", "Masjidga ketishda", "Tahorat qilganda", "Qon oldirganda", "Yoqimsiz tush ko'rganda", "Uyquda qo'rqqanda", "Uxlay olmaganda", "Uxlash uchun yotganda"]
all_spell_names_2 = ["Juma tongida", "Tong va kechqurunda", "Uyqudan uyg'onganda", "Uyquga yotishda", "G’am, tashvish kelganda", "Qiyinchilik va g’amlikda", "Robbimga tavakkal qildim", "Allohim, Sendan pok rizq so'rayman", "Nabiy alayhissalom o'qigan duolar", "Kech kirganda", "Etmish ming farishta", "Zararli narsalardan saqlanish", "Saharlik duosi", "Iftorlik duosi"]

all_spell_button_1 = BotButtons.all_spell_buttons(all_spell_names_1, start_index=1)
all_spell_button_2 = BotButtons.all_spell_buttons(all_spell_names_2, start_index=15)