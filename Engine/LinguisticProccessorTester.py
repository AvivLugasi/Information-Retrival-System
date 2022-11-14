import difflib
from LinguisticProccessor import Processor as prc
from Utils.System import System
import sys

System = System()

def runCaseFoldingTests(token: str, ling_proccessor: prc):
    """Call to Processor's caseFolding function"""
    return ling_proccessor.caseFolding(token)


def runRemovePunctuationTests(token: str, ling_proccessor: prc):
    """Call to Processor's removePunctuation function"""
    return ling_proccessor.removePunctuation(token)

def runRemoveStopWordsTests(token: str, ling_proccessor: prc):
    """Call to Processor's removeStopWords function"""
    return ling_proccessor.removeStopWords(token)

def runPerformStemmingTests(token: str, ling_proccessor: prc):
    """Call to Processor's performStemming function"""
    return ling_proccessor.performStemming(token)

def runLinguisticProccessingTests(token: str, ling_proccessor: prc):
    """Call to Processor's linguisticProccessing function"""
    return ling_proccessor.linguisticProccessing(token)


def performTest(input_file, output_file, ling_proccessor: prc, func):
    """peroform the required function test for each input and write the result to the output file"""
    line_num = 1
    for line in input_file:
        System.log("perform test for {} line number:{}".format(line, str(line_num)))
        # perform test on an input line
        try:
            output = func(line, ling_proccessor)
        # if there is an exception print to the console
        except Exception:
            System.log("Exception was raised")
            output_file.write(str(Exception) + '\n')
            return
        # write output
        line_num += 1
        output_file.write(output)

def check(output_file, correct_output_file, output_path: str, correct_output_path: str):
    """Print to the console the differences if exist in the output and the correct output"""
    System.log("Print differences")
    # read lines from the files
    output_file_txt = output_file.readlines()
    correct_output_file_txt = correct_output_file.readlines()
    # print differences
    for line in difflib.unified_diff(
            output_file_txt, correct_output_file_txt, fromfile=output_path,
            tofile=correct_output_path, lineterm=''):
        System.log(line)

def tester(input_path: str, output_path: str, correct_output_path: str, func_num: int):
    """perform tests on the required function"""
    # open files
    try:
        input_file = open(input_path, 'r')
    except FileNotFoundError:
        System.assertFalse(input_path is None, "input test file is not None")
        sys.exit(1)
    try:
        output_file = open(output_path, 'a+')
    except FileNotFoundError:
        System.assertFalse(output_path is None, "output test file is not None")
        sys.exit(1)
    try:
        correct_output_file = open(correct_output_path, 'r')
    except FileNotFoundError:
        System.assertFalse(correct_output_path is None, "input test file is not None")
        sys.exit(1)

    # instance of the module we want to test
    ling_proccessor = prc()

    # perform test
    if func_num == 1:
        System.log("perform {} tests from{}, writing output to {}".format("CaseFolding", input_path, output_path))
        func = runCaseFoldingTests
        performTest(input_file, output_file, ling_proccessor, func)
    elif func_num == 2:
        System.log(
            "perform {} tests from{}, writing output to {}".format("RemovePunctuation", input_path, output_path))
        func = runRemovePunctuationTests
        performTest(input_file, output_file, ling_proccessor, func)
    elif func_num == 3:
        System.log(
            "perform {} tests from{}, writing output to {}".format("RemoveStopWords", input_path, output_path))
        func = runRemoveStopWordsTests
        performTest(input_file, output_file, ling_proccessor, func)
    elif func_num == 4:
        System.log(
            "perform {} tests from{}, writing output to {}".format("PerformStemming", input_path, output_path))
        func = runPerformStemmingTests
        performTest(input_file, output_file, ling_proccessor, func)
    else:
        System.log(
            "perform {} tests from{}, writing output to {}".format("LinguisticProccessing", input_path, output_path))
        func = runLinguisticProccessingTests
        performTest(input_file, output_file, ling_proccessor, func)

    # check differences
    System.log("Check differences")
    output_file.seek(0)
    check(output_file, correct_output_file, output_path, correct_output_path)

    # close files
    System.log("Closing Files")
    input_file.close()
    output_file.close()
    correct_output_file.close()

# driver code
#tester("Testing/TestsInputs/LinguisticProccessorCaseFolding1.txt", "Testing/TestOutputs/LinguisticProccessorCaseFolding1Out.txt", "Testing/CorrectOutput/LinguisticProccessorCaseFolding1Correct.txt", 1)