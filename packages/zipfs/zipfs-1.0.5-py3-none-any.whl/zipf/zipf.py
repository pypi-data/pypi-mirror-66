import sys
import os
import subprocess
import shutil
from subprocess import call
from datetime import datetime

CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'
CBWHITE = '\033[1;37m'
CBBLUE = '\033[1;34m'
CBASE = '\033[0m'


def _help_requested(args):
    if len(args) == 1 and (args[0] == "-h" or args[0] == "--help"):
        readme_path = "/usr/lib/zipf/README.md"

        f = open(readme_path, 'r')
        print(CBBLUE + "\n\t#######      zipf documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', ''). \
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', ''). \
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


def _get_abs_path(f_path):
    return os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(f_path))))


def _error_man(init_msg, err_msg, folder_path, moved_folder_path):
    _error(init_msg + " error:\n\t\t" + str(err_msg))

    sudo_conf = input(CBWHITE + "\n\t\tuse sudo?\n\t\t\t[Enter] to proceed\t\t[any case] to skip\n")
    if sudo_conf == "":
        subprocess.check_call(['sudo', "mv", folder_path, moved_folder_path])
    else:
        _skipped()


def _check_f_moved(folder_path, moved_folder_path):
    if os.path.exists(folder_path) or not os.path.exists(moved_folder_path):
        if os.path.exists(folder_path):
            _warning(CBBLUE + "%s" % folder_path + CBASE + " still exists")
        if not os.path.exists(moved_folder_path):
            _warning(CBBLUE + "%s" % moved_folder_path + CBASE + " doesn't exist")
        return False
    return True


def _check_archive_created(archive_name):
    archive_path = os.getcwd() + "/" + archive_name + ".zip"
    if os.path.isfile(archive_path):
        _ok(CBBLUE + "%s" % archive_path + CBASE + " created")
        return True
    else:
        _error(CBBLUE + "%s" % archive_path + CBASE + " not created")
        return False


def _zip_folder(folder_path, archive_name=None):
    if not archive_name:
        cdatetime = datetime.now()
        archive_name = cdatetime.strftime("%Y_%m_%d-%H_%M_%S")

    shutil.make_archive(archive_name, 'zip', folder_path)
    _check_archive_created(archive_name)
    # shutil.rmtree(folder_path)


def _zip_files(flist, archive_name=None):
    cdatetime = datetime.now()
    ctime = cdatetime.strftime("%Y_%m_%d-%H_%M_%S")

    if not archive_name:
        archive_name = ctime

    cpath = os.getcwd()
    folder_path = cpath + "/" + archive_name

    if _path_exists(folder_path):
        _warning(CBBLUE + "%s" % folder_path + CBASE + " already exists" + CBASE)
        moved_folder_path = folder_path + "_" + ctime
        try:
            shutil.move(folder_path, moved_folder_path)

        except PermissionError as err_msg:
            _error_man("permission", err_msg, folder_path, moved_folder_path)

        except OSError as err_msg:
            _error_man("os", err_msg, folder_path, moved_folder_path)

        except Exception as err_msg:
            _error_man("", err_msg, folder_path, moved_folder_path)

        if _check_f_moved(folder_path, moved_folder_path):
            _ok(CBBLUE + "%s" % folder_path + CBASE + " moved" + CBASE)
        else:
            _error("an issue occurred when moving file " + CBBLUE + "%s" % folder_path + CBASE)
            raise ValueError("not able to rename " + CBBLUE + "%s" % folder_path + CBASE)

    try:
        os.mkdir(folder_path)
    except Exception as err_msg:
        _error("an issue occurred when creating folder " + CBBLUE + "%s" % folder_path + CBASE + "\n%s" % err_msg)
        raise ValueError("not able to create " + CBBLUE + "%s" % folder_path + CBASE + " folder")

    for f in flist:
        f_path = _get_abs_path(f)

        if os.path.isdir(f_path):
            call(['cp', '-a', f_path, folder_path])
        elif os.path.isfile(f_path):
            shutil.copy(f_path, folder_path)

    shutil.make_archive(archive_name, 'zip', folder_path)
    _check_archive_created(archive_name)
    shutil.rmtree(folder_path)


def main():
    inputs = sys.argv[1:]
    _help_requested(inputs)

    if len(inputs) == 0:
        _error("needs at least one argument being a folder name or a list of files/folders")
        raise ValueError("no input ... no zip ...")

    elif len(inputs) == 1:
        f_path = _get_abs_path(inputs[0])
        print(f_path)
        if _path_exists(f_path):
            if os.path.isdir(f_path):
                _zip_folder(f_path)
            else:
                _zip_files([f_path])
        else:
            _error(CBBLUE + "%s" % f_path + CBASE + " path doesn't exist")
            raise ValueError(
                "needs at least one existing path in argument being a folder name or a list of files/folders")

    elif len(inputs) == 2 and not _path_exists(_get_abs_path(inputs[1])) and os.path.isdir(_get_abs_path(inputs[0])):
        folder_path = _get_abs_path(inputs[0])
        archive_name = inputs[1]
        _zip_folder(folder_path, archive_name)

    else:
        last_arg = inputs[-1]
        if _path_exists(_get_abs_path(last_arg)):
            _zip_files(inputs)
        else:
            _zip_files(inputs[:-1], last_arg)


if __name__ == "__main__":
    main()
