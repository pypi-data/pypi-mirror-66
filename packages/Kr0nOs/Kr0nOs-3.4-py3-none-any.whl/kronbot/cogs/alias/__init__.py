from kronbot.core.bot import Kron

from .alias import Alias


def setup(bot: Kron):
    bot.add_cog(Alias(bot))
