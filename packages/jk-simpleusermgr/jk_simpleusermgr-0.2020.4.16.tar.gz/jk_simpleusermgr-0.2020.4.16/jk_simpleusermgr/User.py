

import os
import json








class User(object):

	def __init__(self, userName:str, dirPath:str):
		assert isinstance(userName, str)
		if dirPath is not None:
			assert isinstance(dirPath, str)

		dataFilePath = os.path.join(dirPath, "data.json")

		self.__name = userName
		self.__dirPath = dirPath
		self.__dataFilePath = dataFilePath

		if (dataFilePath is not None) and os.path.isfile(dataFilePath):
			with open(dataFilePath, "r") as f:
				self.__data = json.load(f)
			assert self.__data["version"] == 1
		else:
			raise Exception()
	#

	@property
	def dirPath(self) -> str:
		return self.__dirPath
	#

	@property
	def hasKeyPair(self) -> bool:
		return False
	#

	@property
	def privileges(self) -> tuple:
		ret = self.__data.get("privileges", [])
		assert isinstance(ret, list)
		return tuple(ret)
	#

	@property
	def name(self) -> str:
		return self.__name
	#

	def __str__(self):
		return self.__name
	#

	def hasPrivilege(self, privilege:str) -> bool:
		assert isinstance(privilege, str)
		ret = self.__data.get("privileges", [])
		assert isinstance(ret, list)
		return privilege in ret
	#

	def __eq__(self, value):
		if isinstance(value, User):
			return value.__name == self.__name
		else:
			return None
	#

#

















