# iBake
iBake (<b>i</b>OS <b>BA</b>c<b>K</b>up Extractor) is an iOS backup extractor and utility.

# Installation
Just paste this in a terminal (sudo permissions required!)

    sudo curl https://raw.githubusercontent.com/Maxmad68/ibake/master/ibake.py > /usr/local/bin/ibake && sudo chmod +x /usr/local/bin/ibake


# Usage
<code>
Extract a backup:
  ibake extract <Backup-ID> <Extraction-Path>
  ibake extract <Backup-ID> <Extraction-Path> -d <domain>
  ibake extract <Backup-ID> <Extraction-Path> -d <domain> -f <file>
  ibake extract <Backup-ID> <Extraction-Path> -h <hash>

List all backups:
  ibake list

Print information about a backup:
  ibake info <Backup-ID>

Read backup:
  ibake read <Backup-ID> domains
  ibake read <Backup-ID> files
  ibake read <Backup-ID> files -d <domain>

Upload file to backup:
  ibake upload <Backup-ID> <Local-file> <Domain-name> <Backup-path>

Generate file name hash:
  ibake hash <Domain-name> <Relative-path>

</code>
# Examples

Retrieve SMS database:

   ibake extract <Backup-ID> ~/sms.db -d HomeDomain -f Library/SMS/sms.db
   
Retrieve all camera roll:

   ibake extract <Backup-ID> Camera-roll -d CameraRollDomain
