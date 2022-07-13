# CloudletEngine
Platform for writing bots for VK `Python 3.7+`
<i><br />moved to https://github.com/SekaiTeam/cloudlet_engine</i>

### Installing this project
```shell
git clone https://github.com/YamioKDL/CloudletEngine.git
```

Install all the necessary packages to work with the project:
```shell
pip install -r requirements.txt
```

At the end, configure the connection to the database and run the migrations command:
```shell
python manage.py migrate
```

### Run bot

To start the bot, use the command:
```shell
python manage.py startbot
```

### API

Examples and API of the platform can be viewed [here](https://github.com/YamioKDL/CloudletEngine/blob/main/app/bot/commands/api.py)
<br />Commands need to be created in Python files and saved along the path /app/bot/commands/
