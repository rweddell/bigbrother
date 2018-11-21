# Overview
This project consists of a slackbot that uses a webcam directed to the entrance of an office and sends a message to the general channel whenever somebody comes in. It doesn’t need a starting dataset, it asks users to label data through the Slack channel chat.

# System diagram
![System Diagram](https://github.com/estefanytorres/bigbrother/blob/master/documentation/diagram.png "System Diagram")

# Installation and setup
In order to install this bot locally and add it to your slack channel you must follow this steps. It has only been tested in Ubuntu 18.04 so far, the most complicated requirement is to build dlib and I did not try this on a windows OS.

**1. Create your own app**

First you need your own slack workspace to try this at, if you don't use slack you can create a workspace at [slack](https://slack.com/get-started#create)

Once you have a workspace you can create an app at [the slack api page](https://api.slack.com/), click start building and give a name and workspace to your app (I suggest you use bigbrother to keep the theme). Then at the left panel click on _Features > Bot Users_ and create a bot, add bot user and dont forget to save changes! 

Now you need to give a scope to your bot, you can do this at _Features > OAuth & Permissions_

**5. Clone this repository**

navigate to your projects folder using the terminal and type

    ```
    $ git clone https://github.com/estefanytorres/bigbrother.git
    ```

**6. Install requirements**

you will need to build dlib previously, this is a [tutorial](https://www.youtube.com/watch?v=h0Uidh-sq9M) I used on how to do that if your not familiar with building in linux.

    ```
    $ pip install -r requirements.txt
    ```



# Demo video
[Youtube - BigBrother walkthrough and demo](https://youtu.be/PDqX2kdnBGM)
