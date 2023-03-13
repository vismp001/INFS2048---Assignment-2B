import os
import click
from dataclasses import dataclass
from abc import ABC, abstractclassmethod

# Specify and validate paths for the ConsoleApp
# This section is part of the code stub.
VALID_FORMATS = ['.csv', '.txt']
def validate_output_paths(_ctx, _param, paths):
    """Verify that the extension of each output file path corresponds to a known
          output format, and return a dictionary mapping the path
          to its format."""
    def get_format_from_path(path):
        _base, extension = os.path.splitext(path)
        return extension.lower()

    output_spec = {}
    for path in paths:
        format = get_format_from_path(path)
        if format not in VALID_FORMATS:
            raise click.BadParameter(f"Output file {path} has an invalid format {format}. Known formats are {', '.join(VALID_FORMATS)}.")
        output_spec[path] = format

    return output_spec


# Encapsulated in the ConsoleApp component
class ConsoleApp():
    def __init__(self):
        self.__wordStatsManager

    @click.command(no_args_is_help=True)
    @click.option("--number", default=10, type=click.IntRange(min=1), help="Maximum number of frequent words to include")
    @click.option("--output", "output_spec", required=True, multiple=True, type=click.Path(), callback=validate_output_paths, help="Path of an output file. The extension (.txt or .csv) determines the output format.")
    @click.argument("input_paths", required=True, type=click.Path(exists=True), nargs=-1)
    def main(number, output_spec, input_paths):
        """Main entry point of the console application."""
        print(output_spec, type(output_spec['out.txt']))
        print(input_paths, type(input_paths[1]))


# Encapsulated in the WordStatsManager component
class WordStatsManager():
    def __init__(self):
        pass

    def proccess(self, inputPath:str, outputPath:str, frequencyRankAmount:int):
        '''Proccess and provide a summary for single input and output path at a time'''
        pass

    def proccessMultiple(self, inputPaths:list, outputPaths:list, frequencyRankAmount:int):
        '''Proccess, and provide a summary for multiple input or output paths at a time'''
        pass


# Encapsulated in the Summarising component
@dataclass
class DescriptorInfo():
    '''Contains statistical information, usually generated from a Descriptor'''
    readOrder:int
    description:str
    value:any

    def __init__(self, readOrder:int, description:str, value:any):
        self.readOrder = readOrder
        self.description = description
        self.value = value

class Descriptor(ABC):
    '''Analyzes tokens to generate useful statistics, and returns information encapsulated in DescriptorInfo'''
    def __init__(self):
        self.descriptorName:str
        self.__priority:int

    @abstractclassmethod
    def describe(self, tokens:list[str], rankAmount:int=1) -> DescriptorInfo:
        '''Describes the statistics associated to the descriptors meaning. RankAmount specifies how many results to return within a limit.'''
        pass

    def getDescriptorName(self) -> str:
        return self.descriptorName

class DuplicateDescriptorException(Exception):
    def __init__(self):
        super().__init__("Cannot add a duplicate descriptor to the same summary")

class Summary():
    '''Analyzes a document and generates statistics based on provided descriptors'''
    def __init__(self):
        self.__descriptors:list[Descriptor] = []

    def addDescriptor(self, descriptor:Descriptor, rankAmount:int) -> DescriptorInfo:
        '''Analyzes and adds a descriptor to the summary'''
        duplicateDescriptorFound:bool = False
        descriptorIndex:int = 0

        # Searches and raises exception for duplicate descriptor
        while duplicateDescriptorFound == False and descriptorIndex < len(self.__descriptors):
            proccessedDescriptor = self.__descriptors[descriptorIndex]
            if proccessedDescriptor.descriptorName == descriptor.descriptorName:
                raise DuplicateDescriptorException()
            
        self.__descriptors.append(descriptor)

    def getDescriptors(self) -> list[Descriptor]:
        '''Returns a list of descriptors'''
        return self.__descriptors.copy()

class Summarising():
    '''Creates the summary object, which is used to read statistics on new documents'''
    def __init__(self):
        pass
    
    def createSummary(self, tokens:list[str]) -> Summary:
        '''Creates a Summary given a list of string tokens'''
        newSummary:Summary = Summary()
        return newSummary

class WordFrequency(Descriptor):
    def __init__(self):
        self.descriptorName = 'Word Frequency'

    def describe(self, tokens:list[str], rankAmount:int=1) -> dict:
        pass

class WordCount(Descriptor):
    def __init__(self):
        self.descriptorName = 'Word Count'
        print(self.descriptorName)
    
    def describe(self, tokens:list[str], rankAmount:int=1) -> int:
        pass


# Encapsulated in the Tokenising component
class Filter(ABC):
    '''Responsible for filtering tokens'''
    def __init__(self):
        pass

    @abstractclassmethod
    def applyFilter(self, uniqueWord:str):
        '''Applies the filter to the given string word. If it returns true, the word passes the filter'''
        pass

class TokenizeBehaviour(ABC):
    '''The behaviour defined for tokenizing a string into a list of tokens'''
    def __init__():
        pass

    @abstractclassmethod
    def tokenize(self, rawString:str) -> list[str]:
        '''Split string into usable tokens'''
        pass

class Tokeniser():
    '''Handles filtering tokens and the tokenizing proccess'''
    def __init__(self, rawString:str):
        self.__filters:list[Filter] = []
        self.__rawString:str = rawString

    def addFilter(self, filter:Filter):
        '''Adds a filter to the list of filters being applied'''
        pass

    def tokenize(self, tokenBehaviour:TokenizeBehaviour) -> list[str]: # returns an ordered list of words as string
        '''Seperates a single string into an interpreted list of string tokens'''
        pass

class WhiteSpaceSeperator(TokenizeBehaviour):
    def __init__():
        pass

    def tokenize(self, rawString: str) -> list[str]:
        pass

class Tokenising():
    '''Responsible for creating new Tokenisers, which are used to split words into tokens'''
    def __init__(self):
        pass

    def createTokeniser(self, rawText : str) -> Tokeniser:
        '''Creates a Tokeniser, responsible for splitting text into tokens strings that are neccesary in calculating statistics'''
        pass


class FormatType(ABC):
    '''Interprets statistics and outputs the human-readable string for the associated file extension'''
    def __init__(self):
        pass

    def interpret(self, descriptorInformation:list[DescriptorInfo]) -> str:
        '''Creates a new string containing the summary information, given a list of DescriptorInfo'''
        pass

class Formatting():
    '''Manages generating statistical output and for the extension type'''
    def __init__(self):
        self.__extensionToFormatType = {
            'csv': CSVFormat(),
            'txt': TXTFormat(),
        }

    def generateOutput(self, descriptorInformation:list[DescriptorInfo], formatType:FormatType) -> str:
        '''Generates output from a list of Descriptor Info, and the format type for the expected output file'''
        pass

    def getFormatTypeFromExtension(self, fileExtension:str) -> FormatType:
        pass

class CSVFormat(FormatType):
    def __init__(self):
        pass

    def interpret(self, descriptorInformation:list[DescriptorInfo]) -> str:
        pass

class TXTFormat(FormatType):
    def __init__(self):
        pass

    def interpret(self, descriptorInformation:list[DescriptorInfo]) -> str:
        pass

# Encapsulated in FileAccess component
class FileMethod(ABC):
    '''Specifies import and export methods for a filetype'''
    def __init__(self):
        pass
    
    @abstractclassmethod
    def importFile(self, path:str):
        '''Import file to analyze'''
        pass

    @abstractclassmethod
    def exportFile(self, path:str, source:str):
        '''Export analysis file'''
        pass

class FileAccess():
    '''Access files to be analyzed'''
    def __init__(self):
        pass

    def performImport(fileMethod:FileMethod, path:str) -> bool | str:
        '''Perform the import method for the specified FileMethod and path'''
        pass

    def performExport(fileMethod:FileMethod, path:str, source:str) -> bool:
        '''Perform the export method for the specified FileMethod, path and new document source'''
        pass

class Local(FileMethod):
    def __init__(self):
        pass
    
    def importFile(self, path:str):
        pass

    def exportFile(self, path:str, source:str):
        pass

# Main entry point to the application
if __name__ == '__main__':
    consoleApp:ConsoleApp = ConsoleApp()
    consoleApp.main()