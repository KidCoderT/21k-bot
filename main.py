import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import dotenv
import discord
import schedule
import time

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

options = webdriver.ChromeOptions()
options.add_argument(
    f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 12_1)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/96.0.4664.110 Safari/537.36"
)
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--headless")


class StudentPortalInstance:
    MSG_DATE_FORMAT = "%d/%m/%Y %H:%M"

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome(options=options)
        self.__initialize_portal()

    def __initialize_portal(self):
        self.driver.get("https://www.21kschool.in/#portal")

        # Log in To Website
        username_textbox = self.driver.find_element(By.NAME, "t_username")
        username_textbox.send_keys(self.username)

        password_textbox = self.driver.find_element(By.NAME, "t_password")
        password_textbox.send_keys(self.password)

        login_button = self.driver.find_element(
            By.CSS_SELECTOR, "div.Button.main_button._clickable.css-uz7xs5"
        )
        login_button.click()

        self.driver.implicitly_wait(3)

    @property
    def stats(self) -> tuple[tuple[int, int], float, tuple[int, int]]:
        # fmt: off
        div_text = self.driver.find_element(By.CSS_SELECTOR, "a.chart_completed > div > div._top-progress > div").text
        assignment_success = tuple([int(num) for num in div_text.split() if num.isdigit()])
        
        assignment_avg_score = float(
            self.driver.find_element(
                By.CSS_SELECTOR,
                "a.chart_avg_score > div > div._top-progress > div > span",
            ).text
        )

        div_text = self.driver.find_element(By.CSS_SELECTOR, "a.chart_attendance > div > div._top-progress > div").text
        attendance = tuple([int(num) for num in div_text.split() if num.isdigit()])

        return assignment_success, assignment_avg_score, attendance
        # fmt: on

    @property
    def mail(self):
        # fmt: off
        def extract_mail(message_div):
            date_text = message_div.find_element(By.CSS_SELECTOR, "div._meta > span._date").text
            date = datetime.strptime(date_text, self.MSG_DATE_FORMAT)
            subject = message_div.find_element(By.CSS_SELECTOR, "div._subject").text
            body = message_div.find_element(By.CSS_SELECTOR, "div._body").text

            return {"data": date, "subject": subject, "body": body}

        self.driver.implicitly_wait(3)
        messages = self.driver.find_elements(By.CSS_SELECTOR, "div._list > div")
        return [extract_mail(message) for message in messages[::2]]
        # fmt: on


# tejas = StudentPortalInstance(username, password)
# print(tejas.stats)
# print(tejas.mail)

bot = discord.Bot()
CTX = discord.context.ApplicationContext
people: dict[int, StudentPortalInstance] = {}


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command(description="Login & Open the Portal")
async def login(ctx: CTX, username: str, password: str):
    if ctx.author.id in people:
        return await ctx.respond("You have already been logged in 😑!")

    await ctx.defer()

    student = StudentPortalInstance(username, password)
    people[ctx.author.id] = student

    await ctx.respond("Logged in Successfully ✅")


@bot.command(description="Logout of the Portal")
async def logout(ctx: CTX, password: str):
    if ctx.author.id not in people:
        return await ctx.respond("You haven't even logged in 😑!")

    if people[ctx.author.id].password != password:
        return await ctx.respond("Password mismatch")

    await ctx.defer()

    people[ctx.author.id].driver.close()
    del people[ctx.author.id]

    await ctx.respond("Logged out Successfully ✅")


@bot.command(description="Sends the bot's latency.")
async def ping(
    ctx: CTX,
):
    await ctx.respond(f"Namaste! Latency is {bot.latency}")


bot.run(token)
