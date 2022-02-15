import discord
import os
# import sys
# import subprocess
# from email import message
# from operator import le
# import string
# from attr import NOTHING
# import schedule
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import schedule

# check_notif = __import__('check_notif')

TOKEN = os.environ.get('TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


def check_notif():
    CHROMEDRIVER_PATH = Service(
        "./chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.headless = True
    global username
    global password

    username = username.content
    password = password.content

    driver = webdriver.Chrome(
        service=CHROMEDRIVER_PATH, options=options)
    driver.get("https://www.21kschool.in/#portal/80/")
    var = 0

    # Log in To Website
    username_textbox = driver.find_element(By.NAME, "t_username")
    username_textbox.send_keys(username)

    password_textbox = driver.find_element(By.NAME, "t_password")
    password_textbox.send_keys(password)
    login_button = driver.find_element(By.NAME, "t_login")
    login_button.click()
    while True:
        time.sleep(1)
        alert = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[6]/a[6]/span").text
        var = 0
        if int(alert) >= 1:
            try:
                # get the number of messages unread (alert.text)

                # if int(alert) > var:
                #     var = int(alert)
                var = int(alert)
                time.sleep(3)
                driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[6]/a[6]").click()

                time.sleep(3)
                driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[3]/div/ul[1]/li[1]/div").click()

                time.sleep(3)
                # finds the parent element of all text
                conversation = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[3]/div[1]/form/div[2]/div/div[2]/div/div[3]")

                # get the title of the message
                message_title = driver.find_element(
                    By.CLASS_NAME, "messages-msg-title").text.strip()

                # get the sender of the message

                message_sender_and_recipient = driver.find_element(
                    By.CLASS_NAME, "messages-msg-msg-title").text.strip()

                message_sender = message_sender_and_recipient.split("(", 1)[
                    0]

                # get the contents of the message
                convo_text = conversation.find_elements(
                    By.XPATH, "./child::*")

                message = []
                message_again = ''''''

                for i in convo_text:
                    message.append(i.text)

                for x in message:
                    if x == " ":
                        x = "\n"
                    message_again += (x + "\n")

                whole_message = (f'''**Title:** {message_title.lstrip()}\n**From:** {message_sender.lstrip()}\n**Message:**\n{message_again.strip()}
                    ''')
                # for number in range(0, len(variable)):
                #     print(variable[number])
                # return variable
                return whole_message

                # elif int(alert.text) < var:
                #     break
                # else:
                #     break

        # This error occurs when there are no notifs
            except NoSuchElementException:
                var = 0
                return None
                break


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!setup"):
        global username
        global password
        await message.channel.send("Enter you're username: ")
        username = await client.wait_for('message')

        await message.channel.send("Enter you're password: ")
        password = await client.wait_for('message')

    if message.content.startswith("!start"):
        # notif = schedule.every(30).seconds.do(check_notif)
        await message.channel.send(
            f"{username.author.mention} \n" + check_notif())
        print("check 1")
        # await message.channel.send(f"{username.author.mention} \n" + check_notif())


client.run(TOKEN)
