#
# Author: James Lemieux (<jimmygtr11@gmail.com>)
#
# This program downloads Youtube mp3 files through search queries given in a text file.
#
# This program requires Python 2.7, the Selenium package, and phantomjs.
#

import urllib
from urlparse import urljoin
import os, sys, shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


new_list=[]
stars = "**************************"*3
dot_line = "--------------------------"*3

# your path to your text file containing the "song name-artist" searches. If you haven't created the file, run the program, and it will create it for you in the correct format
song_list_path = "C:\Users\JimmyGtr11\Desktop\song_list.txt"

# your path to phantomjs.exe
path_to_phantomjs_exe = "C:\Python27\phantomjs.exe"


# your path to the ghostdriver.log (may not be needed). If ghostdriver.log does not exist or you get a permissions error, put the creation path to the phantomjs folder like the below code
path_to_ghostdriver_log = "C:\Python27\Lib\site-packages\selenium\webdriver\phantomjs\ghostdriver.log"

# your path to your "Automatically add to media library" folder, if you have one
path_to_auto_add = "C:\Users\JimmyGtr11\Music\iTunes\iTunes Media\Music\Automatically Add to iTunes"


#!!! Important !!! See below to specify your desired destination path of the downloaded mp3 files !!! Important !!!#


# gets a list of youtube search queries from your file
def create_file():
	global mylist
	if os.path.exists(song_list_path):
		f = open(song_list_path, 'r')
		mylist = f.read().splitlines()

	else:
		f = open(song_list_path, 'w+')
		line1 = "(FORMAT: song name-artist) (EXAMPLE: piano man-billy joel) Don't delete this line or the dotted line. One song name-artist per line."
		line2 = "--------------------------------------------------------------------------------------------------------------------------------------"
		f.write(line1)
		f.write("\n")
		f.write(line2)
		f.write("\n")
		f.close()
		print "Created song_list.txt in ["+song_list_path+"].\nEdit it based on instructions given in song_list.txt."
		print stars+'\n'
		sys.exit()

def translate_non_alphanumerics(to_translate, translate_to=u''):
	global title_text
	not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
	translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
	title_str_text = to_translate.translate(translate_table)
	title_text = title_str_text
	
os.system('cls')# makes it prettier
print "\n"+stars
		
create_file()

# converts queries into Youtube format
for i in mylist[2:]:
	i=i.replace("\t", " ")
	i=i.replace(" ", "+")
	i=i.replace("-", "+")
	i=i+"+lyrics"
	if i == "+lyrics":
		print "ERROR: Make sure only one song name-artist per line. Edit your file."
		sys.exit()
	else:
		new_list.append(i)


# starts phantomjs
driver = webdriver.PhantomJS(executable_path= path_to_phantomjs_exe, service_log_path= path_to_ghostdriver_log)

print "PhantomJS has started!\n"
print dot_line

# search Youtube with the search queries from your list
for i in new_list:
	print "Searching Youtube for: ", i, "...\n"
	driver.get("https://www.youtube.com/results?filters=video&lclk=video&search_query="+i+"+lyrics")
	
	# find href link within Youtube html, then parse the video id
	links = driver.find_elements(By.CLASS_NAME, "yt-lockup-title")
	link = links[0]
	link = link.get_attribute('innerHTML')
	link = link.split(' ')[1]
	link = link.replace('href="/watch?v=', '')
	link = link.replace('"', '')
	
	print "Converting video to mp3...\n"
	# reload phantomjs to the converted Youtube link
	driver.get("http://www.youtube-mp3.org/?e=t_exp&r=true#v="+link)
	
	# wait for download link to appear
	element = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.LINK_TEXT, "Download")))
	
	# parse link and video title through youtube-mp3.org html
	link = element.get_attribute('href')
	title_element = driver.find_element_by_id("title")
	title_text = title_element.get_attribute('innerHTML')
	title_text = title_text.replace("<b>Title:</b>", "")
	translate_non_alphanumerics(title_text)
	#title_text = title_text.replace(" ", "")
	#title_text = title_text.replace("/", "")
	#title_text = title_text.replace("\\", "")
	
	# your desired destination path of the downloaded mp3 files
	mp3_download_path = "C:\Users\JimmyGtr11\Downloads\downloaded_music\\"+title_text+".mp3"
	
	download_directory = mp3_download_path.replace(title_text, '')
	download_directory = download_directory.replace('.mp3', '')
	
	print "Downloading "+title_text+".mp3...\n"
	# if link has already been downloaded, cancel download and try the next link
	if os.path.exists(mp3_download_path):
		print "Download FAILED: "+title_text+".mp3"+" already\nexists in "+download_directory+"\n"
		print dot_line
		continue
	# if link has not been downloaded, download link, then automatically add it to your media player's library
	else:
		urllib.urlretrieve(link, mp3_download_path)
		shutil.copy(mp3_download_path, path_to_auto_add)
		print "Download SUCCESS: "+title_text+".mp3"+" downloaded to\nfolder "+download_directory+"\n"
		print dot_line

print "\nPhantomJS has quit!"
print stars+"\n"		
		
driver.quit()#!!! Important !!! If phantomjs is not quit properly, it will continue to run invisibly !!!Important!!!#