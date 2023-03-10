# -*- coding: utf-8 -*-

import discord, asyncio, pytz, datetime
import time
import pytz
from discord.ext import commands
from datetime import datetime, timedelta

def times():
    return time.time()

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

now = datetime.now()
DISALLOWED_LINK = 'https://discord.gg/eftdolphin'
DISALLOWED_LINK2 = 'discord.gg/eftdolphin'
ALLOWED_MESSAGES_PER_HOUR = 3
ALLOWED_TIMEFRAME_HOURS = 1
tt = "๊ณต์ง์ฌํญ"
cn = 1035777248466313259
idlist = {1035777247992348704: True, 987654321: True}

user_data = {}
admin = '๐ฏ๐ป๐ด๐ณ#7777'

@bot.event
async def on_ready():
    print('login.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("ํ๋ฅด์ฝํ DLC ์ต์ ๊ฐ ๋ํ์ต"))
    for guild in bot.guilds:
        if guild.id not in idlist:  # idlist์ ์์ผ๋ฉด
            await guild.leave()  # ์๋์ผ๋ก ๋๊ฐ๊ธฐ
            print("์ด์ํ ์๋ฒ์ ์ ์๋์ด ๋๊ฐ์ต๋๋ค")
        else:
            print(f'{guild.name}์ด ์์ธ์ค ์๋ฃ ๋์์.')

@bot.event
async def on_guild_join(guild):
    if guild.id not in idlist:  # idlist์ ์์ผ๋ฉด
        await guild.leave()  # ์๋์ผ๋ก ๋๊ฐ๊ธฐ
        print("์ด์ํ ์๋ฒ์ ์ ์๋์ด ๋๊ฐ์ต๋๋ค")
    else:
        print(f'Joined {guild.name}.')  # idlist์ ์์ผ๋ฉด ๊ทธ๋๋ก ๋จธ๋ฌด๋ฅด๊ธฐ

@bot.event #๊ณ์  ์์ฑ์ผ ํํฐ
async def on_member_join(member):
    setting = '0'
    setting = int(setting)

    created = times() - member.created_at.timestamp()
    created = int(created) / 86400
    created = round(created)

    if created < setting:
        embed = discord.Embed(title='โ  ๊ณ์  ์์ฑ์ผ ๋ฏธ๋ฌ', description=f'๊ณ์  ์์ฑ์ผ์ด {setting}์ผ ๋ฏธ๋ง์ด๋ฏ๋ก **{member.guild}**์์ ์ถ๋ฐฉ๋์์ต๋๋ค')
        embed.set_footer(text=f'{admin}์ผ๋ก ๋ฌธ์์ฃผ์ธ์')
        await member.send(embed=embed)
        await member.kick(reason='๊ณ์  ์์ฑ์ผ ๋ฏธ๋ฌ')

@bot.event 
#์๋ฉ ๋ฐฉ์ง๊ธฐ
async def on_message(message):
    global cn
    global tt
    if message.author == bot.user:
        return

    author_id = message.author.id

    # ์ฌ์ฉ์ ๋ฐ์ดํฐ๊ฐ ์์ผ๋ฉด ์ด๊ธฐํํฉ๋๋ค.
    if author_id not in user_data:
        user_data[author_id] = {
            'message_count': 0,
            'last_message_time': datetime.now()
        }

    # ํ์ฌ ์๊ฐ๊ณผ ๋ง์ง๋ง ๋ฉ์์ง ์ ์ก ์๊ฐ์ ๋น๊ตํ์ฌ ์๊ฐ ์ฐจ์ด๋ฅผ ๊ณ์ฐํฉ๋๋ค.
    last_message_time = user_data[author_id]['last_message_time']
    time_diff = datetime.now() - last_message_time

    # ๋ฉ์์ง๋ฅผ ๋ณด๋ธ ์๊ฐ์ด 1์๊ฐ ์ด์ ์ง๋ ๊ฒฝ์ฐ ๋ฉ์์ง ์นด์ดํธ๋ฅผ ์ด๊ธฐํํฉ๋๋ค.
    if time_diff > timedelta(hours=ALLOWED_TIMEFRAME_HOURS):
        user_data[author_id]['message_count'] = 0

    # ๋ฉ์์ง์ ๋งํฌ๊ฐ ์๊ณ , DISALLOWED_LINK๋ฅผ ํฌํจํ์ง ์์ผ๋ฉด ๋ฉ์์ง ์นด์ดํธ๋ฅผ ์ฆ๊ฐ์ํต๋๋ค.
    if message.content.find('http') != -1 and DISALLOWED_LINK not in message.content:
        user_data[author_id]['message_count'] += 1
        user_data[author_id]['last_message_time'] = datetime.now()
        await message.delete()
        await message.author.send(f'{message.author.mention}, '
                                      f'๋ํ์ต์์ ๋งํฌ๋ ๊ธ์ง๋ฉ๋๋ค! '
                                      f'{ALLOWED_TIMEFRAME_HOURS}์๊ฐ ์ด๋ด์ {ALLOWED_MESSAGES_PER_HOUR}๊ฐ ์ด์์ ๋งํฌ๋ฅผ ๋ณด๋ด๋ฉด '
                                      f'์๋ฒ์์ ์ถ๋ฐฉ๋นํฉ๋๋ค!.')
        if user_data[author_id]['message_count'] > ALLOWED_MESSAGES_PER_HOUR:
            await message.author.send(f'{message.author.mention}, '
                                      f'๋น์ ์ {ALLOWED_TIMEFRAME_HOURS}์๊ฐ ๋์ 'f'{ALLOWED_MESSAGES_PER_HOUR}๊ฐ ์ด์์ ๋งํฌ๋ฅผ ๋ณด๋๊ธฐ ๋๋ฌธ์ 'f'์๋ฒ์์ ์ถ๋ฐฉ๋์์ต๋๋ค.')
            await message.author.kick(reason='๋งํฌ ์ฌ์ฉ ์ ํ ์ด๊ณผ')
            return
    if message.content.find('discord.gg/') != -1 and DISALLOWED_LINK not in message.content:
        user_data[author_id]['message_count'] += 1
        user_data[author_id]['last_message_time'] = datetime.now()
        await message.delete()
        await message.author.send(f'{message.author.mention}, '
                                      f'๋ํ์ต์์ ๋งํฌ๋ ๊ธ์ง๋ฉ๋๋ค! '
                                      f'{ALLOWED_TIMEFRAME_HOURS}์๊ฐ ์ด๋ด์ {ALLOWED_MESSAGES_PER_HOUR}๊ฐ ์ด์์ ๋งํฌ๋ฅผ ๋ณด๋ด๋ฉด '
                                      f'์๋ฒ์์ ์ถ๋ฐฉ๋นํฉ๋๋ค!.')
        if user_data[author_id]['message_count'] > ALLOWED_MESSAGES_PER_HOUR:
            await message.author.send(f'{message.author.mention}, '
                                      f'๋น์ ์ {ALLOWED_TIMEFRAME_HOURS}์๊ฐ ๋์ '
                                      f'{ALLOWED_MESSAGES_PER_HOUR}๊ฐ ์ด์์ ๋งํฌ๋ฅผ ๋ณด๋๊ธฐ ๋๋ฌธ์ '
                                      f'์๋ฒ์์ ์ถ๋ฐฉ๋์์ต๋๋ค.')
            await message.author.kick(reason='๋งํฌ ์ฌ์ฉ ์ ํ ์ด๊ณผ')
            return


    # ํ์คํธ ๋ช๋ น์ด
    if message.content == '!๋ช๋ น์ด':
        await message.channel.send('ํ์คํธ')

    # ๊ณต์ง
    if message.content.startswith ("!๊ณต์ง"):
        await message.delete()
        if message.author.guild_permissions.administrator:
            notice = message.content[3:]
            channel = bot.get_channel(int(cn))
            embed = discord.Embed(title = tt, description="๊ณต์ง์ฌํญ์ด ์์ต๋๋ค!\n========================================\n\n{}\n\n========================================".format(notice), color=0x0000FF)
            embed.set_footer(text="๋ณด๋ธ์ฌ๋ : {}".format(message.author), icon_url="https://i.imgur.com/QvQRDuy.png")
            embed.set_thumbnail(url="https://i.imgur.com/QvQRDuy.png")
            await channel.send ("@everyone", embed=embed)
            await message.author.send("\n========================================\n```[ BOT ์๋ ์๋ฆผ ] | ์ ์์ ์ผ๋ก ๊ณต์ง๊ฐ ์ฑ๋์ ์์ฑ์ด ์๋ฃ๋์์ต๋๋ค : )\n\n[ ๊ธฐ๋ณธ ์์ฑ ์ค์  ์ฑ๋ ] : {}\n[ ๊ณต์ง ๋ฐ์ ์ ] : {}\n\n[ ๋ด์ฉ ]\n{}```\n========================================\n".format(channel, message.author, notice))
        else:
            await message.author.send("{}, ๋น์ ์ ๊ด๋ฆฌ์๊ฐ ์๋๋๋ค".format(message.author.mention))

    if message.content.startswith('!์ ๋ชฉ'):
        await message.delete()
        if message.author.guild_permissions.administrator:
            if len(message.content.split()) > 1:
                tt2 = message.content.split()[1]
                tt = tt2
                await message.author.send("\n========================================\n```[ BOT ์๋ ์๋ฆผ ] | ์ ๋ชฉ์ ์ ์์ ์ผ๋ก! {} ๋ก ์ค์ ํ์จ์ต๋๋ค!```\n========================================\n".format(tt))
            else:
                await message.author.send("\n========================================\n```[ BOT ์๋ ์๋ฆผ ]** | ์ ๋ชฉ์ ์๋ชป ์๋ ฅํ์จ์ต๋๋ค!```\n========================================\n")
        else:
            await message.author.send("{}, ๋น์ ์ ๊ด๋ฆฌ์๊ฐ ์๋๋๋ค".format(message.author.mention))

    if message.content.startswith('!์ฑ๋'):
        await message.delete()
        if message.author.guild_permissions.administrator:
            if len(message.content.split()) > 1:
                cn2 = message.content.split()[1]
                cn = cn2
                await message.author.send("\n========================================\n```[ BOT ์๋ ์๋ฆผ ] | ์ฑ๋์ ์ ์์ ์ผ๋ก! {} ๋ก ์ค์ ํ์จ์ต๋๋ค!```\n========================================\n".format(cn))
            else:
                await message.author.send("\n========================================\n```[ BOT ์๋ ์๋ฆผ ]** | ์ฑ๋์ ์๋ชป ์๋ ฅํ์จ์ต๋๋ค!```\n========================================\n")
        else:
            await message.author.send("{}, ๋น์ ์ ๊ด๋ฆฌ์๊ฐ ์๋๋๋ค".format(message.author.mention))




bot.run('token')