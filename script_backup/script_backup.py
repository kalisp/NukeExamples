import nuke
import os
import time
import sys
import subprocess

BACKUP_DIR = "{}/nuke_backups".format(os.path.expanduser("~"))
KEEP_VERSIONS = 5

def open_backup_dir():
    """
        Opens backup dir in OS dependent viewer (explorer, Finder, etc.)
    Returns: None

    """
    print("Open_backup_dir")
    if sys.platform == "darwin":
        subprocess.check_call(["open", BACKUP_DIR])
    if sys.platform == "linux2":
        subprocess.check_call(["gnome-open", BACKUP_DIR])
    if sys.platform == "windows":
        subprocess.check_call(["explorer", BACKUP_DIR])


def get_script_name():
    """
    Gets currently edited script
    Returns: file name without extension

    """
    full_path = nuke.root().name()
    script_name = os.path.splitext(os.path.basename(full_path))[0] # get name without extension

    return script_name


def do_backup():
    """
    Saves script into BACKUP_DIR folder after each save.
    If more then KEEP_VERSIONS files are present, deletes them
    Returns: None

    """
    if not os.path.isdir(BACKUP_DIR):
        try:
            os.mkdir(BACKUP_DIR)
        except:
            nuke.message("Cannot create backup folder {}".format(BACKUP_DIR))

    current_time_str = time.strftime("%Y%m%d_%H%M")

    backup_file_url = "{}/bckp_{}_{}.nknc".format(BACKUP_DIR, get_script_name(), current_time_str)

    try:
        import shutil
        nuke.removeOnScriptSave(do_backup) #remove call on save to limit recursion
        nuke.scriptSave(backup_file_url)
        nuke.addOnScriptSave(do_backup)

        delete_old_version()
    except IOError as e:
        nuke.message("Cannot write file {}, {}".format(backup_file_url,e))


def delete_old_version():
    """
    Keep only KEEP_VERSIONS count of backups
    Returns:

    """
    bckp_files = []
    for file_name in os.listdir(BACKUP_DIR): # files are sorted by date ASC
        if file_name.startswith("bckp"):
            bckp_files.append(file_name)

    for file_name in bckp_files[:-KEEP_VERSIONS]: # keep KEEP_VERSIONS files from end
        try:
            os.remove(BACKUP_DIR + "/" + file_name)
        except:
            nuke.message("Cannot delete file {}".format(BACKUP_DIR + "/" + file_name))

