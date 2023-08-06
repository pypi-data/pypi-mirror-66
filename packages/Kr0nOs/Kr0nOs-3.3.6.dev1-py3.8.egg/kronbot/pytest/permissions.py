import pytest

from kronbot.cogs.permissions import Permissions
from kronbot.core import Config


@pytest.fixture()
def permissions(config, monkeypatch, kron):
    with monkeypatch.context() as m:
        m.setattr(Config, "get_conf", lambda *args, **kwargs: config)
        return Permissions(kron)
