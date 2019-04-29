#! /usr/bin/env python3

# *** A script to get list of episodes names from IMDB and rename the episodes files in a given Directory. ***

import bs4, requests, os, shutil, re, sys, ctypes, glob
	
episodesNames = []
workingDirectory = ''
userConfirmed = False
seasonNumber = 0
extensions = (".mkv", ".mp4", ".avi")
# extensions = (".srt")

class Series:
	def __init__(self, name, number, episodes):
		self.name = name
		self.number = number
		self.episodes = episodes

def startScript():
	print('Enter IMDB Series Url:')
	url = input()
	print('Downloading data from IMDB...\n')
	returnedSoupObject = downloadSeriesDataFrom(url)

	episodes = extractEpisodesNamesFrom(returnedSoupObject)

	seriesName = extractSeriesNameFrom(returnedSoupObject)

	sNumber = extractSeasonNumberFrom(returnedSoupObject)


	series = Series(seriesName, sNumber, episodes)

	print('Series:',series.name)
	print('Season:',series.number)

	print('These are the episodes names:\n')
	for episode in series.episodes:
		print(episode)

	print('\n')
	print('Press Y to Continue.')
	confirmation = input()

	if(confirmation == 'Y' or confirmation == 'y'):
		newWorkingDirectory()
		renameFiles('n')
		print('Do you want to continue? Type Y to continue or N to abort')
		rename = input()

		if(rename == 'Y' or rename == 'y'):
			renameFiles(rename)

		elif(rename == 'N' or rename == 'n'):
			print('Script Terminated.')
			quit()

		else:
			print('Please type Y or N.')


	elif(confirmation == 'N' or confirmation == 'n'):
		print('Script Terminated')
		quit()

	else:
		print('Please type Y or N.')


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
		sNumber = item.find(selected="selected").get("value")
	return sNumber

def extractEpisodesNamesFrom(soupObject):
	# -- Get list of episodes within calss "info".
	episodes = soupObject.find_all(class_="info")
	for episode in episodes:
		episodeName = (episode.a.get_text())
		episodesNames.append(episodeName)
	return episodesNames


# -- Check if the file is not hidden.
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

# -- Change working directory.
def newWorkingDirectory():
	wd = os.getcwd()
	print('Current working directory is:', wd)
	print('Enter directory path.')
	folderPath = input()
	folderPath = folderPath.replace("\\", "").strip()
	os.chdir(os.path.abspath(folderPath))
	wd = os.getcwd()
	print('Current working directory is:', wd)
	global workingDirectory
	workingDirectory = wd

# -- Sort files in directory.
def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)		

def renameFiles(rename):
	# -- Get filenames in the current directory.
	counter = 0
	folderPath = workingDirectory
	dirlist = sorted_aphanumeric(os.listdir(folderPath))
	for filename in dirlist:
		if filename.endswith(extensions) and not is_hidden(filename):
			fileExtension = os.path.splitext(filename)[1]
			global seasonNumber
			if(rename == 'N' or rename == 'n'):
				print('File will be renamed from:',os.path.join(folderPath,filename),'to -> ',str(seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + episodesNames[counter])
			# -- Rename files.
			if(rename == 'Y' or rename == 'y'): 
				# -- Rename to 00Seoson00Episode - Episode Name. 
				shutil.move(os.path.join(folderPath,filename),str(seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + episodesNames[counter] + fileExtension)
				print('File renamed from:',os.path.join(folderPath,filename),'to -> ',str(seasonNumber).zfill(2) + 'E' + str(counter + 1).zfill(2) + ' - ' + episodesNames[counter])
			counter += 1


startScript()
