from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**🔊 ഞങ്ങളുടെ 𝙈𝙖𝙞𝙣 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 ജോയിൻ ചെയ്താൽ മാത്രമേ സിനിമ ലഭിക്കുകയുള്ളൂ. 🤷‍ചാനലിൽ join ചെയ്തിട്ട് ഒന്നുകൂടി Try ചെയ്യ്. ❤️😁 Hey..Bruh🙋‍♂️...Please Join My Updates Channel to use Me 👹!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⭕ 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊𝐒 ⭕", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        btn.append(

            [InlineKeyboardButton(text="🚨 Subscribe Channel And Try 🚨", url="https://t.me/joinchat/_T2AlAivCsVkZWRl")]

            )
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"📒 {get_size(file.file_size)} ‣ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"gtnero#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAALO_GFPY0CyHLMEF65JgfPTJTnmT0urAALOAAP-788VQR05D4RW-z0hBA')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="● ɴᴏ ɴᴇxᴛ ᴘᴀɢᴇ ●",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>●🎪Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ 🇱 🇮 🇳 🇰 : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>●⚡🎬Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ 🇱 🇮 🇳 🇰  : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="● ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ ●",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ● 《 1 - {data['total']}》",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>●🎬⚡Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ 🇱 🇮 🇳 🇰  : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>●🎬⚡Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ 🇱 🇮 🇳 🇰  : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"📒 {get_size(file.file_size)} ‣ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="● ɴᴏ ɴᴇxᴛ ᴘᴀɢᴇ ●",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>●🎬⚡Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ ʟɪɴ𝐊s : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>●🎬⚡Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ ʟɪɴ𝐊s : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="● ɢᴏ ᴛᴏ ɴᴇxᴛ ᴘᴀɢᴇ ●",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ● 《1 - {data['total']}》",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>●🎬⚡Tɪᴛʟᴇ :</b> <code>{search}</code>\n\n<b>●ᴄʜᴀɴɴᴇʟ 🇱 🇮 🇳 🇰 : [𝙅𝙊𝙄𝙉](https://telegram.dog/cinemacollections)\n● ᴘᴏᴡᴇʀᴇᴅ ʙʏ : CɪɴEMACOʟʟECTɪOɴS</b>\n\n<b>ɪ𝙵 ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 ᴛʜɪ𝚂 ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ 𝙵ᴏʀ . ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("അല്ലയോ മഹാൻ താങ്കൾ ക്ലിക്ക് ചെയ്തത് പഴയ മെസ്സേജ് ആണ് വേണമെങ്കിൽ ഒന്നും കൂടെ റിക്വസ്റ്റ് ചെയ് 😉\n\nYou are using this for one of my old message, please send the request again",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("● ɢᴏ ᴛᴏ ᴘʀᴇᴠɪᴏᴜs ᴘᴀɢᴇ ●", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ●《{int(index)+2} - {data['total']}》", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("● ʙᴀᴄᴋ ᴘᴀɢᴇ ●", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("● ɴᴇxᴛ ᴘᴀɢᴇ ●", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ● 《{int(index)+2} - {data['total']}》", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("**You are using this for one of my old message, please send the request again.**",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("● ɴᴇxᴛ ᴘᴀɢᴇ ●", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ● 《{int(index)} - {data['total']}》", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("● ʙᴀᴄᴋ ᴘᴀɢᴇ ●", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("● ɴᴇxᴛ ᴘᴀɢᴇ ●", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"● ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ ● 《{int(index)} - {data['total']}》", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('⭕ OUR MOVIE CHANNEL⭕', url='https://t.me/Cinemacollections),
                    InlineKeyboardButton('♏мᴀʟᴀʏᴀʟᴀм мovιᴇs ♏', url='https://t.me/Malayalam_Only')
                ]
                ]
            await message.reply(text="<b>Developer : <a href='https://t.me/anjalinas'>🇦 🇳 🇯 🇦 🇱 🇮 🇳 🇦<a/> ", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"<b>🗃 ғɪʟᴇ ɴᴀᴍᴇ :</b>\n<code>{file_name}</code>"
                buttons = [
                    [
                        InlineKeyboardButton('⭕ 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊 ⭕', url='https://t.me/joinchat/_T2AlAivCsVkZWRl')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"<b>🗃 ғɪʟᴇ ɴᴀᴍᴇ :</b>\n<code>{file_name}</code>"
                buttons = [
                    [
                        InlineKeyboardButton('⭕ 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊 ⭕', url='https://t.me/joinchat/_T2AlAivCsVkZWRl')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("🔊 ഞങ്ങളുടെ 𝙈𝙖𝙞𝙣 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 ജോയിൻ ചെയ്താൽ മാത്രമേ സിനിമ ലഭിക്കുകയുള്ളൂ. 🤷‍ചാനലിൽ join ചെയ്തിട്ട് ഒന്നുകൂടി Try ചെയ്യ്. ❤️😁",show_alert=True)
