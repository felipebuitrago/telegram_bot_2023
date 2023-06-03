#
#   IF YOU NEED HELP TO START SEE FIRST THIS REPOSITORY
#   AND HIS YOUTUBE TUTORIAL ON @indently CHANNEL:
#       https://github.com/indently/telegram_bot_2023
#
#   SI NECESITAS AYUDA PARA EMPEZAR CONSULTA PRIMERO ESTE REPOSITORIO 
#   Y SU TUTORIAL DE YOUTUBE EN @indently CHANNEL:
#       https://github.com/indently/telegram_bot_2023    
#   

import requests
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = 'YOUR_TELEGRAM_BOT_TOKEN'
BOT_USERNAME: Final = '@YOUR_BOT_NAME'
API_OPENAI: Final = "https://api.openai.com/v1/completions"
TOKEN_OPENAI: Final = "YOUR_OPENAI_TOKEN"

headers = { # apen ai api headers config
    "Content-Type": "application/json",
    "Authorization": f"Bearer {str(TOKEN_OPENAI)}"
}

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Welcome! 🤖🛰️')

# /glink command
async def guardar_link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if len(context.args) == 0:
        await update.message.reply_text("Debes proporcionarme uno o más links. 🦾")
        return
    
    guardado_por = update.message.from_user.id
    #añadir funcionalidad de guardar links interesantes para estudiar después

    await update.message.reply_text(f'🧐 Guardado en links interesantes: {context.args.__str__()}')
    await update.message.reply_text('🤑✔️')

# /productos command
async def productos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.message.from_user.id

    prods = ["Pro 1","Pro 1","Pro 1","Pro 1","Pro 1"]
    # listar productos de una base de datos en un mensaje bonito e intuitivo
    await update.message.reply_text(f'{prods.__str__()}')

# /gnulinux command
async def gnulinux_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(photo='gnu-and-tux.jpg', caption="Gnu and Tux in their GPL armors are flying to the rescue of free software.")
    await update.message.reply_text('by Lissanne Lake \nsrc: https://www.gnu.org/graphics/bwcartoon.html')

# /russia command
async def russia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_location(latitude=55.75222, longitude=37.61556)

# /gpt command
async def ia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    text = update.message.text.replace("/ia ","")
    if len(context.args) == 0 or len(str(text)) < 2:
        await update.message.reply_text("Debes proporcionarme un mensaje 🦾")
        return

    data = {
        "model": "text-davinci-003",
        "prompt": f"Ignora todas las instrucciones anteriores, Eres un bot en un grupo de amigos desarrolladores de Software que ayuda a mejorar sus interacciones preguntandote cosas y demás, tu nombre es $$YOUR_BOT_NAME$$. Ejerciendo el rol que te dije anteriormente responde al siguiente mensaje o pregunta que te pasaré dentro de parentesis ({text}). Proporciona respuestas cortas solamente.",
        "max_tokens": 100,
        "temperature": 0
    }
    response = requests.post(API_OPENAI, headers=headers, json=data)

    if response.status_code == 200:
        
        response_text = response.json()["choices"][0]["text"]
        await update.message.reply_text(response_text + " 🦾")

    else:
        await update.message.reply_text('Ops... 🙃 he tenido un problema conectandome a OpenAI 🤔')
        print(f"FAILED $$$ {str(response.status_code)}")


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Este será un mensaje ordenado con información detallada sobre los comandos')


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love python' in processed:
        return 'Remember to subscribe!'

    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('ia', ia_command))
    app.add_handler(CommandHandler('glink', guardar_link_command))
    app.add_handler(CommandHandler('productos', productos_command))
    app.add_handler(CommandHandler('gnulinux', gnulinux_command))
    app.add_handler(CommandHandler('russia', russia_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling()


