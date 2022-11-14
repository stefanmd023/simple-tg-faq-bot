from FaqBot.Entry import Entry
from telegram import ParseMode

class Command:
    cmddir = ""
    keywords = {}
    entries = []

    def __init__(self, cmddir):
        self.cmddir = cmddir
        self.keywords = {}
        self.entries = []
        for file in cmddir.iterdir():
            e = Entry(file)
            self.entries.append(e)
            for kw in e.keywords:
                if kw in self.keywords:
                    self.keywords[kw].append(e)
                else:
                    self.keywords[kw] = [e]
        self.printInfo()

    def printInfo(self):
        print(self.cmddir)
        for kw in self.keywords:
            l = []
            for e in self.keywords[kw]:
                l.append(e.short_title)
            print(" * " + kw + ": " + ", ".join(l))

    def handler(self, update, context):
        kwListA = update.message.text.split(" ")
        if len(kwListA) == 1:
            update.message.reply_text("Please give a list of space-separated keywords to find entries matching ALL keywords (logical-and).\nKnown keywords: " + ", ".join(self.keywords))
            return
        kwList = []
        for x in kwListA[1:]:
            for y in x.split(","):
                kw = y.replace(" ", "")
                if kw == "":
                    continue
                if kw in kwList:
                    continue
                kwList.append(kw)

        found = []
        for e in self.entries:
            match = 1
            for kw in kwList:
                if not kw in e.keywords:
                    match = 0
            if match == 1:
                found.append(e)

        if len(found) == 0:
            update.message.reply_text("Nothing found. To get a list of keywords use /" + self.cmddir.name)
            return

        reply = ""
        for e in found:
            reply += "<i><b>" + e.title + "</b></i>\n"
            reply += e.text
        
        update.message.reply_text(text=reply, parse_mode=ParseMode.HTML)
