import os
import sys

DEBUG = False

def muError(block, line, etype, syntax, tprint="the syntax is", internal=True):
    print("\nError at block["+block+"] at line["+str(line)+"]")
    print("\tType: "+etype)
    print("\tFor a "+block+" block, "+tprint+" '"+syntax+"'")
    if internal:
        print("\tThis error happened inside the program (err_internal)\n")
    else:
        print("\tThis error happened outside the program (err_external)\n")

    exit(1)

#try:
#    programName = argv[0]
#except:
#try:
#    targetName = argv[1]
#except:
#    print("Please enter a target")

try:
    file = open("MuFile", "r")
except:
    muError("Root", 0, "file_not_loadable_exception", "create a file named MuFile", "you need to")

#if os.name == "nt":
#    import win32com.shell.shell as shell
#    ASADMIN = 'asadmin'
#
#    if sys.argv[-1] != ASADMIN:
#        script = os.path.abspath(sys.argv[0])
#        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
#        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
#        sys.exit(0)

fileData = file.read()
splitByLine = fileData.split("\n")
lineNumber = 1

targetNames = []
targetCommands = {}
fullVariables = {}
currentTarget = ""

for line in splitByLine:
    if line == "":
        continue
    if list(line)[0] == "/" and list(line)[1] == "/":
        continue
    data = line.split(" ")
    if data[0] == "Define":
        try:
            data[1]
            data[2]
        except:
            muError("Define", lineNumber, "syntax_exception", "Define [VARNAME] VARDATA")
        if DEBUG:
            print("[parser] Define: "+data[1]+" with value: "+data[2])
        stringOfItems = ""
        lastItemOnList = len(data) - 1
        for item in data:
            if item == data[0]:
                continue
            if item == data[1]:
                continue
            else:
                stringOfItems += item + " "
        l = len(stringOfItems)
        stringOfItems = stringOfItems[:l-1]
        fullVariables[data[1]] = stringOfItems
    elif data[0] == "Target":
        try:
            data[1]
            data[2]
        except:
            muError("Target", lineNumber, "syntax_exception", "Target [PLATFORM] NAME")
        if DEBUG:
            print("[parser] Target: "+data[2]+" for platform: "+data[1])
        currentTarget = [data[2], data[1]]
        targetCommands[currentTarget[0]+currentTarget[1]] = []
        targetNames.append(currentTarget)
        #print(targetNames)
    elif data[0] == "End":
        if DEBUG:
            print("[parser] End: "+currentTarget[0]+" platform: "+currentTarget[1])
        currentTarget = ""
    else:
        if data[0] == "" and data[1] == "" and data[2] == "" and data[3] == "":
            pass
        else: 
            muError("Command", lineNumber, "syntax_exception", "insert 4 spaces (not a tab character) at the beginning of a command.", "please ensure you")

        newdata = data
        newdata.pop(0)
        newdata.pop(0)
        newdata.pop(0)
        newdata.pop(0)

        stringForExec = ""
        for item in newdata:
            stringForExec += item
            stringForExec += " "

        withVariablesList = list(stringForExec)
        while "&" in withVariablesList:
            if "&" in withVariablesList:
                location = withVariablesList.index("&")
                locationEnd = withVariablesList.index(" ", location, len(withVariablesList) - 1)
                charactersNeeded = withVariablesList[location+1:locationEnd]
                stringItem = ""
                for item in charactersNeeded:
                    stringItem += item
                try:
                    varData = fullVariables[stringItem]
                except:
                    muError("Variable", lineNumber, "name_exception", "use a valid variable name.", "please ensure you")
                #print(varData)
                varData = list(varData)
                withVariablesListCopy = withVariablesList
                del withVariablesListCopy[location:locationEnd]
                inputLoc = location
                for item in varData:
                    withVariablesListCopy.insert(inputLoc, item)
                    inputLoc += 1
                withVariablesList = withVariablesListCopy
                
        stringForExec = ""
        for char in withVariablesList:
            stringForExec += char

        targetCommands[currentTarget[0]+currentTarget[1]].append(stringForExec)


    lineNumber += 1

for target in targetNames:
    sitem = targetCommands[target[0]+target[1]]
    length = len(sitem)
    sitem = sitem[:length-1]

file.close()

try:
    target = sys.argv[1]
except:
    muError("argv", 0, "command_exception", "mubuild [TARGET]", "the correct command syntax is:", False)

if os.name == "nt":
    osname = "_nt"
else:
    osname = "_posix"

targetName = [target, osname]
targetNameConcat = target + osname
if not targetName in targetNames:
    muError("argv", 0, "no_target_exception", "does not exist", "the target you entered")

if DEBUG:
    print("Processing target: "+target)
    print("Operating System:  "+osname)
    print("Full Target Name:  "+targetNameConcat)
else:
    print("Building target "+target+" for OS "+osname+" ...")

#print("TargetCommands"+targetCommands[targetNameConcat])

for command in targetCommands[targetNameConcat]:
    #print(command)
    integerCode = os.system(command)
    if integerCode != 0:
        print("Build failed. Do you want to exit?")
        if input("(Y for Yes, N for No) > ").lower() == "n":
            pass
        else:
            exit(1)