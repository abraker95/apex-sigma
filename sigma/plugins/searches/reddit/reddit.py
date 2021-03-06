﻿import praw
import random
import discord
from config import RedditClientID, RedditClientSecret
from sigma.core.permission import check_channel_nsfw


async def reddit(cmd, message, args):

    if not args:
        await message.channel.send(cmd.help())
        return

    if (RedditClientID == '') or (RedditClientSecret == ''):
        embed = discord.Embed(color=0xDB0000)
        embed.add_field(name='API key RedditClientID and/or RedditClientSecret not found.', value='Please ask the bot owner to add them.')
        await message.channel.send(None, embed=embed)
        return

    req = praw.Reddit(user_agent='Apex Sigma', client_id=RedditClientID, client_secret=RedditClientSecret)
    q = ' '.join(args)
    sub = req.subreddit(str(q))

    if sub.over18:
        nsfw_allowed = check_channel_nsfw(cmd.db, message.channel.id)
        if not nsfw_allowed:
            embed_content = discord.Embed(title=':eggplant: Channel does not have NSFW permissions set, sorry.', color=0x9933FF)
            await message.channel.send(None, embed=embed_content)
            return

    posts = sub.hot(limit=100)
    url_list = []
    for post in posts:
        url_list.append(post.url)

    out_tex = random.choice(url_list)
    await message.channel.send(out_tex)
