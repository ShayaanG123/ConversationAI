from openai import OpenAI
import openai
import os
import assemblyai as aai
from langauageCode import getLanguageCode

#Open AI API Key
key = os.environ.get("OPENAI_API_KEY2")
client = OpenAI(api_key=key)

#Assembly AI API Key
aai.settings.api_key = 'ae057d06e0f24402a188b064117cc8b6'
transcriber = aai.Transcriber()

def translate(audioFile):
    translation = client.audio.translations.create(
    model="whisper-1", 
    file=audioFile,
    response_format= 'verbose_json')
    print('\n\n')
    print(translation.language)
    print(translation.text)
    return translation.text

def transcribe(audioFile, spoken_language):
    lang = getLanguageCode(spoken_language)
    config = aai.TranscriptionConfig(language_code= lang)
    transcript = transcriber.transcribe(audioFile, config)
    if transcript.error:
        return transcript.error
    return transcript.text