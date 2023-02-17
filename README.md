# Python tool to extract and grade D2L submissions

## Installation

* `git clone` the repository
* `cd` into the repository, and install it with `pip install .`

This provides two scripts: `d2l_unpack` and `d2l_grade`.

## Unpacking

* Download the ZIP file containing all the submissions, and put it in a directory of your choice.
* Let's say the ZIP file is in the folder `../midterm_1`.
* Unpack all submissions with: `d2l_unpack ../midterm_1`.

### Templates folder

If a folder named `templates` exists in the same directory as the ZIP file, its contents will be copied into each submission folder.

## Grading

* You can run a command in each submission folder.
* Let's say you want to run `pytest` for each submission in `../midterm_1` (unpacked from before).
* Run: `d2l_grade ../midterm_1 pytest`.
* After each run of the `pytest` command, choose between:
  * `a`: run the command again
  * `d`: move the submission to the `done` folder
  * `q`: quit

Happy grading!