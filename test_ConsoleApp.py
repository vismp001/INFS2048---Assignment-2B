import pytest
from word_statistics_app import *

@pytest.fixture()
def __wordStatsManagerAccess():
    return WordStatsManager()

def test_consoleAppCompiles():
    consoleApp = ConsoleApp(WordStatsManager)
    assert isinstance(consoleApp, ConsoleApp)