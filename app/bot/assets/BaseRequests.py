import traceback, sys, asyncio

class Command:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler', 'admin'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']
        self.admin = kwargs['admin']
        self.with_args = kwargs['with_args']

    async def handle(self, msg, user):
        try:
            asyncio.ensure_future(self.__handler(msg, user))
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            return False

class PayloadCommand:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']

    async def handle(self, bot, user):
        try:
            asyncio.ensure_future(self.__handler(bot, user))
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            return False

class CallbackCommand:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name']
        self.dialog = kwargs['dialog']
        self.__handler = kwargs['handler']

    async def handle(self, bot, user):
        try:
            asyncio.ensure_future(self.__handler(bot, user))
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            return False