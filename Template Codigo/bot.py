from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)

NOME, = range(1)
TOKEN = "TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou seu primeiro bot.")
    await update.message.reply_text("Envie seu nome:")

    return NOME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE,):
    context.user_data["nome"] = update.message.text

    await update.message.reply_text(f"Olá, {context.user_data['nome']}!")

    keyboard = [
        [
            InlineKeyboardButton(
                "Sobre",
                callback_data="sobre",
            ),
            InlineKeyboardButton(
                "Ajuda",
                callback_data="ajuda",
            ),
        ],
        [
            InlineKeyboardButton(
                "Contato",
                callback_data="contato",
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Escolha uma opção:", reply_markup=reply_markup)

    return ConversationHandler.END

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    acao = query.data

    respostas = {
        "sobre": "Sou um bot criado com Python!",
        "ajuda": "Escolha uma opção nos botões para continuar.",
        "contato": "Entre em contato pelo canal de atendimento.",
    }

    mensagem = respostas.get(
        acao,
        "Opção não reconhecida.",
    )

    await query.edit_message_text(
        text=mensagem,
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "Defina a variável de ambiente TELEGRAM_BOT_TOKEN."
        )

    app = Application.builder().token(TOKEN).build()

    conversa = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            NOME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receber_nome,
                ),
            ],
        },
        fallbacks=[],
    )

    app.add_handler(conversa)
    app.add_handler(CallbackQueryHandler(button))

    print("Bot iniciado!")
    app.run_polling()

if __name__ == "__main__":
    main()