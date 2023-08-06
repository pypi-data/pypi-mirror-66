from kronbot.core.bot import Kron

from .cleanup import Cleanup


def setup(bot: Kron):
    bot.add_cog(Cleanup(bot))
