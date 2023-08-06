"""
    Name: utils.py
    Author: Charles Zhang <694556046@qq.com>
    Propose: A tool box contains many frequently used functions.
    Coding: UTF-8
"""

import os
import time
import shutil
import subprocess
from typing import Tuple, List


class Exec(object):
    """Exec

    A Exec class instance contains all exec result.

    Attributes:
        cmd: Exec command.
        stdout: Standard output.
        stderr: Standard error.
        exec_time: Execute time.
        returncode: Return code.
    """

    def __init__(self, cmd: str, stdout: str, stderr: str, exec_time: int, returncode: int):
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr
        self.exec_time = exec_time
        self.returncode = returncode


def exec(cmd: str, input_str: str = "") -> Exec:
    """Run a shell command

    Run a shell command with bash.

    Args:
        cmd: A command string.
        input_str: Input resources for stdin.

    Returns:
        exec_result: A Exec instance.
    """
    begin = time.time()
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               encoding="utf8")
    out, err = process.communicate(input_str)
    end = time.time()
    exec_time = int((end - begin) * 1000)
    return Exec(cmd, out, err, exec_time, process.returncode)


def bash(cmd: str) -> Tuple:
    """Run a shell command

    ### This function is obsolete and will be removed in future release! ###

    Run a shell command with bash.

    Args:
        cmd: A command string.

    Returns:
        status: 0 for success, 1 for fail
        output: running log from bash
        exec_time: command execute time
    """
    begin = time.time()
    status, output = subprocess.getstatusoutput(cmd)
    end = time.time()
    exec_time = int((end - begin) * 1000)

    return status, output, exec_time


def copyfile(src: str, dst: str):
    """Copy File"""
    shutil.copyfile(src, dst)


def copytree(src: str, dst: str):
    """Copy Tree"""
    shutil.copytree(src, dst)


def move(src: str, dst: str):
    """Move File"""
    shutil.move(src, dst)


def rmtree(src: str):
    """Remove Tree"""
    shutil.rmtree(src)


def rmfile(src: str):
    """Remove File"""
    os.remove(src)


def rename(old: str, new: str):
    """Rename File"""
    os.rename(old, new)


def readfile(src: str) -> str:
    """
    Read file and return string with \n.
    Auto remove blank line at the end of the file
    """
    cmd = ["cat", src]
    ret = bash(" ".join(cmd))
    return ret[1]


def writefile(src: str, lines: str, option: str = "w"):
    """
    Write string to file
    """
    with open(src, option, encoding='utf-8') as f:
        f.write(lines)


def readfile_list(src: str) -> List:
    """
    Read file and return list.
    Auto remove blank line at the end of the file
    """
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].rstrip('\n')

        while "" == lines[-1]:
            lines.pop()

        return lines


def writefile_list(src: str, lines: List, option: str = "w"):
    """
    Write string list to file
    """
    with open(src, option, encoding='utf-8') as f:
        f.writelines(lines)


def str2list(src: str) -> List:
    """Separate a string to a list by \n and ignore blank line at the end automatically."""
    ret = src.split("\n")
    while ret[-1] == "\n" or ret[-1] == "":
        ret.pop()
    return ret


def compare_str(str1: str, str2: str) -> bool:
    """Compare two string and ignore \n at the end of two strings."""
    return str1.rstrip() == str2.rstrip()


def compare_list(list1: List, list2: List) -> bool:
    """Compare two list and ignore \n at the end of two list."""
    while list1[-1] == "\n" or list1[-1] == "":
        list1.pop()
    while list2[-1] == "\n" or list2[-1] == "":
        list2.pop()
    return list1 == list2


def edit_distance(obj1, obj2) -> int:
    """Calculates the edit distance between obj1 and obj2"""
    edit = [[i + j for j in range(len(obj2) + 1)] for i in range(len(obj1) + 1)]

    for i in range(1, len(obj1) + 1):
        for j in range(1, len(obj2) + 1):
            if obj1[i - 1] == obj2[j - 1]:
                d = 0
            else:
                d = 1
            edit[i][j] = min(edit[i - 1][j] + 1, edit[i][j - 1] + 1, edit[i - 1][j - 1] + d)

    return edit[len(obj1)][len(obj2)]
