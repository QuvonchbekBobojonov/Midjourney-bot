from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

ADMIN_ID = env.str("ADMIN_ID")

# DATABESE config

HOST = env.str("HOST")
PORT = env.str("PORT")
DATABESE = env.str("DATABASE")
USER = env.str("USER")
PASSWORD = env.str("PASSWORD")
