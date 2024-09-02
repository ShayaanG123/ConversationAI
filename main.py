from openai import OpenAI
import openai
import os
import pyaudio
import glob
import time
from playsound import playsound
from recordClass import RecAUD
from translation import translate, transcribe


key = os.environ.get("OPENAI_API_KEY2")
client = OpenAI(api_key=key)

convoCount = 1

spoken_language = input('What language are you learning: ')


while True:
    #Record Audio
    file_name = f'audioFile{convoCount}'
    aud = RecAUD(file_name)
    
    if aud.stopConvo == True:
        break

    
    audio_file= open(f"{file_name}.wav", "rb")

    #Transcribe Audio
    transcribedText = transcribe(audio_file, spoken_language)
    print(transcribedText)

    #Translate Text
    #translatedText = translate(audio_file)

    #Assistant Creation Code
    assistant = client.beta.assistants.create(
    name="ConvoAI",
    instructions=f"""You are a conversation partner to help people learn languages. Please respond to the prompt as if it were a conversation
                        and use words of similar difficulty as the prompt. Additionally make sure to answer any questions asked in the prompt and
                        end your response with a follow-up question relating to the conversation. The user should percieve that the conversation is
                        with another human. Please make sure your response is in {spoken_language}""",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
    )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= transcribedText
        )
    


    run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
    
    
    still_running = True
    while still_running:
        latest_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        still_running = latest_run.status != "completed"
        if (still_running):
            time.sleep(2)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print('\n\n')

    #Slicing String to output
    output = str((messages.data[0].content))
    x = output.split('value=')
    output = x[1]
    output = output[:-16]
    print(output)




    #Text to speech
    speech_file_path = 'convo_output_speech_generated.mp3'
    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="echo",
        input= output
    ) as response:
        response.stream_to_file(speech_file_path)
    #Play the output file
    playsound(f'//Users//shayaangandhi//Documents//python//ConversationAI//{speech_file_path}')
    time.sleep(5)



    convoCount += 1

print('Thank you for having a conversation with us!')