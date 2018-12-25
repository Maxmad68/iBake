#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os,shutil
import sys
import plistlib
import re
import hashlib


argv = sys.argv

#  Copyright 2018 Maxime MADRAU

__author__ = 'Maxime Madrau (maxime@madrau.com)'
__version__ = '1.5'

def readBinaryPlist(path):
	plist = {}

	content = os.popen('defaults read \'{realpath}\''.format(realpath=os.path.realpath(path))).read()
	keys = re.findall(r'(?<=    ).+(?= = )',content)

	for k in keys:
		valRaw = re.findall(r'(?<={k} = ).+(?=;)'.format(k=k),content)[0]
		try:
			val = eval(valRaw)
		except:
			val = valRaw
		plist[k] = val
		
	return plist
		


def usage():
	print
	print 'iBake {version}, by Maxime Madrau'.format(version=__version__)
	print 'Usage:'
	print
	print 'Extract a backup:'
	print '	ibake extract <Backup-ID or Path> <Extraction-Path>'
	print '	ibake extract <Backup-ID or Path> <Extraction-Path> -d <domain>'
	print '	ibake extract <Backup-ID or Path> <Extraction-Path> -d <domain> -f <file>'
	print '	ibake extract <Backup-ID or Path> <Extraction-Path> -h <hash>'
	print
	print 'List all backups:'
	print '	ibake list'
	print '	ibake list <Directory>'
	print
	print 'Print information about a backup:'
	print '	ibake info <Backup-ID or Path> [-a]'
	print
	print 'Read backup:'
	print '	ibake read <Backup-ID or Path> domains'
	print '	ibake read <Backup-ID or Path> files'
	print '	ibake read <Backup-ID or Path> files -d <domain>'
	print
	print 'Upload file to backup:'
	print '	ibake upload <Backup-ID or Path> <Local-file> <Domain-name> <Backup-path>'
	print
	print 'Downgrade backup:'
	print '	ibake downgrade <Backup-ID or Path> <iOS Version> <iOS Build Number>'
	print
	print 'Generate file name hash:'
	print '	ibake hash <Domain-name> <Relative-path>'
	print
	print 'Execute shell in backups directory:'
	print '	ibake shell <Shell>'

	exit()

try:
	whattodo = argv[1]
except:
	usage()

if whattodo == 'extract':
	try:
		backupId = argv[2]
		reformDir = argv[3]
	except:
		usage()
		
	
		
	if os.path.isdir(reformDir):
		print 'Extraction Directory must not exist! (Will be created by iBake)'
		exit()
		
	user = os.environ['HOME']
	
	if os.path.isdir(backupId):
		path = backupId
	else:
		path = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
	dbPath = os.path.join(path,'Manifest.db')
	#print dbPath
	conn = sqlite3.connect(dbPath)
	c = conn.cursor()


	if len(argv) >= 5:
		if argv[4] == '-d':
			try:
				domain = argv[5]
			except:
				usage()
			else:
				allDir = c.execute('''SELECT * FROM Files WHERE flags IS 2 AND domain IS "%s"'''%domain).fetchall()
		
		elif argv[4] == '-h':
			try:
				hash_ = argv[5]
			except:
				usage()
			else:
				try:
					res = c.execute('''SELECT * FROM Files WHERE flags IS 1 AND fileID IS "%s"'''%(hash_)).fetchone()
					#print res
					id_,domain,file,flag,f = res
					subDir = id_[:2]
					print 'Extracting file...'
					shutil.copy(os.path.join(path,subDir,id_),reformDir)
					print 'Done!'
				except Exception as e:
					print 'Error!'
					print e
				exit()
		
		if len(argv) >= 7:
			if argv[4] == '-d' and argv[6] == '-f':
				try:
					file_ = argv[7]
				except:
					usage()
				else:
					try:
						res = c.execute('''SELECT * FROM Files WHERE flags IS 1 AND domain IS "%s" AND relativePath IS "%s"'''%(domain,file_)).fetchone()
						#print res
						id_,domain,file,flag,f = res
						subDir = id_[:2]
						print 'Extracting file...'
						shutil.copy(os.path.join(path,subDir,id_),reformDir)
						print 'Done!'
					except Exception as e:
						print 'Error!'
						print e
					exit()
	else:
		allDir = c.execute('''SELECT * FROM Files WHERE flags IS 2''').fetchall()
		
	print 'Building Subirectories'
	for id_,domain,file,flag,f in allDir:
		if not os.path.isdir(os.path.join(reformDir,domain)):
			os.makedirs(os.path.join(reformDir,domain))
		if not os.path.isdir(os.path.join(reformDir,domain,file)):
			os.makedirs(os.path.join(reformDir,domain,file))

	print 'Subdirectories built!'
	print
	
	if len(argv) >= 5:
		if argv[4] == '-d':
			try:
				domain = argv[5]
			except:
				usage()
			else:
				allFiles = c.execute('''SELECT * FROM Files WHERE flags IS 1 AND domain IS "%s"'''%domain).fetchall()
	else:
		allFiles = c.execute('''SELECT * FROM Files WHERE flags IS 1''').fetchall()

	total = float(len(allFiles))
	current = 0
	error = 0

	print 'Building Files'
	print
	for id_,domain,file,flag,f in allFiles:
		#print id,domain,flag
		current += 1
		sys.stdout.write("\033[F")
		sys.stdout.write("\033[K")
		print 'File %i on %i (%0.2f%%)'%(current,total,(current/total)*100)

		
		if flag == 1:
			splitedPath = os.path.split(file)
			
			subDir = id_[:2]
			try:
				shutil.copy(os.path.join(path,subDir,id_),os.path.join(reformDir,domain,file))
			except Exception as e:
				print 'Error:',e
				error += 1
				print
				print 
		
	print 'Files build!'
	print 'Backup extraction proceed (with %i error%s)'%(error,'s' if error>1 else '')
	
elif whattodo == 'list':
	user = os.environ['HOME']
	if len(sys.argv) >= 3:
		backupDir = sys.argv[2]
	else:
		backupDir = os.path.join(user,'Library/Application Support/MobileSync/Backup/')
	print 'All backups:'
	for backupId in os.listdir(backupDir):
		if backupId[0] != '.':
			
			if 'Snapshot' in os.listdir(os.path.join(backupDir,backupId)):
				print '%s: Backuping'%backupId
				continue 
			
			try:
				plist = plistlib.readPlist(os.path.join(backupDir,backupId,'Info.plist'))
				deviceName = plist['Device Name']
				osVersion = plist['Product Version']
				date = plist['Last Backup Date']
			except:
				
				print '%s: Unreadable backup'%backupId
			else:
				print '%s: %s - iOS %s , on %s'%(backupId,deviceName,osVersion,date)
	
elif whattodo == 'info':
	print
	try:
		backupId = argv[2]
	except:
		usage()
	user = os.environ['HOME']
	if os.path.isdir(backupId):
		backupDir = backupId
	else:
		backupDir = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
	
	backuping = os.path.isdir(os.path.join(backupDir,'Snapshot'))
	
	if not backuping:
		showApps = '-a' in argv
		plist = plistlib.readPlist(os.path.join(backupDir,'Info.plist'))
		if not showApps:
			print 'Backup ID: '+backupId
			print 'Last Backup Date: '+str(plist.get('Last Backup Date','Unknown'))
			print 'Device Name: '+plist.get('Device Name','Unknown')
			print 'Device Type: %s (%s)'%(plist.get('Product Name','Unknown'),plist.get('Product Type','Unknown'))
			print 'Serial Number: '+plist.get('Serial Number','Unknown')
			print 'GUID: '+plist.get('GUID','Unknown')
			print 'ICCID: '+plist.get('ICCID','Unknown')
			print 'IMEI: '+plist.get('IMEI','Unknown')
			print 'UUID: '+plist.get('Unique Identifier','Unknown')
			print 'Target Identifier: '+plist.get('Target Identifier','Unknown')
			print 'iOS Version: %s (%s)' %(plist.get('Product Version','Unknown'),plist.get('Build Version','Unknown'))
			print 'iTunes Version: '+plist.get('iTunes Version','Unknown')
		else:
			print 'Installed Applications: (%i)'%len(plist['Installed Applications'])
			print ''.join(map(lambda s: '\n   - '+s,plist['Installed Applications']))
	
	else:
		plistPath = os.path.join(backupDir,'Status.plist')
		plist = readBinaryPlist(plistPath)
		print 'Backup ID: '+backupId
		print 'UUID: '+plist['UUID']
		print 'Date: '+re.findall(r'.+(?= \+)',plist['Date'])[0]
		print 'Backup State: '+plist['BackupState']
		print 'Snapshot State: '+plist['SnapshotState']

elif whattodo == 'read':
	try:
		backupId = argv[2]
		readKey = argv[3]
	except:
		usage()
		
	user = os.environ['HOME']
	if os.path.isdir(backupId):
		path = backupId
	else:
		path = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
	dbPath = os.path.join(path,'Manifest.db')
	conn = sqlite3.connect(dbPath)
	c = conn.cursor()
	
	if readKey == 'domains':
		allDir = c.execute('''SELECT DISTINCT domain FROM Files''').fetchall()
		print '\n'.join(filter(lambda x:isinstance(x,basestring),map(lambda x:x[0],allDir)))
	if readKey == 'files':
		if len(argv) >= 5:
			if argv[4] == '-d':
				try:
					domain = argv[5]
				except:
					usage()
				else:
					allDir = c.execute('''SELECT fileID,relativePath,domain from Files WHERE domain IS "%s" AND flags IS 1'''%domain).fetchall()
		else:
			allDir = c.execute('''SELECT fileID,relativePath,domain from Files WHERE flags IS 1''').fetchall()		
		print ''.join(map(lambda s: '[%s]  %s : %s\n'%(s[2],s[0],s[1]),allDir))


elif whattodo == 'upload':
	try:
		backupId = argv[2]
		localFile = argv[3]
		domain = argv[4]
		file_ = argv[5]
	except:
		usage()		
	user = os.environ['HOME']
	if os.path.isdir(backupId):
		path = backupId
	else:
		path = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
	dbPath = os.path.join(path,'Manifest.db')
	conn = sqlite3.connect(dbPath)
	c = conn.cursor()
	
	domainExists = bool(c.execute('''SELECT count(*) FROM Files WHERE domain IS "%s"'''%domain).fetchone()[0])
	
	if not domainExists:
		print 'Domain "%s" doesn\' exist in that backup. Upload anyway? (y/n)'%domain
		uploadAnyway = raw_input()
		if uploadAnyway != 'y':
			exit()
			
	print 'Building parent directories hashes...'
	
	all = []
	for parentDir in os.path.split(file_)[0].split('/'):
		all.append(parentDir)
		parentDirPath = '/'.join(all)
		parentExists = bool(c.execute('''SELECT count(*) FROM Files WHERE relativePath IS "%s" AND flags IS 2'''%parentDirPath).fetchone()[0])
		if not parentExists:
			backupPath = '%s-%s'%(domain,parentDirPath)
			id_ = hashlib.sha1(backupPath).hexdigest()
			c.execute('''INSERT INTO Files (fileID,domain,relativePath,flags,file) VALUES ("%s","%s","%s",2,NULL)'''%(id_,domain,parentDirPath))
		
			
	print 'Hashing file id...'
	backupPath = '%s-%s'%(domain,file_)
	id_ = hashlib.sha1(backupPath).hexdigest()
	print 'File id is '+id_
	
	print 'Copying file...'
	subDir = id_[:2]
	shutil.copyfile(localFile, os.path.join(path,subDir,id_))
	
	print 'Updating database...'
	c.execute('''INSERT INTO Files (fileID,domain,relativePath,flags,file) VALUES ("%s","%s","%s",1,NULL)'''%(id_,domain,file_))
	conn.commit()
	print 'Done!'	
	
elif whattodo == 'downgrade':
	try:
		backupId = argv[2]
		iosVersion = argv[3]
		iosBuild = argv[3]
	except:
		usage()
		
	user = os.environ['HOME']
	if os.path.isdir(backupId):
		backupDir = backupId
	else:
		backupDir = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
		
	mustCopyBeforeOperating = raw_input('This backup will be modified. In case of error, all data it contains will be lost. Copy backup before operating? (y/n)')=='y'
		
	if mustCopyBeforeOperating:
		parent,name = os.path.split(backupDir)
		print 'Copying backup... (this may take a long time!)'
		shutil.copytree(backupDir, os.path.join(parent,name+'-BACKUP'))
		print 'Ending copying...'
		
		plistPath = os.path.join(backupDir,'Info.plist')
		plist = plistlib.readPlist(plistPath)
		plist['Display Name'] += ' - iBake Backup'
		plistlib.writePlist(plist, plistPath)
		
	print 'Downgrading backup...'
	
	manifestPlistPath = os.path.join(backupDir,'Manifest.plist')
	infoPlistPath = os.path.join(backupDir,'Info.plist')
	
	os.system('plutil -convert xml1 "{path}"'.format(path=os.path.realpath(manifestPlistPath)))
	manifestPlist = plistlib.readPlist(manifestPlistPath)
	manifestPlist['Lockdown']['ProductVersion'] = iosVersion
	manifestPlist['Lockdown']['BuildVersion'] = iosBuild
	plistlib.writePlist(manifestPlist, manifestPlistPath)
	os.system('plutil -convert binary1 "{path}"'.format(path=os.path.realpath(manifestPlistPath)))

	
	infoPlist = plistlib.readPlist(infoPlistPath)
	infoPlist['Product Version'] = iosVersion
	infoPlist['Build Version'] = iosBuild
	plistlib.writePlist(infoPlist, infoPlistPath)
	
	print 'Backup Downgraded to {version} ({build})'.format(version = iosVersion,build=iosBuild)
	
elif whattodo == 'hash':
	try:
		domain = argv[2]
		file_ = argv[3]
	except:
		usage()
		
	backupPath = '%s-%s'%(domain,file_)
	id_ = hashlib.sha1(backupPath).hexdigest()
	print id_
	
elif whattodo == 'shell':
	command = ' '.join(argv[2:])
	pwd = os.environ['PWD']
	os.chdir('Library/Application Support/MobileSync/Backup/')
	os.system(command)
	os.chdir(pwd)
		
else:
	usage()
	
	
	
