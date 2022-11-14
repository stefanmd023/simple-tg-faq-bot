#!/usr/bin/env python3
import os, sys, getopt, logging

from FaqBot.Command import Command;

from telegram.ext import (
    Updater,
    CommandHandler
)

from pathlib import Path

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

commands = {}

def loadFiles(basedir) -> None:
    base = Path(basedir)
    for cmd in base.iterdir():
        if not cmd.is_dir():
            continue
        commands[cmd.name] = Command(cmd)
    return

def main(argv) -> None:
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

    if basedir == '':
        print("Please pass a basedir using -b")
        sys.exit(1)

    if tokenfile == '':
        print("Please pass a tokenfile using -t")
        sys.exit(1)

    loadFiles(basedir)

    tokenF = open(tokenfile, "r")
    token = tokenF.read().replace("\n", "")

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    for cmd in commands:
        dispatcher.add_handler(CommandHandler(cmd, commands[cmd].handler))

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main(sys.argv[1:])
