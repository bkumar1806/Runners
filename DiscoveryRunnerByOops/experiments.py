class experiemnt:
    def __init__(self):
        self.user = "ram"

    def printtext(self):
        def printt():
            print(self.user)

        printt()


exp = experiemnt()
exp.printtext()