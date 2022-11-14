import re;

class Entry:
    title = ""
    short_title = ""
    keywords = []
    text = ""
    file = ""

    def setKeywords(self, kwStr):
        for s in kwStr.split(","):
            s = s.replace(" ", "")
            if not s in self.keywords:
                self.keywords.append(s)

    def setShortTitle(self, string):
        self.short_title = string

    def setTitle(self, string):
        self.title = string

    def valid(self):
        return self.title != "" and self.short_title != "" and len(self.keywords) > 0 and self.text != "" and self.file != ""

    def printInfo(self):
        print(self.file)
        if self.valid():
            print(" * Valid: true")
        else:
            print(" * Valid: false")
        print(" * Title: " + self.title)
        print(" * Short Title: " + self.short_title)
        print(" * Keywords: " + ", ".join(self.keywords)) # the language designer must have been on drugs
        print(" * Text:\n" + self.text)
    
    def __init__(self, file):
        self.file = file
        f = open(file, "r")
        addText = 0
        lineno = 0
        self.keywords = []
        for line in f:
            ++lineno

            if addText == 1:
                self.text += line
                continue

            m = re.match("^\s*(title|short-title|keywords|text):\s*(.*)", line)
            if not m:
                continue
            
            if m[1] == "keywords":
                self.setKeywords(m[2])
            elif m[1] == "short-title":
                self.setShortTitle(m[2])
            elif m[1] == "title":
                self.setTitle(m[2])
            elif m[1] == "text":
                addText = 1
            else:
                print("Bad key at " + file + ":" + lineno)
       
        self.printInfo() 
        return
