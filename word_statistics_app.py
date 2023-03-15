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
    def __init__(self, wordStatsManagerAccess):
        self.__wordStatsManager:WordStatsManager = wordStatsManagerAccess

    def main(self, number, output_spec:dict, input_paths):
        '''Main entry point of the console application.'''
        
        # Standardize input and output paths to single datatype which is iterable
        inputPaths:list = list(input_paths)
        outputPaths:list = list(output_spec.keys())

        # Analyze document and output results
        self.__wordStatsManager.proccess(inputPaths, outputPaths, 4)


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

class DuplicateDescriptorException(Exception):
    def __init__(self):
        super().__init__("Cannot add a duplicate descriptor to the same summary")

class Summary():
    '''Analyzes a document and generates statistics based on provided descriptors'''
    def __init__(self, tokens:list[str]):
        self.__descriptors:list[Descriptor] = []
        self.__tokens:list[str] = tokens

    def addDescriptor(self, descriptor:Descriptor, topResults:int) -> DescriptorInfo:
        '''Analyzes and adds a descriptor to the summary'''
        duplicateDescriptorFound:bool = False
        descriptorIndex:int = 0

        # Searches and raises exception for duplicate descriptor
        while duplicateDescriptorFound == False and descriptorIndex < len(self.__descriptors):
            proccessedDescriptor = self.__descriptors[descriptorIndex]
            if proccessedDescriptor.descriptorName == descriptor.descriptorName:
                raise DuplicateDescriptorException()
            descriptorIndex += 1
        
        self.__descriptors.append(descriptor)

    def getDescriptors(self) -> list[DescriptorInfo]:
        '''Returns a list of descriptions via DescriptorInfo'''
        descriptorInformation:list[DescriptorInfo] = []
        for descriptor in self.__descriptors:
            descriptorInfo:DescriptorInfo = descriptor.describe(self.__tokens)
            descriptorInformation.append(descriptorInfo)

        return descriptorInformation

class Summarising():
    '''Creates the summary object, which is used to read statistics on new documents'''
    def __init__(self):
        pass
    
    def createSummary(self, tokens:list[str]) -> Summary:
        '''Creates a Summary given a list of string tokens'''
        newSummary:Summary = Summary(tokens)
        return newSummary

class WordFrequency(Descriptor):
    def __init__(self):
        self.descriptorName = 'Word Frequency'

    def describe(self, tokens:list[str], topResults:int=4) -> DescriptorInfo:
        frequencyOfWords:dict = dict()

        # Generates and sorts token frequency dictionary
        for token in tokens:
            if frequencyOfWords.get(token) == None:
                frequencyOfWords[token] = 0
            frequencyOfWords[token] += 1

        # Sort the frequency of tokens in order of frequency
        frequencyOfWords = {token: frequency for token, frequency in sorted(frequencyOfWords.items(), key = lambda value: value[1], reverse = True)}
        
        # Only grab top results specified by topResults parameter
        limitedResultsFrequencyOfWords:dict = {}
        if topResults == -1:
            limitedResultsFrequencyOfWords = frequencyOfWords
        else:
            tokenIndex:int = 0
            for token, frequency in frequencyOfWords.items():
                limitedResultsFrequencyOfWords[token] = frequency
                if tokenIndex >= topResults:
                    break

                tokenIndex += 1
            
        # Generate a description for word frequencies within the document
        listedFrequencies:list[str] = []
        for token, frequency in limitedResultsFrequencyOfWords.items():
            singularWrittenFrequency = token + ' (' + str(frequency) + ')'
            listedFrequencies.append(singularWrittenFrequency)
        frequenciesWritten = str.join(', ', listedFrequencies)

        readOrder:int = 2
        description:str = f"Frequent words are: {frequenciesWritten}"
        return DescriptorInfo(readOrder, description, limitedResultsFrequencyOfWords)

class WordCount(Descriptor):
    def __init__(self):
        self.descriptorName = 'Word Count'
    
    def describe(self, tokens:list[str], topResults:int=-1) -> DescriptorInfo:
        # Count all tokens, otherwise counts up to the top results specified and stops
        wordCount:int
        wordTotal = len(tokens)
        if topResults == -1 or wordTotal < topResults:
            wordCount = len(tokens)
        else:
            wordCount = topResults
        
        readOrder:int = 1
        description:str = f"Contains {wordCount} words"
        value = wordCount
        return DescriptorInfo(readOrder, description, value)


# Encapsulated in the Tokenising component
class Filter(ABC):
    '''Responsible for filtering tokens'''
    def __init__(self, inclusions:list[str]):
        pass

    @abstractclassmethod
    def applyFilter(self, uniqueWord:str):
        '''Applies the filter to the given string word. If it returns true, the word passes the filter'''
        pass

class BlacklistFilter(Filter):
    def __init__(self, inclusions:list[str]):
        self.__inclusions = inclusions

    def applyFilter(self, uniqueWord:str):
        return uniqueWord in self.__inclusions and True or False

class WhitelistFilter(Filter):
    def __init__(self, inclusions:list[str]):
        self.__inclusions = inclusions

    def applyFilter(self, uniqueWord:str):
        return uniqueWord not in self.__inclusions and True or False

class TokenizeBehaviour(ABC):
    '''The behaviour defined for tokenizing a string into a list of tokens'''
    def __init__():
        pass

    @abstractclassmethod
    def tokenize(self, rawText:str) -> list[str]:
        '''Split string into usable tokens'''
        pass

class Tokeniser():
    '''Handles filtering tokens and the tokenizing proccess'''
    def __init__(self, rawText:str):
        self.__filters:list[Filter] = []
        self.__rawText:str = rawText

    def addFilter(self, filter:Filter):
        '''Adds a filter to the list of filters being applied'''
        self.__filters.append(filter)

    def tokenize(self, tokenBehaviour:TokenizeBehaviour) -> list[str]: # returns an ordered list of words as string
        '''Seperates a single string into an interpreted list of string tokens'''
        tokenizedText:list[str] = tokenBehaviour.tokenize(self.__rawText)
        return tokenizedText

class WhiteSpaceSeperator(TokenizeBehaviour):
    def __init__(self):
        pass

    def tokenize(self, rawText:str) -> list[str]:
        splitText:list[str] = str.split(rawText)
        return splitText

class Tokenising():
    '''Responsible for creating new Tokenisers, which are used to split words into tokens'''
    def __init__(self):
        pass

    def createTokeniser(self, rawText:str) -> Tokeniser:
        '''Creates a Tokeniser, responsible for splitting text into tokens strings that are neccesary in calculating statistics'''
        tokeniser:Tokeniser = Tokeniser(rawText)
        return tokeniser


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
            '.csv': CSVFormat(),
            '.txt': TXTFormat(),
        }

    def generateOutput(self, fileName:str, descriptorInformation:list[DescriptorInfo], formatType:FormatType) -> str:
        '''Generates output from a list of Descriptor Info, and the format type for the expected output file'''
        formatttedText:str = formatType.interpret(fileName, descriptorInformation)
        return formatttedText

    def getFormatTypeFromExtension(self, fileExtension:str) -> FormatType:
        formatType:FormatType = self.__extensionToFormatType[fileExtension]
        return formatType

class CSVFormat(FormatType):
    def __init__(self):
        pass

    def interpret(self, fileName:str, descriptorInformation:list[DescriptorInfo]) -> str:
        interpretedCollection = [fileName]

        for descriptorInfo in descriptorInformation:
            descriptorValue:any = descriptorInfo.value

            # Prepare key value pairs interpreter or just output value
            if isinstance(descriptorValue, dict):
                for interpretedKey, interpretedValue in descriptorValue.items():
                    interpretedCollection.append(str(interpretedKey))
                    interpretedCollection.append(str(interpretedValue))
            else:
                interpretedCollection.append(str(descriptorInfo.value))
        
        interpreted:str = str.join(',', interpretedCollection)
        return interpreted


class TXTFormat(FormatType):
    def __init__(self):
        pass

    def interpret(self, fileName:str, descriptorInformation:list[DescriptorInfo]) -> str:
        interpretedCollection = []

        for descriptorInfo in descriptorInformation:
            description:str = descriptorInfo.description
            interpretedCollection.append(description)
        
        interpreted:str = f"File {fileName} "

        # lowercase first letter to join it onto the first sentence
        firstSentence:str = interpretedCollection[0]
        firstSentence = firstSentence[0].lower() + firstSentence[1:]
        interpretedCollection[0] = firstSentence

        # Join onto the rest of the output
        interpreted = interpreted + str.join('. ', interpretedCollection)

        return interpreted

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

    def performImport(self, fileMethod:FileMethod, path:str) -> bool | str:
        '''Perform the import method for the specified FileMethod and path'''
        source = fileMethod.importFile(path)
        return source

    def performExport(self, fileMethod:FileMethod, path:str, source:str) -> bool:
        '''Perform the export method for the specified FileMethod, path and new document source'''
        fileMethod.exportFile(path, source)

class Local(FileMethod):
    def __init__(self):
        pass
    
    def importFile(self, path:str):
        success:bool
        source:str

        try:
            file = open(path, 'r')
            fileSource:str = file.read()
            file.close()

            source = fileSource
            success = True
        except:
            source = ""
            success = False
        
        return source

    def exportFile(self, path:str, source:str):
        success:bool
        
        try:
            file = open(path, 'w+')
            file.write(source)
            file.close()
            success = True
        except:
            success = False


# Encapsulated in the WordStatsManager component
class WordStatsManager():
    def __init__(self, summarisingAccess, tokenisingAccess, formattingAccess, fileAccess:FileAccess):
        self.__summarising:Summarising = summarisingAccess
        self.__tokenising:Tokenising = tokenisingAccess
        self.__formatting:Formatting = formattingAccess
        self.__fileAcess:FileAccess = fileAccess

    def proccess(self, inputPaths:list[str], outputPaths:list[str], frequencyRankAmount:int):
        '''Proccess and provide a summary for single input and output path at a time'''
        for outputPath in outputPaths:
            outputLines:list[str] = []
            for inputPath in inputPaths:
                # Check if the file was successfully imported and get its text source
                rawText = self.__fileAcess.performImport(Local(), inputPath)

                # Split text based on whitespace between words in the document
                tokeniser:Tokeniser = self.__tokenising.createTokeniser(rawText)
                tokens:list[str] = tokeniser.tokenize(WhiteSpaceSeperator())

                # Introduce descriptors, which describe, and analyze the document
                wordCountDescriptor:Descriptor = WordCount()
                wordFrequencyDescriptor:Descriptor = WordFrequency()

                # Generate summary from tokens and add descriptors to them
                summary:Summary = self.__summarising.createSummary(tokens)
                summary.addDescriptor(wordCountDescriptor, -1)
                summary.addDescriptor(wordFrequencyDescriptor, 4)
                descriptorInformation:list[DescriptorInfo] = summary.getDescriptors()

                # Get extension type and get input fileName without parent directories
                _baseInput, inputExtension = os.path.splitext(inputPath)
                _baseOutput, outputExtension = os.path.splitext(outputPath)
                inputFileName:str = _baseInput + inputExtension

                # Format text to the corresponding filetype
                formatType:FormatType = self.__formatting.getFormatTypeFromExtension(outputExtension.lower())
                outputText:str = self.__formatting.generateOutput(inputFileName, descriptorInformation, formatType)

                # Add to list of output lines
                outputLines.append(outputText)

            # Generate combined output and export to a new file
            source:str = str.join('\n', outputLines)
            self.__fileAcess.performExport(Local(), outputPath, source)
        
@click.command(no_args_is_help=True)
@click.option("--number", default=10, type=click.IntRange(min=1), help="Maximum number of frequent words to include")
@click.option("--output", "output_spec", required=True, multiple=True, type=click.Path(), callback=validate_output_paths, help="Path of an output file. The extension (.txt or .csv) determines the output format.")
@click.argument("input_paths", required=True, type=click.Path(exists=True), nargs=-1)
def main(number, output_spec:dict, input_paths):
    __consoleApp.main(number, output_spec, input_paths)

# Main entry point to the application to intansiate services
if __name__ == '__main__':
    __summarisingAccess:Summarising = Summarising()
    __tokenisingAccess = Tokenising()
    __formattingAccess = Formatting()
    __fileAccess = FileAccess()
    __wordStatsManagerAccess = WordStatsManager(__summarisingAccess, __tokenisingAccess, __formattingAccess, __fileAccess)
    __consoleApp:ConsoleApp = ConsoleApp(__wordStatsManagerAccess)

    main()