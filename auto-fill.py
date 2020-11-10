from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random
import config
import time
emails = []

max_iterations = 10

class Votant:
    def __init__(self) :
        self.name = generate_name()
        self.zipCode = generate_zipCode()
        self.mail = None

    def display(self) :
        if self.isValid == False : return "None"
        nn = self.name[0] + " " + self.name[1]
        return """USER: """ + nn + """
    -> zip code : """+ str(self.zipCode) + """
    -> email : """+ str(self.mail) + """
        """

    def isValid(self) :
        for addr in emails :
            if addr == self.mail : return False
            else : continue
        
        return True

def verify_email(addr) :
    for mail in emails :
        if addr == mail :
            return False

    return True

def generate_name() :
    return [random.choice(config.firstnames), random.choice(config.names)]

def generate_zipCode() :
    departement = random.randint(10,90)
    zipCode = random.randint(100,999)

    return int(str(departement) + str(zipCode))

def mail_manager(drive) :
    drive.get('https://generator.email/')
    new_addr = drive.find_elements_by_class_name('btn')[1]
    new_addr.click()

    addr = drive.find_element_by_id('email_ch_text').text

    if addr == "" :
        print("ERROR GETTING THE EMAIL ADDR")
    else :
        print("LOG : Address is set to", addr)
        if verify_email(addr) : 
            emails.append(addr)
            return addr
        
        return None

def vote(drive, mail) :
    drive.get('https://noussommespour.fr/')
    votant = Votant()
    votant.mail = mail

    print("LOG : Setting up voter")

    if True or votant.isValid() :
        print("LOG : Voter is valid")
        try :
            print("LOG : starting completion loop")
            firstname_tf = drive.find_element_by_id('form-field-first_name')
            name_tf = drive.find_element_by_id('form-field-last_name')
            email_tf = drive.find_element_by_id('form-field-email')
            zip_tf = drive.find_element_by_id('form-field-location_zip')

            if firstname_tf == None or name_tf == None or email_tf == None or zip_tf == None :
                return False

            submit_button = drive.find_elements_by_class_name('elementor-button')[0]

            print("-> fn")
            firstname_tf.click()
            firstname_tf.send_keys(str(votant.name[0]))

            print("-> sn")
            name_tf.click()
            name_tf.send_keys(str(votant.name[1]))

            print("-> ml")
            email_tf.click()
            email_tf.send_keys(str(votant.mail))

            print("-> zp")
            zip_tf.click()
            zip_tf.send_keys(str(votant.zipCode))

            print("-> btn")
            submit_button.click()
            print(votant.display())

            return True
        except Exception as err:
            print("ERROR", err)
            time.sleep(0.5)
            return False

        except : print("ERROR")

    else : return False

def verify_petition(drive, mail) :
    drive.get('https://generator.email/')
    print("LOG : connected to e-mail generator website")

    time.sleep(4)
    print("LOG : Correct sender")
    link = ""
    index = 0
    while link == "" :
        index += 1
        try :
            messages = drive.find_elements_by_tag_name('center')

            if len(messages) > 0 :
                link = messages[0].find_elements_by_tag_name('a')[0]
                link.click()
                print("LOG : VERIFIED")
                drive.switch_to_window('Nous Sommes Pour – Jean-Luc Mélenchon 2022')
                drive.close()
            else :
                if index % 100 == 0 : print("ISSUE : Message has not arrived yet")
                if index >= 1000 :
                    print("ERROR : Abort message receiving mission -> timeout")
                    return None
                link = ""
        except Exception as err:
            print("ERROR : ", err)
            return None

def register() :
    drive = webdriver.Chrome('./chromedriver')
    index = 0
    n_err = 0

    Log_file = open("voting_logs.txt", 'w')
    Log_file.write("VOTING LOGS\n")
    Log_file.close()

    while True :
        index += 1
        print("==========[CYCLE", str(index) + "]==========")
        addr = mail_manager(drive)
        err = True
        if not (addr == "" or addr == None) :
            print("LOG : Begin vote")
            vt = vote(drive, addr)
            if vt == True :
                verify_petition(drive, addr)
                err = False
            else : print("ERROR : e-mail is empty")
        #vote(drive)

        Log_file = open("voting_logs.txt", "a")
        if not err :
            Log_file.write("VOTED : " + str(datetime.now()) + " for error rate of " + str((n_err/index) * 100) + "%\n")
        else :
            n_err += 1
            Log_file.write("ERROR : " + str(datetime.now()) + " for error rate of " + str((n_err/index) * 100) + "%\n")
        Log_file.close()

register()
input()