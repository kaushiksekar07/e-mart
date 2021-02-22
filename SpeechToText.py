from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

config = json.load(open('keys/config.json', 'r'))
apiKey = config["ibmApiKey"]
apiUrl = config["ibmUrl"]

authenticator = IAMAuthenticator(apiKey)
speech_to_text = SpeechToTextV1( authenticator=authenticator)

speech_to_text.set_service_url(apiUrl)

def speechToText(audio_file):
    result = speech_to_text.recognize(audio=audio_file, model = "en-AU_NarrowbandModel").get_result()
    result = (result["results"][result["result_index"]]).get("alternatives")[result["result_index"]].get("transcript")
    return result


