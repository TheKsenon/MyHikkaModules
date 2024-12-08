from .. import loader, utils
import requests
import io
import aiohttp
import logging

logger = logging.getLogger(__name__)

version = (1, 5, 0)
__version__ = version

@loader.tds
class KsenonGPTMod(loader.Module):
    """KsenonGPT module for text and image generation using KsenonAPI"""

    strings = {
        "name": "KsenonGPT",
        "no_api_key": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>You have not set up the API key!</b>\n\n<emoji document_id=5879585266426973039>🌐</emoji> <b>The key is very easy to get, it's free.</b>\n\n<emoji document_id=6034962180875490251>🔓</emoji> <b>Bot: </b><b>@ksenonapi_gettoken_bot</b>",
        "generating_text": "<emoji document_id=5891243564309942507>💬</emoji> <b>Responding to your message...</b>",
        "text_generated": "<emoji document_id=5870984130560266604>💬</emoji> <b>Request:</b> <code>{}</code>\n\n<emoji document_id=5891243564309942507>💬</emoji> {}",
        "generating_image": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Generating image...</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Model:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Request:</b> <code>{}</code>",
        "image_generated": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Image generated!</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Model:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Request:</b> <code>{}</code>\n\n<emoji document_id=5877307202888273539>📥</emoji> <b>Link:</b> {}",
        "error_blocked": "<emoji document_id=5832546462478635761>🔒</emoji> <b>You have been blocked!</b>\n\n<emoji document_id=5879896690210639947>🗑</emoji><b>NSFW | politics etc. generation is prohibited.</b>",
        "error_occurred": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>An error occurred!</b>\n\n<emoji document_id=5967816500415827773>💻</emoji> <b>Model:</b> {}\n<emoji document_id=5874986954180791957>📶</emoji> <b>Server status, code:</b> {}\n<emoji document_id=5832251986635920010>➡️</emoji> <b>Error:</b> {}",
        "text_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Text models:</b>\n\n<blockquote>o1-preview\ngpt-4o\nclaude-3-5-sonnet\nsearchgpt (GPT + Internet)\nblackboxai-pro\nclaude-3-5-sonnet-20240620\nclaude-3-haiku-ddg\ngemini-1.5-pro-latest\nllama-3.1-405b\ngpt-3.5-turbo-202201\ngpt-4o-mini-ddg\ngpt-4o-2024-05-13\nmicrosoft/Phi-3.5-mini-instruct\nQwen/Qwen2.5-Coder-32B-Instruct\nQwen/QwQ-32B-Preview</blockquote>\n\n<emoji document_id=5843908536467198016>✅️</emoji> <b>We have 167 models!</b>\n<emoji document_id=5778423822940114949>🛡</emoji><b> </b><a href=\"theksenon.pro/v1/api/text/models\"><b>theksenon.pro/v1/api/text/models</b></a>",
        "image_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Image models:</b>\n\n<blockquote><b>flux-pro-mg\nflux-dev\nsd3-ultra\npixart-alpha</b></blockquote>",
        "no_args": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>No arguments provided!</b>",
        "update_available": "<emoji document_id=5420323339723881652>⚠️<emoji> <b>KsenonGPT update available!</b>\n\n<emoji document_id=5449683594425410231>🔼</emoji> <b>New version: {}</b>\n<emoji document_id=5447183459602669338>🔽</emoji> <b>Current version: {}</b>\n\n<emoji document_id=5447410659077661506>🌐</emoji> <b>Changelog:</b>\n<emoji document_id=5458603043203327669>🔔</emoji> <i>{}</i>\n\n<emoji document_id=5206607081334906820>✔️</emoji> <b>Command to update:</b>\n<code>.dlmod http://aeza.theksenon.pro/v1/api/ksenongpt.py</code>",
        "latest_version": "<emoji document_id=5370870691140737817>🥳</emoji> <b>You have the latest version of KsenonGPT!</b>\n\n<emoji document_id=5447644880824181073>⚠️</emoji><b>Developers are making updates and fixes almost every day, check frequently!</b>",
    }

    strings_ru = {
        "name": "KsenonGPT",
        "no_api_key": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Вы не настроили API ключ!</b>\n\n<emoji document_id=5879585266426973039>🌐</emoji> <b>Ключ очень легко достать, он бесплатный.</b>\n\n<emoji document_id=6034962180875490251>🔓</emoji> <b>Бот: </b><b>@ksenonapi_gettoken_bot</b>",
        "generating_text": "<emoji document_id=5891243564309942507>💬</emoji> <b>Отвечаю на ваше сообщение...</b>",
        "text_generated": "<emoji document_id=5870984130560266604>💬</emoji> <b>Запрос:</b> <code>{}</code>\n\n<emoji document_id=5891243564309942507>💬</emoji> {}",
        "generating_image": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Генерирую изображение...</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Модель:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Запрос:</b> <code>{}</code>",
        "image_generated": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Изображение сгенерировано!</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Модель:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Запрос:</b> <code>{}</code>\n\n<emoji document_id=5877307202888273539>📥</emoji> <b>Ссылка:</b> {}",
        "error_blocked": "<emoji document_id=5832546462478635761>🔒</emoji> <b>Вы были заблокированы!</b>\n\n<emoji document_id=5879896690210639947>🗑</emoji><b>Запрещено генерировать NSFW | политика и т.д.</b>",
        "error_occurred": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Произошла ошибка!</b>\n\n<emoji document_id=5967816500415827773>💻</emoji> <b>Модель:</b> {}\n<emoji document_id=5874986954180791957>📶</emoji> <b>Статус сервера, код:</b> {}\n<emoji document_id=5832251986635920010>➡️</emoji> <b>Ошибка:</b> {}",
        "text_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Текстовые модели:</b>\n\n<blockquote>o1-preview\ngpt-4o\nclaude-3-5-sonnet\nsearchgpt (GPT + Internet)\nblackboxai-pro\nclaude-3-5-sonnet-20240620\nclaude-3-haiku-ddg\ngemini-1.5-pro-latest\nllama-3.1-405b\ngpt-3.5-turbo-202201\ngpt-4o-mini-ddg\ngpt-4o-2024-05-13\nmicrosoft/Phi-3.5-mini-instruct\nQwen/Qwen2.5-Coder-32B-Instruct\nQwen/QwQ-32B-Preview</blockquote>\n\n<emoji document_id=5843908536467198016>✅️</emoji> <b>У нас 167 моделей!</b>\n<emoji document_id=5778423822940114949>🛡</emoji><b> </b><a href=\"api.theksenon.pro/v1/api/text/models\"><b>api.theksenon.pro/v1/api/text/models</b></a>",
        "image_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Модели для изображений:</b>\n\n<blockquote><b>flux-pro-mg\nflux-dev\nsd3-ultra\npixart-alpha</b></blockquote>",
        "no_args": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Не указаны аргументы!</b>",
        "update_available": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Доступно обновление KsenonGPT!</b>\n\n<emoji document_id=5449683594425410231>🔼</emoji> <b>Новая версия: {}</b>\n<emoji document_id=5447183459602669338>🔽</emoji> <b>Текущая версия: {}</b>\n\n<emoji document_id=5447410659077661506>🌐</emoji> <b>Список изменений:</b>\n<emoji document_id=5458603043203327669>🔔</emoji> <i>{}</i>\n\n<emoji document_id=5206607081334906820>✔️</emoji> <b>Команда для обновления:</b>\n<code>.dlmod http://aeza.theksenon.pro/v1/api/ksenongpt.py</code>",
        "latest_version": "<emoji document_id=5370870691140737817>🥳</emoji> <b>У вас последняя версия KsenonGPT!</b>\n\n<emoji document_id=5447644880824181073>⚠️</emoji><b>Разработчики делают обновления и исправления почти каждый день, проверяйте чаще!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                "API key from @ksenonapi_gettoken_bot",
                validator=loader.validators.Hidden(),
            )
        )

    async def gentextcmd(self, message):
        """Генерировать текст - .gentext <prompt> <model>"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            prompt, model = args.rsplit(maxsplit=1)
        except ValueError:
            prompt = args
            model = "gpt-4o"

        msg = await utils.answer(message, self.strings["generating_text"])

        headers = {
            "Authorization": self.config["api_key"],
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "prompt": prompt
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://aeza.theksenon.pro/v1/api/text/generate",
                headers=headers,
                json=data
            ) as response:
                result = await response.json()

                if response.status != 200:
                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            response.status,
                            result.get("error", "Unknown error")
                        )
                    )
                    return

                if "error" in result:
                    if result["error"] == "Your token has been blocked":
                        await utils.answer(msg, self.strings["error_blocked"])
                        return

                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            "N/A",
                            result["error"]
                        )
                    )
                    return

                await utils.answer(
                    msg,
                    self.strings["text_generated"].format(
                        prompt,
                        result["response"]
                    )
                )

    async def genimgcmd(self, message):
        """Генерировать изображение - .genimg <prompt> <model>"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            prompt, model = args.rsplit(maxsplit=1)
        except ValueError:
            prompt = args
            model = "flux-pro-mg"

        msg = await utils.answer(
            message,
            self.strings["generating_image"].format(model, prompt)
        )

        headers = {
            "Authorization": self.config["api_key"],
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "prompt": prompt
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://aeza.theksenon.pro/v1/api/image/generate",
                headers=headers,
                json=data
            ) as response:
                result = await response.json()

                if response.status != 200:
                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            response.status,
                            result.get("error", "Unknown error")
                        )
                    )
                    return

                if "error" in result:
                    if result["error"] == "Your token has been blocked":
                        await utils.answer(msg, self.strings["error_blocked"])
                        return

                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            "N/A",
                            result["error"]
                        )
                    )
                    return

                image_url = result["url"]
                async with session.get(image_url) as response:
                    if response.status != 200:
                        await utils.answer(
                            msg,
                            self.strings["error_occurred"].format(
                                model,
                                response.status,
                                "Failed to download image"
                            )
                        )
                        return

                    image_data = io.BytesIO(await response.read())
                    image_data.name = "image.png"

                    await self._client.send_file(
                        message.peer_id,
                        image_data,
                        caption=self.strings["image_generated"].format(
                            model,
                            prompt,
                            image_url
                        ),
                        reply_to=message.reply_to_msg_id
                    )

                    if message.out:
                        await message.delete()

    async def txtmodelscmd(self, message):
        """Лист текстовых моделей"""
        await utils.answer(message, self.strings["text_models"])

    async def imgmodelscmd(self, message):
        """Лист моделей для изображений"""
        await utils.answer(message, self.strings["image_models"])
        
    async def kupdatecmd(self, message):
        """Проверить обновления"""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.theksenon.pro/v1/api/version") as response:
                if response.status != 200:
                    return
                    
                content = await response.text()
                
                version_match = content.split('\n')[0]
                changelog_match = content.split('# changelog: ')[1] if '# changelog: ' in content else "Нет информации"
                
                latest_version = tuple(map(int, version_match.strip().split('.')))
                
                current_version = ".".join(map(str, version))
                new_version = ".".join(map(str, latest_version))
                
                if latest_version > version:
                    await utils.answer(
                        message,
                        self.strings["update_available"].format(
                            new_version,
                            current_version,
                            changelog_match,
                            "http://api.theksenon.pro/v1/api/ksenongpt.py"
                        )
                    )
                else:
                    await utils.answer(message, self.strings["latest_version"])
