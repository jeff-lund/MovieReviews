from google.cloud import texttospeech
from google.cloud import storage
from flask import current_app
import random
import string

def read_text(text, language):
    """
    Takes in input text and uses Google Text-to-Speech API to convert to mp3 file.
    The file is stored in a Google cloud storage bucket.
    :return storage bucket blob name
    """
    # Set up clients.
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(current_app.config['STORAGE'])
    client = texttospeech.TextToSpeechClient()
    # Read text to create mp3.
    input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(language_code=language, ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(input, voice, audio_config)
    # Create random filename from lowercase letters and numbers.
    filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) + '.mp3'    
    # Store to google cloud bucket.
    blob = bucket.blob(filename)
    blob.upload_from_string(response.audio_content, content_type='audio/mp3')
 
    return blob.name
