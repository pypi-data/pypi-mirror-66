import asyncio
import codecs
import contextlib
import datetime
import logging
import sys
import traceback
from datetime import timedelta

import aiohttp
import discord
import pkg_resources
from colorama import Fore, Style, init
from pkg_resources import DistributionNotFound

from kronbot.core.commands import KronHelpFormatter
from kronbot.core.i18n import Translator

from .. import VersionInfo
from .. import __version__ as kron_version
from .. import version_info as kron_version_info
from . import commands
from .config import get_latest_confs
from .utils._internal_utils import format_fuzzy_results, fuzzy_command_search
from .utils.chat_formatting import bordered, format_perms_list, humanize_timedelta, inline

log = logging.getLogger("kronbot")
init()

INTRO = r"""
 @@@  @@@ @@@@@@@   @@@@@@  @@@  @@@  @@@@@@   @@@@@@
 @@!  !@@ @@!  @@@ @@!  @@@ @@!@!@@@ @@!  @@@ !@@    
 @!@@!@!  @!@!!@!  @!@  !@! @!@@!!@! @!@  !@!  !@@!! 
 !!: :!!  !!: :!!  !!:  !!! !!:  !!! !!:  !!!     !:!
  :   :::  :   : :  : :. :  ::    :   : :. :  ::.: : 
                                                     

"""

_ = Translator(__name__, __file__)


def init_events(bot, cli_flags):
    @bot.event
    async def on_connect():
        if bot._uptime is None:
            print("Connected to Discord. Getting ready...")

    @bot.event
    async def on_ready():
        if bot._uptime is not None:
            return

        bot._uptime = datetime.datetime.utcnow()

        guilds = len(bot.guilds)
        users = len(set([m for m in bot.get_all_members()]))

        app_info = await bot.application_info()

        if app_info.team:
            if bot._use_team_features:
                bot.owner_ids = {m.id for m in app_info.team.members}
        else:
            if bot.owner_id is None:
                bot.owner_id = app_info.owner.id

        try:
            invite_url = discord.utils.oauth_url(app_info.id)
        except:
            invite_url = "Could not fetch invite url"

        prefixes = cli_flags.prefix or (await bot._config.prefix())
        lang = await bot._config.locale()
        kron_pkg = pkg_resources.get_distribution("Kr0nOs")
        dpy_version = discord.__version__

        INFO = [
            str(bot.user),
            "Prefixes: {}".format(", ".join(prefixes)),
            "Language: {}".format(lang),
            "Kron Bot Version: {}".format(kron_version),
            "Discord.py Version: {}".format(dpy_version),
            "Shards: {}".format(bot.shard_count),
        ]

        if guilds:
            INFO.extend(("Servers: {}".format(guilds), "Users: {}".format(users)))
        else:
            print("Ready. I'm not in any server yet!")

        INFO.append("{} cogs with {} commands".format(len(bot.cogs), len(bot.commands)))

        outdated_kron_message = ""
        with contextlib.suppress(aiohttp.ClientError, asyncio.TimeoutError):
            async with aiohttp.ClientSession() as session:
                async with session.get("https://pypi.org/pypi/red-discordbot/json") as r:
                    data = await r.json()
            if VersionInfo.from_str(data["info"]["version"]) > kron_version_info:
                INFO.append(
                    "Outdated version! {} is available "
                    "but you're using {}".format(data["info"]["version"], kron_version)
                )
                outdated_kron_message = (
                    "Your Kron instance is out of date! {} is the current "
                    "version, however you are using {}!"
                ).format(data["info"]["version"], kron_version)
        INFO2 = []

        reqs_installed = {"docs": None, "test": None}
        for key in reqs_installed.keys():
            reqs = [x.name for x in kron_pkg._dep_map[key]]
            try:
                pkg_resources.require(reqs)
            except DistributionNotFound:
                reqs_installed[key] = False
            else:
                reqs_installed[key] = True

        options = (
            ("Voice", True),
            ("Docs", reqs_installed["docs"]),
            ("Tests", reqs_installed["test"]),
        )

        on_symbol, off_symbol, ascii_border = _get_startup_screen_specs()

        for option, enabled in options:
            enabled = on_symbol if enabled else off_symbol
            INFO2.append("{} {}".format(enabled, option))

        print(Fore.RED + INTRO)
        print(Style.RESET_ALL)
        print(bordered(INFO, INFO2, ascii_border=ascii_border))

        if invite_url:
            print("\nInvite URL: {}\n".format(invite_url))

        bot._color = discord.Colour(await bot._config.color())
        bot._kron_ready.set()
        if outdated_kron_message:
            await bot.send_to_owners(outdated_kron_message)

    @bot.event
    async def on_command_completion(ctx: commands.Context):
        await bot._delete_delay(ctx)

    @bot.event
    async def on_command_error(ctx, error, unhandled_by_cog=False):

        if not unhandled_by_cog:
            if hasattr(ctx.command, "on_error"):
                return

            if ctx.cog:
                if commands.Cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                    return
        if not isinstance(error, commands.CommandNotFound):
            await bot._delete_delay(ctx)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help()
        elif isinstance(error, commands.ArgParserFailure):
            msg = _("`{user_input}` is not a valid value for `{command}`").format(
                user_input=error.user_input, command=error.cmd,
            )
            if error.custom_help_msg:
                msg += f"\n{error.custom_help_msg}"
            await ctx.send(msg)
            if error.send_cmd_help:
                await ctx.send_help()
        elif isinstance(error, commands.ConversionFailure):
            if error.args:
                await ctx.send(error.args[0])
            else:
                await ctx.send_help()
        elif isinstance(error, commands.UserInputError):
            await ctx.send_help()
        elif isinstance(error, commands.DisabledCommand):
            disabled_message = await bot._config.disabled_command_msg()
            if disabled_message:
                await ctx.send(disabled_message.replace("{command}", ctx.invoked_with))
        elif isinstance(error, commands.CommandInvokeError):
            log.exception(
                "Exception in command '{}'".format(ctx.command.qualified_name),
                exc_info=error.original,
            )

            message = _(
                "Error in command '{command}'. Check your console or logs for details."
            ).format(command=ctx.command.qualified_name)
            exception_log = "Exception in command '{}'\n" "".format(ctx.command.qualified_name)
            exception_log += "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
            bot._last_exception = exception_log
            await ctx.send(inline(message))
        elif isinstance(error, commands.CommandNotFound):
            fuzzy_commands = await fuzzy_command_search(
                ctx,
                commands={
                    c async for c in KronHelpFormatter.help_filter_func(ctx, bot.walk_commands())
                },
            )
            if not fuzzy_commands:
                pass
            elif await ctx.embed_requested():
                await ctx.send(embed=await format_fuzzy_results(ctx, fuzzy_commands, embed=True))
            else:
                await ctx.send(await format_fuzzy_results(ctx, fuzzy_commands, embed=False))
        elif isinstance(error, commands.BotMissingPermissions):
            if bin(error.missing.value).count("1") == 1:  # Only one perm missing
                msg = _("I require the {permission} permission to execute that command.").format(
                    permission=format_perms_list(error.missing)
                )
            else:
                msg = _("I require {permission_list} permissions to execute that command.").format(
                    permission_list=format_perms_list(error.missing)
                )
            await ctx.send(msg)
        elif isinstance(error, commands.UserFeedbackCheckFailure):
            if error.message:
                await ctx.send(error.message)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(_("That command is not available in DMs."))
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.send(_("That command is only available in DMs."))
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            if delay := humanize_timedelta(seconds=error.retry_after):
                msg = _("This command is on cooldown. Try again in {delay}.").format(delay=delay)
            else:
                msg = _("This command is on cooldown. Try again in 1 second.")
            await ctx.send(msg, delete_after=error.retry_after)
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(
                _(
                    "Too many people using this command."
                    " It can only be used {number} time(s) per {type} concurrently."
                ).format(number=error.number, type=error.per.name)
            )
        else:
            log.exception(type(error).__name__, exc_info=error)

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
        discord_now = message.created_at
        if (
            not bot._checked_time_accuracy
            or (discord_now - timedelta(minutes=60)) > bot._checked_time_accuracy
        ):
            system_now = datetime.datetime.utcnow()
            diff = abs((discord_now - system_now).total_seconds())
            if diff > 60:
                log.warning(
                    "Detected significant difference (%d seconds) in system clock to discord's "
                    "clock. Any time sensitive code may fail.",
                    diff,
                )
            bot._checked_time_accuracy = discord_now

    @bot.event
    async def on_command_add(command: commands.Command):
        disabled_commands = await bot._config.disabled_commands()
        if command.qualified_name in disabled_commands:
            command.enabled = False
        for guild in bot.guilds:
            disabled_commands = await bot._config.guild(guild).disabled_commands()
            if command.qualified_name in disabled_commands:
                command.disable_in(guild)

    async def _guild_added(guild: discord.Guild):
        disabled_commands = await bot._config.guild(guild).disabled_commands()
        for command_name in disabled_commands:
            command_obj = bot.get_command(command_name)
            if command_obj is not None:
                command_obj.disable_in(guild)

    @bot.event
    async def on_guild_join(guild: discord.Guild):
        await _guild_added(guild)

    @bot.event
    async def on_guild_available(guild: discord.Guild):
        # We need to check guild-disabled commands here since some cogs
        # are loaded prior to `on_ready`.
        await _guild_added(guild)

    @bot.event
    async def on_guild_leave(guild: discord.Guild):
        # Clean up any unneeded checks
        disabled_commands = await bot._config.guild(guild).disabled_commands()
        for command_name in disabled_commands:
            command_obj = bot.get_command(command_name)
            if command_obj is not None:
                command_obj.enable_in(guild)

    @bot.event
    async def on_cog_add(cog: commands.Cog):
        confs = get_latest_confs()
        for c in confs:
            uuid = c.unique_identifier
            group_data = c.custom_groups
            await bot._config.custom("CUSTOM_GROUPS", c.cog_name, uuid).set(group_data)


def _get_startup_screen_specs():
    """Get specs for displaying the startup screen on stdout.

    This is so we don't get encoding errors when trying to print unicode
    emojis to stdout (particularly with Windows Command Prompt).

    Returns
    -------
    `tuple`
        Tuple in the form (`str`, `str`, `bool`) containing (in order) the
        on symbol, off symbol and whether or not the border should be pure ascii.

    """
    encoder = codecs.getencoder(sys.stdout.encoding)
    check_mark = "\N{SQUARE ROOT}"
    try:
        encoder(check_mark)
    except UnicodeEncodeError:
        on_symbol = "[X]"
        off_symbol = "[ ]"
    else:
        on_symbol = check_mark
        off_symbol = "X"

    try:
        encoder("┌┐└┘─│")  # border symbols
    except UnicodeEncodeError:
        ascii_border = True
    else:
        ascii_border = False

    return on_symbol, off_symbol, ascii_border
