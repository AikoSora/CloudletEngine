import asyncio, aiohttp, os

from json import loads
from django.conf import settings
from random import choice as CH

API_URL = "https://api.vk.com/method/"

async def get(url = API_URL, method="", params={}):
	session = aiohttp.ClientSession(trust_env = True, connector=aiohttp.TCPConnector(verify_ssl=False))
	try:
		async with session.get(f"{url}{method}", params=params) as response:
			response = await response.read()
		await session.close()
		return loads(response)
	except:
		await session.close()
		return await get(url, method, params)

async def post(url = API_URL, method="", params={}):
	session = aiohttp.ClientSession(trust_env = True, connector=aiohttp.TCPConnector(verify_ssl=False))
	try:
		async with session.post(f"{url}{method}", params=params) as response:
			response = await response.read()
		await session.close()
		return loads(response)
	except:
		await session.close()
		return await post(url, method, params)

async def api(method="", params={}):
	params.update({'access_token': CH(settings.BOT_TOKENS), 'group_id': settings.BOT_GROUP_ID, "v": settings.API})
	response = await post(method = method, params=params)
	return response

class LongPoll:
	def __init__(self):
		os.system("clear")
		print("Starting...")
		self.wait = 25
		self.data = {"server": None, "key": None, "ts": None}
		self.is_work = True
		self.func = None

	async def get_server(self):
		response = await api("groups.getLongPollServer")
		self.data['server'] = response["response"]["server"]
		self.data['key'] = response["response"]["key"]
		self.data["ts"] = response['response']["ts"]

	def event(self, **kwargs):
		def wrapper(func):
			self.func = func
		return wrapper

	async def update(self):
		print("Loading is Done :)")
		while self.is_work:
			if self.data["ts"] is None:
				await self.get_server()

			longpoll_response = await get(f'{self.data["server"]}?act=a_check&key={self.data["key"]}&ts={self.data["ts"]}&wait={self.wait}')

			if settings.DEBUG_BOT:
				print(f"[Cloudlet Engine] {longpoll_response}")

			if "failed" in longpoll_response:
				self.handle_error(longpoll_response)
				continue

			self.data["ts"] = longpoll_response["ts"]

			for item in longpoll_response["updates"]:
				await self.func(item)

	def handle_error(self, error):
		if error["failed"] == 1:
			self.data["ts"] = error["ts"]
		elif error["failed"] in [2, 3]:
			self.data["ts"] = None