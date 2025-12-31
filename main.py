import telebot

# --- SETUP ---
BOT_TOKEN = "APNA_NEW_BOT_TOKEN_DAALEIN" # @BotFather se naya bot banakar token yahan daalein
TARGET_BOT = "INDRAJIT_TCP_BOT"         # Aapka bataya hua bot
OWNER_ID = 123456789                    # Aapki numerical ID (@userinfobot se lein)
ADMIN_IDS = [987654321]                 # Admin ki IDs (comma se separate karein)

bot = telebot.TeleBot(BOT_TOKEN)

print(f"🚀 Bot Active! @{TARGET_BOT} se aane wale data ka wait kar raha hoon...")

@bot.message_handler(func=lambda message: True)
def handle_forwarding(message):
    # Check karega ki message INDRAJIT_TCP_BOT se aaya hai
    if message.from_user and message.from_user.username == TARGET_BOT:
        
        # Message ka format
        final_msg = (
            f"📥 **NEW DATA RECEIVED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{message.text}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 From: @{TARGET_BOT}"
        )

        # 1. Pehle Owner (Aapko) bhejega
        bot.send_message(OWNER_ID, f"👑 **[OWNER]**\n{final_msg}")

        # 2. Phir Admins ko bhejega
        for admin_id in ADMIN_IDS:
            try:
                bot.send_message(admin_id, f"🛠 **[ADMIN]**\n{final_msg}")
            except Exception as e:
                print(f"Admin {admin_id} error: {e}")

bot.infinity_polling()
