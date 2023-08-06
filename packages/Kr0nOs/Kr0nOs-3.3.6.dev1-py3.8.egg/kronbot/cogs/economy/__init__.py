from kronbot.core.bot import Kron

from .economy import Economy


def setup(bot: Kron):
    bot.add_cog(Economy(bot))
