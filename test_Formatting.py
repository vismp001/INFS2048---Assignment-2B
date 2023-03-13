import pytest
from word_statistics_app import *

def getTokens() -> list[str]:
    return ['This', 'is', 'a', 'test', 'list', 'of', 'tokens', 'to', 'run', 'a', 'pytest', 'alongside']

@pytest.fixture()
def setupTokens():
    return getTokens()

@pytest.fixture()
def setupFormatting() -> Formatting:
    return Formatting()

@pytest.fixture()
def setupDescriptors() -> list[DescriptorInfo]:
    descriptorInformation:list[DescriptorInfo] = [WordCount().describe(getTokens()), WordFrequency().describe(getTokens())]
    return descriptorInformation

def test_interperetDescriptorsIsString(setupDescriptors):
    CSVFormatter:FormatType = CSVFormat()
    result:str = CSVFormatter.interpret('file1.txt', setupDescriptors)
    assert isinstance(result, str)

def test_interpretDescriptorExpectedOutputCSV(setupDescriptors):
    CSVFormatter:FormatType = CSVFormat()
    result:str = CSVFormatter.interpret('file1.txt', setupDescriptors)
    assert result == "file1.txt,12,a,2,This,1,is,1,test,1"

def test_interpretDescriptorExpectedOutputTXT(setupDescriptors):
    CSVFormatter:FormatType = TXTFormat()
    result:str = CSVFormatter.interpret('file1.txt', setupDescriptors)
    assert result == "File file1.txt contains 12 words. Frequent words are: a (2), This (1), is (1), test (1)"

def test_returnsCorrectFormatTypeTXT(setupFormatting:Formatting):
    formatType:FormatType = setupFormatting.getFormatTypeFromExtension('txt')
    assert isinstance(formatType, TXTFormat)

def test_returnsCorrectFormatTypeCSV(setupFormatting:Formatting):
    formatType:FormatType = setupFormatting.getFormatTypeFromExtension('csv')
    assert isinstance(formatType, CSVFormat)

def test_formattingGeneratesOutputString(setupFormatting:Formatting, setupDescriptors):
    output:str = setupFormatting.generateOutput('file1.txt', setupDescriptors, TXTFormat())
    assert isinstance(output, str)