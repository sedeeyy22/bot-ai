import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# قم بملء بياناتك هنا
TELEGRAM_BOT_TOKEN = "8569637923:AAF0tO_lVBq8Y-JkMxBled6Lj8MQqYfUYwE"
OPENAI_API_KEY = "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"

# إعداد التسجيل لرؤية الأخطاء
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

# إعداد عميل OpenAI
openai.api_key = OPENAI_API_KEY

# وظيفة الرد على أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً بك! أنا بوت ذكي يعمل بالذكاء الاصطناعي. كيف يمكنني مساعدتك اليوم؟")

# وظيفة الرد على الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if not user_message:
        return

    try:
        # إرسال رسالة المستخدم إلى نموذج الذكاء الاصطناعي (GPT-3.5-turbo كمثال)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ولطيف ومفيد."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        ai_response = response.choices.message.content
        await update.message.reply_text(ai_response)
    except Exception as e:
        logging.error(f"حدث خطأ أثناء الاتصال بـ OpenAI: {e}")
        await update.message.reply_text("عذراً، حدث خطأ في الاتصال بخدمة الذكاء الاصطناعي.")

def main() -> None:
    """تشغيل البوت."""
    # إنشاء التطبيق وتمرير رمز البوت المميز
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة معالجات الأوامر والرسائل
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # بدء تشغيل البوت
    print("البوت يعمل...")
    application.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
