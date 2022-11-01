#!/usr/bin/env python3
"""
TODO:
    1. add list functionality
        1) all by default
        2) --current-dir, -C 
        3) paths
"""

from pathlib import Path
from typing import Optional, List
import typer

from file_sync import FileSync
from json_handler import JsonHandler


app = typer.Typer()

@app.command()
def add(
        origin: Path = typer.Argument(..., help="Origin file path"),
        destination: Optional[List[Path]] = typer.Argument(..., help="Destination file path")
    ):
    """
    Add files to synchronize list
    """
    print(f"Add origin:{origin}, destination:{destination}")
    fs = FileSync()
    fs.add(origin, destination)

@app.command()
def sync(
    path: Optional[List[Path]] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
    all: bool = typer.Option(False, "--all", "-A", help="Synchronize all added files"),
    ):
    """
    Synchronize added files
    """
    fs = FileSync()
    if all:
        print("Sync all added files")
        fs.sync_all()

    elif path:
        print(f"Sync added files in path")
        for p in path:
            if p.is_dir():
                for f in p.iterdir():
                    print(f"sync in dir {p}: {f}")
                    sync(f)
            else:
                print(f"sync: {p}")
                sync(p)

    else:
        typer.secho("No file input")

@app.command()
def list(
    path: Optional[List[Path]] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to synchronize list"),
    all: bool = typer.Option(False, "--all", "-A", help="Show list of all add files"),
    ):
    """
    Show all files to synchronize
    """
    fs = FileSync()
    if all:
        print("Show all added files")
        for origin in fs.get_origins():
            print(origin)
            for copy in fs.get_copies(origin):
                print(f"--- {copy}")

    elif path:
        print("Show added files")
        origins = fs.get_origins()
        for p in path:
            if p.is_dir():
                for f in p.iterdir():
                    if f in origins:
                        print("success")
                        for copy in fs.get_copies(f):
                            print(copy)
                    else:
                        print("bad")
                        pass

            else:
                if p in origins:
                    for copy in fs.get_copies(p):
                        print(copy)


if __name__ == "__main__":
    app()
