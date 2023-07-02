from app.src.bot.commands.user import add_commands as user
from app.src.bot.commands.admin import add_commands as admin


def all_commands(app):
    user(app)
    admin(app)
