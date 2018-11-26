# Overview
This project consists of a slackbot that uses a webcam directed to the entrance of an office and sends a message to the general channel whenever somebody comes in. It doesn’t need a starting dataset, it asks users to label data through the Slack channel chat.

# System diagram
![System Diagram](https://github.com/estefanytorres/bigbrother/blob/master/documentation/diagram.png "System Diagram")

# Installation and setup (Under construction)
In order to install this bot locally and add it to your slack channel you must follow this steps. It has only been tested in Ubuntu 18.04 so far, the most complicated requirement is to build dlib and I did not try this on a windows OS.

**1. Create your own app**

First you need your own slack workspace to try this at, if you don't use slack you can create a workspace at [slack](https://slack.com/get-started#create)

Once you have a workspace you can create an app at [the slack api page](https://api.slack.com/), click start building and give a name and workspace to your app (I suggest you use bigbrother to keep the theme). Then at the left panel click on _Features > Bot Users_ and create a bot, add bot user and dont forget to save changes! 

**2. Configure your bot**

Now you need to give a scope to your bot, you can do this at _Features > OAuth & Permissions_ in the scope section select chat:write:bot and save changes. 

We also need to enable events and subscribe to them, go to _Features > Event Subscriptions_ and turn it on, in the subscribe to Bot Events section add only messages.channel for now.

**3. Clone this repository**

Navigate to your projects folder using the terminal and type

```bash
$ git clone https://github.com/estefanytorres/bigbrother.git
```

**4. Install requirements**

You will need to build dlib previously, this is a [tutorial](https://www.youtube.com/watch?v=h0Uidh-sq9M) I used on how to do that if your not familiar with building in linux.

Then you can pip install all the python packages by typing in the bigbrother folder.

```bash
$ pip install -r requirements.txt
```

**5. Add configuration to your code**

Create a configs.json file in your bot's directory and copy the slack bot token _(OAuth & Permissions > OAuth Tokens & Redirect URLs > Bot User OAuth Access Token)_ and the slack signing secret _(Basic Information > App Credentials > Signing Secret)_ from the app configuration in this format:


``` json
{
"slack_bot_token":"XXXX-XXXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX",
"slack_signing_secret":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

**6. Start your bot**

You need three terminals to run bigbrother, in one you will run eyes.py by navigating to the folder and typing

```bash
$ python eyes.py
```

In the second terminal run app.py with the following command

```bash
$ python app.py
```

and finally you will need to download, install and run [ngrok](https://ngrok.com/) to make your localhost public, follow the instructions in the web page and launch port 3000 in this way

```bash
$ ./ngrok http 3000
```

This will give you a list of public urls, copy the https one and add it to your app's configuration in the Events subscription Request URL field.

**7. Start your bot**

Install your app into the workspace at _Settings > Install App_, invite it to the channel you will use for training and start using your bot!



# Demo video
[Youtube - BigBrother walkthrough and demo](https://youtu.be/PDqX2kdnBGM)
