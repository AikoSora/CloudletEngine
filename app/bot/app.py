import time
import asyncio, aiohttp, re
import os, importlib, uvloop

from json import loads
from math import floor
from app.bot import handler
from app.models import Account
from django.conf import settings
from ast import literal_eval as LE
from app.bot.Message import Message
from random import randint as random
from app.bot.LongPoll import LongPoll, api

class VKBot:

	def __init__(self):
		os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
		uvloop.install()
		self.ioloop = asyncio.get_event_loop()
		self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.start_bot())]))

	def load_or_create(self, data):
		return Account.objects.get_or_create(user_id=data['id'], defaults={'username': data['first_name']})[0]

	async def start_bot(self):
		self.longpoll = LongPoll()
		await self.longpoll.get_server()
		self.read_handlers()
		Account.TempBot.bot = api

		@self.longpoll.event()
		async def _(item):
			if item['type'] == "message_new":
				if item['object']['message']['from_id'] > 1:
					data = await api("users.get", {"user_ids": item['object']['message']['from_id']})
					user = self.load_or_create(data['response'][0])

					msg = Message(item)
					if not item['object']['message'].keys() & {"payload"}:
						if "action" in item["object"]['message']:
							if item["object"]['message']['action']['type'] == "chat_invite_user":
								await msg("Спасибо что добавили в беседу 😊")
						else:
							processed_name = re.sub(r'^[^а-яА-ЯёЁ]\s', '', item['object']['message']['text'].lower().strip())
							processed_name = re.sub(fr'\[club{settings.BOT_GROUP_ID}|@?.+\]\s', '', processed_name)
							processed_name = processed_name.replace("/", "")
							path_args = re.split(r'\s+', processed_name)
							msg.path_args = path_args

							for command in handler.commands:
								if ((not command.with_args and command.name in ['', processed_name]) or (command.with_args and command.name in ['', path_args[0], " ".join(x for x in path_args[0:len(command.name.split())]) if len(path_args) >= len(command.name.split()) else ""])) and (command.dialog == user.dialog or command.dialog == "all"):
									if not await command.handle(msg, user):
										await msg('❌ Произошла ошибка, попробуйте чуть позже')
									break
							else:
								if item['object']['message']['peer_id'] < 2000000000:
									await msg('Команда не найдена, воспользуйтесь кнопками 😔')
					else:
						try:
							payload_command = LE(item['object']['message']['payload'])
							if payload_command.keys() & {"command"}:
								if payload_command['command'] == "not_supported_button":
									payload_command = loads(payload_command['payload'])["button"].split() 
							else:
								payload_command = payload_command["button"].split()

							msg.path_args = payload_command

							for command in handler.payload_commands:
								if (command.name in ['', payload_command[0]]) and (command.dialog == user.dialog or command.dialog == "all"):
									if not await command.handle(msg, user):
										await msg('❌ Произошла ошибка, попробуйте чуть позже')
										#await msg(sticker_id=8471)
									break
							else:
								if item['object']['message']['peer_id'] < 2000000000:
									await msg('Команда не найдена, воспользуйтесь кнопками 😔')
						except:
							pass

			elif item['type'] == "message_event":
				data = await api("users.get", {"user_ids": item['object']['user_id']})
				user = self.load_or_create(data['response'][0])
				callback_command = item['object']['payload']['button'].split()
				msg = Message(item, True)
				msg.path_args = callback_command

				for command in handler.callback_commands:
					if (command.name in ['', callback_command[0]]) and (command.dialog == user.dialog or command.dialog == "all"):
						if not await command.handle(msg, user):
							await msg('❌ Произошла ошибка, попробуйте чуть позже')
							#await msg(sticker_id=8471)
						break
				else:
					if item['object']['message']['peer_id'] < 2000000000:
						await msg('Команда не найдена, воспользуйтесь кнопками 😔')

		await self.longpoll.update()

	def read_handlers(self):
		for root, dirs, files in os.walk('app/bot/commands'):
			check_extension = filter(lambda x: x.endswith('.py'), files)
			for command in check_extension:
				path = os.path.join(root, command)
				spec = importlib.util.spec_from_file_location(command, os.path.abspath(path))
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(module)

