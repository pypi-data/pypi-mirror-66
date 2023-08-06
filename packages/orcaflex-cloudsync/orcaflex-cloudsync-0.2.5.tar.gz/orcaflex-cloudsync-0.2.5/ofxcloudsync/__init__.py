import os

import yaml
from appdirs import AppDirs

dirs = AppDirs("ofx-cloudsync", "AgileTek")

SYNC_OFX = os.path.join(dirs.user_data_dir, "sync.ofx")


def load_sync_ofx():
    if os.path.exists(SYNC_OFX):
        with open(SYNC_OFX, "r") as ymlfile:
            return yaml.safe_load(ymlfile)
    else:
        return None


def write_sync_ofx(data):
    with open(SYNC_OFX, "w") as wf:
        yaml.dump(data, wf)


def update_progress(progress, prefix='', for_sysout=True):
    barLength = 10  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    if for_sysout:
        text = "\r{0} [{1}] {2:2.0f}% {3}".format(prefix, "=" * block + " " * (barLength - block), progress * 100,
                                                  status)
    else:
        text = "{0} [{1}] {2:2.0f}% {3}".format(prefix, "=" * block + " " * (barLength - block), progress * 100, status)

    return text
