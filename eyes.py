import bot
import guard
import cv2
import time

# Configuration


# Main
guard = guard.Guard()
bigbrother = bot.BigBrother()
lastprediction = {}

while True:

    # Data collection
    frame = guard.getFrame()
    frame.display()

    if guard.humanDetected():

        # First human EVER!
        if len(guard.knownMembers()) == 0:
            img = frame.getFace(0)
            if img is not None:
                bigbrother.post_image("guest", img)
                bigbrother.post_message(
                    "I'm sorry, I'm new here, could you identify this person that just came in? \n"
                    " please respond in this channel with the person's name")
                if guard.getLabel(img, frame.getFaceEncoding(0)):
                    bigbrother.post_message("Thanks! I'll remember that")
                else:
                    bigbrother.post_message("Never mind, I guess you're busy")
        else:
            face_encoding = frame.getFaceEncoding(0)
            if face_encoding is not None:
                prediction = guard.identify(face_encoding)
                print(prediction)
                if prediction.get("error") == "not enough data":
                    img = frame.getFace(0)
                    bigbrother.post_image("guest", img)
                    bigbrother.post_message(
                        "ok, I'm still learning, could you help me identify this person?  \n"
                        " please respond in this channel with the person's name")
                    if guard.getLabel(img, face_encoding):
                        bigbrother.post_message("Got it!")
                    else:
                        bigbrother.post_message("Never mind, I guess you're busy")
                else:
                    if len(guard.knownMembers()) == 1:
                        img = frame.getFace(0)
                        bigbrother.post_image("guest", img)
                        bigbrother.post_message("Is this also " + prediction.get("name") + "?")
                        confirmation = guard.getConfirmation()
                        if confirmation.get("response") is None:
                            if confirmation.get("text") is None:
                                bigbrother.post_message("ok, I guess you're busy, never mind...")
                            else:
                                bigbrother.post_message(
                                    "sorry, I didn't understand your answer could you be more clear like saying yes or no?")
                                confirmation = guard.getConfirmation()
                                if confirmation.get("response") is None:
                                    if confirmation.get("text") is None:
                                        bigbrother.post_message("oh never mind :face_with_rolling_eyes:")
                                    else:
                                        bigbrother.post_message(
                                            "oh... this is obviously to hard for you, never mind :face_with_rolling_eyes:")
                                else:
                                    if confirmation.get("response"):
                                        bigbrother.post_message("great! thanks")
                                        guard.addLabeledData(prediction.get("id"), face_encoding)
                                    else:
                                        bigbrother.post_message(
                                            "oh ok, sorry I'm still getting to know you guys \n who is it then?")
                                        if guard.getLabel(img, face_encoding):
                                            bigbrother.post_message(
                                                "ok! I'll try to remember, I'll get better soon don't worry")
                                        else:
                                            bigbrother.post_message(
                                                "well, looks like you are busy right now, never mind")
                        else:
                            if confirmation.get("response"):
                                bigbrother.post_message("great! thanks")
                                guard.addLabeledData(prediction.get("id"), face_encoding)
                            else:
                                bigbrother.post_message(
                                    "oh ok, sorry I'm still getting to know you guys \n who is it then?")
                                if guard.getLabel(img, face_encoding):
                                    bigbrother.post_message("ok! I'll try to remember")
                                else:
                                    bigbrother.post_message("well, looks like you are busy right now, never mind")
                    else:
                        if prediction.get("probability") > 0.9:
                            ts = time.time()
                            last_ts = lastprediction.get(prediction.get("id"))
                            if last_ts is None:
                                last_ts = 0
                            lastprediction[prediction.get("id")] = ts
                            if (ts - last_ts) > 5400:  # 15 minutes
                                bigbrother.post_message(
                                    prediction.get("name") + " just entered the office :slightly_smiling_face:",
                                    permanent=False)
                        else:
                            if prediction.get("probability") > 0.7:
                                img = frame.getFace(0)
                                bigbrother.post_image("guest", img)
                                bigbrother.post_message("is this " + prediction.get("name") + "? I'm not quite sure")
                                confirmation = guard.getConfirmation()
                                if confirmation.get("response") is None:
                                    if confirmation.get("text") is None:
                                        bigbrother.post_message("ok, I guess you're busy, never mind...")
                                    else:
                                        bigbrother.post_message(
                                            "sorry, I didn't understand your answer could you be more clear like saying yes or no?")
                                        confirmation = guard.getConfirmation()
                                        if confirmation.get("response") is None:
                                            if confirmation.get("text") is None:
                                                bigbrother.post_message("oh never mind :face_with_rolling_eyes:")
                                            else:
                                                bigbrother.post_message(
                                                    "oh... this is obviously too hard for you, never mind :face_with_rolling_eyes:")
                                        else:
                                            if confirmation.get("response"):
                                                bigbrother.post_message("great! thanks")
                                                guard.addLabeledData(prediction.get("id"), face_encoding)
                                            else:
                                                bigbrother.post_message(
                                                    "oh ok, sorry I'm still getting to know you guys \n who is it then?")
                                                if guard.getLabel(img, face_encoding):
                                                    bigbrother.post_message(
                                                        "ok! I'll try to remember, I'll get better soon don't worry")
                                                else:
                                                    bigbrother.post_message(
                                                        "well, looks like you are busy right now, never mind")
                                else:
                                    if confirmation.get("response"):
                                        bigbrother.post_message("great! thanks")
                                        guard.addLabeledData(prediction.get("id"), face_encoding)
                                    else:
                                        bigbrother.post_message(
                                            "oh ok, sorry I'm still getting to know you guys \n who is it then?")
                                        if guard.getLabel(img, face_encoding):
                                            bigbrother.post_message("ok! I'll try to remember")
                                        else:
                                            bigbrother.post_message(
                                                "well, looks like you are busy right now, never mind")
                            else:
                                # print("here!")
                                img = frame.getFace(0)
                                bigbrother.post_image("guest", img)
                                bigbrother.post_message(
                                    "well, I don't know who this is, could you help me identify this person?  \n"
                                    " please respond in this channel with the person's name")
                                if guard.getLabel(img, face_encoding):
                                    bigbrother.post_message(
                                        "Thanks, I'm learning, don't worry, I'll get better at this soon")
                                else:
                                    bigbrother.post_message("Never mind, I guess you're busy")
        time.sleep(8)
        bigbrother.delete_messages()
        bigbrother.delete_images()

    # Stop logic
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# End
guard.release()
