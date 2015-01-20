Steps:

###dternyak change

1) Run the "python-2.7.6.msi" installer with "C:\Python27" as the install destination.

2) Open Control Panel> System and Maintenance> System> Advanced System Setting and 
add ";C:\Python27;C:\Python27\Scripts;C:\Python27\Lib\site-packages" to the path.

3) Move "get-pip.py" from "winYoutubeMp3" to "C:\Python27\Lib\site-packages".

4) In cmd, run "python get-pip.py".

3) Install selenium via pip. (pip install selenium)

4) Create folder named "downloaded_music" inside Downloads folder.


5) Edit 4 paths in "win_youtube_mp3.py":
	
	>song_list_path = "path\to\Desktop\winYoutubeMp3\song_list.txt"
	
	>path_to_phantomjs_exe = "path\to\Desktop\winYoutubeMp3\phantomjs-1.9.8-windows\phantomjs.exe"
	
	>path_to_auto_add = "path\to\Music\iTunes\iTunes Media\Music\Automatically Add to iTunes"
	
	>mp3_download_path = "path\to\Downloads\downloaded_music\\"+title_text+".mp3"
 

6) Edit path in "YoutubeMp3.bat".
	
	>"& {python path\to\Desktop\winYoutubeMp3\win_youtube_mp3.py}"


7) After running "YoutubeMp3.bat" once, if desired, create shortcuts of "YoutubeMp3.bat" and "song_list.txt" and put them on the desktop.

	>Rename the "YoutubeMp3.bat" and "song_list.txt" shortcuts to desired names.
