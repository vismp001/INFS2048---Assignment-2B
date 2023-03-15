import pytest
from word_statistics_app import *

@pytest.fixture()
def setupTXTOutput() -> Formatting:
    return "File file1.txt contains 12 words. Frequent words are: a (2), This (1), is (1), test (1)"

@pytest.fixture
def setupCSVOutput() -> Formatting:
    return "file1.txt,12,a,2,This,1,is,1,test,1"

def fileAccessCompiles():
    FileAccess()

# Cannot test import or export functionalities without modifying external environment
# Cannot use Mock due to limitations of assesment piece.
#    - Tests that would run here otherwise, include test_importSuccess, test_importIsString and test_exportSuccess
#    - Fixtures in test_FileAccess.py show how import / export methods results would be compared