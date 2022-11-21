#!/usr/bin/env python3
"""
TODO:
    1. refactor sync
        1) detect and sync files or directories
        2) remove -D flag

    2. add list functionality
        1) all by default
        2) --current-dir, -C
        3) paths
    2. add update func
    3. fix sync func 
        1) add exception
    4. fix list func


"""

from pathlib import Path
from typing import Optional, List, Callable
import typer

from fs_core import FileSync
# from json_handler import JsonHandler


app = typer.Typer(help="File Sync allaw you to synchronize files in different directories")


@app.command()
def add(
        origin: Path = typer.Argument(...,
                                      help="Origin file path"),
        destination: Optional[List[Path]] = typer.Argument(...,
                                                           help="Destination file path")):
    """
    Add files to synchronize list
    """
    print(f"Add origin:{origin}, destination:{destination}")
    fs = FileSync()
    fs.add(origin, destination)


@app.command()
def sync(
    path_list: Optional[List[Path]] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to origin",
    ),
    all: bool = typer.Option(False,
                             "--all",
                             "-A",
                             help="Synchronize all added files"
                             )):
    """
    Synchronize added files
    """
    fs = FileSync()
    if all:
        print("Sync all added files")
        fs.sync_all()

    elif path_list:
        print("Sync added files in path")
        parsePathes(path_list, fs, FileSync.sync)

    else:
        typer.secho("No file input")


@app.command()
def update(
    path_list: Optional[List[Path]] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to origin",
    ),
    all: bool = typer.Option(False,
                             "--all",
                             "-A",
                             help="Update all added files"
                             )):
    """
    Update statuses of added files
    """
    fs = FileSync()
    if all:
        print("Update statuses all added files")
        fs.update_all_hashes()

    elif path_list:
        print("Update statuses added files in path")
        parsePathes(path_list, fs, FileSync.set_copies_hashes)
    else:
        typer.secho("No file input")


@app.command()
def list(
    path_list: Optional[List[Path]] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to synchronize list"),
    all: bool = typer.Option(False,
                             "--all",
                             "-A",
                             help="Show list of all add files")):
    """
    Show files in synchronize list
    """
    fs = FileSync()
    if all:
        print("Show all added files")
        for origin in fs.get_origins():
            print()
            print(origin)
            for copy in fs.get_copies(origin):
                state: str = '-'
                if not fs.compare_hashes(origin, copy):
                    # changed
                    state = 'c'

                print(f"-{state}- {copy}")

    elif path_list:
        print("Show added files")
        # print(f"working dir: {path}")
        origins = fs.get_origins()
        for p in path_list:
            if p.is_dir():
                for f in p.iterdir():
                    if f in origins:
                        print("success")
                        for copy in fs.get_copies(f):
                            print(copy)
                    else:
                        # print("not in origins", p, f)
                        print("bad")
                        pass

            else:
                if p in origins:
                    for copy in fs.get_copies(p):
                        print(copy)


def parsePathes(path_list: List[Path], fs: FileSync, func: Callable) -> None:
    for p in path_list:
        if p.is_dir():
            origins: List[Path] = fs.get_origins()
            for f in p.iterdir():
                if f in origins:
                    fs.func(f)
        else:
            fs.func(p)


if __name__ == "__main__":
    app()
