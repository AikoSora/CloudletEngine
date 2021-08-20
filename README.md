# CloudletEngine
Platform for writing bots for VK `Python 3.7+`

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

To start the server, use the command:
```shell
python manage.py runserver
```
