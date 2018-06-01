# iBake
iBake (<b>i</b>OS <b>BA</b>c<b>K</b>up <b>E</b>xtractor) is an iOS backup extractor and utility.

# Installation
Just paste this in a terminal (sudo permissions required!)

    sudo wget https://raw.githubusercontent.com/Maxmad68/ibake/master/ibake.py -O /usr/local/bin/ibake && sudo chmod +x /usr/local/bin/ibake


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
    
<br>
Read backup:<br>

    ibake read <Backup-ID> domains
	ibake read <Backup-ID> files
	ibake read <Backup-ID> files -d <domain>
    
<br>
Upload file to backup:<br>

    ibake upload <Backup-ID> <Local-file> <Domain-name> <Backup-path>

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
