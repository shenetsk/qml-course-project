import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

ApplicationWindow {
	visible: true
	width: 1100
	height: 600
	title: qsTr("Files Viewer")

	Connections {
		target: foldersModel

		function onFolderResult(folder) {
			currentPath.text = folder
		}
	}
	
	Connections {
		target: filesModel

		function onFileResult(file, text) {
			if (text)
			{
				textPreview.text = text
				imagePreview.visible = false
				textPreview.visible = true
			}
			else if (file.match(".png|.jpg$"))
			{
				imagePreview.source = file
				imagePreview.visible = true
				textPreview.visible = false
			}
			else
			{
				imagePreview.visible = false
				textPreview.visible = false
			}
		}
	}

	menuBar: MenuBar {
		Menu {
			title: qsTr("File")
			MenuItem {
				text: "Close"
				onTriggered:{
					Qt.quit();
				}
			}
		}
		
		Menu {
			title: qsTr("Favorites")
			MenuItem {
				text: "Add folder..."
				onTriggered:{
					usersModel.loadUsers()
					
					addFavoriteWindow.open()
				}
			}
		}
	}

	GridLayout {
		Layout.fillWidth: true
		anchors.fill: parent
		columns: 1

		// path	
		RowLayout {
			Layout.fillWidth: true
			Layout.rightMargin: 10
			Label {
				width: 200
				text: "Folder:"
				padding: 10
			}
			
			TextField {
				id: currentPath
				Layout.fillWidth: true
			}
			
		}

		SplitView {
			Layout.fillHeight: true
			Layout.fillWidth: true			

			// 1 folders
			ScrollView {
				width: parent.width / 4

				ListView {
					id: folders
					model: foldersModel
					width: parent.width
					focus: true
					currentIndex: -1

					delegate: RowLayout {
						id: foldersLayout
						width: folders.width

						Image {
							source: "images/folder.png"
							
							MouseArea {
								anchors.fill: parent
								onClicked: foldersLayout.ListView.view.currentIndex = index
								onDoubleClicked: selectFolder(index)
							}
						}

						Label {
							text: folderName
							width: parent.width

							MouseArea {
								anchors.fill: parent
								onClicked: foldersLayout.ListView.view.currentIndex = index
								onDoubleClicked: selectFolder(index)
							}
						}

						MouseArea {
							Layout.fillWidth: true
							Layout.fillHeight: true
							onClicked: foldersLayout.ListView.view.currentIndex = index
							onDoubleClicked: selectFolder(index)
						}

						function selectFolder(index){
							foldersLayout.ListView.view.currentIndex = index;
							
							foldersModel.selectFolder(index)
						}
					}
					highlight: Rectangle { color: "lightsteelblue" }
				}
			}

			// 2 files
			ScrollView {
				width: parent.width / 4
				ListView {
					id: files
					model: filesModel
					width: parent.width

					focus: true
					currentIndex: -1
					delegate: RowLayout{
						id: filesLayout
						width: files.width

						Label {
							text: fileName
							width: parent.width

							MouseArea {
								anchors.fill: parent
								onClicked: selectFile(index)
							}						
						}

						MouseArea {
							Layout.fillWidth: true
							Layout.fillHeight: true
							onClicked: selectFile(index)
						}

						function selectFile(index){
							filesLayout.ListView.view.currentIndex = index
							
							filesModel.selectFile(index)
						}						
					}
					highlight: Rectangle { color: "lightsteelblue" }
				}
			}

			// 3 preview
			RowLayout {
				Layout.fillWidth: True
				Layout.fillHeight: True

				Layout.leftMargin: 10
				Layout.rightMargin: 10
				Layout.bottomMargin: 10

				Rectangle {
					id: preview
					//Layout.preferredWidth: 150
					//Layout.preferredHeight: 150
					clip: true
					color: "transparent"

					border.color: "black"
					border.width: 1

			        anchors.fill: parent

					Image {
						id: imagePreview
						anchors.fill: parent
						visible: false
						fillMode: Image.PreserveAspectFit
					}

					Text {
						id: textPreview
						visible: false
						anchors.fill: parent
						anchors.margins: 5	
					}
				}
			}
		}	
	}

	AddFavorite {
		id: addFavoriteWindow
		title: qsTr("Add Favorite")
	}
	


}