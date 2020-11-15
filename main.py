#importing required modules
import os
import sys
import datetime as date


pwd = os.getcwd() + "/mods"
sys.path.insert(0, pwd)

import interface


if __name__ == "__main__":
    print("Date and time: " + str(date.datetime.now()))
    interface.ui()



