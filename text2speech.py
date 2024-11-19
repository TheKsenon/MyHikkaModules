# ------------------------------------------------------------
# Module: Text2Speech
# Description: Модуль для озвучки текста
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .text2speech .t2s
# scope: hikka_only
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
import requests
import urllib.parse
import os
from telethon.tl.functions.channels import JoinChannelRequest

@loader.tds
class Text2SpeechMod(loader.Module):
    """🎤 Модуль для преобразования текста в речь"""
    
    strings = {
        "name": "Text2Speech",
        "processing": "<emoji document_id=5325834523068342417>🫥</emoji> <b>Озвучиваю текст...</b>\n\n<emoji document_id=5933541411558264121>🎤</emoji> <b>Голос: {}</b>",
        "completed": "<emoji document_id=5897554554894946515>🎤</emoji> <b>Голос озвучен</b>!\n\n<emoji document_id=5776375003280838798>✅</emoji> <b>Текст:</b> <code>{}</code>\n\n<emoji document_id=6048354593279053992>🗣</emoji> <b>Голос:</b> <i>{}</i>",
        "error": "❌ Произошла ошибка при создании аудио",
        "args_error": "<b>❌ Укажите текст и голос (alex/sophia)!</b>"
    }

    async def client_ready(self, client, db):
        await client(JoinChannelRequest("kmodules"))

    async def t2s_process(self, message):
        args = utils.get_args_raw(message).split()
        
        if len(args) < 2:
            await utils.answer(message, self.strings["args_error"])
            return
            
        voice = args[-1].lower()
        text = " ".join(args[:-1])
        
        if voice not in ["alex", "sophia"]:
            await utils.answer(message, self.strings["args_error"])
            return
            
        await utils.answer(message, self.strings["processing"].format(voice.title()))
        
        base_url = "http://theksenon.pro/api/text2speech/generate"
        encoded_text = urllib.parse.quote(text)
        url = f"{base_url}?text={encoded_text}&voice={voice}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open("voice.mp3", "wb") as f:
                    f.write(response.content)
                    
                await message.client.send_file(
                    message.chat_id,
                    "voice.mp3",
                    voice_note=True,
                    caption=self.strings["completed"].format(text, voice.title())
                )
                
                if message.out:
                    await message.delete()
                    
                os.remove("voice.mp3")
            else:
                await utils.answer(message, self.strings["error"])
        except Exception:
            await utils.answer(message, self.strings["error"])

    @loader.command()
    async def text2speech(self, message):
        """Преобразовать текст в речь (использование: .text2speech <текст> <alex/sophia>)"""
        await self.t2s_process(message)

    @loader.command()
    async def t2s(self, message):
        """Алиас команды .text2speech, использование: .t2s <текст> <alex/sophia>"""
        await self.t2s_process(message)
