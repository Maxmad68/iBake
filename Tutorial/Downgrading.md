# How to downgrade a backup

## Why downgrade a backup?

<br>
Most of the time, you would like to downgrade a backup if you downgraded your iPhone.<br>
As you may know, a backup of a device running a higher version could not be restored on a device running a lower version.<br>
This mean you can't downgrade your iPhone with keeping your data as they were before without using a tool like iBake.<br>
<br>

![Error](https://github.com/Maxmad68/iBake/blob/master/Tutorial/Images/erroritunes.png)<br>

<br>

## The solution
<br>
iBake has a functionnality to downgrade a backup, I mean to make a backup able to be restored on a device running a lower version than the backed up one.<br>
First, you'll need to get the identifier of the backup you want to downgrade.

    ibake list
  
This command will give you the list of every backup stored locally for your user account.<br>
The backup identifier is a string of hexadecimal characters (numbers and letters from A to F) and dashes.<br>
Then, confirm that this identifier is really corresponding to the backup you want to downgrade with this command:

    ibake info <identifier>
  

After that, you need to know the "destination" iOS version (the one you want to make your backup restorable to, easy), and it's <u>build number</u>.<br>
To get the build number of an iOS version, you can use the website [ipsw.me](https://ipsw.me). After choosing your device, the site will give you all iOS versions available for your device, and their build numbers between parenthesis.<br>
Example: On this image, we can see Build Number for iOS 12.1.3 is 16D40<br>
![Error](https://github.com/Maxmad68/iBake/blob/master/Tutorial/Images/ipswme.png)<br>
<br>
Note: on the latest versions of iBake, iBake will verify the build number and iOS version are matching with the device type, so you couldn't do any mistake. However, you can override this verification by specifiing -f argument.
<br>
Then, use the command to downgrade the backup:

    ibake downgrade <identifier> <iOS Version> <Build Number>
  


Because after downgrading the backup, some files may not be restored to the device (see below), iBake will ask you to be sure you have a working copy of the backup before processing.<br>

<br>
An other solution, for example if you have downgraded all your iOS device from an IPSW file, you can use iBake to downgrade your backup using the IPSW file to get the destination version informations. By using that method, you would need to provide iBake the path of the IPSW file, but you won't have to search for build numbers and version number.

    ibake downgrade <Backup-ID> <IPSW File>


## Be careful!

Every iOS version store files another way. It means that by downgrading a backup, some files may not be restored correctly on the device.<br>
For this reason, I recommend downgrading a backup only to experimented people, and not on an "important" device (such as professional phone).<br>
Most of the times, errors happen when downgrading from a major version to a lower version (for example, downgrading from iOS 12 to iOS 11.4.1).<br>
Normally, downgrading a backup in the same "major" version than the original version (from iOS 12.1.3 to iOS 12.1.2) will not cause any trouble.

