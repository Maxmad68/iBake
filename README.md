# iBake
iBake (<b>i</b>OS <b>BA</b>c<b>K</b>up Extractor) is an iOS backup extractor and utility.

# Installation
Just paste this in a terminal (sudo permissions required!)

    sudo curl https://raw.githubusercontent.com/Maxmad68/ibake/master/ibake.py > /usr/local/bin/ibake && sudo chmod +x /usr/local/bin/ibake


# Usage

Extract a backup:</br>
  ibake extract &lt;Backup-ID&gt; &lt;Extraction-Path&gt;<br>
  ibake extract &lt;Backup-ID&gt; &lt;Extraction-Path> -d &lt;domain&gt;<br>
  ibake extract &lt;Backup-ID&gt; &lt;Extraction-Path> -d &lt;domain&gt; -f &lt;file&gt;<br>
  ibake extract &lt;Backup-ID&gt; &lt;Extraction-Path> -h &lt;hash&gt;<br>
<br>
List all backups:<br>
  ibake list<br>
<br>
Print information about a backup:<br>
  ibake info &lt;Backup-ID&gt;<br>
<br>
Read backup:<br>
  ibake read &lt;Backup-ID&gt; domains<br>
  ibake read &lt;Backup-ID&gt; files<br>
  ibake read &lt;Backup-ID&gt; files -d <domain><br>
<br>
Upload file to backup:<br>
  ibake upload &lt;Backup-ID&gt; &lt;Local-file&gt; &lt;Domain-name&gt; &lt;Backup-path><br>
<br>
Generate file name hash:<br>
  ibake hash &lt;Domain-name&gt; &lt;Relative-path&gt;<br>
<br>

# Examples

Retrieve SMS database:

   ibake extract &lt;Backup-ID&gt; ~/sms.db -d HomeDomain -f Library/SMS/sms.db
   
Retrieve all camera roll:

   ibake extract &lt;Backup-ID&gt; Camera-roll -d CameraRollDomain
