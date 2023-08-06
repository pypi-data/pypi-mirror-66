Beautiful Custom Start Page
===
BCST allow you to create a beautiful start page very quickly. To install the dependencies, simply run:

    > pip install jinja2

Simple write a simple json resource file:
```
{
   "title":"Default Theme",
   "bookmarks":{
	  "engines":{
		 "Qwant":"https://www.qwant.com/",
		 "DDG":"https://duckduckgo.com/",
		 "Google":"http://google.fr"
	  },
	  "Reddit":{
		 "Home":"https://www.reddit.com/",
		 "Unixporn":"https://www.reddit.com/r/Unixporn",
		 "Linux":"https://www.reddit.com/me/m/linux"
	  },
	  "Social":{
		 "Discord":"https://discordapp.com/channels/@me",
		 "Twitter":"https://twitter.com/",
		 "LinuxRocks":"https://linuxrocks.online/web/getting-started"
	  }
   }
}
```
Then simply run:

> ./src/bcst.py \<resource-file-path> \<start-page-destination>
