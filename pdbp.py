# Python DataBase Panel(PDBP)

'''
About PDBP:
PBDP(current version 1.0-beta.1) is an open-source tool,
available on Github as jsm8946's work.

License:
This software is licensed under GNU General Public License v3.0.

Requirements: 
Python, pip, MySQL

Modules used:
sys, os, termcolor, mysql.connector, time,
datetime, random

Compatible with:
MySQL

How to use:
Run, connect and execute queries.
Also works as an executable.

Command line method:
(reference to this file) (host) (user) (pass) (db)

Credits:
(none)
'''

import sys
import os
import time
import datetime
import random

def getTime():
    currentDate = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    sinceEpoch = currentDate - epoch
    secSinceEpoch = sinceEpoch.total_seconds()
    msecSinceEpoch = round(secSinceEpoch * 1000)
    return msecSinceEpoch

startTime = getTime()

def timeElapsed():
    currentTime = getTime()
    return currentTime - startTime

def clearCmd():
    # The command is dependent on the OS.
    try:
        os.system("cls")
    except:
        os.system("clear")
    finally:
        pass

def checkPip():
    try:
        os.system("py -3 -m pip")
    except:
        print("Install pip before proceeding.")

checkPip()

def installTermcolor():
    try:
        import termcolor as tc
    except:
        os.system("py -3 -m pip install termcolor")

installTermcolor()
import termcolor as tc

GREEN = "green" # Success messages
RED = "red" # Failure messages and errors
YELLOW = "yellow" # Warnings and temporary issues
BLUE = "blue" # Instructions
MAGENTA = "magenta" # Name of this module
WHITE = "white" # Inputs
CYAN = "cyan" # Time elapsed
GRAY = "dark_grey" # Other

# "dark_grey" is GRAY on purpose.
# I always spell "gray" with an "a".

def cmdline(data, color):
    t = tc.colored(timeElapsed(), CYAN)
    line = "[" + t + "] " + tc.colored(data, color)
    print(line)

def randomDelay(bottom, top):
    delay = random.randint(bottom, top)
    time.sleep(delay / 1000)

def refresh():
    clearCmd()

    randomDelay(100, 2000)
    cmdline("PDBP", MAGENTA)

    randomDelay(50, 1000)
    cmdline("Python DataBase Panel", MAGENTA)

    randomDelay(100, 500)

refresh()

def installMySQL():
    try:
        cmdline("Checking if mysql-connector-python is installed", GRAY)
        randomDelay(200, 500)
        import mysql.connector as mysql

    except:
        cmdline("mysql-connector-python not installed. Installing.", YELLOW)
        randomDelay(1000, 5000)
        os.system("py -3 -m pip install mysql-connector-python")

    finally:
        cmdline("mysql-connector-python installed. Process can be continued.", GRAY)
        randomDelay(100, 500)

installMySQL()
import mysql.connector as mysql

def getData(text):
    t = tc.colored(timeElapsed(), CYAN)
    line = "[" + t + "] " + tc.colored(text, WHITE)
    return input(line)

def getArgvData(index, message):
    if len(sys.argv) > index:
        return sys.argv[index]
    else:
        return str(getData(message))

def getCredentials():
    # sys.argv contains all necessary Python arguments.
    # The 0th(aka. 1st) is the filename.
    # The following ones are passed like:
    # py -3 foo.py(0th) bar(1st) lorem(2nd)

    yield getArgvData(1, "Enter database host: ")
        
    port = str(getData("Enter database port(empty for 3306): "))
    if bool(port):
        yield str(port)
    else:
        yield "3306"
    
    yield getArgvData(2, "Enter database username: ")
    yield getArgvData(3, "Enter database password: ")
    db = getArgvData(4, "Enter database name(optional): ")

    if not bool(db):
        yield None
    else:
        yield db

def connect():
    global dbcon
    dbcon = None

    while not dbcon:
        host, port, user, password, base = getCredentials()
        cmdline("Connecting...", GRAY)
        randomDelay(8000, 20000)

        try:
            dbcon = mysql.connect(host = host, 
                user = user, 
                password = password, 
                database = base, 
                port = port)
        except Exception as e:
            cmdline("Error while connecting as " + user + "@" + host, RED)
            randomDelay(100, 400)
            cmdline(e, RED)
            randomDelay(200, 600)

    cmdline("Connected successfully. ", GREEN)
    randomDelay(1000, 2500)

    global cursor
    cursor = dbcon.cursor()

    if base is not None:
        cmdline("Database: " + base, BLUE)
        randomDelay(100, 200)

connect()

def abort():
    cmdline("Aborting connection...", GRAY)
    randomDelay(1000, 4000)
    dbcon = None
    cursor = None
    cmdline("Connection aborted.", GRAY)
    randomDelay(100, 500)

    connect()

def query(q):
    if q.upper() == "ABORT":
        query("COMMIT")
        abort()
        return
    elif q.upper() == "DONE":
        query("COMMIT")
        cmdline("Exiting...", GRAY)
        randomDelay(1000, 2000)
        sys.exit()
    
    try:
        if not q.upper() == "COMMIT":
            cmdline("Executing the query...", GRAY)
            randomDelay(5000, 15000)
        cursor.execute(q)
    except Exception as e:
        cmdline("Error while executing query.", RED)
        randomDelay(100, 400)
        cmdline(e, RED)
        randomDelay(100, 400)
        return
    
    if not q.upper() == "COMMIT":
        cmdline("Query successful.", GREEN)
        randomDelay(100, 400)
    for x in cursor:
        cmdline(x, BLUE)
        randomDelay(100, 200)

def main():
    while True: 
        try:      
            cmdline("Type ABORT to abort this connection.", BLUE)
            randomDelay(200, 500)
            cmdline("DONE ends the program.", BLUE)
            randomDelay(200, 500)

            q = str(getData("Enter your query here: "))
            query(q)
        except KeyboardInterrupt:
            query("COMMIT")
            sys.exit()
        except SystemExit:
            query("COMMIT")
            sys.exit()

main()
