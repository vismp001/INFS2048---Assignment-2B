import pytest
from word_statistics_app import *

@pytest.fixture()
def setupSummarisingAccess():
    return Summarising()

@pytest.fixture()
def setupTokenisingAccess():
    return Tokenising()

@pytest.fixture()
def setupFormattingAccess():
    return Formatting()

@pytest.fixture()
def setupFileAccess():
    return FileAccess()

def test_WordStatsManagerCompiles(setupSummarisingAccess, setupTokenisingAccess, setupFormattingAccess, setupFileAccess):
    wordStatsManager = WordStatsManager(setupSummarisingAccess, setupTokenisingAccess, setupFormattingAccess, setupFileAccess)
    assert isinstance(wordStatsManager, WordStatsManager)