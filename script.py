from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import traceback
import random
import time


#error logging + main program
try:
    #ouvrir quizlet sur un navigateur et tralalilala
    def initialisation():        
        #Regarde si on a un driver firefox ou chrome et adapte le programme en accordance
        global driver
        try:
            driver = webdriver.Chrome()
        except:
            driver = webdriver.Firefox()


        #ouvre la page principale
        driver.get('https://quizlet.com/login?redir=https://quizlet.com/latest')

        #connexion à quizlet
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )

            #ouvre les fichiers où les identifiants sont stockés et les entre la où il faut :)
        text = open("user_info.txt", "r").read()
        
        username = str(text.partition(";")[0])
        username = str(username.partition('"')[2])
        username = str(username.partition('"')[0])

        password = str(text.partition(";")[2])
        password = str(password.partition('"')[2])
        password = str(password.partition('"')[0])

        element = driver.find_element_by_id('username')
        element.send_keys(username)
        element = driver.find_element_by_id('password')
        element.send_keys(password)
        element.send_keys(Keys.RETURN)

        #ouvrir une liste
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="UserLink-content"]//a'))
        )
        drivery = driver.find_element_by_class_name('DashboardPage')
        drivery = drivery.find_elements_by_class_name('UIContainer')
        drivery = drivery[1] #[1] est celui qu'on veut, les deux autres sont inutiles.
        drivery = drivery.find_elements_by_class_name('UILink')
        
        #trouver le liens des listes affichés
        def testlink():
            for i in range (0,len(drivery)-1):
                text = drivery[i].text
                textlink = drivery[i].get_attribute('href')

                if ((i%3) == 0) and (i>0):
                    text = "link"

                if (text == ""):
                    text = "image"

                print(i,text,"\n",textlink,"\n")

        link_list = []
        for i in range (0,len(drivery)-1):
            if (i%3 == 0) and (i != 0):     #Les liens vers les listes sont tous des multiples de 3 comme mis en évidence par testlink()
                link_list += [i]
                        
        quizz_todo = random.choice(link_list)
        quizzlink = drivery[3].get_attribute('href')

        driver.get(quizzlink)

        #fermer le foutu popup de ses morts.
        element = WebDriverWait(driver,20).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="UIModal-closeButtonWrapper"]//div'))
        )
        element = driver.find_element_by_class_name('UIModal-closeButton').click() #cliquer sur la croix pour fermer le popup de ces morts

        #commencer la liste
            #compte le nombre d'éléments dans la liste
        element = WebDriverWait(driver,20).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="CardsList-navControl progressIndex"]//span'))
        )
        cards_count = driver.find_element_by_xpath('//div[@class="CardsList-navControl progressIndex"]//span').text

        cards_max = int(cards_count.partition("/")[2])
        cards_number = int(cards_count.partition("/")[0])

        time.sleep(1)

        info = driver.find_elements_by_xpath('//div[@class="SetPageTerm-content"]//div//a//span')

            #stocke les Questions / réponses
        global answers 
        answers = []    
        for i in range(0,(cards_max)*2):
            info_text = info[i].text
            answers += [info_text]
        print(answers)

            #clique sur la flèche à droite pour aller vers le truc pour apprendre la tu sais le truc laaaa
        for i in range (0, cards_max):
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="CardsList-navControl nextButton"]//span//button//span'))
            )
            element.click()
        
            #Commencer le mode apprendre
        element = driver.find_element_by_xpath('//div[@class="UIDiv CardsEnd-upsellCtas"]//a//span').click()
        element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="OnboardingView-gotItButton"]//button//span'))
        )
        element = driver.find_element_by_xpath('//div[@class="OnboardingView-gotItButton"]//button//span').click()

    def QNA():
        question = driver.find_element_by_xpath('//div[@class="FormattedTextWithImage"]//div//div').text
        i = 0
        while answers[i] != question:
            i += 1
        element = driver.find_element_by_xpath('//div[@class="AutoExpandTextarea-wrapper"]//textarea')
        element.send_keys(answers[(i-1)])
        element = driver.find_element_by_xpath('//div[@class="TypeTheAnswerField-actions"]//button//span').click()
        time.sleep(3)

    def QCM():
        question = driver.find_element_by_xpath('//div[@class="FormattedTextWithImage"]//div//div').text
        possible_answer = driver.find_elements_by_xpath('//div[@class="MultipleChoiceQuestionPrompt-termOptions"]//div//div//div//div')
        i = 0
        while answers[i] != question:
            i += 2
        k = 0
        while possible_answer[k].text != answers[(i-1)]:
            k += 1
        element = driver.find_element_by_xpath('//div[@class="MultipleChoiceQuestionPrompt-termOptions"]//div//div//div//div[@aria-label="'+possible_answer[k].text+'"]').click()
        time.sleep(4)

    def DACCORD():
        text = driver.find_element_by_xpath('//div[@class="ScrollableViewLayout-content"]//div').click()
        time.sleep(2)
        daccord = driver.find_element_by_xpath('//div[@class="UIButtonWithKeyboardHint"]//button//span[@class="UIButton-wrapper"]').click()



    for i in range(0,100):
        initialisation()
        k = 0
        while k < 100:
            try:
                if any(driver.find_elements_by_xpath('//div[@class="MultipleChoiceQuestionPrompt-termOptions"]//div//div//div//div')):
                    print("QCM")
                    QCM()
                else:
                    try:
                        print("qna")
                        QNA()
                    except:
                        print("d'accord")
                        DACCORD()
            except:
                driver.close()  
                k = 100         
except:
    with open ("exceptions.log", "a") as logfile:
        traceback.print_exc(file=logfile)
    raise