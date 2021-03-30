# GUI Pages for Discord.py
import time
import asyncio
import random


import math
import discord


# class Page(discord.Embed):
#     pass

# class Pages():
#     pass

def book(template, fields, fields_per_page=3):
    pages = results_per_page(fields, fields_per_pages)
    embeds = add_fields_to_embeds(template, fields)
    return embeds


def _add_fields(embed, fields):
    for field in fields:
        embed.add_field(field)


def add_fields_to_embeds(template, field_pages):
    template.clear_fields()
    # [[f1, f2, f3], [f4, f5, f6], [f7, f8, f9], ....etc]
    
    embeds = []
    for fields in field_pages:
        e = template.copy()
        
        add_fields_to_embed(e, fields)

            
        embeds.append(e)

    return embeds
    


def results_per_page(items, maxResults):
    pagedResults = []
    neededPages = math.ceil(len(items)/maxResults)
    for i in range(neededPages):
        results = items[i*maxResults:(i+1)*maxResults]
        pagedResults.append(results)   

    return pagedResults



def _add_reacts(msg, rs):
    for r in rs:
        msg.add_reaction(r)




async def paginate(
            bot,
            ctx, 
            pages, 
            target_user=None, 
            duration=60000, 
            remove_on_finish=True
        ):
    # You can specify a target user (the user whose reacts we care about)
    # as we may not always want the author of an invoked command as the target.
    # i.e. [p]propose @user "@user, do you want to marry @author?" etc.
    # However, not specifying one just defaults to the ctx.author
    if target_user == None:
        target_user = ctx.author
    
    # The reactions we want to handle for.
    rw, b, f, ff, x = sym = ("⏪", "⬅️", "➡️", "⏩", "❌")
    

    # page markers
    first_page, last_page = 0, len(pages)-1
    
    current_page = first_page
    
    # The message that will display in chat and that the user will react to.
    book = await ctx.send(embed=pages[current_page])
    
    # Add all of our reactions to the message
    _add_reacts(book, sym)
    
    # u (User who added the reaction) | r (The Reaction object itself)
    
    # 1. check that the one who initially invoked the command is the one who reacted
    # 2. check that the message being reacted to is the confirmation message
    # 3. check that the reaction that was added is one we handle for.
    check = lambda r, u: (u == target_user) and (r.msg.id == book.id) and (r.name in sym)
    while 1:
        try:
            r, u = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            assert r != x
        except asyncio.TimeoutError and AssertionError:
            if remove_on_finish:
                await book.delete()
                return
            await book.edit("*(This message is no longer active)*", embed=pages[current_page])
            return
        else:
            # Rewind
            if r == rw: current_page = first_page  
            # FastForward
            elif r == ff: current_page = last_page  
            # Back
            elif r == b:
                if current_page == 0: current_page = last_page
                else: current_page -= 1   
            # forward
            elif r == f:     
                if current_page == last_page: current_page = first_page
                else: current_page += 1
                
            book.edit(embed=pages[current_page])

# Usage
# result = await confirm(ctx, page)

# if result: # they said yes
#     do stuff
# else: # they said no
#     do other stuff

async def confirm(
            bot,
            ctx,
            page,
            target_user=None,
            duration=20.0, 
            remove_on_finish=True
        ):
    """Prompts a user to confirm. React with a yes for true, react with an X for false.

    Args:
        ctx (discord.ext.commands.Context): Invocation context of a command.
        page (discord.Embed): The embed to display and have a user react to.
        target_user (discord.Member, optional): Optional member to specify if the one who 
        needs to react is not the author of the command. Defaults to None.
        duration (float, optional): How long to wait before timing out. Defaults to 20.0.
        remove_on_finish (bool, optional): Whether or not the bot should remove the 
        message once reactions have finished. Defaults to True.

    Returns:
        [Bool]: If the user accepted or denied the confirmation.
    """
    
    # You can specify a target user (the user whose reacts we care about)
    # as we may not always want the author of an invoked command as the target.
    # i.e. [p]propose @user "@user, do you want to marry @author?" etc.
    # However, not specifying one just defaults to the ctx.author
    if target_user == None:
        target_user = ctx.author
    
    # The reactions we want to handle for.
    x, _ = sym = ("✅", "❌")
    
    
    
    # The message that will display in chat and that the user will react to.
    confirmation_message = await ctx.send(embed=page)
    
    # Add all of our reactions to the message
    _add_reacts(confirmation_message, sym)
    
    # u (User who added the reaction) | r (The Reaction object itself)
    
    # 1. check that the one who initially invoked the command is the one who reacted
    # 2. check that the message being reacted to is the confirmation message
    # 3. check that the reaction that was added is one we handle for.
    check = lambda r, u: (u == target_user) and (r.msg.id == confirmation_message.id) and (r.name in sym)
    
    try:
        r, u = await bot.wait_for('reaction_add', timeout=duration, check=check)
        
    except asyncio.TimeoutError:
        if remove_on_finish:
            await confirmation_message.delete()
        else:
            await confirmation_message.edit("*(This message is no longer active)*", embed=page)
        return False
    
    else:
        if remove_on_finish:
            await confirmation_message.delete()
        else:
            await confirmation_message.edit("*(This message is no longer active)*", embed=page)
            
        if r == x:
            return True
        return False
            
    
    