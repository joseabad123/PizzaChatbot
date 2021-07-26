from os import name
from telegram.ext import *
import logging
import ConsultaDBPedia as dbpedia
import ConsultaLoxaPizza as botLoxa
import ResponseOwl as RespOwl
import Respuesta

# Set up the logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

# Message error


def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')


def menu_command(update, context):
    update.message.reply_text("Bienvenid@ a la galaxia de las Pizzas",
                              reply_markup=RespOwl.main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text="Bienvenid@ a la galaxia de las Pizzas",
                            reply_markup=RespOwl.main_menu_keyboard())


def first_menu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="¿Qué tipo de pizza deseas?",
        reply_markup=RespOwl.first_menu_keyboard())


def first_submenu(update, context):
    query = update.callback_query
    query.edit_message_text(
        text="Le gustaría ordenar esta pizza?",
        reply_markup=RespOwl.first_submenu_keyboard())

# Options

def help_command(update, context):
    update.message.reply_text(
        "LoxaPizzaBot permite realizar pedidos y crear pizzas con base a ingredientes de tu elección!"
        "\n\nYo seré tu asistente de Loxa Pizza y te apoyare en todo tu recorrido"
        )


def ingredients_command(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text(
        "Los ingredientes de  " + user_says + " son:\n\n"+dbpedia.get_response_dbpedia_ingredients(user_says.capitalize()))


def pizza_command(update, context):
    update.message.reply_text(
#        "Puedes encontrar información de las siguientes pizzas :"
#        "\nNeapolitan_pizza"
    )


def start_command(update, context):
    update.message.reply_text(
        'Hola, yo seré tu asistente:\n\nUtilizando la información de DBpedia y de Loxa Pizza')
    update.message.reply_text(
        "Puedes usar las siguientes opciones:\n"
        "\n/menu -> Menú"
        "\n/listPizzaDb Lista de pizzas de DBpedia"
        "\n/listPizzaLoxa -> Lista de pizzas de Loxa Pizza"
        "\n/pizza -> Lista de las pizzas que se puede buscar"
        "\n/ingredientes -> lista de los ingredientes de la pizza"
        "\n/infomacion -> Preguntas frecuentas"
        )


def types_command_dbpedia(update, context):
    qres = dbpedia.get_response_dbpedia_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name, comment, image_url = result['name']['value'], result['comment']['value'], result['image']['value']
        update.message.reply_text('Nombre de la pizza : ' + name +
                                  "\n\nDescripción : " + comment + "\n" + image_url)


def types_command_botLoxa(update, context):
    qres = botLoxa.get_response_pizzas()
    for i in range(len(qres['results']['bindings'])):
        result = qres['results']['bindings'][i]
        name = result['name']['value']
        update.message.reply_text('Nombre de la pizza : ' + name)


def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    listNoun = []
    listVerb = []

    '''doc = analysis.spacy_info(text)
    for w in doc:
        update.message.reply_text(
            w.text + " es un " + w.pos_ + " lemma: " + w.lemma_)
        if w.pos_ == "NOUN":
            print("NOUN " + w.text)
            listNoun.append(w.text)
        if w.pos_ == "VERB":
            print("VERB " + w.text)
            listVerb.insert(0, w.lemma_)
    '''

    response = Respuesta.get_response(listVerb[0])
    if (response):
        update.message.reply_text("Tu requerimiento es :")
        for list in listNoun:
            if list == "pizza":
                update.message.reply_text(
                    " -  \""+list+"\" :\n"+dbpedia.get_response_dbpedia(list.capitalize()))
            else:
                temp = "pizzas que contiene " + list + " :\n"
                qres = dbpedia.get_response_dbpedia_food(list)
                for i in range(len(qres['results']['bindings'])):
                    result = qres['results']['bindings'][i]
                    label = result['label']['value']
                    temp += "\n - " + label

                update.message.reply_text(temp)

    else:
        text = "No se comprendió el mensaje\n\nUsaste las siguientes intenciones :\n"
        for w in listVerb:
            temp = " - " + w + "\n"
            text += temp
        text += "\n(Por favor usa una única acción)"
        update.message.reply_text(text)

if __name__ == '__main__':
    updater = Updater(token="1777762186:AAFGLWBxCqnAZjs788MNQn2FRTcNVAMRMB4", use_context=True)

    dp = updater.dispatcher

    # Commands
    # dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('menu', menu_command))
    dp.add_handler(CommandHandler('listPizzaDb', types_command_dbpedia))
    dp.add_handler(CommandHandler('listPizzaLoxa', types_command_botLoxa))
    dp.add_handler(CommandHandler('pizza', pizza_command))
    dp.add_handler(CommandHandler('ingredientes', ingredients_command, pass_args=True))
    dp.add_handler(CommandHandler('infomacion', help_command))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()