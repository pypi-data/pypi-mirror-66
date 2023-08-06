## Project Description

Simple utility to execute linux egrep command. The intention is to extend the capability of the egrep command from linux to python.

### Repo

If you wish to add aditional features to the command take a look at: https://github.com/rhimmelbauer/egrep

### Runtime

It has only been tested with Python3.6 onwards. This package will only work in linux OS that have the egrep command.

### Example

You must at least pass 2 variables when constructing an egrep instance. 1. Should be the regex expression and the second should be the filepath as a string. If you wish to add command options you can add them as initial parameter. Make sure the the second to last is the regex expression and the last is the filepath.

```
# No option
egrepInstance = egrep("'\d+'","directory.txt")
egrepInstance.execute()
print(egrepInstance.expressionsFound)

# Must match whole expression.
egrepInstance = egrep("-w","'\d+'","directory.txt")
egrepInstance.execute()
print(egrepInstance.expressionsFound)
```

### Methods & Properties:

At least 2 arguments:
1. The regex expresion as a String with single quotes eg: "'[agxc].A'".
2. The filepath as a string eg: "testfile.txt"
3. Any egrep command. Make sure the are at the beiging eg: "-w","regex","filepath"
```

def __init__(*args)
```

The constructor will validate if the file existis. If it does not it will through a egrepError.

To execute the egrep use the execute method were it will store the result in the property expressionsFound, which is a list.

