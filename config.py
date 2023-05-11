from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

OPENAI_TOKEN = env.str("OPENAI_TOKEN")
API_TOKEN = env.str("API_TOKEN")

ADMIN_ID = env.str("ADMIN_ID")
