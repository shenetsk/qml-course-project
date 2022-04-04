import os
from PyQt5.QtCore import Qt, QByteArray, QAbstractListModel, QModelIndex, pyqtSlot
from UserRecordsModel import Users
from RecordsModel import Favorites

class UsersModel(QAbstractListModel):
	userName = Qt.UserRole + 1

	def __init__(self, parent=None):
		self.base = parent
		
		super().__init__(parent)
		
		self.users = []

	def rowCount(self, parent=QModelIndex()):
		return len(self.users)

	def data(self, index, role):
		return self.users[index.row()]['userName']
		
	def roleNames(self):	
		default = super().roleNames()
		default[self.userName] = QByteArray(b"userName")
		return default

	@pyqtSlot()
	def loadUsers(self):
		self.beginResetModel()

		self.users = []

		query = Users.select()
		
		for user in query:
			self.users.append({'userName': user.name, 'id': user.id})
		
		self.endResetModel()
		
	@pyqtSlot(int)
	def saveFavorite(self, index):
		with self.base.db.atomic():
			Favorites.create(user_id=self.users[index]['id'], path=self.base.folders.currentDirectoryPlain)