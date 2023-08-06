from kronbot.core.bot import Kron

from .reports import Reports


def setup(bot: Kron):
    bot.add_cog(Reports(bot))
