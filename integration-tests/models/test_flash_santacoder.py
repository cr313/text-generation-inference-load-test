import pytest

from utils import health_check


@pytest.fixture(scope="module")
def flash_santacoder(launcher):
    with launcher("bigcode/santacoder") as client:
        yield client


@pytest.mark.asyncio
async def test_flash_santacoder(flash_santacoder, snapshot_test):
    await health_check(flash_santacoder, 60)

    response = await flash_santacoder.generate("def print_hello", max_new_tokens=10)

    assert response.details.generated_tokens == 10
    assert snapshot_test(response)


@pytest.mark.asyncio
async def test_flash_santacoder_load(flash_santacoder, generate_load, snapshot_test):
    await health_check(flash_santacoder, 60)

    responses = await generate_load(
        flash_santacoder, "def print_hello", max_new_tokens=10, n=4
    )

    assert len(responses) == 4

    assert snapshot_test(responses)
