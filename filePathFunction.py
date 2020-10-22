import os  # imports modules that allows one to run functions and perform actions that are otherwise dependent on OS functionality


def checkFilePath(fileName): # function allows the use of pcap or .txt file that is outside of the working directory when a function asks for users to input a file
    fileLocation = (input("Is " + str(fileName) + " located in the current working directory? (Y/N) ")).lower()
    if fileLocation == 'y':
        return fileName
    elif fileLocation == 'n':
        absFilePath = input("Please enter the absolute path (full file path) of the file you wish to use: ")
        if '.txt' in absFilePath:
            absFileName = os.path.realpath(absFilePath)
            return absFileName
        elif '.pcap' in absFilePath:
            absFileName = os.path.realpath(absFilePath)
            return absFileName
        else:
            absFileName = os.path.join(absFilePath, fileName)
            absFileName = os.path.realpath(absFileName)
            return absFileName
    else:
        print("Invalid Response")
        checkFilePath(fileName)