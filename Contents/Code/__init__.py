PREFIX   				= "/video/current"

TITLE 					= 'Current TV'
ART 					= 'art-default.png'
ICON 					= 'icon-default.png'

CURRENT_ROOT            	= "http://current.com"
CURRENT_PLAYLIST_URL	= 'http://current.com/proxy/index.php/cccp/%s/items.htm?id=%s&sort=new&start=0&len=50&filter=allVeepableVideos&include=contentPageAsset%%2CcontentParentGroup%%2CgroupSkin%%2CfeaturedContent'

####################################################################################################
def Start():
	Plugin.AddPrefixHandler(PREFIX, MainMenu, TITLE, ICON, ART)
	Plugin.AddViewGroup('InfoList', viewMode = 'InfoList', mediaType = 'items')

	ObjectContainer.view_group = 'InfoList'
	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)

	DirectoryObject.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['X-Requested-With'] = "XMLHttpRequest"

####################################################################################################
def MainMenu():
	oc = ObjectContainer()

	oc.add(DirectoryObject(key = Callback(CurrentShows, title = 'Current Shows'), title = 'Current Shows'))
	oc.add(DirectoryObject(key = Callback(ShortFilms, title = 'Short Films'), title = 'Short Films'))

	return oc

####################################################################################################
def CurrentShows(title):
	oc = ObjectContainer(title2 = title)

	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'The Beat', id = '90004943', type = 'tag'), title = 'The Beat'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'The Burried Life', id = '90001176', type = 'tag'), title = 'The Burried Life'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Extreme Tourist', id = '90000647', type = 'tag'), title = 'Extreme Tourist'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Deadliest Journeys', id = '89832869', type = 'tag'), title = 'Deadliest Journeys'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'What Did I Do Last Night', id = '89952425', type = 'tag'), title = 'What Did I Do Last Night'))

	return oc

####################################################################################################
def ShortFilms(title):
	oc = ObjectContainer(title2 = title)

	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Culture and Society', id = 'groups%2Fculture-and-society-docs', type = 'group'), title = 'Culture and Society'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Sex and Relationships', id = 'documentaries%2Fsex-and-relationships', type = 'group'), title = 'Sex and Relationships'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Environment', id = 'documentaries%2Fenvironment', type = 'group'), title = 'Environment'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Comedy', id = 'comedy', type = 'group'), title = 'Comedy'))
	oc.add(DirectoryObject(key = Callback(PlaylistMenu, title = 'Sport', id = 'documentaries%2Fsport', type = 'group'), title = 'Sport'))

	return oc

####################################################################################################
def PlaylistMenu(title, id, type):
	oc = ObjectContainer(title2 = title)

	playlist = JSON.ObjectFromURL(CURRENT_PLAYLIST_URL % (type, id))
	for item in playlist['items']:
		url = CURRENT_ROOT + item['url']
		title = item['contentTitle']
		summary = item['contentText']
		date = Datetime.ParseDate(item['dateAdded'])
		duration = int(item['pageAsset']['duration'])

		thumb = item['pageAsset']['thumbUrl']
		if thumb.endswith('.jpg') == False:
			thumb = thumb + '_400x300.jpg'

		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = thumb,
			duration = duration,
			originally_available_at = date))

	return oc

