""" 
----------------- API CloudletEngine -----------------
______________________________________________________
Cloudlet Engine - Asynchronous Engine!

be sure to import! | Обязательны в каждом файле
from app.bot import handler
from app.models import Account

Decorator: 
handler -|- message(name=str, dialog=str, with_args=bool) # with_args требуется для получения аргументов в команде боту
		 |- payload(name=str, dialog=str) # Dialog - указывает в каком диалоге работает команда

Function:
msg(text=str, attachment=str, sticker_id=int, user_id=int) - msg is an asynchronous function and is called via await!
----------------------------------------------------------
msg -|- buttons(dict) - options = {"name": "name", "payload": "payload_command", "color": "primary/negative/positive/secondary"} / not asynchronous function
	 |- inline_buttons(dict) - options = {"name": "name", "payload": "payload_command", "color": "primary/negative/positive/secondary"} / not asynchronous function
	 |- request("method", params) - params = dict / request is an asynchronous function and is called via await!
	 |- event - LongPoll event dict / variable 
______________________________________________________
Building buttons|
________________|

msg.buttons({"name": "1"})
_____________________________
|			   1			|
-----------------------------

msg.buttons({"name": "1"}, {"name": '2'})
________________________________
|		1	   |		2		|
--------------------------------

msg.buttons({"name": "1"}, {"name": '2'})
msg.buttons({"name": "3"})

________________________________
|		1	   |		2		|
--------------------------------
|				3				|
---------------------------------

With Inilne buttons as well.
Buttons are built before calling the msg(text) function
"""

# Example Command

from app.bot import handler #Importing Decorators
from app.models import Account #Importing Account model Django
from random import randint as random

@handler.message(name = 'test') #Decorator Message
async def _(msg, user):

	msg.buttons({"name": "Default Button"})
	msg.buttons({"name": "Payload Button", "payload": "test"}) #Setting up the button on the payload decorator
	msg.buttons({"name": "Colored Button", "color": "negative"})
	await msg("Button")

	msg.inline_buttons({"name": "Default Inline"})
	msg.inline_buttons({"name": "Payload Inline", "payload": "test payload button"}) #Setting up the button on the payload decorator
	msg.inline_buttons({"name": "Colored Inline", "color": "negative"})
	await msg("Inline Button")
	
	await msg("User ID", user_id=msg.event['object']['message']['from_id']) # тут можно было написать user.user_id но указан msg.event для демонстрации работы
	await msg.request("messages.send", {"peer_id": msg.event['object']['message']['peer_id'], "message": "API Request", 'random_id': random(0, 100000)})

@handler.payload(name = 'test') #Decorator Payload
async def _(msg, user):
	print(msg.path_args)
	await msg("Payload Command")


#CALLBACK BUTTONS
@handler.payload(name = 'test_command')
async def _(msg, user):
	await msg("Простите, Callback кнопки работают только в мобильном приложении ВК")

@handler.message(name = 'callback')
async def _(msg, user):
	user.temp = "0"
	user.save()

	msg.callback_buttons({"name": "Нажми меня", "command": "test_command", "color": "positive"})
	await msg("Вы нажали 0 раз")

@handler.callback(name = 'test_command')
async def _(msg, user):
	user.temp = f"{int(user.temp) + 1}"
	user.save()

	if int(user.temp) % 5 == 0:
		await msg.snackbar(f"Достижение!\nВы нажали {user.temp} раз на кнопку")
		await msg("Поздравляем!")

	msg.callback_buttons({"name": "Нажми меня", "command": "test_command", "color": "positive"})
	await msg.edit(f"Вы нажали {user.temp} раз")