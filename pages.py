# GUI Pages for Discord.py
import time
import random


import math
import discord


# class Page(discord.Embed):
#     pass

# class Pages():
#     pass



def add_fields_to_embed(embed, fields):
    for field in fields:
        embed.add_field(field)


def create_embeds_from_fields(template, field_pages):
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

async def paginate(
            channel, 
            target_user, 
            pages, 
            duration=60000, 
            remove_on_finish=True
        ):
    pass




async def confirm(
            ctx,
            page,
            target_user=None,
            duration=20.0, 
            remove_on_finish=True
        ):
    
    # You can specify a target user (the user whose reacts we care about)
    # as we may not always want the author of an invoked command as the target.
    # i.e. [p]propose @user "@user, do you want to marry @author?" etc.
    # However, not specifying one just defaults to the ctx.author
    if target_user == None:
        target_user = ctx.author
    
    # The reactions we want to handle for.
    x, _ = sym = (":white_check_mark:", ":x:")
    
    # The message that will display in chat and that the user will react to.
    confirmation_message = await ctx.send(embed=page)
    
    # Add all of our reactions to the message
    for r in sym:
        confirmation_message.add_reaction(r)
    
    # u (User who added the reaction) | r (The Reaction object itself)
    
    # 1. check that the one who initially invoked the command is the one who reacted
    # 2. check that the message being reacted to is the confirmation message
    # 3. check that the reaction that was added is one we handle for.
    check = lambda r, u: (u == target_user) and (r.msg == confirmation_message) and (r.name in sym)
    
    try:
        r, u = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        if not remove_on_finish:
            await confirmation_message.edit("*(This message is no longer active)*", embed=page)
    finally:
        if remove_on_finish:
            await confirmation_message.delete()
        if r == x:
            return True
        else:
            return False
            
    
    