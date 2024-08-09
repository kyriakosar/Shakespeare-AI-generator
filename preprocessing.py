import os
import re
import string

def getLinesFromFile(filename):
    file = os.path.dirname(__file__) + f'/data/{filename}'
    file_handler = open(file, 'r')
    lines = file_handler.readlines()
    file_handler.close()
    return lines

def deleteLines(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.strip())
    for i in range(len(new_lines)-1,-1,-1):
        if '[' in new_lines[i] or ']' in new_lines[i]:
            del new_lines[i]
            continue
        if '{' in new_lines[i] or '}' in new_lines[i]:
            del new_lines[i]
            continue
        if 'title' in new_lines[i] or 'author' in new_lines[i] or 'lines' in new_lines[i] or 'linecount' in new_lines[i]:
            del new_lines[i]
            continue
    return new_lines

def deleteSymbols(lines):
    new_lines = []
    for tmp in lines:
        if '"' in tmp:
            tmp = tmp.replace('"','')
        if ',' in tmp:
            tmp = tmp.replace(',','')
        if '?' in tmp:
            tmp = tmp.replace('?','')
        if ';' in tmp:
            tmp = tmp.replace(';','')
        if '!' in tmp:
            tmp = tmp.replace('!','')
        if '.' in tmp:
            tmp = tmp.replace('.','')
        if ':' in tmp:
            tmp = tmp.replace(':','')
        new_lines.append(tmp)
    return new_lines

def fixLines(lines):
    new_lines = []
    for line in lines:
        if line == '':
            continue
        line = line.strip()
        new_lines.append(line + '.\n')
    return new_lines

def writeFile(target):
    file = os.path.dirname(__file__) + f'/data/{target}'
    file_handler = open(file, 'w')    
    file_handler.writelines(lines)
    file_handler.close()

if __name__ == '__main__':
    file = 'shakespeare_lib.txt'
    target = 'shakespeare.txt'
    lines = getLinesFromFile(file)
    lines = deleteLines(lines)
    lines = deleteSymbols(lines)
    lines = fixLines(lines)
    writeFile(target)