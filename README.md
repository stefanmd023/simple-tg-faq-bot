# About

This is a simple FAQ bot for telegram, written in python.

# Usage

To create a bot, just create a folder structure:

`<some_name>/<bot_command>/<parameter>.txt`

Then, into the `<parameter>.txt`, put something like this (we go into details later):

```
# The keywords tell the bot under what keywords this should show up
keywords: read-only, ro, tmp

# The long title, given in bold
title: Can not write to '...' (Read-only file system)

# A short title, not used right now, but make it unique ;-)
short-title: read-only

# Optionally, you can also add an image. The file path is relative to the text file:
img: my-image.jpg

# Everything after the "text" line will be the actual article.
text:
The file can not be written to the current directory (probably "/").
Do a "cd /tmp" to get to a location you can write to.
```

Each such file is an article that can be found by sending the bot `/<bot_command>`.

You may put this into a simple file system structure `examplebot/faq/cdtmp.txt`, and your Telegram bot token into a file `token.txt` (e.g. `2143214321:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`).

Start the bot via

`python faqbot.py -b examplebot/ -t token.txt`

Now once you start a conversation with the bot, you can send it `/faq` and it will list all the keywords it knows.
You can get a specific article by querying `/faq ro` (`ro` was one of the example keywords).

# TODO

1. List dependencies (mostly `python-telegram-bot`)
2. Produce an Arch Linux `PKGBUILD`
3. Give an example bot dir structure
4. Make single articles better referenceable (e.g. via `/something short-title`)
5. Allow generation of FAQ pages (that's what the `short-title`s are intended for!)
