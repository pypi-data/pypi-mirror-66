from HystrixBox.Decoders.ASCIICipher import ASCIIDecoder
from HystrixBox.Decoders.Base64Cipher import Base64Decoder
from HystrixBox.Decoders.CaesarCipher import CaesarDecoder
from HystrixBox.Decoders.HashCipher import HashDecoder
from HystrixBox.Decoders.ReverseCipher import ReverseDecoder
############################
from HystrixBox.Extractors.emailExtractor import EmailExtractor
from HystrixBox.Extractors.ipExtractor import IPExtractor
from HystrixBox.Extractors.md5Extractor import MD5Extractor
from HystrixBox.Extractors.urlExtractor import URLExtractor
############################
from HystrixBox.personal_parser import MyParser
import argparse
###########################


ARGS_STR = """
    ___                                                 __       
   /   |   _____ ____ _ __  __ ____ ___   ___   ____   / /_ _____
  / /| |  / ___// __ `// / / // __ `__ \ / _ \ / __ \ / __// ___/
 / ___ | / /   / /_/ // /_/ // / / / / //  __// / / // /_ (__  ) 
/_/  |_|/_/    \__, / \__,_//_/ /_/ /_/ \___//_/ /_/ \__//____/  
              /____/                                             
"""

EPILOGUE_STR = 'Made by zomry1 and Matssu ©'

DECODERS_MAP = {'ascii': ASCIIDecoder.safe_decode,
                'base64': Base64Decoder.safe_decode,
                'caesar': CaesarDecoder.safe_decode,
                'reverse': ReverseDecoder.safe_decode,
                'hash': HashDecoder.safe_decode
                }

EXTRACTOR_MAP = {'url': URLExtractor.extract,
                 'ip': IPExtractor.extract,
                 'email': EmailExtractor.extract,
                 'md5': MD5Extractor.extract
                 }


###########################
def createBasicParser(description):
    # Create argumentParser
    parser = MyParser(
        prog='',
        description='\n' + description + '\n'
                    'just type the optional arguments that you need from the list\n\n' + ARGS_STR,
        epilog=EPILOGUE_STR,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.version = '1.0'

    parser.add_argument('filename',
                        type=argparse.FileType('r'))

    # Version flag
    parser.add_argument('--version', action='version')

    # Verbose flag
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')

    # Output to file
    parser.add_argument('-o', '--output',
                        help='Output file to save the results',
                        metavar='FILENAME')

    return parser


def createExtractorParser():
    # Create argumentParser
    parser = createBasicParser(    'The Ultimate Extractor, Drop your RAW DATA FILE here')
    # Specific extractor flag
    parser.add_argument('-e', '--extractor',
                        help='Choose specific extractor, {%(choices)s}',
                        choices=EXTRACTOR_MAP.keys(),
                        metavar='EXTRACTOR')
    return parser


def createEmailAnalyzerParser():
    return createBasicParser('Analyze email file')


def createStegoLSBParser():
    return createBasicParser('Try to decode data from image by LSB encode')


def createZipExtractParser():
    parser = createBasicParser('Extract recursive zip files')
    # Specific path to extract
    parser.add_argument('-p', '--path',
                        help='Choose path for extract',
                        metavar='PATH')
    return parser


def createStringParser():
    # Create argumentParser
    parser = createBasicParser('Finds and prints text strings embedded in binary files such as executables.')
    # Number of results to print
    parser.add_argument('-n',
                        type=int,
                        help='Print sequences of characters that are at least min-len characters long, Default 4',
                        metavar='NUMBER',
                        default=4)
    return parser


def createFileParser():
    return createBasicParser('Determine the type of a file')


def createDecrypterParser():
    Parser = MyParser(
        prog='',
        description='\nThe Ultimate Decoder, Drop your Cipher-text here\n'
                    'just type the optional arguments that you need from the list\n\n' + ARGS_STR,
        epilog=EPILOGUE_STR,
        formatter_class=argparse.RawTextHelpFormatter
    )

    Parser.version = '1.1'

    # Add input flag required (string or filename)
    input_group = Parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-c', '--ciphertext')
    input_group.add_argument('-f', '--filename', type=argparse.FileType('r'))

    # Version flag
    Parser.add_argument('--version', action='version')

    # Specific decoder flag
    Parser.add_argument('-d', '--decoder',
                        help='Choose specific decoder, {%(choices)s}',
                        choices=DECODERS_MAP.keys(),
                        metavar='DECODER')

    # Evaluators flags
    Parser.add_argument('-cl', '--checkLetter',
                        help='Evaluate results by letter analysis check',
                        action='store_true')

    Parser.add_argument('-cw', '--checkWord',
                        help='Evaluate results by word analysis check',
                        action='store_true')

    Parser.add_argument('-cf', '--checkFlag',
                        help='Evaluate results by flag format check',
                        metavar='FORMAT')

    # Number of results to print
    Parser.add_argument('-n', '--number',
                        type=int,
                        help='Number of results to be printed (sorted by descending score)',
                        metavar='NUMBER',
                        default=1)
    # Verbose flag
    Parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')

    # Output to file
    Parser.add_argument('-o', '--output',
                        help='Output file to save the results',
                        metavar='FILENAME')

    return Parser
