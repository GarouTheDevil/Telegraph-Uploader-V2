# Made with python3
# (C) @FayasNoushad
# Copyright permission under GNU General Public License v3.0
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Telegraph-Uploader-Bot/blob/main/LICENSE

import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file

FayasNoushad = Client(
    "Telegraph Uploader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START = """
<b>Hello {}, \nIam A Telegraph Uploader Bot</b>
"""

HELP = """
<b>• Forward Me A Media File</b>
<b>• I will Download It And Upload It To Telegraph</b>
<b>• And Send You The Generated Link</b>
"""

ABOUT = """
<b>A Modified Telegraph Uploader Bot </b>
"""

# start command
@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=START.format(update.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "HELP", callback_data="help"),
                                        InlineKeyboardButton(
                                            "ABOUT", callback_data="about"),
                                    ],[
                                      InlineKeyboardButton(
                                            "CLOSE", callback_data="closeme")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@FayasNoushad.on_message(filters.command(["help"]))
async def help(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=HELP,
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "ABOUT", callback_data="about"),
                                        InlineKeyboardButton(
                                            "START", callback_data="start"),
                                    ],[
                                      InlineKeyboardButton(
                                            "CLOSE", callback_data="closeme")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@FayasNoushad.on_message(filters.command(["about"]))
async def help(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=ABOUT,
        reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "HELP", callback_data="help"),
                                        InlineKeyboardButton(
                                            "START", callback_data="start"),
                                    ],[
                                      InlineKeyboardButton(
                                            "CLOSE", callback_data="closeme")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")


# Main function
@FayasNoushad.on_message(filters.media & filters.private)
async def getmedia(bot, update):
    medianame = "./DOWNLOADS/"  + "FayasNoushad/FnTelegraphBot"
    text = await bot.send_message(
        chat_id=update.chat.id,
        text="<b>Downloading ⬇️</b>",
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<b>Uploading ⬆️</b>"
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True
        )
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"), InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}"),],
                                           [InlineKeyboardButton(text="Join Channel", url="https://telegram.me/DevilBotz")]])
    )
    try:
        os.remove(medianame)
    except:
        pass


@pyrogram.Client.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)
      if "closeme" in cb_data:
      await update.message.delete()

FayasNoushad.run()
