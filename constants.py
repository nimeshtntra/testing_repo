import environ

LOG_FORMAT=('{lineno} *** {name} *** {asctime} *** {message}')
env = environ.Env()
env.read_env('/home/botree/travel_search_bot/.env')
TOKEN = env('USER_BOT_TOKEN')
DATABASE = env("DATABASE")


