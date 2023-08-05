import subprocess
from os import path


class EgrepErrors(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return f"EGREP Exception Raised: {self.message}"
        else:
            return "EGREP Exception Raised"

class egrep:
    ERROR_INVALID_NUMBER_OF_ARGUMENTS = "Invalid number of arguments. Need at least two, eg:\nEGREP(\"regex\",\"file-path\")"
    ERROR_FILE_DOES_NOT_EXIST_AT = "File does not exist at: "

    EGREP = "egrep "

    MINIMUM_ARGUMENTS = 2

    def __init__(self, *args):
        try:
            if(self.validateArguments(*args)):
                self.command = self.EGREP + " ".join(args)
                
        except EgrepErrors as error:
            print(error)

    def execute(self):
        command = subprocess.Popen([self.command], stdout=subprocess.PIPE,shell=True)
        (command_output, error) = command.communicate()
        if error:
            raise EgrepErrors(error)
        else:
            for word in self.createOutputList(command_output):
                print(word)
    
    def createOutputList(self, command_output):
        return str(command_output)[1:].split("\\n")

    def validateArguments(self, *args):
        self.isValidLength(*args)
        self.isValidFilePath(args[-1])
        return True

    def isValidLength(self, *args):
        if len(args) < self.MINIMUM_ARGUMENTS:
            raise EgrepErrors(self.ERROR_INVALID_NUMBER_OF_ARGUMENTS)
    
    def isValidFilePath(self, filePath):
        if path.exists(filePath) == False:
            raise EgrepErrors(self.ERROR_FILE_DOES_NOT_EXIST_AT + filePath)

