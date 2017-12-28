#!/usr/bin/env python
import argparse
import datetime
import os
from grp import getgrgid
from pwd import getpwuid

EPILOG = """
    The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
    Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).
    
    Using color to distinguish file types is disabled both by default and
    with --color=never.  With \n --color=auto, ls emits color codes only when
    standard output is connected to a terminal.  The LS_COLORS environment
    variable can change the settings.  Use the dircolors command to set it.
    
    Exit status:
     0  if OK,
     1  if minor problems (e.g., cannot access subdirectory),
     2  if serious trouble (e.g., cannot access command-line argument).
    
    GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
    Full documentation at: <http://www.gnu.org/software/coreutils/ls>
    or available locally via: info '(coreutils) ls invocation'
    """

parser = argparse.ArgumentParser(
    description="""
    List information about the FILEs (the current directory by default)
    Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
    """,
    usage='ls [OPTION]... [FILE]...',
    epilog=EPILOG)
parser.add_argument('-l', action='store_true', help='use a long listing format')
parser.add_argument('-a', action='store_true', help='do not ignore entries starting with .')
args = parser.parse_args()


def humanize_size(bytes):
    if bytes < 1024.0:
        return bytes
    bytes /= 1024.0

    for unit in ['K', 'M', 'G', 'T']:
        if bytes < 1024.0:
            return "{:3.1}{}".format(bytes, unit)
        bytes /= 1024.0


def long_format(name, stat):
    """
    represents line with long format
    """
    username = getpwuid(stat.st_uid).pw_name
    group = getgrgid(stat.st_gid).gr_name
    permissions = oct(stat.st_mode)[-3:]
    size = humanize_size(stat.st_size)
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%a %b %d %H:%M')
    return '{:<8}{:<15}{:<15}{} {}{:<15}'.format(permissions,
                                                 username,
                                                 group,
                                                 size,
                                                 mtime,
                                                 name)

def short_format(name, stat):
    """
    represents line with short format
    """
    return '{}'.format(name)


def main():
    for entry in os.scandir():
        if not args.a and entry.name.startswith('.'):
            continue

        if args.l:
            print(long_format(entry.name, entry.stat()))
        else:
            print(short_format(entry.name, entry.stat()), end=' ')


if __name__ == '__main__':
    main()
