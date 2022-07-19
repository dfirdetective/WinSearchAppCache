# WinSearchAppCache

While working through an interview process, I came across the old "Microsoft.Windows.Cortana" artifacts and wondered what they would look like on my personal computer that had never configured or given permissions to Cortana. I found AppCache#.txt and within it, I found some data that wasn't available in other artifacts or that was different from other artifacts. As a result, I wrote a simple script to parse out the JSON data to a CSV with slightly cleaner headers for easier sorting. 

Here is where I'll put my notes and script so far. This is *ongoing research* and a work in progress. 

## Basic Info AppCache#.txt

> C:\Users\%USERNAME%\AppData\Local\Packages\Microsoft.Windows.Search_cw5n1h2txyewy\LocalState\DeviceSearchCache\AppCache[##################].txt 

The numbers at the end of the filename are the Windows filetime stamp of the iteration of AppCache. It appears that it may write every hour. 
The file is in JSON format and not locked - so easily copied out while running.   
As far as the contents, it's pretty straight forward. Only note I have is, it appears that the "Type:" is 5 if the "Value:" is an integer and 12 if it is a string. 

## Actual Data and Hypotheses

![Sample Screenshot](https://user-images.githubusercontent.com/88520889/179432469-de404371-80a4-4490-9b13-86d59ab8d54b.png)

|Headers|Sample|Hypothesis|
|---|---|---|
|System.FileExtension|{'Value': '.exe', 'Type': 12}|The file extension for the indexed file.|
|System.Software.ProductVersion|{'Value': '1.0.4.0', 'Type': 12}|If available, the product version for the application.|
|System.Kind|{'Value': 'program', 'Type': 12}|Program, document, link, and unknown are the options.|	
|System.ParsingName|{'Value': 'Chrome', 'Type': 12}|Anything from app name, to full path, to an AutoGenerated GUID|
|System.Software.TimesUsed|{'Value': 221, 'Type': 5}|Does not match other artifacts like prefetch run count|
|System.Tile.Background|{'Value': 4280291898, 'Type': 5}|Unsure, may be whether the app also runs in the background?|
|System.AppUserModel.PackageFullName|{'Value': 'Microsoft.BingWeather_4.53.41681.0_x64 __8wekyb3d8bbwe', 'Type': 12}|Full name|
|System.Identity|{'Value': 'Microsoft.BingWeather_8wekyb3d8bbwe', 'Type': 12}|Short name|
|System.FileName|{'Value': 'vmware', 'Type': 12}|Actual filename without extension|
|System.ConnectedSearch.JumpList|List of values, in Screenshot|Contains jumplists for some apps that don't have jumplists in the normal location|
|System.ConnectedSearch. VoiceCommandExamples|Unknown|Not sure yet, all my rows were blank.|
|System.ItemType|Trusted Immersive|Options on my machine are "Trusted Immersive", "Immersive", or "Desktop"|
|System.DateAccessed|133022364739230000|Date of access in Windows Filetime - not last access for all|
|System.Tile.EncodedTargetPath|C:\Users\%USERNAME%\AppData\Local\Programs\Python\ Python310\pythonw.exe|May be full file path or same as ParsingName|		
|System.Tile.SmallLogoPath|images\logo.png|Mostly Windows services have this, looks like part of path to the logo/icon image|
|System.ItemNameDisplay|GitHub Desktop|Basic application display name.|

Additional Notes:
If ParsingName starts with "6D809377-6AF0-444B-8957-A3773F02200E" or "7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E" that seems to refer to the folder "\Program Files (x86)\". Confirmed by both registry folder values (HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FolderDescriptions) and looking at the full path of the executable. If it starts with "1AC14E77-02E7-4E5D-B744-2EB1AE5198B7" or "D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27" that seems to refer to System32 or SysWOW64. Last, if it starts with "F38BF404-1D43-42F2-9305-67DE0B28FC23", it is located in the C:\Windows folder.  
It appears that "Tile.Background" has a common value of 16777215 on my machine for most applications and then some Windows applications have other larger values.

## Script Info

I will be continuing to work on this as time allows. It is intended only for my research purposes at this time. You can run it from any folder on a Windows machine and it *should* pull the AppCache#.txt file from the host machine and copy it to a folder within the working directory along with the csv of simply parsed data. The ConnectedSearch.Jumplists needs more parsing but I wanted a quick way to pull on different machines so I could just copy one folder over. I am running this on Python 3.10.4. 
