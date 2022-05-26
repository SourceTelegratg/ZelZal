import random
import re
import time
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from zthon import StartTime, zedub, zedversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import zedalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "العروض"


@zedub.zed_cmd(
    pattern="فحص$",
    command=("فحص", plugin_category),
    info={
        "header": "- لـ التحـقق من ان البـوت يعمـل بنجـاح ✓",
        "الاسـتخـدام": [
            "{tr}فحص",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    ANIME = None
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or zed_temp
    if "ANIME" in cat_caption:
        data = requests.get("https://animechan.vercel.app/api/random").json()
        ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    zedevent = await edit_or_reply(event, "**⎆┊جـاري .. فحـص البـوت الخـاص بك**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    Z_EMOJI = gvarstatus("ALIVE_EMOJI") or "✥┊"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "** بـوت  زدثــون 𝙕𝞝𝘿𝙏𝙃𝙊𝙉  يعمـل .. بنجـاح ☑️ 𓆩 **"
    ZED_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/f821d27af168206b472ad.mp4"
    caption = cat_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        ANIME=ANIME,
        Z_EMOJI=Z_EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        zdver=zedversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if ZED_IMG:
        ZED = list(ZED_IMG.split())
        PIC = random.choice(ZED)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await zedevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                zedevent,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            zedevent,
            caption,
        )


zed_temp = """{ALIVE_TEXT}

**{Z_EMOJI} قاعدۿ البيانات :** تعمل بنـجاح
**{Z_EMOJI} إصـدار التـيليثون :** `{telever}`
**{Z_EMOJI} إصـدار زدثــون :** `{zdver}`
**{Z_EMOJI} إصـدار البـايثون :** `{pyver}`
**{Z_EMOJI} الوقـت :** `{uptime}`
**{Z_EMOJI} المسـتخدم:** {mention}
**{Z_EMOJI} قنـاة السـورس :** [اضغـط هنـا](https://t.me/ZedThon)"""


@zedub.zed_cmd(
    pattern="الفحص$",
    command=("الفحص", plugin_category),
    info={
        "header": "- لـ التحـقق من ان البـوت يعمـل بنجـاح .. بخـاصيـة الانـلايـن ✓",
        "الاسـتخـدام": [
            "{tr}الفحص",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    Z_EMOJI = gvarstatus("ALIVE_EMOJI") or "✥┊"
    cat_caption = "** بـوت  زدثــون 𝙕𝞝𝘿𝙏𝙃𝙊𝙉  يعمـل .. بنجـاح ☑️ 𓆩 **\n"
    cat_caption += f"**{Z_EMOJI} إصـدار التـيليثون :** `{version.__version__}\n`"
    cat_caption += f"**{Z_EMOJI} إصـدار زدثــون :** `{zedversion}`\n"
    cat_caption += f"**{Z_EMOJI} إصـدار البـايثون :** `{python_version()}\n`"
    cat_caption += f"**{Z_EMOJI} المسـتخدم :** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@zedub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await zedalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
