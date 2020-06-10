import sqlite3
import base64
import imageio
import cv2
from hashlib import sha256
from getpass import getpass

#psw = sha256('1234'.encode('utf-8')).hexdigest()
psw = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
connect = 0
attempts = 0

while connect == 0:
  if attempts > 4:
    break
  attempts += 1
  usr_psw = sha256(getpass().encode('utf-8')).hexdigest()
  connect = [0, 1][psw == usr_psw]
  print(["Wrong password\n", "\n"][connect])

if connect == 1:
    db = sqlite3.connect('./safe.db')
    try:
        db.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print("\n" + "*"*15)
        print("Commands:")
        print("q = quit program")
        print("o = open file")
        print("s = store file")
        print("*"*15 + "\n")
        input_ = input(">>> ")

        if input_ == "q":
          print("Bye!")  
          break
        if input_ == "o":
          # open the file
          file_name = input("What is the name of the file you want to open?\n")

          cursor = db.execute(
            f"SELECT * from SAFE WHERE FULL_NAME={file_name}")

          file_string = ""
          for row in cursor:
            file_string = row[3]
          with open(file_name1234, 'wb') as f_output:
            print(file_string)
            f_output.write(base64.b64decode(file_string))

        if input_ == "s":
          # store file
          PATH = input(
            "Type in the full path to the file you want to store.\nExample: /Users/Myname/Desktop/Myfile.doc\n")

          FILE_TYPES = {
            "txt": "TEXT",
            "java": "TEXT",
            "dart": "TEXT",
            "py": "TEXT",
            "jpg": "IMAGE",
            "png": "IMAGE",
            "jpeg": "IMAGE"
          }

          file_name = PATH.split("/")[-1]
          file_string = ""

          NAME = file_name.split(".")[0]
          EXTENSION = file_name.split(".")[1]

          try:
            EXTENSION = FILE_TYPES[EXTENSION]
          except:
            Exception()

          if EXTENSION == "IMAGE":
            IMAGE = cv2.imread(PATH)
            file_string = base64.b64encode(
              cv2.imencode('.jpg', IMAGE)[1]).decode()

          elif EXTENSION == "TEXT":
            file_string = open(PATH, "r").read()
            file_string = base64.b64encode(file_string)

          command = f'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES ({file_name},{NAME},{EXTENSION},{file_string});'

          db.execute(command)
          db.commit()
