import pytest
from word_statistics_app import *

def setupTokens() -> list[str]:
    return ['This', 'is', 'a', 'test', 'list', 'of', 'tokens', 'to', 'run', 'pytest', 'alongside']

@pytest.fixture()
def setupTokens():
    return setupTokens()

@pytest.fixture(autouse=True)
def summarisingAccessor():
    return Summarising()

@pytest.fixture()
def setupSummary() -> Summary:
    dummyTokens:list[str] = setupTokens()
    summarisingAccessor:Summarising = Summarising()
    return summarisingAccessor.createSummary(dummyTokens)



def test_createSummary(setupSummary:Summary):
    assert isinstance(setupSummary, Summary)

def test_addDescriptor(setupSummary:Summary):
    setupSummary.addDescriptor(WordCount(), -1)
    descriptors = setupSummary.getDescriptors()
    firstDescriptor = descriptors[0]
    assert(firstDescriptor.getDescriptorName() == 'Word Count')

def test_duplicateDescriptor(setupSummary:Summary):
    setupSummary.addDescriptor(WordCount(), -1)
    with pytest.raises(DuplicateDescriptorException):
        setupSummary.addDescriptor(WordCount(), 2)