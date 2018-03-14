# iBake
iBake (<b>i</b>OS <b>BA</b>c<b>K</b>up Extractor) is an iOS backup extractor and utility.

# Installation
Just paste this in a terminal (sudo permissions required!)

    sudo curl https://raw.githubusercontent.com/Maxmad68/ibake/master/ibake.py > /usr/local/bin/ibake && sudo chmod +x /usr/local/bin/ibake


# Usage
<code>
Extract a backup:<br>
  ibake extract <Backup-ID> <Extraction-Path><br>
  ibake extract <Backup-ID> <Extraction-Path> -d <domain><br>
  ibake extract <Backup-ID> <Extraction-Path> -d <domain> -f <file><br>
  ibake extract <Backup-ID> <Extraction-Path> -h <hash><br>
<br>
List all backups:<br>
  ibake list<br>
<br>
Print information about a backup:<br>
  ibake info <Backup-ID><br>
<br>
Read backup:<br>
  ibake read <Backup-ID> domains<br>
  ibake read <Backup-ID> files<br>
  ibake read <Backup-ID> files -d <domain><br>
<br>
Upload file to backup:<br>
  ibake upload <Backup-ID> <Local-file> <Domain-name> <Backup-path><br>
<br>
Generate file name hash:<br>
  ibake hash <Domain-name> <Relative-path><br>
<br>
</code>
# Examples

Retrieve SMS database:

   ibake extract <Backup-ID> ~/sms.db -d HomeDomain -f Library/SMS/sms.db
   
Retrieve all camera roll:

   ibake extract <Backup-ID> Camera-roll -d CameraRollDomain
