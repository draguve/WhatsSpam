import speech_recognition as sr 

class sTT:
	def __init__(self):
		self.mic_name = 'default'
		self.sampling_rate = 48000
		self.chunk_size = 2048
		self.r = sr.Recognizer()
		self.deviceID = None

	def getDeviceID(self):
		mic_list = sr.Microphone.list_microphone_names()

		for i, microphone_name in enumerate(mic_list):
			if microphone_name == self.mic_name:
				deviceID = i
		
		self.deviceID = deviceID
		

	def getInput(self, field):
		print(field)
		with sr.Microphone(device_index = self.deviceID, sample_rate = self.sampling_rate, chunk_size = self.chunk_size) as source:
			self.r.adjust_for_ambient_noise(source)
			print("listening....")
			audio = self.r.listen(source)

			try:
				text = self.r.recognize_google(audio)
				return text

			except sr.UnknownValueError:
				print("Pardon...")

			except sr.RequestError as e:
				print("Could not request results from server;{0}".format(e))

