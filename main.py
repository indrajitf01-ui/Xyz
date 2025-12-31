import telebot
import re
from telebot import types

BOT_TOKEN = "8543718582:AAHGr1Ro-6s2Wbj7SlpVZX5DgIA4DuNeF84"
OWNER_ID = 7743079399

LVL68_IMAGE = "https://t.me/INDRAJITXALL/207"
LVL80_IMAGE = "https://t.me/INDRAJITXALL/221"
QR_IMAGE    = "https://t.me/INDRAJITAPI/112"

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# ---------------- WELCOME TEXT ----------------

WELCOME_TEXT = """
<b>━━━━━━━━━━━━━━━━━━━━━━</b>
🔥🔥 <b>HELLO BROTHER 👋</b> 🔥🔥
<b>━━━━━━━━━━━━━━━━━━━━━━</b>

👑 <b>INDRAJIT 1M</b> 👑
✨ <b>OFFICIAL & TRUSTED NAME</b> ✨

🚀 <b>ALL TYPE OF CODES AVAILABLE</b> 🚀

✅ <b>ALL RARE IDS</b>
✅ <b>LEVEL 68 / 80 ACCOUNTS</b>
✅ <b>GUEST ACCOUNT GENERATOR</b>

🛡️ <b>100% GENUINE | NO SCAM</b>
🛡️ <b>DIRECT OWNER DEAL</b>

🔥 <b>QUALITY FIRST – TRUST FOREVER</b> 🔥
"""

# ---------------- START ----------------

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🛒 BUY ID", callback_data="buy"),
        types.InlineKeyboardButton("🤖 GUEST GEN (₹89)", callback_data="guest"),
        types.InlineKeyboardButton("💳 PAYMENT", callback_data="payment")
    )
    bot.send_message(message.chat.id, WELCOME_TEXT, parse_mode="HTML", reply_markup=kb)

# ---------------- BUY ----------------

@bot.callback_query_handler(func=lambda c: c.data == "buy")
def buy(c):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔥 ₹299 – LEVEL 68 ACCOUNT", callback_data="buy_299"),
        types.InlineKeyboardButton("🔥 ₹699 – LEVEL 80 ACCOUNT", callback_data="buy_699")
    )
    bot.send_message(c.message.chat.id, "<b>SELECT ACCOUNT TYPE</b>", parse_mode="HTML", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def select_account(c):
    price = int(c.data.split("_")[1])
    product = "LEVEL 68 ACCOUNT" if price == 299 else "LEVEL 80 ACCOUNT"

    user_data[c.from_user.id] = {
        "price": price,
        "product": product
    }

    image = LVL68_IMAGE if price == 299 else LVL80_IMAGE

    bot.send_photo(
        c.message.chat.id,
        image,
        caption=f"<b>{product}\nPRICE ₹{price}</b>",
        parse_mode="HTML"
    )

# ---------------- GUEST GEN ----------------

@bot.callback_query_handler(func=lambda c: c.data == "guest")
def guest(c):
    user_data[c.from_user.id] = {
        "price": 89,
        "product": "GUEST ACCOUNT GENERATOR"
    }

    bot.send_message(
        c.message.chat.id,
        """
<b>🤖 GUEST ACCOUNT GENERATOR</b>

💰 <b>PRICE: ₹89</b>
✅ SAFE & INSTANT
✅ WORKING CODE

👉 <b>PAY ₹89 & CONTINUE TO PAYMENT</b>
""",
        parse_mode="HTML"
    )

# ---------------- PAYMENT ----------------

@bot.callback_query_handler(func=lambda c: c.data == "payment")
def payment(c):
    data = user_data.get(c.from_user.id)

    if not data:
        bot.send_message(
            c.message.chat.id,
            "<b>❌ PEHLE PRODUCT SELECT KARE</b>",
            parse_mode="HTML"
        )
        return

    bot.send_photo(
        c.message.chat.id,
        QR_IMAGE,
        caption=f"""
<b>💳 SCAN & PAY</b>

📦 <b>PRODUCT:</b> {data['product']}
💰 <b>AMOUNT:</b> ₹{data['price']}

⚠️ <b>ISI AMOUNT KA PAYMENT KARE</b>

<b>TXN ID DAALE</b>
""",
        parse_mode="HTML"
    )
    bot.register_next_step_handler(c.message, get_txn)

# ---------------- TXN ----------------

def get_txn(message):
    txn = message.text.strip()

    if not re.match(r'^[A-Za-z0-9]{10,}$', txn):
        msg = bot.send_message(
            message.chat.id,
            "<b>❌ INVALID TXN ID\nFIR SE DAALE</b>",
            parse_mode="HTML"
        )
        bot.register_next_step_handler(msg, get_txn)
        return

    user_data[message.from_user.id]["txn"] = txn

    msg = bot.send_message(
        message.chat.id,
        "<b>📸 PAYMENT SCREENSHOT BHEJE</b>\n<b>(AMOUNT CLEAR DIKHNA CHAHIYE)</b>",
        parse_mode="HTML"
    )
    bot.register_next_step_handler(msg, get_screenshot)

# ---------------- SCREENSHOT ----------------

def get_screenshot(message):
    if not message.photo:
        msg = bot.send_message(
            message.chat.id,
            "<b>❌ SCREENSHOT ZAROORI HAI</b>",
            parse_mode="HTML"
        )
        bot.register_next_step_handler(msg, get_screenshot)
        return

    data = user_data[message.from_user.id]

    bot.send_photo(
        OWNER_ID,
        message.photo[-1].file_id,
        caption=f"""
🟢 <b>VERIFIED PAYMENT</b>

👤 <b>USER:</b> @{message.from_user.username}
🆔 <b>ID:</b> {message.from_user.id}

📦 <b>PRODUCT:</b> {data['product']}
💰 <b>AMOUNT:</b> ₹{data['price']}
💳 <b>TXN ID:</b> <code>{data['txn']}</code>

👑 <b>INDRAJIT 1M</b>
""",
        parse_mode="HTML"
    )

    bot.send_message(
        message.chat.id,
        f"""
🟢 <b>PAYMENT VERIFIED</b>

📦 <b>Aapne kharida:</b> {data['product']}
💰 <b>Amount:</b> ₹{data['price']}

⏳ <b>Owner se ID / Code milega</b>
👑 <b>INDRAJIT 1M</b>
""",
        parse_mode="HTML"
    )

# ---------------- RUN ----------------

bot.infinity_polling()