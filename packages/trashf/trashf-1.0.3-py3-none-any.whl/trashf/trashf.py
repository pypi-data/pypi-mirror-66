import sys
import os
import subprocess
import ntpath
import shutil
from os import stat
from pwd import getpwuid
from datetime import datetime

__author__ = 'Yann Orieult'

CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'

CBWHITE = '\033[1;37m'
# CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'

CBASE = '\033[0m'

TRASH_PATH = os.environ['HOME'] + "/.local/share/Trash/files/"


def _help_requested(args):
    if len(args) == 1 and (args[0] == "-h" or args[0] == "--help"):
        readme_path = "/usr/lib/trashf/README.md"

        f = open(readme_path, 'r')
        print(CBBLUE + "\n\t#######      trashf documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', '').\
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', '').\
                replace('***', '').replace('***', '').replace('**', '').replace('*', '')

            print(" " + line, end='')
        print(CBASE)
        exit()


def _ok(msg=""):
    print(CBGREEN + "\n\t[OK] " + CBASE + msg)


# def _info(msg=""):
#     print(CBWHITE + "\n\t[INFO] " + CBASE + msg)


def _warning(msg=""):
    print(CBORANGE + "\n\t[WARNING] " + CBASE + msg)


def _error(msg=""):
    print(CBRED + "\n\t[ERROR] " + CBASE + msg)


def _skipped():
    print(CBBLUE + "\n\t\t\tskipped\n\n" + CBASE)


def _path_exists(path):
    if not os.path.exists(path):
        return False
    return True


def _get_abs_paths(fs):
    abs_f_paths = list()
    for f in fs:
        abs_f_paths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(f)))))
    return abs_f_paths


def _get_f_name(f_path):
    head, tail = ntpath.split(f_path)
    return tail or ntpath.basename(head)


def _error_man(init_msg, err_msg, f_path, f_path_in_trash):
    _error(init_msg + " error:\n\t\t" + str(err_msg))

    sudo_conf = input(CBWHITE + "\n\t\tuse sudo?\n\t\t[Enter] to proceed\t\t[any case] to skip\n")
    if sudo_conf == "":
        subprocess.check_call(['sudo', "mv", f_path, f_path_in_trash])
    else:
        _skipped()
        return False
    return True


def _trashf(f_path):
    f_name = _get_f_name(f_path)
    f_path_in_trash = TRASH_PATH + f_name

    if _path_exists(f_path_in_trash):
        _warning(CBBLUE + "%s " % f_name + CBASE + "already exists in trash")

        cdatetime = datetime.now()
        ctime = cdatetime.strftime("_%Y_%m_%d-%H_%M_%S")
        f_path_in_trash = f_path_in_trash + ctime
        print("\t\trenaming " + CBBLUE + " %s " % f_name + CBASE + "to " +
              CBBLUE + "%s " % (f_name + ctime) + CBASE + "before moving to trash")

    moved = True

    try:
        shutil.move(f_path, f_path_in_trash)

    except PermissionError as err_msg:
        moved = _error_man("permission", err_msg, f_path, f_path_in_trash)

    except OSError as err_msg:
        moved = _error_man("os", err_msg, f_path, f_path_in_trash)

    except Exception as err_msg:
        moved = _error_man("", err_msg, f_path, f_path_in_trash)

    if moved:
        if _check_f_moved_to_trash(f_path, f_path_in_trash):
            _ok(CBBLUE + "%s" % f_path + CBASE + " moved to trash" + CBASE)
        else:
            print("an issue occurred when moving file " + CBBLUE + "%s" % f_path + CBASE +
                  " to trash\n\tplease check the integrity of this file")


def _check_f_moved_to_trash(f_path, f_path_in_trash):
    if os.path.exists(f_path) or not os.path.exists(f_path_in_trash):
        if os.path.exists(f_path):
            _warning(CBBLUE + "%s" % f_path + CBASE + " still exists")
        if not os.path.exists(f_path_in_trash):
            _warning(CBBLUE + "%s" % f_path_in_trash + CBASE + " not in trash")
        return False
    return True


def _get_f_owner(f_path):
    return getpwuid(stat(f_path).st_uid).pw_name


def main():
    input_f_paths = sys.argv[1:]
    _help_requested(input_f_paths)
    f_paths = _get_abs_paths(input_f_paths)

    for f_path in f_paths:

        if not _path_exists(f_path):
            _warning(CBBLUE + " %s " % f_path + CBASE + "doesn't exists")
            _skipped()
            continue

        _trashf(f_path)


if __name__ == "__main__":
    main()
