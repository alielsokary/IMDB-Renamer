#! /usr/bin/env python3

# *** A script to get list of episodes names from IMDB and rename the episodes files in a given Directory. ***

import bs4, requests, os, shutil, re, sys, ctypes, glob
	
class Series:
	def __init__(self, name, seasonNumber, episodes):
		self.name = name
		self.seasonNumber = seasonNumber
		self.episodes = episodes

episodesNames = []
workingDirectory = ''
userConfirmed = False
mediaExtensions = (".mkv", ".mp4", ".avi")
subtitlesExtensions = (".srt", "sub")
series = Series("","",[])

def startScript():
	print('Enter IMDB Series Url:')
	url = input()
	print('Downloading data from IMDB...\n')
	returnedSoupObject = downloadSeriesDataFrom(url)

	episodes = extractEpisodesNamesFrom(returnedSoupObject)
	seriesName = extractSeriesNameFrom(returnedSoupObject)
	seasonNumber = extractSeasonNumberFrom(returnedSoupObject)

	global series
	series = Series(seriesName, seasonNumber, episodes)

	print('Series:',series.name)
	print('Season:',series.seasonNumber)

	print('These are the episodes names:\n')
	for episode in series.episodes:
		print(episode)

	print('\n')
	print('Press Y to Continue')
	confirmation = input()

	if(confirmation == 'Y' or confirmation == 'y'):
		getCurrentWorkingDirectory()
		getNewWorkingDirectory()
		renameFiles('n')

		print('Do you want to continue? Type Y to continue or N to abort')
		rename = input()
		shouldProceedToRenaming(rename, mediaExtensions)

		if shouldRenameSubtitiles():
			renameFiles('n', subtitlesExtensions)
			print('Do you want to continue? Type Y to continue or N to abort')
			rename = input()
			shouldProceedToRenaming(rename, subtitlesExtensions)

	elif(confirmation == 'N' or confirmation == 'n'):
		print('Script Terminated')
		quit()

	else:
		print('Please type Y or N')

def downloadSeriesDataFrom(seriesUrl):
	res = requests.get(seriesUrl)
	# -- Check for a successful 200.
	res.raise_for_status()
	soupObject = bs4.BeautifulSoup(res.text, 'html.parser')
	return soupObject

def extractSeriesNameFrom(soupObject):
	seriesName = soupObject.find(itemprop="name")
	seriesName = seriesName.a.get_text()
	return seriesName

def extractSeasonNumberFrom(soupObject):
	seasonsList = soupObject.find_all(class_="seasonAndYearNav")
	for item in seasonsList:
		seasonNumber = item.find(selected="selected").get("value")
	return seasonNumber

def extractEpisodesNamesFrom(soupObject):
	# -- Get list of episodes within calss "info".
	episodes = soupObject.find_all(class_="info")
	for episode in episodes:
		episodeName = (episode.a.get_text())
		episodesNames.append(episodeName)
	return episodesNames

def getCurrentWorkingDirectory():
	wd = os.getcwd()
	print('Current working directory is:', wd)

def getNewWorkingDirectory():
	print('Enter directory path')
	folderPath = input()
	folderPath = folderPath.replace("\\", "").strip()
	os.chdir(os.path.abspath(folderPath))
	wd = os.getcwd()
	print('Current working directory is:', wd)
	global workingDirectory
	workingDirectory = wd

def shouldRenameSubtitiles():
	if (directoryHasSubtitles):
		print('Subtitles found. Do you want to rename subtitles?')
		renameSubtitiles = input()
		if(renameSubtitiles == 'Y' or renameSubtitiles == 'y'):
			return True
		else: 
			return False

	else:
		return False

def directoryHasSubtitles():
	if filename.endswith(subtitlesExtensions) and not is_hidden(filename):
		return True

def shouldProceedToRenaming(command, extension):
	if(command == 'Y' or command == 'y'):
		renameFiles(command, extension)

	elif(command == 'N' or command == 'n'):
		print('Script Terminated.')
		quit()

	else:
		print('Please type Y or N')

def renameFiles(rename, extension = mediaExtensions):
	counter = 0
	folderPath = workingDirectory
	dirlist = sorted_aphanumeric(os.listdir(folderPath))
	for filename in dirlist:
		if filename.endswith(extension) and not is_hidden(filename):
			fileExtension = os.path.splitext(filename)[1]
			if(rename == 'N' or rename == 'n'):
				print('File will be renamed from:',os.path.join(folderPath,filename),'to -> ', series.name + ' - ' + 'S' + str(series.seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + series.episodes[counter])
			# -- Rename files.
			if(rename == 'Y' or rename == 'y'): 
				# -- Rename to SeriesName - S00SeosonE00Episode - Episode Name. 
				shutil.move(os.path.join(folderPath,filename), str(series.name + ' - ' + 'S' + str(series.seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + series.episodes[counter] + fileExtension))
				print('File renamed from:',os.path.join(folderPath,filename),'to -> ', series.name + ' - ' + 'S' + str(series.seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + series.episodes[counter])
			counter += 1

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)		

def is_hidden(filepath):
	name = os.path.basename(os.path.abspath(filepath))
	return name.startswith('.') or has_hidden_attribute(filepath)

def has_hidden_attribute(filepath):
	try:
		attrs = ctypes.windll.kernel32.GetFileAttributesW(unicode(filepath))
		assert attrs != -1
		result = bool(attrs & 2)
	except (AttributeError, AssertionError):
		result = False
	return result


startScript()
