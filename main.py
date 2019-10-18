from telegram.ext import Updater, Filters, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler
import logging

from app import constants, handlers, filters
import config


# set logging
logging.basicConfig(
    format='%(asctime)s – %(levelname)s – %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

# create updater and dispatcher
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher


def setup_service_handlers():
    # handle all errors
    dispatcher.add_error_handler(handlers.handle_error)

    # handle command /admin and provide admin panel
    dispatcher.add_handler(CommandHandler(
        command=constants.admin_command,
        filters=Filters.user(user_id=config.admins) & Filters.private,
        callback=handlers.handle_admin
    ))

    # reboot the bot
    dispatcher.add_handler(CallbackQueryHandler(
        pattern=constants.reboot_callback,
        callback=handlers.handle_reboot
    ))

    # send mailing form
    dispatcher.add_handler(CallbackQueryHandler(
        pattern=constants.mailing_callback,
        callback=handlers.handle_mailing
    ))

    # send statistics about the bot
    dispatcher.add_handler(CallbackQueryHandler(
        pattern=constants.statistics_callback,
        callback=handlers.handle_statistics
    ))


def setup_mailing_handlers():
    # cancel adding content to mailing message
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.regex(constants.cancel_adding_button) & filters.adding_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_cancel_adding
    ))

    # cancel mailing and delete the data
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.regex(constants.cancel_mailing_button) & filters.mailing_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_cancel_mailing
    ))

    # send mailing message to everyone
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.regex(constants.send_mailing_button) & filters.mailing_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_send_mailing
    ))

    # send preview of the mailing message
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.regex(constants.preview_button) & filters.mailing_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_preview
    ))

    # set state before adding to the mailing message
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.regex(constants.add_content_button) & filters.mailing_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_add_content
    ))

    # add content to the mailing message
    dispatcher.add_handler(MessageHandler(
        filters=((Filters.text | Filters.photo) & filters.adding_filter
                 & Filters.user(user_id=config.admins) & Filters.private),
        callback=handlers.handle_mailing_content
    ))


def setup_menu_handlers():
    # handle cat button
    dispatcher.add_handler(MessageHandler(
        filters=Filters.regex(constants.animals_button),
        callback=handlers.handle_animal
    ))

    # handle lang button
    dispatcher.add_handler(MessageHandler(
        filters=Filters.regex(constants.lang_button) & Filters.private,
        callback=handlers.handle_change_lang
    ))

    # handle send button
    dispatcher.add_handler(MessageHandler(
        filters=Filters.regex(constants.send_button) & Filters.private,
        callback=handlers.handle_send_to_friend
    ))


def setup_inline_handlers():
    # handle inline language button
    dispatcher.add_handler(CallbackQueryHandler(
        pattern=constants.lang_inline_button,
        callback=handlers.handle_inline_lang
    ))

    # handle inline requests
    dispatcher.add_handler(InlineQueryHandler(
        callback=handlers.handle_inline,
        pattern=constants.animals_pattern
    ))


def setup_commands_handlers():
    # handle command /start
    dispatcher.add_handler(CommandHandler(
        filters=Filters.private,
        command=constants.start_command,
        callback=handlers.handle_start
    ))

    # handle command /cat or /dog
    dispatcher.add_handler(CommandHandler(
        command=[constants.cat_command, constants.dog_command],
        callback=handlers.handle_animal
    ))


def main():
    # setup all handlers
    setup_service_handlers()
    setup_mailing_handlers()
    setup_commands_handlers()
    setup_inline_handlers()
    setup_menu_handlers()

    # setup webhook
    updater.start_webhook(
        listen=config.listen,
        port=config.port,
        url_path=config.token,
        key=config.key_path,
        cert=config.cert_path,
        webhook_url=config.webhook_url
    )

    # log the start
    logging.info('Bot has been started.')


if __name__ == '__main__':
    main()
