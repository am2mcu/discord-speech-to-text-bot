import requests
import time
import os

UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
HEADER = header = {
        'authorization': os.environ.get("API_KEY_STT"),
        'content-type': 'application/json'
        }

# Helper for `upload_file()`
def read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data


# Uploads a file to AAI servers
def upload_file(audio_file, header):
    upload_response = requests.post(
        UPLOAD_ENDPOINT,
        headers=header, data= read_file(audio_file)
    )

    debug(upload_response.json())

    return upload_response.json()


# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url, header):
    transcript_request = {
        'audio_url': upload_url['upload_url']
    }
    transcript_response = requests.post(
        TRANSCRIPT_ENDPOINT,
        json=transcript_request,
        headers=header
    )

    debug(transcript_response.json())

    return transcript_response.json()


# Make a polling endpoint
def make_polling_endpoint(transcript_response):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']

    debug(polling_endpoint)

    return polling_endpoint


# Wait for the transcript to finish
def wait_for_completion(polling_endpoint, header):
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()

        debug(polling_response)

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)


# Get the paragraphs of the transcript
def get_paragraphs(polling_endpoint, header):
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", headers=header)
    paragraphs_response = paragraphs_response.json()

    debug(paragraphs_response)

    paragraphs = []
    for para in paragraphs_response['paragraphs']:
        paragraphs.append(para)

    debug(paragraphs)

    return paragraphs


def debug(txt):
    # print(txt)
    pass


async def main(url):
    debug("uploading the audio...")

    # audio_file = "music/audio.mp3"
    # upload_url = upload_file(audio_file, header) # local
    upload_url = {'upload_url': url}

    # Request a transcription
    transcript_response = request_transcript(upload_url, header)

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    wait_for_completion(polling_endpoint, header)

    # Request the paragraphs of the transcript
    paragraphs = get_paragraphs(polling_endpoint, header)

    transcripted_result = ""

    for para in paragraphs:
        transcripted_result += para['text'] + '\n'
        # print(para['text'] + '\n')

    return transcripted_result