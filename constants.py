import environ

LOG_FORMAT=('{lineno} *** {name} *** {asctime} *** {message}')
env = environ.Env()
env.read_env('/home/botree/travel_search_bot/.env')
TOKEN = env('LOCAL_TOKEN')
DATA_BASE = env("DATA_BASE")

TOKEN_STATUS = [
       ('Active', 'Active'),
       ('Expire', 'Expire')
    ]