﻿import discord
from sigma.core.permission import check_admin


async def greetmsg(cmd, message, args):
        
    if not check_admin(message.author, message.channel):
        embed = discord.Embed(title='⛔ Unpermitted', color=0xDB0000)
        await message.channel.send(None, embed=embed)
        return

    if not args:
        greet_message = cmd.db.get_settings(message.guild.id, 'GreetMessage')
        embed = discord.Embed(color=0x0099FF)
        embed.add_field(name='ℹ Current Greet Message', value='```\n' + greet_message + '\n```')
    else:
        cmd.db.set_settings(message.guild.id, 'GreetMessage', ' '.join(args))
        embed = discord.Embed(title='✅ New Greet Message Set', color=0x66CC66)    
    
    await message.channel.send(None, embed=embed)
