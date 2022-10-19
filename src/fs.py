#!/usr/bin/env python3

from pathlib import Path
from typing import Optional, List
import typer


app = typer.Typer()

@app.command()
def add(origin: Path = typer.Argument(..., help="Origin file path"), destination: Path = typer.Argument(..., help="Destination file path")):
    """
    Add files to synchronize list
    """
    print(f"Add origin:{origin}, destination:{destination}")

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
    current_dir: bool = typer.Option(False, "--current-dir", "-C", help="Synchronize added files in current directory"),
    ):
    """
    Synchronize added files
    """
    if (all):
        print(f"Sync all added files")

    elif (current_dir and not path):
        print(f"Sync added files in current directory")

    elif (current_dir and path):
        print(f"Sync added files in current directory and files")
        for p in path:
            print(p)

    elif (path):
        print(f"Sync files")
        for p in path:
            print(p)
    else:
        typer.secho("No file input")

@app.command()
def list(
    path: Path = typer.Argument(
        Path("$HOME/.config/fs/list.json"),
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to synchronize list"),
    ):
    """
    Show all files to synchronize
    """
    print("List cli")
    #  for p in path:
        #  print(p)
    


if __name__ == "__main__":
    app()
