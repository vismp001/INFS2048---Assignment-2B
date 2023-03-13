import pytest
from word_statistics_app import *

def getTokens() -> list[str]:
    return ['This', 'is', 'a', 'test', 'list', 'of', 'tokens', 'to', 'run', 'a', 'pytest', 'alongside']

@pytest.fixture()
def setupTokens():
    return getTokens()

@pytest.fixture(autouse=True)
def summarisingAccessor():
    return Summarising()

@pytest.fixture()
def setupSummary() -> Summary:
    dummyTokens:list[str] = getTokens()
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

def test_descriptorReturnsDescriptorInfo(setupTokens):
    descriptor:Descriptor = WordFrequency()
    descriptorInfo:DescriptorInfo = descriptor.describe(setupTokens)

    assert(isinstance(descriptorInfo, DescriptorInfo))

def test_descriptorDescriptionExists(setupTokens):
    descriptor:Descriptor = WordFrequency()
    descriptorInfo:DescriptorInfo = descriptor.describe(setupTokens)

    assert(isinstance(descriptorInfo.description, str))

def test_descriptorValueExists(setupTokens):
    descriptor:Descriptor = WordFrequency()
    descriptorInfo:DescriptorInfo = descriptor.describe(setupTokens)

    assert(descriptorInfo.description is not None)

# def test_descriptorNegativeTopResultsReadsAll(newSummary:Summary):