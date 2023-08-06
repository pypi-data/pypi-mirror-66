from kronbot.core.bot import Kron

from .modlog import ModLog


def setup(bot: Kron):
    bot.add_cog(ModLog(bot))
