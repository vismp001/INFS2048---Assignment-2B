import pytest
from word_statistics_app import *

def getTokens() -> list[str]:
    return ['This', 'is', 'a', 'test', 'list', 'of', 'tokens', 'to', 'run', 'a', 'pytest', 'alongside']

def getRawString() -> str:
    return "This is a test list of tokens to run a pytest alongside"

@pytest.fixture()
def setupFilterInclusions():
    return ['test', 'a' 'list', 'tokens']

@pytest.fixture()
def setupTokens():
    return getTokens()

@pytest.fixture()
def setupRawString():
    return getRawString()

@pytest.fixture()
def setupTokeniser():
    return Tokeniser(getRawString())

@pytest.fixture()
def setupTokenising():
    return Tokenising()


def test_intentionalFilterChange(setupTokens, setupFilterInclusions):
    blacklist:Filter = BlacklistFilter(setupFilterInclusions)
    whitelist:Filter = WhitelistFilter(setupFilterInclusions)

    keepBlacklistWord:bool = blacklist.applyFilter(setupTokens[4])
    keepWhitelistWord:bool = whitelist.applyFilter(setupTokens[4])
    assert keepWhitelistWord == True and keepBlacklistWord == False

def test_tokenizeEquals(setupRawString:str, setupTokens:list[str]):
    tokenizeBehaviour:TokenizeBehaviour = WhiteSpaceSeperator()
    newTokens = tokenizeBehaviour.tokenize(setupRawString)
    assert str(newTokens) == str(setupTokens)

def test_addFilterToSummariser(setupTokeniser:Tokeniser, setupFilterInclusions:list[str]):
    blacklist:Filter = BlacklistFilter(setupFilterInclusions)
    setupTokeniser.addFilter(blacklist)

def test_summariserTokenizeReturnsTokens(setupTokeniser:Tokeniser, setupFilterInclusions:list[str]):
    tokens:list[str] = setupTokeniser.tokenize(WhiteSpaceSeperator())

    foundNonStringToken = False
    for token in tokens:
        if isinstance(token, str) == False:
            foundNonStringToken = True
    
    assert not foundNonStringToken

def test_tokenisingCreatesTokeniser(setupTokenising:Tokenising, setupRawString:str):
    newTokeniser:Tokeniser = setupTokenising.createTokeniser(setupRawString)
    assert isinstance(newTokeniser, Tokeniser)
