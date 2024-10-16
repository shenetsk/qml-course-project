import re
import os
from PyQt5.QtCore import Qt, QByteArray, QAbstractListModel, QModelIndex, pyqtSlot, pyqtSignal

class FoldersModel(QAbstractListModel):
	folderName = Qt.UserRole + 1

	folders = []

	folderResult = pyqtSignal(str, arguments=['folder'])

	def __init__(self, parent=None):
		self.base = parent
	
		super().__init__(parent)
		
		self.currentDirectory = re.findall('%s[^%s]+' % (os.sep, os.sep), os.path.dirname(os.path.abspath(__file__)))
	
	def getFolders(self):
		self.folders = []
		
		if (len(self.currentDirectory)):
			self.folders.append({'folderName': '..'})
		
		self.currentDirectoryPlain = ''.join(self.currentDirectory) + os.sep
		
		self.folderResult.emit(self.currentDirectoryPlain)
		
		self.base.files.getFiles(self.currentDirectoryPlain)

		self.beginResetModel()
	
		self.folders += [{'folderName': d} for d in sorted(os.listdir(self.currentDirectoryPlain)) if os.path.isdir(self.currentDirectoryPlain + d)]
		
		self.endResetModel()

	def rowCount(self, parent=QModelIndex()):
		return len(self.folders)

	def data(self, index, role):
		return self.folders[index.row()]['folderName']
		
	def roleNames(self):	
		default = super().roleNames()
		default[self.folderName] = QByteArray(b"folderName")
		return default

	@pyqtSlot(int)
	def selectFolder(self, index):	
		if index == 0 and len(self.currentDirectory):
			self.currentDirectory.pop()
		else:
			self.currentDirectory.append(os.sep + self.folders[index]['folderName'])
		
		self.getFolders()