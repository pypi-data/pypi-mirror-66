from kronbot.core.bot import Kron

from .filter import Filter


def setup(bot: Kron):
    bot.add_cog(Filter(bot))
