from slackclient import SlackClient
from cv2 import imwrite
import json

# slack_api_token = "xoxb-460164821393-460770132274-FbKJyyQR7bPPCuqTZPuJCaLd"
config = {}
with open('configs.json') as json_data:
	config = json.load(json_data)
	json_data.close()



class BigBrother():

	def __init__(self):
		self.channel = config.get("channel_training")
		self.client = SlackClient(config.get("slack_bot_token"))

	def post_message(self, message):
		response = self.client.api_call(
			"chat.postMessage",
			channel = self.channel,
			text = message,
			as_user = True
			)
		if response["ok"]:
			print("Message posted: "+message)
			return  True
		else:
			print("Error: Message not posted: "+message)
			return False

	def post_image(self, title, img):
		path = "tmp/"+title+".png"
		imwrite(path, img)
		response = self.client.api_call(
			"files.upload",
			channels = [self.channel],
			filename = path,
			title = title,
			file = open(path, "rb"),
			as_user = True
			)
		if response["ok"]:
			print("Image posted: "+title+".png")
			return  True
		else:
			print("Error: Image not posted: "+title+".png")
			return False
