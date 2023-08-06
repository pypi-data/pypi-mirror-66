from kronbot.core import Config
from kronbot.core.bot import Kron

from .apis import _pass_config_to_apis
from .audio_dataclasses import _pass_config_to_dataclasses
from .converters import _pass_config_to_converters
from .databases import _pass_config_to_databases
from .playlists import _pass_config_to_playlist
from .utils import _pass_config_to_utils


def pass_config_to_dependencies(config: Config, bot: Kron, localtracks_folder: str):
    _pass_config_to_databases(config, bot)
    _pass_config_to_utils(config, bot)
    _pass_config_to_dataclasses(config, bot, localtracks_folder)
    _pass_config_to_apis(config, bot)
    _pass_config_to_playlist(config, bot)
    _pass_config_to_converters(config, bot)
