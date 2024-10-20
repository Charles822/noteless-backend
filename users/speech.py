import requests

API_URL = "https://api-inference.huggingface.co/models/SWivid/F5-TTS"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
audio, sampling_rate = query({
	"inputs": "Adrianna is lying on the floor, thinking",
})
# You can access the audio with IPython.display for example
from IPython.display import Audio
Audio(audio, rate=sampling_rate)