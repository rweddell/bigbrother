from slackeventsapi import SlackEventAdapter
import os
import json

config = {}
request_file = "tmp/request.pickle"
response_file = "tmp/response.pickle"

with open('configs.json', "r") as file:
	config = json.load(file)
	file.close()

slack_events_adapter = SlackEventAdapter(str(config.get("slack_signing_secret")), "/slack/events")

@slack_events_adapter.on("message")
def handle_message(event_data):
	print(event_data.get("event").get("user"))
	if event_data.get("event").get("user") != config.get("bot_user"):
		message = event_data.get("event")
		if os.path.isfile(request_file):
			os.remove(request_file)
			with open(response_file, "w") as file:
				json.dump(message, file)
				file.close()


@slack_events_adapter.on("error")
def error_handler(err):
	print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)
