import pytest
import vcr

from yippi import AsyncYippiClient
from yippi import YippiClient


@pytest.fixture
def client():
    return YippiClient("Yippi", "0.1", "Error-")


@pytest.fixture
async def async_client():
    async_client = AsyncYippiClient("Yippi", "0.1", "Error-")
    yield async_client
    await async_client.close()


@vcr.use_cassette("tests/vcr/post_1383235.yaml", decode_compressed_response=True)
def test_post(client):
    post = client.post(1383235)
    post.tags["general"].append("solo")
    post.tags["general"].remove("male/male")
    assert post.get_tags_difference() == "solo -male/male"


@vcr.use_cassette("tests/vcr/notes_post.yaml", decode_compressed_response=True)
def test_note(client):
    note = client.notes(limit=1)[0]
    assert note.get_post()


@vcr.use_cassette("tests/vcr/pools_post.yaml", decode_compressed_response=True)
def test_pool_sync(client):
    pool = client.pools("Weekend 2")[0]
    posts = pool.get_posts()
    assert len(posts) == 48


@pytest.mark.asyncio
async def test_pool_async(async_client):
    pool = (await async_client.pools("Weekend 2"))[0]
    posts = await pool.get_posts()
    assert len(posts) == 48


@vcr.use_cassette("tests/vcr/flag_post.yaml", decode_compressed_response=True)
def test_flag(client):
    flag = client.flags(limit=1)[0]
    assert flag.get_post()
