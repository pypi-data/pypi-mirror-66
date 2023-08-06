import pytest

__all__ = ["cog_mgr", "default_dir"]


@pytest.fixture()
def cog_mgr(kron):
    return kron._cog_mgr


@pytest.fixture()
def default_dir(kron):
    return kron._main_dir
