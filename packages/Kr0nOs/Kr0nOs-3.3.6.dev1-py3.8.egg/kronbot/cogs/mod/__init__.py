from kronbot.core.bot import Kron

from .mod import Mod


async def setup(bot: Kron):
    cog = Mod(bot)
    bot.add_cog(cog)
    await cog.initialize()
