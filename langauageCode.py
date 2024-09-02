langCodeDict = { 
'English': 'en',
'Spanish': 'es',
'French':	'fr',
'German':	'de',
'Italian':	'it',
'Portuguese':	'pt',
'Dutch':	'nl',
'Hindi':	'hi',
'Japanese':	'ja',
'Chinese':	'zh',
'Finnish':	'fi',
'Korean':	'ko',
'Polish':	'pl',
'Russian':	'ru',
'Turkish': 'tr',
'Ukrainian':	'uk',
'Vietnamese':	'vi'}

def getLanguageCode(spoken_language):
    if spoken_language not in langCodeDict.keys():
        return "Language Not Supported"
    else:
        return langCodeDict[spoken_language]
