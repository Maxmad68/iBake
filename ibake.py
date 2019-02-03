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
__version__ = '1.6'

def read_binary_plist(path):
	'''
	Parse a binary plist file
		path (String) : Path of the bin plist to parse
		
	TODO: Use Google lib (https://github.com/google/binplist)
	'''
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
	
def makeHash(domain,path):
	'''
	Make a hash string from the domain name and the relative path of a file
		domain (String) : Domain name
		path (String) : Relative path
	'''
	backupPath = '%s-%s'%(domain,path)
	hash_ = hashlib.sha1(backupPath).hexdigest()
	return hash_
	
def isBackup(backupPath):
	'''
	Check if the specified path can be a backup
		backupPath (String) : The path
	
	Returns :
		Bool : True if the backup can be a backup, False otherwise
	''' 
	if os.path.isdir(backupPath):
		content = os.listdir(backupPath)
		return ('Info.plist' in content and 'Manifest.db' in content) or ('Status.plist' in content and 'Snapshot' in content)
	return False
	
def extract(backupDir,outputDir):
	dbPath = os.path.join(path,'Manifest.db')
	conn = sqlite3.connect(dbPath)  # Connect to Manifest.db
	c = conn.cursor()


	if len(argv) >= 5: # If a parameter like -d or -h is specified
		if argv[4] == '-d': # If -d parameter is specified: extract domain only
			try:
				domain = argv[5] # Domain to extract 
			except:
				usage()
			else:
				allDir = c.execute('''SELECT * FROM Files WHERE flags IS 2 AND domain IS "%s"'''%domain).fetchall() # Get directories to extract (specified domain only)
		
		elif argv[4] == '-h': # If -h parameter is specified: Copy file with hash
			try:
				hash_ = argv[5] #Hash file to extract
			except:
				usage()
			else:
				try:
					res = c.execute('''SELECT * FROM Files WHERE flags IS 1 AND fileID IS "%s"'''%(hash_)).fetchone() # Get id, domain name, file name, flag, content (maybe) of file with hash
					id_,domain,file,flag,f = res # same
					subDir = id_[:2] # Get two first letters of the has to know the directory the file is in
					print 'Extracting file...'
					shutil.copy(os.path.join(path,subDir,id_),outputDir) # Copy the file
					print 'Done!'
				except Exception as e: 
					print 'Error!'
					print e
				exit()
		
		if len(argv) >= 7: # If parameters -d and -f are specified (just that case for the moment)
			if argv[4] == '-d' and argv[6] == '-f': # Extract one file with name and domain
				try:
					file_ = argv[7] # File name
				except:
					usage()
				else:
					try:
						res = c.execute('''SELECT * FROM Files WHERE flags IS 1 AND domain IS "%s" AND relativePath IS "%s"'''%(domain,file_)).fetchone() # Get file properties
						id_,domain,file,flag,f = res
						subDir = id_[:2] # Get two first letters of the has to know the directory the file is in
						print 'Extracting file...'
						shutil.copy(os.path.join(path,subDir,id_),outputDir) # Copy the file
						print 'Done!'
					except Exception as e:
						print 'Error!'
						print e
					exit()
	else:
		# All backup extraction
		allDir = c.execute('''SELECT * FROM Files WHERE flags IS 2''').fetchall() # Retrieve all sub-directories infos
		
	print 'Building Sub-directories'
	
	for id_,domain,file,flag,f in allDir:
		# Mkdirs to create sub-sirectories
		if not os.path.isdir(os.path.join(outputDir,domain)):
			os.makedirs(os.path.join(outputDir,domain))
		if not os.path.isdir(os.path.join(outputDir,domain,file)):
			os.makedirs(os.path.join(outputDir,domain,file))

	print 'Subdirectories built!'
	print
	
	# Retrieve every file infos
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

	total = float(len(allFiles)) #Files number
	current = 0 # Set to 0 (for counter)
	error = 0 # Set to 0 (to count errors)

	print 'Building Files'
	print
	
	for id_,domain,file,flag,f in allFiles:
		current += 1 # For counter
		sys.stdout.write("\033[F") # Erase last line
		sys.stdout.write("\033[K") # same
		print 'File %i on %i (%0.2f%%)'%(current,total,(current/total)*100) # Counter

		
		if flag == 1:
			splitedPath = os.path.split(file)
			
			subDir = id_[:2]
			try:
				shutil.copy(os.path.join(path,subDir,id_),os.path.join(outputDir,domain,file)) # Copy file
			except Exception as e:
				print 'Error:',e
				error += 1
				print
				print 
		
	print 'Files build!'
	print 'Backup extraction proceed (with %i error%s)'%(error,'s' if error>1 else '')
	
def listBackups(oath):
	for backupId in os.listdir(path): 
		if isBackup(os.path.join(path, backupId)):
			if backupId[0] != '.':
					
				if 'Snapshot' in os.listdir(os.path.join(path,backupId)):
					print '%s: Backuping'%backupId
					continue 
					
				try:
					plist = plistlib.readPlist(os.path.join(path,backupId,'Info.plist'))
					deviceName = plist['Device Name']
					osVersion = plist['Product Version']
					date = plist['Last Backup Date']
				except:
						
					print '%s: Unreadable backup'%backupId
				else:
					print '%s: %s - iOS %s , on %s'%(backupId,deviceName,osVersion,date)
		

def backupInfo(backupDir):
	backuping = os.path.isdir(os.path.join(backupDir,'Snapshot')) # Is this backup in progress?
	if not backuping: # Show normal informations
		showApps = '-a' in argv # Is -a (show apps) parameter specified?
		plist = plistlib.readPlist(os.path.join(backupDir,'Info.plist')) # Main backup information property list
		if not showApps: # If mustn't show apps infos
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
		else: # If must show apps infos
			print 'Installed Applications: (%i)'%len(plist['Installed Applications'])
			print ''.join(map(lambda s: '\n   - '+s,plist['Installed Applications']))
	
	else: # If backup is in progress: Show every information we can
		try:
			plistPath = os.path.join(backupDir,'Status.plist') # Backup information file while backuping (bin plist)
			plist = read_binary_plist(plistPath) # Parse bin plist
			print 'Backup ID: '+backupId
			print 'UUID: '+plist['UUID']
			print 'Date: '+re.findall(r'.+(?= \+)',plist['Date'])[0]
			print 'Backup State: '+plist['BackupState']
			print 'Snapshot State: '+plist['SnapshotState']
		except: # Error probably on the read_binary_plist
			print 'Backup ID: '+backupId
			print 'Backuping, can\'t get any information.'
			
def readBackup(path):
	dbPath = os.path.join(path,'Manifest.db')
	conn = sqlite3.connect(dbPath) # Connect to Manifest.db
	c = conn.cursor()
	
	if readKey == 'domains': # List all domains in backup
		allDir = c.execute('''SELECT DISTINCT domain FROM Files''').fetchall()
		print '\n'.join(filter(lambda x:isinstance(x,basestring),map(lambda x:x[0],allDir)))
		
	if readKey == 'files': # List all files in backup (maybe in specified domain)
		if len(argv) >= 5: # If an additionnal parameter is specified
			if argv[4] == '-d': # If domain name is specified
				try:
					domain = argv[5]
				except:
					usage()
				else:
					files = c.execute('''SELECT fileID,relativePath,domain from Files WHERE domain IS "%s" AND flags IS 1'''%domain).fetchall() # List files just in specified domain
		else:
			files = c.execute('''SELECT fileID,relativePath,domain from Files WHERE flags IS 1''').fetchall() # List files in all backup
		print ''.join(map(lambda s: '[%s]  %s : %s\n'%(s[2],s[0],s[1]),files))


def uploadFileToBackup(backupId,localFile,domain,relativePath):
	dbPath = os.path.join(path,'Manifest.db') 
	conn = sqlite3.connect(dbPath) # Connect to Manifest.db
	c = conn.cursor()

	domainExists = bool(c.execute('''SELECT count(*) FROM Files WHERE domain IS "%s"'''%domain).fetchone()[0]) # Check if specified domain exists

	if not domainExists: # If domain doesn't exist, ask if we need to upload anyway
		print 'Domain "%s" doesn\' exist in that backup. Upload anyway? (y/n)'%domain
		uploadAnyway = raw_input()
		if uploadAnyway != 'y':
			exit()
			
	print 'Building parent directories hashes...'

	all = []
	for parentDir in os.path.split(relativePath)[0].split('/'): # Get every "levels" of the relative path (level1/level2/level3/file)
		all.append(parentDir)
		parentDirPath = '/'.join(all)
		parentExists = bool(c.execute('''SELECT count(*) FROM Files WHERE relativePath IS "%s" AND flags IS 2'''%parentDirPath).fetchone()[0])
		if not parentExists: # If this level doesn't already exists, create it in the database
			id_ = makeHash(domain, parentDirPath)
			c.execute('''INSERT INTO Files (fileID,domain,relativePath,flags,file) VALUES ("%s","%s","%s",2,NULL)'''%(id_,domain,parentDirPath))
		
			
	print 'Hashing file id...'
	id_ = makeHash(domain,relativePath)
	print 'File id is '+id_

	print 'Copying file...'
	subDir = id_[:2] # Get directory name
	shutil.copyfile(localFile, os.path.join(path,subDir,id_)) # Copy file to backup

	print 'Updating database...'
	c.execute('''INSERT INTO Files (fileID,domain,relativePath,flags,file) VALUES ("%s","%s","%s",1,NULL)'''%(id_,domain,relativePath)) # Add the file in the database
	conn.commit() # Save every changes in the database
	print 'Done!'	

def usage():
	'''
	Show man
	'''
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
	whattodo = argv[1] # Main command to execute (list, extract, ...)
except:
	usage()

if whattodo == 'extract': # Extract backup content
	try:
		backupId = argv[2]
		outputDir = argv[3]
	except:
		usage()
		
	
		
	if os.path.isdir(outputDir): # Output path specified already exists:
		print 'Extraction Directory must not exist! (Will be created by iBake)'
		exit()
		
	user = os.environ['HOME']
	
	if os.path.isdir(backupId): # If backup-id arg is a backup path
		path = backupId
	else:
		path = os.path.join(user,'Library/Application Support/MobileSync/Backup/',backupId)
	
	extract(path, outputDir)
	
	
elif whattodo == 'list': # List all backups
	user = os.environ['HOME']
	
	if len(sys.argv) >= 3: # If backup-id arg is a backup path
		path = sys.argv[2]
	else:
		path = os.path.join(user,'Library/Application Support/MobileSync/Backup/')
	print 'All backups:'
	
	listBackups(path)
	
elif whattodo == 'info': # Get infos of backup
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
	
	backupInfo(backupDir)

elif whattodo == 'read': # Read files/domains in a backup
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
	
	readBackup(path)


elif whattodo == 'upload': # Upload a file to a backup
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
	
	uploadFileToBackup(backupId,localFile,domain,file_)
	
elif whattodo == 'downgrade': # Make a backup in a version able to be restored on a device with a previous version
	try:
		backupId = argv[2]
		iosVersion = argv[3]
		iosBuild = argv[4]
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
	
elif whattodo == 'hash': # Make a hash
	try:
		domain = argv[2]
		file_ = argv[3]
	except:
		usage()
		
	id_ = makeHash(domain, file_)
	print id_
	
elif whattodo == 'shell': # Just execute a shell in a backup dir
	command = ' '.join(argv[2:]) # Reform the command from the sys.argv
	pwd = os.environ['PWD'] # Get current working directory
	os.chdir('Library/Application Support/MobileSync/Backup/') # CD to the backup dir 
	os.system(command) # Execute command (os.system because we want the standard stdout, stdin, and stderr)
	os.chdir(pwd) # CD to the working directory caught before
		
else:
	usage()
	
	
	
