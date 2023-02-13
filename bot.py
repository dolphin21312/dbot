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
tt = "공지사항"
cn = 1035777248466313259
idlist = {1035777247992348704: True, 987654321: True}

user_data = {}
admin = '𝑯𝑻𝑴𝑳#7777'

@bot.event
async def on_ready():
    print('login.')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("타르코프 DLC 최저가 돌핀샵"))
    for guild in bot.guilds:
        if guild.id not in idlist:  # idlist에 없으면
            await guild.leave()  # 자동으로 나가기
            print("이상한 서버에 접속되어 나갔습니다")
        else:
            print(f'{guild.name}이 엑세스 완료 되었음.')

@bot.event
async def on_guild_join(guild):
    if guild.id not in idlist:  # idlist에 없으면
        await guild.leave()  # 자동으로 나가기
        print("이상한 서버에 접속되어 나갔습니다")
    else:
        print(f'Joined {guild.name}.')  # idlist에 있으면 그대로 머무르기

@bot.event #계정 생성일 필터
async def on_member_join(member):
    setting = '0'
    setting = int(setting)

    created = times() - member.created_at.timestamp()
    created = int(created) / 86400
    created = round(created)

    if created < setting:
        embed = discord.Embed(title='❗  계정 생성일 미달', description=f'계정 생성일이 {setting}일 미만이므로 **{member.guild}**에서 추방되었습니다')
        embed.set_footer(text=f'{admin}으로 문의주세요')
        await member.send(embed=embed)
        await member.kick(reason='계정 생성일 미달')

@bot.event 
#앞메 방지기
async def on_message(message):
    global cn
    global tt
    if message.author == bot.user:
        return

    author_id = message.author.id

    # 사용자 데이터가 없으면 초기화합니다.
    if author_id not in user_data:
        user_data[author_id] = {
            'message_count': 0,
            'last_message_time': datetime.now()
        }

    # 현재 시간과 마지막 메시지 전송 시간을 비교하여 시간 차이를 계산합니다.
    last_message_time = user_data[author_id]['last_message_time']
    time_diff = datetime.now() - last_message_time

    # 메시지를 보낸 시간이 1시간 이상 지난 경우 메시지 카운트를 초기화합니다.
    if time_diff > timedelta(hours=ALLOWED_TIMEFRAME_HOURS):
        user_data[author_id]['message_count'] = 0

    # 메시지에 링크가 있고, DISALLOWED_LINK를 포함하지 않으면 메시지 카운트를 증가시킵니다.
    if message.content.find('http') != -1 and DISALLOWED_LINK not in message.content:
        user_data[author_id]['message_count'] += 1
        user_data[author_id]['last_message_time'] = datetime.now()
        await message.delete()
        await message.author.send(f'{message.author.mention}, '
                                      f'돌핀샵에서 링크는 금지됩니다! '
                                      f'{ALLOWED_TIMEFRAME_HOURS}시간 이내에 {ALLOWED_MESSAGES_PER_HOUR}개 이상의 링크를 보내면 '
                                      f'서버에서 추방당합니다!.')
        if user_data[author_id]['message_count'] > ALLOWED_MESSAGES_PER_HOUR:
            await message.author.send(f'{message.author.mention}, '
                                      f'당신은 {ALLOWED_TIMEFRAME_HOURS}시간 동안 'f'{ALLOWED_MESSAGES_PER_HOUR}개 이상의 링크를 보냈기 때문에 'f'서버에서 추방되었습니다.')
            await message.author.kick(reason='링크 사용 제한 초과')
            return
    if message.content.find('discord.gg/') != -1 and DISALLOWED_LINK not in message.content:
        user_data[author_id]['message_count'] += 1
        user_data[author_id]['last_message_time'] = datetime.now()
        await message.delete()
        await message.author.send(f'{message.author.mention}, '
                                      f'돌핀샵에서 링크는 금지됩니다! '
                                      f'{ALLOWED_TIMEFRAME_HOURS}시간 이내에 {ALLOWED_MESSAGES_PER_HOUR}개 이상의 링크를 보내면 '
                                      f'서버에서 추방당합니다!.')
        if user_data[author_id]['message_count'] > ALLOWED_MESSAGES_PER_HOUR:
            await message.author.send(f'{message.author.mention}, '
                                      f'당신은 {ALLOWED_TIMEFRAME_HOURS}시간 동안 '
                                      f'{ALLOWED_MESSAGES_PER_HOUR}개 이상의 링크를 보냈기 때문에 '
                                      f'서버에서 추방되었습니다.')
            await message.author.kick(reason='링크 사용 제한 초과')
            return


    # 테스트 명령어
    if message.content == '!명령어':
        await message.channel.send('테스트')

    # 공지
    if message.content.startswith ("!공지"):
        await message.delete()
        if message.author.guild_permissions.administrator:
            notice = message.content[3:]
            channel = bot.get_channel(int(cn))
            embed = discord.Embed(title = tt, description="공지사항이 있습니다!\n========================================\n\n{}\n\n========================================".format(notice), color=0x0000FF)
            embed.set_footer(text="보낸사람 : {}".format(message.author), icon_url="https://i.imgur.com/QvQRDuy.png")
            embed.set_thumbnail(url="https://i.imgur.com/QvQRDuy.png")
            await channel.send ("@everyone", embed=embed)
            await message.author.send("\n========================================\n```[ BOT 자동 알림 ] | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n\n[ 기본 작성 설정 채널 ] : {}\n[ 공지 발신자 ] : {}\n\n[ 내용 ]\n{}```\n========================================\n".format(channel, message.author, notice))
        else:
            await message.author.send("{}, 당신은 관리자가 아닙니다".format(message.author.mention))

    if message.content.startswith('!제목'):
        await message.delete()
        if message.author.guild_permissions.administrator:
            if len(message.content.split()) > 1:
                tt2 = message.content.split()[1]
                tt = tt2
                await message.author.send("\n========================================\n```[ BOT 자동 알림 ] | 제목을 정상적으로! {} 로 설정하셨습니다!```\n========================================\n".format(tt))
            else:
                await message.author.send("\n========================================\n```[ BOT 자동 알림 ]** | 제목을 잘못 입력하셨습니다!```\n========================================\n")
        else:
            await message.author.send("{}, 당신은 관리자가 아닙니다".format(message.author.mention))

    if message.content.startswith('!채널'):
        await message.delete()
        if message.author.guild_permissions.administrator:
            if len(message.content.split()) > 1:
                cn2 = message.content.split()[1]
                cn = cn2
                await message.author.send("\n========================================\n```[ BOT 자동 알림 ] | 채널을 정상적으로! {} 로 설정하셨습니다!```\n========================================\n".format(cn))
            else:
                await message.author.send("\n========================================\n```[ BOT 자동 알림 ]** | 채널을 잘못 입력하셨습니다!```\n========================================\n")
        else:
            await message.author.send("{}, 당신은 관리자가 아닙니다".format(message.author.mention))




bot.run('token')