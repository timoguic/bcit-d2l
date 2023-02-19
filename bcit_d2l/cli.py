from pathlib import Path
import subprocess
import sys
import shutil
import click

from .unpack import (
    clean_folders,
    copy_templates,
    create_folders_and_move_files,
    find_student_files,
    unzip_d2l_archives,
    unzip_student_archives,
)


@click.command()
@click.argument("folder")
def unpack(folder: str) -> None:
    base_folder = Path(folder)

    unzip_d2l_archives(base_folder)
    mapping = find_student_files(base_folder)
    create_folders_and_move_files(base_folder, mapping)
    unzip_student_archives(mapping)
    clean_folders(mapping)
    copy_templates(base_folder)

@click.command()
@click.argument("folder")
@click.argument("command")
def grade(folder: str, command: str) -> None:
   
    for node in Path(folder).iterdir():
        if not node.is_dir():
            continue
        if node.name.startswith("."):
            continue
        if node.name.startswith("template") or node.name.startswith("done"):    
            continue

        again = True
        while again:
            proc = subprocess.run(command, cwd=node.resolve(), shell=True)
            print()
            print("=" * 5, node.name, "=" *  5)
            print()
            action = input("Run [a]gain, mark as [d]one, or [q]uit: ").lower()
            if action.lower() == "q":
                sys.exit(0)
            if action == "d":
                done = node.parent / "done"
                Path.mkdir(done, exist_ok=True)
                shutil.move(node, done)
            if action != "a":
                again = False

if __name__ == "__main__":
    grade("../../submissions/2515_mt/pokemon", "pytest")