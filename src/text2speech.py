import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="package.json"
from google.cloud import texttospeech



# def ssmlConverter(text):
#     somePhrase = '<speak> <prosody rate=\"slow\" pitch=\"-2st\">'
#     somePhrase = '<speak> <emphasis level = \"strong\"'
#     counter = 0
#     for token in text.split():
#         if counter == 0:
#             #somePhrase += (token + "</prosody> <emphasis level = \"strong\">")
#             somePhrase += (" " + token)
#             counter += 1
#             continue
#         somePhrase += token
    
#     somePhrase += " </emphasis> </speak>"
#     someSarcasticPlaceHolder = '<speak> Hi i am sarcastic </speak>'
#     return someSarcasticPlaceHolder
        

def synthesize_text_file(text, outputName, isSarcastic = False):
    
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    if isSarcastic:
        print("Yep is sarcastic")
        voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open(outputName, 'wb+') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + outputName)
    return outputName

    