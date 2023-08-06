import time
from os import system, name
import sys
class classA:

    def print_on_screen(self, x, y, string):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, string))
        sys.stdout.flush()

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def toString(self, data):
        if isinstance(data, str):
            return 'Riley Utils Converting Error: Cannot convert type \'str\' to type \'str\'!'
        else:
            data = str(data)
            return data

    def toInt(self, data):
        if isinstance(data, int):
            return 'Riley Utils Converting Error: Cannot convert type \'int\' to type \'int\'!'
        else:
            data = int(data)
            return data

    def red(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[31m' + string
            return string

    def blue(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[34m' + string
            return string

    def green(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[32m' + string
            return string

    def yellow(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[33m' + string
            return string

    def reset(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[0m' + string
            return string

    def cyan(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[36m' + string
            return string

    def magenta(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[35m' + string
            return string

    def black(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[30m' + string
            return string

    def bold(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[1m' + string
            return string

    def underline(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Color Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[4m' + string
            return string

    def reverse(self, string):
        if not isinstance(string, str):
            return 'Riley Utils Atributes Error: Can only add color to type \'str\'!'
        else:
            string = '\u001b[1m' + string
            return string

    # ADD BACKGROUND COLORS BEFORE RELEASE

    def delchar(self, x, y):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, ' '))
        sys.stdout.flush()

    def loadingCounter(self, secs):
        print("Loading...")
        for i in range(0, 100):
            time.sleep(secs / 100)
            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.flush()
            time.sleep(secs / 100)
            sys.stdout.write(str(i + 1) + "%")
            sys.stdout.flush()
        print()

    def move_cursor(self, x, y):
        print('\033[' + str(x) + ';' + str(y) + 'H')

    def beep(self):
        print('\a')

    def lookfor(self, mainstring, searchstring):
        foundit = False
        if not isinstance(mainstring, str) or not isinstance(searchstring, str):
            print('Riley Utils Error: in \'lookfor()\' statement both inputs have to be a string!')
        else:
            for i in mainstring:
                if i == searchstring:
                    foundit = True
            if foundit == True:
                return True
            else:
                return False