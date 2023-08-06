#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-04-20"
__version__ = "0.1.5"

__all__ = ('main', 'write_changelog',)

from pathlib import Path
from os import walk, getcwd
from json import load, dump
from datetime import datetime
from argparse import ArgumentParser
from collections import defaultdict
from typing import Union, List, DefaultDict, Any, Optional


def read(path: Union[Path, str]) -> DefaultDict[str, Any]:
    if not (path := Path(path)).exists():
        return defaultdict(None,
                           filename='changelog.md',
                           identifier=['# NEW', '# new'],
                           current_version=[0, 0, 0],
                           version_increment=[0, 0, 1],
                           files=['.py'],
                           includes=[],
                           excludes=[])
    with path.open('r') as file: return defaultdict(None, load(file))


def write(path: Union[Path, str],
          filename,
          identifier,
          current_version,
          version_increment,
          files,
          includes,
          excludes) -> None:
    with Path(path).open('w') as file: dump(dict(filename=filename or 'changelog.md',
                                                 identifier=identifier or '# NEW',
                                                 current_version=current_version or [0, 0, -1],
                                                 version_increment=version_increment or [0, 0, 1],
                                                 files=files or ['.py'],
                                                 includes=includes or [],
                                                 excludes=excludes or []),
                                            file,
                                            indent=2)


def find_and_replace_changes(path: Union[Path, str], identifier: str, suffixes: List[str], includes: List[str],
                             excludes: List[str]) -> List[str]:
    if not (path := Path(path)).is_dir(): raise NotADirectoryError(f"'{path}' either doesn't exist or is not a folder!")
    for root, _, files in walk(path):
        for file in filter(lambda f: f.suffix in suffixes and str(f) not in excludes, map(Path, files)):
            fpath = Path(root).resolve() / file
            with fpath.open('rt') as rfile:
                lines = rfile.readlines()
            with fpath.open('wt') as wfile:
                for line in lines:
                    if not line.strip("\n").lstrip().startswith(identifier):
                        wfile.write(line)
                    else:
                        txt = line.strip("\n").lstrip()
                        for i in identifier: txt = txt.replace(i, '').lstrip()
                        yield txt


def write_changelog(path: Union[Path, str] = None, settings: Optional[DefaultDict[str, Any]] = None) -> None:
    new_version = tuple(map(sum, zip(settings['current_version'],
                                     settings['version_increment']
                                     )))
    now = datetime.now()
    log = f'\n> **{".".join(map(str, new_version))}**  *{now.year}-{now.month}-{now.day}*'
    for entry in find_and_replace_changes(path,
                                          settings['identifier'],
                                          settings['files'],
                                          settings['includes'],
                                          settings['excludes']): log += f"""\n> - {entry}"""
    log += '\n'
    if (changelog := path / settings['filename']).exists():
        with changelog.open('rt') as rfile:
            lines = rfile.readlines()
        lines.insert(1, log)
        with changelog.open('w') as wfile:
            wfile.writelines(lines)
    else:
        with changelog.open('w') as wfile:
            wfile.write('### Changelog\n')
            wfile.write(log)
    settings.update(current_version=new_version)
    write(path / '.changelog_builder', **settings)


def main():
    parser = ArgumentParser(
        prog='changelog_builder',
        description='tool for building changelog files',
        usage='changelog_builder [path][filename][identifier][current-version]'
              '[version-increment][files][includes][excludes]',
        epilog=f'changelog_builder v{__version__} [{__date__}] by {__author__}'
    )

    parser.add_argument('path', type=str, nargs='?',
                        default=getcwd(), help='The path to the project.')

    parser.add_argument('-fn', '--filename', type=str,
                        default=None, help='The changelog filename.')

    parser.add_argument('-id', '--identifier', type=str, nargs='*',
                        default=None, help='The string which identifies a change.')

    parser.add_argument('-cv', '--current-version', dest='current_version', type=int, nargs=3,
                        default=None, help='The current version.')

    parser.add_argument('-vi', '--version-increment', dest='version_increment', type=int, nargs=3,
                        default=None, help='The version increment.')

    parser.add_argument('-fi', '--files', type=str, nargs='*',
                        default=None, help='The file suffixes to scan.')

    parser.add_argument('-in', '--includes', type=str, nargs='*',
                        default=None, help='Files to include.')

    parser.add_argument('-ex', '--excludes', type=str, nargs='*',
                        default=None, help='Files to exclude.')

    args = vars(parser.parse_args())
    path = Path(args.pop('path'))
    saved_settings = read(path / '.changelog_builder') or defaultdict(None)
    settings = defaultdict(None)
    for key, value, in args.items():
        settings[key] = value or saved_settings[key]
    settings['identifier'] = tuple(settings['identifier'])

    write_changelog(path, settings=settings)


if __name__ == '__main__': main()
