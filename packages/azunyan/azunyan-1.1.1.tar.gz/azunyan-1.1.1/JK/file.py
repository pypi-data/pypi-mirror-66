import os



def find(path, itemType='all'):
    """
    List folders, files or both in a given path.
    
    Arguments:
        path (str)
    
    Keyword Arguments:
        itemType (str)
            '*': all [default]
            'd': dir
            'f': file
    
    Returns:
        list
    """
    result = []
    if itemType == '*':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            result.append(itemPath)
    elif itemType == 'd':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            if os.path.isdir(itemPath):
                result.append(itemPath)
    elif itemType == 'f':
        for itemName in os.listdir(path):
            itemPath = path + '/' + itemName
            if os.path.isfile(itemPath):
                result.append(itemPath)
    return result

def findall(path, fileExts=[]):
    """
    Get all files in a given path recursively.
    
    Arguments:
        path (str)
    
    Keyword Arguments:
        fileExts (list)
            e.g.:
                ['exe', 'jpg']
                ['ini']
            []: matches all files [default]
    
    Returns:
        list
    """
    result = []
    if fileExts == []:
        for root, _, files in os.walk(path):
            for i in files:
                result.append(root.replace('\\','/') + '/' + i)
    else:
        for root, _, files in os.walk(path):
            for i in files:
                if os.path.splitext(i.lower())[-1][1:] in fileExts:
                    result.append(root.replace('\\','/') + '/' + i)
    return result
