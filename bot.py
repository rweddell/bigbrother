from slackclient import SlackClient
from cv2 import imwrite
import json

config = {}
with open('configs.json') as json_data:
    config = json.load(json_data)
    json_data.close()


class BigBrother:

    def __init__(self):
        self.channel = config.get("channel_training")
        self.encoded_channel = ''
        self.client = SlackClient(config.get("slack_bot_token"))
        self.messages_posted = []
        self.images_posted = []

    def post_message(self, message, permanent=False):
        response = self.client.api_call(
            "chat.postMessage",
            channel=self.channel,
            text=message,
            as_user=True
        )
        if response["ok"]:
            print("Message posted: " + message, response['ts'])
            if self.encoded_channel is '':
                self.encoded_channel = response["channel"]
            if permanent==False:
                self.messages_posted.append(response["ts"])
            return True
        else:
            print("Error: Message not posted: " + message)
            return False

    def post_image(self, title, img):
        path = "tmp/" + title + ".png"
        imwrite(path, img)
        response = self.client.api_call(
            "files.upload",
            channels=[self.channel],
            filename=path,
            title=title,
            file=open(path, "rb"),
            as_user=True
        )
        if response["ok"]:
            print("Image posted: " + title + ".png", response['file']['id'])
            self.images_posted.append(response['file']['id'])
            return True
        else:
            print("Error: Image not posted: " + title + ".png")
            return False

    def delete_messages(self):
        # Message deletion works (4/25/19)
        print()
        for timestamp in self.messages_posted:
            try:
                print('Deleting message:', self.channel, timestamp)
                response = self.client.api_call(
                    "chat.delete",
                    channel=self.encoded_channel,
                    ts=timestamp,
                    as_user=True
                    )
                if response["ok"]:
                    print('Message deleted.')
                else:
                    print('Could not delete message')
                    print(response)
            except Exception as ex:
                print("Call to 'bot.delete_messages()' unsuccessful")
                print(ex)
        self.messages_posted = []

    def delete_images(self):
        # Image deletion works (4/24/19)
        print()
        for file in self.images_posted:
            try:
                print('Deleting image:', file)
                response = self.client.api_call(
                    "files.delete",
                    file=file
                    )
                if response["ok"]:
                    print('Image deleted.')
                else:
                    print('Could not delete image', file)
                    print(response)
            except Exception as ex:
                print("Call to 'bot.delete_images()' unsuccessful")
                print(ex)
        self.images_posted = []
