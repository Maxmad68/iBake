# iBake
iBake (<b>i</b>OS <b>BA</b>c<b>K</b>up <b>E</b>xtractor) is a iPhone (iPad/iPod Touch) backup manipulating tool.

What iBake can do:
- Manipulate backups
- Extract files from Backup
- Recover data from uncomplete backup
- Downgrade backup to make it restorable on a lower version

What iBake can't do:
- Backup your iPhone
- Restore backup on your iPhone

Currently, iBake only works on macOS.
Windows support will be added... someday?

TODO:
- [ ] Support Windows
- [ ] Support encrypted backups
- [ ] Support iCloud Backups



# Installation
Just paste this in a terminal (sudo permissions required!)

    sudo curl -o /usr/local/bin/ibake https://raw.githubusercontent.com/Maxmad68/ibake/master/ibake.py && sudo chmod +x /usr/local/bin/ibake && echo && echo "Successfully installed iBake"


# Usage

Extract a backup:</br>

    ibake extract <Backup-ID> <Extraction-Path>
	ibake extract <Backup-ID> <Extraction-Path> -d <domain>
	ibake extract <Backup-ID> <Extraction-Path> -d <domain> -f <file>
	ibake extract <Backup-ID> <Extraction-Path> -h <hash>
   
<br>
List all backups:<br>

    ibake list
    ibake list <Directory>
    
<br>
Print information about a backup:<br>

    ibake info <Backup-ID>
    ibake info <Backup-ID> -a    (Show apps list)
    
<br>
Read backup:<br>

    ibake read <Backup-ID> domains
	ibake read <Backup-ID> files
	ibake read <Backup-ID> files -d <domain>
    
<br>
Upload file to backup:<br>

    ibake upload <Backup-ID> <Local-file> <Domain-name> <Backup-path>
    
<br>
Downgrade backup:<br>
This command allows you to make a backup compatible with a device on an older version. (For exemple, an iOS 16 backup could be restored on an iOS 15 device)
Note that some backuped items may not be compatible with the "destination" version. Please make sure to have a working copy of your backup before using this command.<br>The iOS-Version parameter and the iOS-Build-Number must correspond.

Please read [this page](../master/Tutorial/Downgrading.md)



    ibake downgrade <Backup-ID> <iOS-Version> <iOS-Build-Number> [-f]
    ibake downgrade <Backup-ID> <IPSW File> [-f]


Downgrade from iOS 16 to iOS 15: Tested

<br>
Generate file name hash:<br>

    ibake hash <Domain-name> <Relative-path>
    
<br>

Note that all Backup-ID may be a path.
# Examples

Retrieve SMS database:<br>

    ibake extract <Backup-ID> ~/sms.db -d HomeDomain -f Library/SMS/sms.db
     
Retrieve all camera roll:

    ibake extract <Backup-ID> Camera-roll -d CameraRollDomain
