import datetime
import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

D2L_FILE_REGEX = r"(?P<student_id>A\d{8})_(?P<student_name>[ -_\w]+)_(?P<month>\w{3}) (?P<day>\d+), (?P<year>\d+) (?P<hour>\d{1,2})(?P<minute>\d{2})( ?P<am_pm>AM|PM)?_(?P<filename>.*)$"

def unzip(filename: Path):
    logger.debug("UNZIP: %s", filename)
    with zipfile.ZipFile(filename, "r") as zfp:
        zfp.extractall(filename.parent)


def datetime_from_dict(mdict):
    return datetime.datetime.strptime(
        f"{mdict['day']} {mdict['month']} {mdict['year']} {mdict['hour']}:{mdict['minute']}",
        "%d %b %Y %H:%M",
    )
