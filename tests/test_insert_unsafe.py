from datasette.app import Datasette
from datasette.plugins import pm
import pytest
import sqlite_utils
import httpx


@pytest.fixture
def db_path(tmp_path_factory):
    db_directory = tmp_path_factory.mktemp("dbs")
    db_path = db_directory / "data.db"
    db = sqlite_utils.Database(db_path)
    db.vacuum()
    return db_path


@pytest.mark.asyncio
async def test_plugin_is_installed():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/plugins.json")
        assert 200 == response.status_code
        installed_plugins = {p["name"] for p in response.json()}
        assert "datasette-insert-unsafe" in installed_plugins


@pytest.mark.asyncio
async def test_insert_allowed(db_path):
    app = Datasette([str(db_path)]).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.post(
            "http://localhost/-/insert/data/newtable", json=[{"foo": "bar"}],
        )
        assert 200 == response.status_code


@pytest.mark.asyncio
async def test_insert_disallowed_if_plugin_disabled(db_path):
    app = Datasette([str(db_path)]).app()
    plugin = pm.unregister(name="insert_unsafe")
    try:
        async with httpx.AsyncClient(app=app) as client:
            response = await client.post(
                "http://localhost/-/insert/data/newtable", json=[{"foo": "bar"}],
            )
            assert 403 == response.status_code
    finally:
        pm.register(plugin, name="insert_unsafe")
