import os
import pickle
import cv2
import face_recognition
import time
import json
import pandas as pd
import numpy as np
from cv2 import imwrite
from sklearn import neighbors

camera_nbr = 1

request_file = "tmp/request.pickle"
response_file = "tmp/response.pickle"

# Folder Creation
path_db = "db"
path_member_images = "db/member_images"
path_temp = "tmp"
folders = [path_db, path_member_images, path_temp]
for folder in folders:
	if not os.path.exists(folder):
		os.mkdir(folder)

class Guard:

	def __init__(self):
		self.min_frames_detection = 1
		self.min_frams_non_detection = 1
		self.frames_detecting = 0
		self.frames_not_detecting = 100
		self.cam = cv2.VideoCapture(camera_nbr)
		self.members = None
		self.labeled_db = None
		self.classifier = None
		self.k = 3
		self.load_data()

	def load_data(self):
		try:
			members_file = open("db/members.pickle", "rb")
			self.members = pickle.load(members_file)
			members_file.close()
		except:
			self.members = pd.DataFrame(columns=["id","name","instances"])
		try:
			labeled_db_file = open("db/labeled_db.pickle", "rb")
			self.labeled_db = pickle.load(labeled_db_file)
			labeled_db_file.close()
		except:
			pass
		try:
			classifier_file = open("db/classifier.pickle", "rb")
			self.classifier = pickle.load(classifier_file)
			classifier_file.close()
		except:
			pass

	def knownMembers(self):
		return self.members

	def addMember(self, img, name):
		if len(self.members[self.members.name == name]) > 0:
			return None
		member_id = len(self.members)
		self.members = self.members.append(pd.DataFrame([[member_id,name,0]], columns=["id","name","instances"]), ignore_index=True)
		print(self.members)
		imwrite(path_member_images+"/"+str(self.members.id[member_id])+"-"+str(self.members.name[member_id])+".png", img)
		return member_id

	def getMemberID(self, name):
		if len(self.members[self.members.name == name]) == 0:
			return None
		return self.members.id[self.members.name == name]

	def getMemberName(self, member_id):
		if len(self.members[self.members.id == member_id]) == 0:
			return None
		return self.members.name[self.members.id == member_id]

	def addLabeledData(self, member_id, face_encoding):
		#self.members[self.members.id == member_id].instances = self.members[self.members.id == member_id].instances+1
		if self.labeled_db is None:
			self.labeled_db = np.array([[member_id] + face_encoding.tolist()])
			self.classifier = neighbors.KNeighborsClassifier(self.k, weights="distance")
		else:
			self.labeled_db = np.vstack([self.labeled_db, np.array(([member_id] + face_encoding.tolist()))])
		self.classifier.fit(self.labeled_db[:,1:],np.array(self.labeled_db[:,:1].reshape(self.labeled_db.shape[0]), dtype=int))	
		self.save()

	def getFrame(self):
		frame = Frame(self.cam.read()[1])
		if frame.hasFaces():
			self.frames_detecting = self.frames_detecting + 1
		else:
			self.frames_detecting = 0
		return frame

	def humanDetected(self):
		if self.frames_detecting >= self.min_frames_detection and self.frames_not_detecting >= self.min_frams_non_detection:
			self.frames_not_detecting = 0
			return True
		else:
			self.frames_not_detecting = self.frames_not_detecting + 1
			return False

	def identify(self, face_encoding):
		if self.members is None or len(self.labeled_db) < self.k:
			result = {"error": "not enough data"}
		else:

			prediction = self.classifier.predict([face_encoding])
			probability = self.classifier.predict_proba([face_encoding])
			print("_______")
			print(prediction)
			print(probability)
			print("_______")
			result = {"id": prediction[0], "probability": probability[0][prediction[0]],
					 "name": self.getMemberName(prediction[0])}
		return result

	def getLabel(self, img, face_encoding):
		max_time = 360
		file = open(request_file, "wb")
		pickle.dump(face_encoding, file)
		file.close()
		print("Waiting for face labeling...")

		while True:
			time.sleep(1)
			if not os.path.isfile(request_file) and os.path.isfile(response_file):
				file = open(response_file, "rb")
				message = json.load(file)
				file.close()
				name = message.get("text")
				member_id = self.addMember(img, name)
				if member_id == None:
					member_id = self.getMemberID(name)
				self.addLabeledData(member_id, face_encoding)
				
				
				os.remove(response_file)
				return True

			# request time out
			max_time = max_time-1
			if max_time < 0:
				os.remove(request_file)
				return False

	def getConfirmation(self):
		max_time = 360
		file = open(request_file, "wb")
		pickle.dump("confirm", file)
		file.close()
		print("Waiting for confirmation...")
		while True:
			time.sleep(1)
			if not os.path.isfile(request_file) and os.path.isfile(response_file):
				file = open(response_file, "rb")
				message = json.load(file)
				file.close()
				response = message.get("text")
				os.remove(response_file)
				if response in ["yeah!", "yes", "yeah", "yep", "yes"]:
					return {"response": True}
				if response in ["no", "no!", "nah", "nope"]:
					return {"response": False}
				return {"response": None, "text": response}

			# request time out
			max_time = max_time-1
			if max_time < 0:
				os.remove(request_file)
				return False

			
	def save(self):
		try:
			members_file = open("db/members.pickle", "wb")
			pickle.dump(self.members, members_file)
			members_file.close()
		except:
			print("Error saving members file")
		try:
			labeled_db_file = open("db/labeled_db.pickle", "wb")
			pickle.dump(self.labeled_db, labeled_db_file)
			labeled_db_file.close()
		except:
			print("Error saving labeled_db file")
		try:
			classifier_file = open("db/classifier.pickle", "wb")
			pickle.dump(self.classifier, classifier_file)
			classifier_file.close()
		except:
			print("Error saving classifier file")

	def release(self):
		self.cam.release()
		cv2.destroyAllWindows()


class Frame:

	def __init__(self, img):
		self.img = img
		self.img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.face_locations = face_recognition.face_locations(self.img_gray)
		self.n_faces = len(self.face_locations)
		self.face_encodings = face_recognition.face_encodings(self.img)
		self.img_gray_marked = self.draw_rectangles(self.img_gray, self.face_locations)

	def draw_rectangles(self, img, face_locations):
		result = img.copy()
		for loc in face_locations:
			top, right, bottom, left = loc
			result[top-3:top+3,left:right] = 255
			result[bottom-3:bottom+3,left:right] = 255
			result[top:bottom,left-3:left+3] = 255
			result[top:bottom,right-3:right+3] = 255
		return result

	def display(self, marked=True):
		if marked:
			cv2.imshow("Frame", self.img_gray_marked)
		else:
			cv2.imshow("Frame", self.img_gray)

	def hasFaces(self):
		return self.n_faces > 0

	def getFace(self, index):
		if index >= self.n_faces:
			return None
		return self.crop_face(self.img, self.face_locations[index])

	def getFaceEncoding(self, index):
		if index >= len(self.face_encodings):
			return None
		return self.face_encodings[index]

	def crop_face(self, img, face_location):
		height, width, _ = img.shape
		top, right, bottom, left = face_location
		padding = int(((bottom-top+right-left)/2)*0.3)
		top = top-padding if top-padding > 0 else 0
		bottom = bottom+padding if bottom+padding < height else height
		left = left-padding if left-padding > 0 else 0
		right = right+padding if right+padding < width else width
		return img[top:bottom,left:right]
