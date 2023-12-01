"""
EasyTyping - a simplified notepad software
Copyright (C) 2023 Yiming Yang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from LibMainEdit import MainEdit
from LibThesaurus import ThesaurusDictWidget
from LibFind import FindDialog
from LibReplace import FindReplaceDialog
from LibMotivation import MotivationWidget

import mistletoe




# In case the python scripts are 'forzen', i.e. archived by pyinstaller and other similar tools
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to be the right app path
os.chdir(application_path)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_name = "untitled.md"
        self.is_file_touched = False
        self.setMinimumSize(1024, 768)

        self.setWindowTitle(self.file_name + " - Easy Typing")
        self.setWindowIcon(QtGui.QIcon("assets/icons/edit.svg"))

        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusBar().addWidget(self.status_label,
                                   True)
        # Smaller sized bars and fonts
        self.statusBar().setStyleSheet(
            """
                QStatusBar {
                    border: 1px solid lightgray;
                    font-size: 12px;
                }

                QStatusBar > QLabel {
                    font-size: 12px;
                }
            """
        )

        # Prevent menus on widgets and toolbars
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        self.__create_toolbar()
        self.__create_dock_widgets()

        self.main_edit = MainEdit()
        self.webview = QWebEngineView()
        self.main_edit.edit.textChanged.connect(self.render_markdown)
        #self.webview.setUrl(QUrl("https://example.com"))

        self.webview.setHtml("Please start writing...")

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        splitter = QtWidgets.QSplitter(central_widget)
        splitter.addWidget(self.main_edit)
        splitter.addWidget(self.webview)

        #splitter.setOrientation(0)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.addWidget(splitter)

        self.__init_search_find_dialogs()

        self.__link_toolbar_slots()
        self.__link_shortcuts()

        self.status_timer = QtCore.QTimer(self)
        self.status_timer.start(250)

        self.main_edit.edit.textChanged.connect(self.__touched_file)
        self.status_timer.timeout.connect(self.update_status_bar)
    
    def render_markdown(self):
        markdown_text = self.main_edit.edit.toPlainText()
        html_content = mistletoe.markdown(markdown_text)
        self.webview.setHtml(html_content)
    # Smaller icons , more space for text labels
    def __create_toolbar(self, icon_size=24):
        def add_toolbar_actions(texts: list[str],
                                icon_filenames: list[str]):
            path = "assets/icons/"
            filetype = ".svg"
            for i in range(len(texts)):
                if texts[i] == '|':
                    self.toolbar.addSeparator()
                    continue
                icon_path = path + icon_filenames[i] + filetype
                icon = QtGui.QIcon(icon_path)
                self.toolbar.addAction(icon, texts[i])

        self.toolbar = QtWidgets.QToolBar("Toolbar", self)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QtCore.QSize(icon_size, icon_size))
        # Add text labels to buttons, since the default icons are not very intuitive
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolbar.visibilityChanged.connect(self.toolbar.show)

        # Doc: New, Save, Save As
        toolbar_txt = ["New", "Open", "Save", "Save As"]
        toolbar_icon_path = ["file", "internal", "download", "download.modified"]
        add_toolbar_actions(toolbar_txt, toolbar_icon_path)

        self.toolbar.addSeparator()
        # Text: Cut, Copy, Paste, Find, Replace
        toolbar_txt = ["Cut", "Copy", "Paste", '|', "Find", "Replace"]
        toolbar_icon_path = ["cut", "copy", "paste", '|', "search", "replace"]
        add_toolbar_actions(toolbar_txt, toolbar_icon_path)

        # DockWidget: Thesaurus, Motivation
        self.toolbar.addSeparator()
        add_toolbar_actions(["Thesaurus", "|", "Motivation"],
                            ["thesaurus", "|", "heart"])

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea,
                        self.toolbar)

    def __touched_file(self):
        self.is_file_touched = True
        self.setWindowTitle('*' + os.path.basename(self.file_name) + " - Easy Typing")

    def __untouched_file(self):
        self.is_file_touched = False
        self.setWindowTitle(os.path.basename(self.file_name) + " - Easy Typing")

    def __create_dock_widgets(self):
        self.widget_thesaurus = ThesaurusDictWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.widget_thesaurus)
        self.widget_thesaurus.hide()

        self.widget_motivation = MotivationWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,
                           self.widget_motivation)
        self.widget_motivation.hide()

        # may need some changes to show the WebView

        self.setStyleSheet(
            """
            QDockWidget > QWidget{
                border: 1px solid lightgray;
            }
            """
        )

    def __init_search_find_dialogs(self):
        self.find_dialog = FindDialog(self.main_edit.edit, self)
        self.find_dialog.hide()
        self.replace_dialog = FindReplaceDialog(self.main_edit.edit, self)
        self.replace_dialog.hide()

    def __link_shortcuts(self):
        shortcut_dict = {
            "New": "Ctrl+n",
            "Open": "Ctrl+o",
            "Save": "Ctrl+s",
            "Save As": "Ctrl+Shift+s",
            "Find": "Ctrl+f",
            "Replace": "Ctrl+r",
            "Thesaurus": "Ctrl+t",
            "Motivation": "Ctrl+m"
        }
        for action in self.toolbar.actions():
            key_seq_str = shortcut_dict.get(action.text())
            if key_seq_str is None:
                continue
            action.setShortcut(QtGui.QKeySequence(key_seq_str))

    def __link_toolbar_slots(self):
        slot_dict = {
            "New": self.new_file,
            "Open": self.open_file,
            "Save": self.save_file,
            "Save As": self.save_as_file,
            "Cut": self.main_edit.edit.cut,
            "Copy": self.main_edit.edit.copy,
            "Paste": self.main_edit.edit.paste,
            "Find": self.find_dialog.toggle_visibility,
            "Replace": self.replace_dialog.toggle_visibility,
            "Thesaurus": self.widget_thesaurus.toggle_show_hide,
            "Motivation": self.widget_motivation.toggle_show_hide,
        }

        for action in self.toolbar.actions():
            slot = slot_dict.get(action.text())
            if slot is None:
                continue
            action.triggered.connect(slot)

    def new_file(self):
        if len(self.main_edit.edit.toPlainText()) == 0:
            QtWidgets.QMessageBox.information(self, " ", "No change required.")
            return
        if QtWidgets.QMessageBox.question(self, " ", "Discard changes?",
                                          QtWidgets.QMessageBox.StandardButton.Yes |
                                          QtWidgets.QMessageBox.StandardButton.No) == \
                QtWidgets.QMessageBox.StandardButton.No:
            return
        self.file_name = "untitled.md"
        self.main_edit.edit.clear()
        self.__untouched_file()
        self.main_edit.current_state = self.main_edit.idle_state

    def open_file(self):
        if self.is_file_touched > 0 and \
                QtWidgets.QMessageBox.question(self, " ", "Discard changes?",
                                               QtWidgets.QMessageBox.StandardButton.Yes |
                                               QtWidgets.QMessageBox.StandardButton.No) == \
                QtWidgets.QMessageBox.StandardButton.No:
            return

        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open",
                                                         os.path.join(os.path.join(os.environ['USERPROFILE']),
                                                                      'Desktop'),
                                                         "(*.md *.txt);;Markdown (*.md);;Plain Text (*.txt)")[0]
        if filename == "":
            return

        self.file_name = filename
        self.setWindowTitle(os.path.basename(filename)+" - Easy Typing")
        with open(filename, "r") as f:
            self.main_edit.edit.clear()
            self.main_edit.edit.appendPlainText("".join(f.readlines()))
        self.main_edit.current_state = self.main_edit.idle_state
        self.__untouched_file()

    def save_file(self):
        if self.file_name == "untitled.md":
            self.save_as_file()
            return
        with open(self.file_name, "w") as f:
            f.write(self.main_edit.edit.toPlainText())
        self.__untouched_file()
        self.main_edit.current_state = self.main_edit.idle_state

    def save_as_file(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save As",
                                                         os.path.join(os.path.join(os.environ['USERPROFILE']),
                                                                      'Desktop'),
                                                         "(*.md *.txt);;Markdown (*.md);;Plain Text (*.txt)")[0]
        if filename == "":
            return
        self.file_name = filename
        with open(self.file_name, "w") as f:
            f.write(self.main_edit.edit.toPlainText())
        self.__untouched_file()
        self.main_edit.current_state = self.main_edit.idle_state

    def update_status_bar(self):
        if self.main_edit.current_state == self.main_edit.idle_state:
            self.status_label.setText("Idling. Please start writing.")
        elif self.main_edit.current_state == self.main_edit.typing_state:
            self.status_label.setText(f"Typing. Word Count: {self.main_edit.count_words()}.")
        elif self.main_edit.current_state == self.main_edit.warning_state:
            self.status_label.setText("Please continue typing before timing out.")
        elif self.main_edit.current_state == self.main_edit.failed_state:
            self.status_label.setText(f"Please restart. Word Count: {self.main_edit.count_words()}.")
        elif self.main_edit.current_state == self.main_edit.succeeded_state:
            self.status_label.setText("Congratulations! You have made progress. "
                                      f"Word Count: {self.main_edit.count_words()}.")
        else:
            pass


app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()
