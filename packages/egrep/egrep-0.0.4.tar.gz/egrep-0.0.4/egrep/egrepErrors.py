class EgrepErrors(Exception):
    ERROR_INVALID_NUMBER_OF_ARGUMENTS = "Invalid number of arguments. Need at least two, eg:\nEGREP(\"regex\",\"file-path\")"
    ERROR_FILE_DOES_NOT_EXIST_AT = "File does not exist at: "
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