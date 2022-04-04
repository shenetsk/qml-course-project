import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject
from peewee import SqliteDatabase

db = SqliteDatabase("main.db")

from UsersModel import UsersModel
from FoldersModel import FoldersModel
from FilesModel import FilesModel
from UserRecordsModel import Users
from RecordsModel import Favorites
import names

class Base(QObject):
	def __init__(self, parent=None):
		self.db = db
	
		super().__init__(parent)	
		
		self.initDataBase()
		
		app = QGuiApplication(sys.argv)
		engine = QQmlApplicationEngine()

		self.users = UsersModel(self)
		self.files = FilesModel(self)
		self.folders = FoldersModel(self)

		engine.rootContext().setContextProperty('usersModel', self.users)
		engine.rootContext().setContextProperty('foldersModel', self.folders)
		engine.rootContext().setContextProperty('filesModel', self.files)

		engine.load("main.qml")	

		self.folders.getFolders()

		engine.quit.connect(app.quit)
		sys.exit(app.exec_())
	
	def initDataBase(self):
		if not db.table_exists('users'):
			db.create_tables([Users, Favorites])
			
			with db.atomic():
				for _ in range(10):
					user = Users.create(name=names.get_full_name(gender='male'))