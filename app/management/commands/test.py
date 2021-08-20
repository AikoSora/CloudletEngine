from decimal import Decimal
from django.core.management import BaseCommand
from django.conf import settings
from app.models import Account # Для работы с моделью аккаунтов
from app.bot.Message import Message # Для работы с методом send (на данный момент платформа на большее не способна в API для скриптов Cron)
import os, uvloop, asyncio

class Command(BaseCommand):

    def handle(self, *args, **options):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        uvloop.install()
        self.ioloop = asyncio.get_event_loop() 
        self.ioloop.run_until_complete(asyncio.wait([self.ioloop.create_task(self.job())]))
        self.ioloop.close()
    
    async def job(self):
        for user in Account.objects.all():
            account: Account = Account.objects.filter(user_id = user.user_id).first()
            account.balance += Decimal(100)
            await Message.send("Тебе дали 100$ на халяву", user_id=user.user_id)
            # send(text=None, attachment=None, sticker_id=None, user_id=None)
        
