#!/usr/bin/env python3
import os, sys, getopt, logging

from FaqBot.Command import Command

from telegram.ext import Application, CommandHandler, MessageHandler

from pathlib import Path

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# This contains the list of all commands: `/command`
# stores objects as FaqBot.Command
commands = {}

# Iterate over all command directories, and create a FaqBot.Command for each
# This in turn will iterate over all files to gather their respective FaqBot.Entrys
def loadFiles(basedir) -> None:
    base = Path(basedir)
    for cmd in base.iterdir():
        if not cmd.is_dir():
            continue
        commands[cmd.name] = Command(cmd)
    return

# Debug: Log every message
async def logMessages(update, context):
    print(update.message.text)

# This is our main entry point
def main(argv) -> None:
    # First order of business is argument parsing. We use getopt for that
    basedir = ''
    tokenfile = ''

    try:
        opts, args = getopt.getopt(argv, "b:t:", ["basedir=", "token="]);
    except getopt.GetoptError:
        print(sys.argv[0] + " -d path/to/faq-basedir -t tokenfile")
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-b", "--basedir"):
            basedir = arg
        elif opt in ("-t", "--token"):
            tokenfile = arg

    # Make sure we got all relevant parameters
    if basedir == '':
        print("Please pass a basedir using -b")
        sys.exit(1)

    if tokenfile == '':
        print("Please pass a tokenfile using -t")
        sys.exit(1)

    # Load the Commands + their Entries
    loadFiles(basedir)

    # Open the token file (the intention is to hide the token from the command line)
    tokenF = open(tokenfile, "r")
    token = tokenF.read().replace("\n", "")

    # Prepare the actual bot
    app = Application.builder().token(token).build()

    #app.add_handler(MessageHandler(None, logMessages, block=False))
    # register the handler for each `/cmd`
    for cmd in commands:
        app.add_handler(CommandHandler(cmd, commands[cmd].handler))

    # And start the actual bot.
    # We just quit on ctrl+d (or if the unit file tells us to)
    app.run_polling()

# Start the actual program
if __name__ == '__main__':
    main(sys.argv[1:])
