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

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt


class MyTextViewNoZoom(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, e):
        # Filter out Ctrl+Scroll zoom events
        if e.modifiers() != Qt.KeyboardModifier.ControlModifier:
            super().wheelEvent(e)


class PreviewWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Preview")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea |
                             Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setMinimumSize(480, 600)

        self.preview = MyTextViewNoZoom()
        self.preview.setReadOnly(True)
        self.__preview_doc = QtGui.QTextDocument()

        with open("assets/styles/markdown.css") as file:
            style_str = "".join(file.readlines())
        self.__preview_doc.setDefaultFont(QtGui.QFont("Arial", 15))
        option = QtGui.QTextOption()
        option.setFlags(QtGui.QTextOption.Flag.AddSpaceForLineAndParagraphSeparators)
        self.__preview_doc.setDefaultTextOption(option)
        self.__preview_doc.setDefaultStyleSheet(style_str)

        self.setWidget(self.preview)

        self.update_preview("")


    def update_preview(self, markdown_txt: str):
        self.__preview_doc.setMarkdown(markdown_txt)
        self.__preview_doc.setHtml(self.__preview_doc.toHtml())
        self.preview.setDocument(self.__preview_doc)

    def toggle_show_hide(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
