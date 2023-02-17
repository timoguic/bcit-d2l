import logging
import re
import shutil
from pathlib import Path

from .helpers import datetime_from_dict, unzip, D2L_FILE_REGEX

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def unzip_d2l_archives(base_folder: Path) -> None:
    """
    Unpacks all the zip archives in the specified folder.
    The zip files are most likely going to be D2L files.
    """
    for child in base_folder.iterdir():
        if child.suffix == ".zip":
            unzip(child)
            logger.info("Found and unpacked %s", child)


def find_student_files(base_folder: Path) -> dict:
    students_files_dict = dict()
    # keys: student IDs
    # values: dictionaries, with keys:
    #   name: the name of the student
    #   files: a list of tuples
    #     each tuple is (Path object for the file, filename)
    #   date: the submission date

    for child in base_folder.iterdir():
        if child.is_dir():
            continue

        matches = re.search(D2L_FILE_REGEX, child.name)
        if not matches:
            logger.debug("No match for %s", child)
            continue

        mdict = matches.groupdict()
        student_name = mdict["student_name"]
        student_id = mdict["student_id"]
        submission_date = datetime_from_dict(mdict)

        if student_id in students_files_dict:
            students_files_dict[student_id]["files"].append(
                (
                    child,
                    mdict["filename"],
                )
            )
        else:
            students_files_dict[student_id] = {
                "name": student_name,
                "files": [(child, mdict["filename"])],
                "date": submission_date,
            }

    return students_files_dict


def create_folders_and_move_files(base_folder: Path, mapping: dict):
    for student_id, my_dict in mapping.items():
        student_folder_path = base_folder / f"{my_dict['name']}_{student_id}"
        Path.mkdir(student_folder_path, exist_ok=True)

        mapping[student_id]["folder"] = student_folder_path.resolve()

        # Move files to the folder
        for orig_path, filename in my_dict["files"]:
            orig_path.replace(student_folder_path / filename)
            logger.debug("Moved %s to %s", orig_path, student_folder_path / filename)


def unzip_student_archives(mapping: dict):
    """
    Unzip student archives
    """
    for value in mapping.values():
        files = [file for file in value["folder"].iterdir() if file.is_file()]
        # If we only have one student file and that file is a zip, unpack it
        if len(files) == 1:
            if files[0].suffix == ".zip":
                unzip(files[0])
                # And remove the zip file too
                files[0].unlink()


def clean_folders(mapping: dict):
    """
    If a student submits a ZIP file, they may have a single folder containing all their files.
    This folder will be inside the student folder created before, so we clean them too.
    """
    folders = [elem["folder"] for elem in mapping.values()]
    to_remove = list()

    # Clean single folders inside a folder
    for folder in folders:
        subfolders = [fldr for fldr in folder.iterdir() if fldr.is_dir()]
        if len(subfolders) == 1:
            subfolder = subfolders[0]
            to_remove.append(subfolder)
            for subitem in subfolder.iterdir():
                subitem.rename(folder / subitem.name)

    for folder in to_remove:
        folder.rmdir()


def copy_templates(dest: Path, from_folder=None):
    if from_folder is None:
        from_folder = dest / "templates"
        if not from_folder.exists():
            from_folder = Path(".") / "templates"

    for item in dest.iterdir():
        if not item.is_dir() or item.name.lower().startswith("template"):
            continue

        for to_copy in from_folder.iterdir():
            shutil.copy(to_copy, item)


if __name__ == "__main__":
    p = Path(".")
    unpack(p)
