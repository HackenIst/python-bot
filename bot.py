import random

import discord
import asyncio

from discord import Member, Guild, User

client = discord.Client()


#############################################################

autoroles = {
    481123510945841152: {'memberroles': [482632835195338763], 'rainbowroles': [759021202743492610]}
}


@client.event
async def on_ready():
    print("Welcome Home Sir")
    client.loop.create_task(status_task())





async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue(), discord.Colour.dark_purple()]
    while True:
        await client.change_presence(activity=discord.Game(name="mit 187 User"), status=discord.Status.online)
        await asyncio.sleep(4)

        guild: Guild = client.get_guild(481123510945841152)
        if guild:
            role = guild.get_role(759021202743492610)
            if role:
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))

def is_not_pinned(mess):
    return not mess.pinned

@client.event
async def on_member_join(member):
    guild: Guild = member.guild
    if not member.bot:
        embed = discord.Embed(title='Willkommen auf Milfhunter-Gang 💖 {} '.format(member.name),
                              description='Wir heißen dich herlich Willkommen auf unserem Server!', color=15158332)
        embed.add_field(name="Server beigetreten", value=member.joined_at.strftime("%d.%m.%Y, %H:%M:%S"),
                       inline=True)
        embed.add_field(name="Discord beigetreten", value=member.created_at.strftime("%d.%m.%Y, %H:%M:%S"),
                        inline=True)
        embed.set_footer(text="bot by @hackenistharam")

        try:
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print("Es konnte keine Willkommensnachricht an {} gesendet werden.".format(member.name))
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['memberroles']:
            for roleId in autoguild['memberroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if ("/help") in message.content:
        embed = discord.Embed(title="Hilfetext", description="**/help** - Zeigt diesen Text an\r\n"
                                                             "**/userinfo** - Zeigt dir Informationen\r\n"
                                                             "**/kill** - Tötet einen Member\r\n"
                                                             "**/ban** - bannt einen Member\r\n"
                                                             "**/kick** - kickt einen Member\r\n"
                                                             "**/meme** - erzählt dir ein meme\r\n"
                                                             "**/clear** - cleart den Chat\r\n"
                                                             "**/version** - zeigt dir die Version an",
                      color=15158332)
        await message.channel.send(embed=embed)
    if message.content.startswith("/userinfo"):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title="Userinfo für {}".format(member.name),
                                      description="Dies ist eine Userinfo für den User {}".format(member.mention),
                                      color=15158332)
                embed.add_field(name="Server beigetreten", value=member.joined_at.strftime("%d.%m.%Y    %H:%M:%S"),
                                inline=True)
                embed.add_field(name="Discord beigetreten", value=member.created_at.strftime("%d.%m.%Y    %H:%M:%S"),
                                inline=True)
                embed.set_footer(text="Invision Bot")
                mess = await message.channel.send(embed=embed)
                await mess.add_reaction(':Brimstone_artwork:758768207531606076 ')

    if message.content.startswith("/kill"):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await message.channel.send("Du hast den User {0} getötet".format(member.mention))
                await message.add_reaction("☠")


    if message.content.startswith("/clear"):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send("{} Nachrichten gelöscht!".format(len(deleted)-1))

    if message.content.startswith("/ban") and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send(f'Member {member.name} gebannt!')
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')
    if message.content.startswith("/kick") and message.author.guild_permissions.kick_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send(f'Member {member.name} gekickt!')
            else:
                await message.channel.send(f'Kein User mit dem Namen {args[1]} gefunden.')


    if message.content.startswith("/meme"):
        embed = discord.Embed(title="memes", description="Du bist das meme hier ;:D", color=15158332)
        embed.set_footer(text="by @hackenistharam")
        await message.channel.send(embed=embed)

    if message.content.startswith("/team"):
        embed = discord.Embed(title="Team Liste", description="**Owner**: X-Ray.ReDeX\r\n"
                                                              "\r\n"
                                                              "**Admins**:\r\n"
                                                              "HackenIstHaram\r\n"
                                                              "EinsRandomLel\r\n"
                                                              "Holyboomboomreis\r\n"
                                                              "ReIndex\r\n"
                                                              "X-Ray.KcRumba\r\n"
                                                              "", color=15158332)
        embed.set_footer(text="bot by @hackenistharam")
        await message.channel.send(embed=embed)


    if message.content.startswith("/version"):
        await message.channel.send("Version: 2.0")












client.run("NzUyMTkzNjgyNDY3NDU1MTE2.X1UE9A.1q2Feya-v1kKwSLS4Kn44WYXM78")