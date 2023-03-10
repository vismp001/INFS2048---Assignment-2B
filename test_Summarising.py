import pytest
from word_statistics_app import Summarising, Summary

@pytest.fixture(autouse=True)
def setupTokens():
    return ['This', 'is', 'a', 'test', 'list', 'of', 'tokens', 'to', 'run', 'pytest', 'alongside']

def test_createSummary(setupTokens:list[str]):
    summarising = Summarising()
    newSummary:Summary = Summarising.createSummary(setupTokens)
    assert isinstance(newSummary, Summary)