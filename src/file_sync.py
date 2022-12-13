#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List
from fs_core import FileSync
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QTreeView, QToolBar, QWidget, QMenuBar, QFileDialog, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.fs = FileSync()
        self.refreshOrigins()

        # Window params
        self.setWindowTitle("File Sync")

    def initUI(self):
        """
        QToolBar,
        QVBoxLayout {
            QHBoxLayout {
                QTreeView,
                QTreeView
            }
        }
        """

        # Add toolbar
        self.toolbar = QToolBar("toolbar")
        self.addToolBar(self.toolbar)

        # add toolButton
        self.add_tool_origin_btn = QAction()
        self.add_tool_origin_btn.setText(self.tr("&Add"))
        self.add_tool_origin_btn.triggered.connect(self.onAddToolAction)

        # sync toolButton
        self.sync_action = QAction()
        self.sync_action.setText(self.tr("&Sync"))
        self.sync_action.triggered.connect(self.onSyncAction)
        self.toolbar.addAction(self.sync_action)

        # sync toolButton
        self.sync_all_action = QAction()
        self.sync_all_action.setText(self.tr("Sync all"))
        self.sync_all_action.triggered.connect(self.onSyncAllAction)
        self.toolbar.addAction(self.sync_all_action)

        # delete toolButton
        self.delete_action = QAction()
        self.delete_action.setText(self.tr("&Delete"))
        self.delete_action.triggered.connect(self.onDeleteAction)
        self.toolbar.addAction(self.delete_action)

        # Add menu bar
        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu(self.tr("&File"))
        # load sync list action
        self.load_sync_list_action = QAction(self.tr("&Load sync list.."))
        self.load_sync_list_action.triggered.connect(self.onLoadSyncListAction)
        self.file_menu.addAction(self.load_sync_list_action)

        self.file_menu.addSeparator()
        self.file_menu.addAction(self.tr("&Exit"))

        self.action_menu = self.menu_bar.addMenu(self.tr("&Action"))
        self.action_menu.addAction(self.add_tool_origin_btn)
        self.action_menu.addAction(self.sync_action)
        self.action_menu.addAction(self.sync_all_action)
        self.action_menu.addAction(self.delete_action)

        # About help_menu
        self.about_file_sync = QAction()
        self.about_file_sync.setText(self.tr("About &File Sync"))
        self.about_file_sync.triggered.connect(self.onAboutFileSyncAction)

        # About Qt
        self.about_qt = QAction()
        self.about_qt.setText(self.tr("About &Qt"))
        # self.about_qt.triggered.connect()

        self.help_menu = self.menu_bar.addMenu(self.tr("&Help"))
        self.help_menu.addAction(self.about_file_sync)
        self.help_menu.addAction(self.about_qt)

        self.setMenuBar(self.menu_bar)

        # Add add toolbar
        self.toolbar_add = QToolBar("add")
        self.addToolBar(self.toolbar_add)

        self.toolbar_add.addAction(self.add_tool_origin_btn)

        # add origin browse action
        self.add_tool_origin_action = QAction("brows")
        self.add_tool_origin_action.triggered.connect(self.onBrowseOriginAction)
        self.toolbar_add.addAction(self.add_tool_origin_action)

        # add origin path comboBox
        self.add_tool_origin_combobox = QComboBox()
        self.toolbar_add.addWidget(self.add_tool_origin_combobox)

        # add copy browse action
        self.add_tool_copy_action = QAction("brows")
        self.add_tool_copy_action.triggered.connect(self.onBrowseCopyAction)
        self.toolbar_add.addAction(self.add_tool_copy_action)

        # add copy path lineEdit
        self.add_tool_copy_lineedit = QLineEdit()
        self.toolbar_add.addWidget(self.add_tool_copy_lineedit)

        # Layouts setup
        self.widget = QWidget(self)
        self.main_layout = QVBoxLayout()
        self.tree_view_layout = QHBoxLayout()

        # Add tree view for origins
        self.origins_model = QStandardItemModel(0, 3)
        self.origins_model.setHorizontalHeaderLabels(
            ["Name", "Path", "state"]
        )
        self.tree_view_origins = QTreeView()
        self.tree_view_origins.clicked.connect(self.onOriginTreeViewSelect)
        self.tree_view_origins.setModel(self.origins_model)

        # Add tree view for copies
        self.copies_model = QStandardItemModel(0, 3)
        self.copies_model.setHorizontalHeaderLabels(
            ["Name", "Path", "state"]
        )
        self.tree_view_copies = QTreeView()
        self.tree_view_copies.setModel(self.copies_model)

        self.tree_view_layout.addWidget(self.tree_view_origins)
        self.tree_view_layout.addWidget(self.tree_view_copies)

        self.main_layout.addLayout(self.tree_view_layout)
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def refreshOrigins(self):
        self.origins_model.clear()
        self.origins_model.setHorizontalHeaderLabels(
            ["Name", "Path"]
        )
        self.add_tool_origin_combobox.clear()
        for origin in self.fs.get_origins():
            print(f"display origin {origin}")
            origin_str: str = str(origin.parts[-1])
            # add to treeView
            items = [
                QStandardItem(origin_str),
                QStandardItem(str(origin.resolve()))
            ]
            self.origins_model.appendRow(items)
            # add to comboBox
            self.add_tool_origin_combobox.addItem(str(origin))

    def refreshCopies(self):
        self.copies_model.clear()
        self.copies_model.setHorizontalHeaderLabels(
            ["Name", "Path", "status"]
        )
        if self.tree_view_origins.model().rowCount() != 0:
            origin: Path = Path(self.tree_view_origins.selectedIndexes()[0].data())
            for copy in self.fs.get_copies(origin):
                print(f"display copy {copy}")
                copy_str: str = str(copy.parts[-1])
                # add to treeView
                items = [
                    QStandardItem(copy_str),
                    QStandardItem(str(copy.resolve())),
                    QStandardItem(self.fs.get_copy_status(origin, copy))
                ]
                self.copies_model.appendRow(items)

    def onAddToolAction(self):
        copy: Path = Path(self.add_tool_copy_lineedit.text()).absolute()
        origin: Path = Path(self.add_tool_origin_combobox.currentText())
        print(f"copy path: {copy}")
        if (not copy.is_dir() and not origin.is_dir()):
            print(f"add origin: {origin}, copy: {copy}")
            self.fs.add(origin, [copy])
        else:
            QMessageBox.warning(self, "Wrong path", "Copy path can not be a dir")

        self.refreshOrigins()

    def onBrowseOriginAction(self):
        origin: str
        origin, type = QFileDialog().getOpenFileName(self, caption="Add origin")
        print(f"browse add origin path: {origin}")
        if origin != "":
            self.fs.add_origin(Path(origin))
            self.refreshOrigins()

    def onBrowseCopyAction(self):
        origin: str
        origin, type = QFileDialog().getSaveFileName(self, caption="Add copy")
        print(f"browse add copy path: {origin}")
        self.add_tool_copy_lineedit.setText(origin)

    def onOriginTreeViewSelect(self):
        # Set origin comboBox
        if self.tree_view_origins.selectedIndexes() != []:
            print(f"selected origin {self.origins_model.index(self.tree_view_origins.selectedIndexes()[0].row(),1).data()}")
            # self.add_tool_origin_combobox.setCurrentIndex(self.tree_view_origins.selectedIndexes()[0].row())
        else:
            # QMessageBox.about(self, "text", "text")
            pass

        self.refreshCopies()

    def onSyncAction(self):
        for origin in [Path(self.tree_view_origins.model().index(origin.row(), 1).data()) for origin in self.tree_view_origins.selectedIndexes()]:
            print(f"sync origin: {origin}")
            # TODO: move to thread
            self.fs.sync(Path(origin))

        self.refreshCopies()

    def onSyncAllAction(self):
        self.fs.sync_all()
        print("sync all")
        self.refreshCopies()

    def onDeleteAction(self):
        print("delete")
        origin_indexes: List[QModelIndex]= self.tree_view_origins.selectedIndexes()
        if (len(origin_indexes) != 0):
            origin: Path = Path(self.tree_view_origins.model().index(origin_indexes[0].row(), 1).data())
            print("origin", origin)

            copy_selected = self.tree_view_copies.selectedIndexes()
            if (len(copy_selected) != 0):
                print("len(copy_selected)", len(copy_selected))
                print("copy_selected", copy_selected)
                copies: List[Path] = []
                for copy in copy_selected:
                    print(self.tree_view_copies.model().index(copy.row(), 1).data())
                    copies.append(Path(self.tree_view_copies.model().index(copy.row(), 1).data()))

                print("copies", copies)
                self.fs.delete(origin, copies)
                self.refreshCopies()

            else:
                # Ask confirm
                copies_all: List[Path] = [Path(self.tree_view_copies.model().index(i, 1).data()) for i in range(self.tree_view_copies.model().rowCount())]
                if len(copies_all) != 0:
                    copies_str: str = ""
                    for copy in copies_all:
                        copies_str = f"{copies_str}\n{str(copy)}"

                    msg_box = QMessageBox.question(self,
                                                   "Delete all copies",
                                                   f"Delete copies from sync list:\n{copies_str}",
                                                   QMessageBox.StandardButton.Yes,
                                                   QMessageBox.StandardButton.Cancel)
                    if msg_box == QMessageBox.StandardButton.Yes.value:
                        print("ok")
                        self.fs.delete(origin)
                        self.refreshOrigins()
                        self.refreshCopies()
                    if msg_box == QMessageBox.StandardButton.Cancel.value:
                        print("cancel")

                else:
                    self.fs.delete(origin)
                    self.refreshOrigins()
                    self.refreshCopies()


    def onLoadSyncListAction(self):
        fname = QFileDialog.getOpenFileName(self, 'Open sync list', 
         '',"JSON files (*.json)")
        print(f"set {fname[0]} as sync list")
        if fname != '':
            self.fs.set_synclist(Path(fname[0]))

        self.refreshOrigins()

    def onAboutFileSyncAction(self):
        QMessageBox.about(self, "About FileSync", "FileSync is an app to sync files in different folders or different drives\nSources: https://github.com/MM-empire/FileSync")

    # def onAboutFileSyncAction(self):
    #     QMessageBox.about(self, "About FileSync", "FileSync is an app to sync files in different folders or different drives\nSources: https://github.com/MM-empire/FileSync")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
