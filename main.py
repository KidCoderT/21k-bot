import os
import logging
import schedule
import time

import dotenv
import discord
from discord.ext import pages

import src

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

logging.basicConfig(level=logging.INFO)

bot = discord.Bot()
CTX = discord.context.ApplicationContext


@bot.event
async def on_ready():
    logging.info(f"{bot.user} is ready and online!")


@bot.command(description="Login & Open the Portal")
async def login(ctx: CTX):
    logging.info(f"{ctx.author} initiated the login command.")
    await ctx.send_modal(src.LoginModel())


@bot.command(description="Logout of the Portal")
async def logout(ctx: CTX):
    logging.info(f"{ctx.author} initiated the logout command.")
    peep = src.Peeps.fetch(ctx.author.id)

    if peep is None:
        return await ctx.respond("You haven't even logged in 😑")

    await ctx.defer()
    src.Peeps.delete(ctx.author.id)
    await ctx.respond("Logged out Successfully ✅")


@bot.command(description="Current Stats")
async def stats(ctx: CTX):
    logging.info(f"{ctx.author} initiated the stats command.")
    peep = src.Peeps.fetch(ctx.author.id)

    if peep is None:
        return await ctx.respond("You haven't even logged in 😑")

    assignment_success, assignment_avg_score, attendance = peep.stats

    with src.stats_img(
        assignment_success, assignment_avg_score / 100, attendance
    ) as stats_img:
        await ctx.respond(file=discord.File(stats_img))
        # await ctx.respond(
        #     f"Assignment Success: {assignment_success[0]/assignment_success[1]}\n"
        #     f"Assignment Score: {assignment_avg_score}\n"
        #     f"Attendance: {attendance[0] / attendance[1]}\n"
        # )


@bot.command(description="User Messages")
async def messages(ctx: CTX):
    logging.info(f"{ctx.author} initiated the message command.")
    peep = src.Peeps.fetch(ctx.author.id)

    if peep is None:
        return await ctx.respond("You haven't even logged in 😑")

    await ctx.defer()

    mails = peep.mail
    step = 5

    def create_embed(page_no):
        embed = discord.Embed(title="# School Mail List\n")
        embed.add_field(name="", value="\u200B", inline=False)
        embed.set_footer(text=f"@{peep.name}")

        for email in mails[page_no * step : (page_no + 1) * step]:
            embed.add_field(
                name=email["subject"],
                value=email["date"].strftime("%Y-%m-%d %H:%M"),
                inline=False,
            )

        embed.add_field(name="", value="\u200B", inline=False)
        return embed

    embed_pages = [create_embed(i) for i in range((len(mails) // step))]

    page_buttons = [
        pages.PaginatorButton("first", emoji="⏪", style=discord.ButtonStyle.green),
        pages.PaginatorButton("prev", emoji="⬅", style=discord.ButtonStyle.green),
        pages.PaginatorButton(
            "page_indicator", style=discord.ButtonStyle.gray, disabled=True
        ),
        pages.PaginatorButton("next", emoji="➡", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", emoji="⏩", style=discord.ButtonStyle.green),
    ]

    paginator = pages.Paginator(
        pages=embed_pages,  # type: ignore
        show_disabled=True,
        show_indicator=True,
        use_default_buttons=False,
        custom_buttons=page_buttons,
        loop_pages=True,
    )

    await paginator.respond(ctx.interaction, ephemeral=True)


@bot.command(description="Sends the bot's latency.")
async def ping(
    ctx: CTX,
):
    logging.info(f"{ctx.author} initiated the ping command.")
    await ctx.respond(f"Namaste! Latency is {bot.latency}")


bot.run(token)
