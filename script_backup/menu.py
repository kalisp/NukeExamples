import nuke
import script_backup

nuke.menu('Nuke').addCommand("utilities/auto_backup/open backup dir", "script_backup.open_backup_dir()")
nuke.addOnScriptSave(script_backup.do_backup)
