start = """
Assalamu Alaykum <b><code>{firstName}</code>!</b>

Bu bot sizga Qur'on oyatlari va boshqa ma'lumotlar bera oladi.

U sizga <b>Arabcha</b> va <b>O'zbekcha</b> matnni hamda har bir oyatni va to'liq <b>Audio</b>ni berishi mumkin.
"""

start2 = """
❗️ Iltimos agar botda qandaydir xato va kamchiliklar bo'lsa
<a href="https://t.me/tox_uzb">Admin</a> ga murojaat qiling.

Mukammalik faqat <i>Allohga</> xos 😊
Xato kamchiliklar uchun oldindan uzr so'raymiz!!!

<b>Bog'lanish uchun ⤵️:</b>
<a href="https://t.me/tox_uzb">Telegram</a>
"""

help = """
Agar foydalanishda muammo bo'lsa adminga murojat qiling.


Savollar va takliflar uchun: @Tox_uzb
"""

adminCommands = """
Admin panel bo'limiga xush kelibsiz
Siz adminliginizni tekshirish uchun <b>Login</b> va <b>Parol</b> kiritishingiz zarur.

<u><b>Namuna:</b></u>
"<code>login parol</code>"

❗️ o'rtada bo'sh joy bo'lishi kerak.
"""

admin = """
Admin paneliga xush kelibsiz
quyidagilardan birini tanlang:
"""

user_info = """
ID: <code>{ID}</code>
First Name: <b>{FN}</b>
Username: <b>@{USERNM}</b>
Starting date: <b>{DATE}</b>
"""

allNames = """
<i>Allohning go'zal ismlari</i> ✨

<b>Umumiy isimlar soni:</b> 99 : {COUNT}

<u><b>Arabic:</b></u> <blockquote>{ARABIC}</blockquote>
<u><b>Uzbek:</b></u> <blockquote>{UZBEK}</blockquote>

<u><b>Ma'nosi:</b></u> <blockquote>{MEANING}</blockquote>
"""

# Text for spell
main_spell = """
<i>Har doim o'qib yurishingiz kerak bo'lgan duolar</i> 💫

Quyidagi o'zingizga kerakli bo'lgan <b>Duo</b>ni tanlang:
"""

spell_ = """
<b>{NAME}</b>

<u><b>Tafsif:</b></u> <blockquote>{TEXT}</blockquote>
<u><b>Arabic:</b></u> <blockquote>{ARABIC}</blockquote>
<u><b>Ma'nosi:</b></u> <blockquote>{MEANING} {TEXT2}</blockquote>
"""

date_main = """
<b>Hozirgi vaqt:</b> <i>{CurrDate}</i>
<b>Hijriy yil:</b> <i>{DATE}</i>

Assalomu alaykum quyidagi bo'limlardan o'zingizga kerakli qismini tanlang:
"""

for_user_input_to_hijri = """
<i><u>Hijri</u> yilga o'tkazmoqchi bo'lgan sanani kiriting</i> ⌛️

<b>Namuna:</b>
<code>'%kk-oo-yyyy'</code>
<code>'25-03-2024'</code>

<b>Eslatma:</b>
❗️ O'rtada chiziqchalardan foydalaning (-)
"""

for_user_input_to_georigan = """
<i>gregorian taqvimiga o'tkazmoqchi bo'lgan <u>Hijri</u> sanani kiriting</i> ⌛️

<b>Namuna:</b>
<code>'%kk-oo-yyyy'</code>
<code>'14-09-1445'</code>

<b>Eslatma:</b>
❗️ O'rtada chiziqchalardan foydalaning (-)
"""


hijri_ = """
<b>Hijriy yil:</b> <i>{DATE}</i>

<u><b>Hafta kunlari:</b></u> <blockquote><i>Uzbek</i> - {WeEN} : <i>Arabic</i> - {WeAR}</blockquote>

<u><b>Oy:</b></u> <blockquote><i>Sana</i> - {MoNUM} : <i>Uzbek</i> - {MoEN} : <i>Arabic</i> - {MoAR}</blockquote>

<u><b>Muhim kunlar:</b></u> <blockquote>{HOLIDAY}</blockquote>
"""

georgian_ = """
<b>Hozirgi yil:</b> <i>{DATE}</i>

<u><b>Hafta kunlari:</b></u> <blockquote>{WeEN}</blockquote>

<u><b>Oy:</b></u> <blockquote>{MoNUM} - {MoEN}</blockquote>
"""