

import os
import json

from jk_utils.file_rw import loadBinaryFile, writePrivateBinaryFile, writePrivateJSONFile
from jk_utils import ChModValue

from .User import User









class UserMgr(object):

	def __init__(self, dirPath:str):
		assert isinstance(dirPath, str)

		self.__dirPath = dirPath

		if not os.path.isdir(self.__dirPath):
			os.mkdir(self.__dirPath)
		os.chmod(self.__dirPath, ChModValue("rwx------").toInt())

		self.__users = {}

		allKeys = []
		for entry in os.scandir(self.__dirPath):
			if entry.is_dir():
				allKeys.append(entry.name)

		for userName in allKeys:
			userDirPath = os.path.join(self.__dirPath, userName)
			userDataFilePath = os.path.join(userDirPath, "data.json")
			if os.path.isfile(userDataFilePath):
				user = self._instantiateUserObject(userName, userDirPath)
				self.__users[userName] = user
	#

	def __len__(self):
		return len(self.__users)
	#

	def getAllUserNames(self) -> list:
		return [ key for key in sorted(self.__users.keys()) ]
	#

	def getAllUsers(self) -> list:
		return [ self.__users[key] for key in sorted(self.__users.keys()) ]
	#

	@property
	def allUserNames(self) -> list:
		return [ key for key in sorted(self.__users.keys()) ]
	#

	@property
	def allUsers(self) -> list:
		return [ self.__users[key] for key in sorted(self.__users.keys()) ]
	#

	def getUser(self, userName:str) -> User:
		assert isinstance(userName, str)

		u = self.__users.get(userName)
		return u
	#

	def getUserE(self, userName:str) -> User:
		assert isinstance(userName, str)

		u = self.__users.get(userName)
		if u is None:
			raise Exception("No such user: " + repr(userName))
		return u
	#

	def hasUser(self, userName:str) -> bool:
		assert isinstance(userName, str)

		u = self.__users.get(userName)
		return u is not None
	#

	def getCreateUser(self, userName:str) -> User:
		u = self.getUser(userName)
		if u is None:
			u = self.createUser(userName)
		return u
	#

	def createUser(self, userName:str) -> User:
		assert isinstance(userName, str)

		if userName in self.__users:
			raise Exception("User already exists: " + userName)

		userDirPath = os.path.join(self.__dirPath, userName)
		if not os.path.isdir(userDirPath):
			os.mkdir(userDirPath)
			os.chmod(userDirPath, ChModValue("rwx------").toInt())
		userDataFilePath = os.path.join(self.__dirPath, userName, "data.json")
		writePrivateJSONFile(self._generateInitialUserDataStructure(), userDataFilePath, bPretty=True)

		u = self._instantiateUserObject(userName, userDirPath)
		self.__users[userName] = u
		return u
	#

	#
	# This method creates a raw data structure for user objects.
	# You can overwrite this method if you would like to extend this data structure.
	#
	def _generateInitialUserDataStructure(self) -> dict:
		return {
			"version": 1,
			"privileges": []
		}
	#

	#
	# This method creates a user object.
	# You can overwrite this method if you would like to return a subclass of <c>User</c>.
	#
	def _instantiateUserObject(self, userName:str, userDirPath:str) -> User:
		return User(userName, userDirPath)
	#

#

















