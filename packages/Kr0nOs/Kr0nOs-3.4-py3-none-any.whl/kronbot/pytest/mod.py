import pytest

from kronbot.core import modlog

__all__ = ["mod"]


@pytest.fixture
async def mod(config, monkeypatch, kron):
    from kronbot.core import Config

    with monkeypatch.context() as m:
        m.setattr(Config, "get_conf", lambda *args, **kwargs: config)

        await modlog._init(kron)
        return modlog
