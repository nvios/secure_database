import sqlite3
import base64
import imageio
import cv2
from hashlib import sha256
from getpass import getpass

def main():
  db = sqlite3.connect('./safe.db')
  c = db.cursor()

  try:
    c.execute('CREATE TABLE SECRETS (PASSWORD VARCHAR(255) PRIMARY KEY NOT NULL);')
    psw = (sha256(getpass('Please create a new password: ').encode('utf-8')).hexdigest(),)
    c.execute('INSERT INTO SECRETS VALUES (?)', psw)
    db.commit()
  except:
    print('Insert your password to login.') 

  c.execute('SELECT PASSWORD FROM SECRETS')
  psw = c.fetchone()[0]
  connect = 0
  attempts = 0

  while connect == 0:
    if attempts > 2:
      break
    attempts += 1
    usr_psw = sha256(getpass().encode('utf-8')).hexdigest()
    connect = [0, 1][psw == usr_psw]
    print(["Wrong password\n", ""][connect])

  if connect == 1:
    db = sqlite3.connect('./safe.db')
    try:
      db.execute('''CREATE TABLE SAFE
          (FULL_NAME TEXT PRIMARY KEY NOT NULL,
          NAME TEXT NOT NULL,
          EXTENSION TEXT NOT NULL,
          FILES TEXT NOT NULL);''')
      print("Your safe has been created!\nYou can use it to store passwords, text documents and images")
    except:
      print("You have a safe, what would you like to do today?")

    while True:
      print("\n" + "*" * 25)
      print("*  Commands:            *")
      print("*  q = Quit program     *")
      print("*  o = Open file        *")
      print("*  s = Store file       *")
      print("*  u = Update password  *")
      print("*" * 25 + "\n")
      input_ = input(">>> ")

      if input_ == "q":
        print("\nBye!\n")  
        break
      if input_ == "o":
        file_name = input("\nWhat is the name of the file you want to open?\n")

        cursor = db.execute('SELECT * from SAFE WHERE FULL_NAME = ?', file_name)

        file_string = ""
        for row in cursor:
          file_string = row[3]
        with open(file_name, 'wb') as f_output:
          print(file_string)
          f_output.write(base64.b64decode(file_string))

      if input_ == "s":
        folder = '/Users/luca/Documents/Programming/Automation Scripts/Sqlite Database/'
        PATH = folder + input("\nType the name of the file you want to store (e.g. MyFile.txt)\n")

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
          file_string = open(PATH, "br").read()
          file_string = base64.b64encode(file_string)

        VALUES = [(file_name),(NAME),(EXTENSION),(file_string)]

        db.execute('INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (?,?,?,?)', VALUES)
        db.commit()
        print('\nYou have successfully saved your file to the database!')

      if input_ == "u":
        psw = (sha256(getpass('\nPlease create a new password: ').encode(
            'utf-8')).hexdigest(),)
        db.execute('UPDATE SECRETS SET PASSWORD = ? ', psw)
        db.commit()
        print('\nYou have successfully created a new password!')

if __name__ == "__main__":
  main()
