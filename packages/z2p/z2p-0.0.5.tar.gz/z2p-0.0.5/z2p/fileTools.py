import os


def listDirectoryFiles(filepath,postfix=None):
    '''
    递归列出目录下的所有文件内容，并以列表的形式返回
    
    Args:
        filepath：
            type：str
            所有列出的目录路径

        postfix：
            type：str or None
            后缀，如.php，那么返回的列表中只会有php后缀的文件。如果该项为none，则返回所有文件

    Returns: 
        []
    '''
    files = []
    for parent,dirnames,filenames in os.walk(filepath,followlinks=True):
        for filename in filenames:
            if postfix == None:
                files.append(os.path.join(parent,filename))
            else:
                if filename.endswith(postfix):
                    files.append(os.path.join(parent,filename))
    
    return files


if __name__ == '__main__':

    print(listDirectoryFiles('/Users/z2p/work','.csv'))