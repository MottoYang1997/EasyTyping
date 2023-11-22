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

from PyQt6.QtWidgets import (
    QWidget, QDockWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPlainTextEdit, QPushButton, QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal
import requests
my_api_key = "your_api_key_here"


class ThesaurusDictWorker(QObject):
    got_response = pyqtSignal(requests.Response)
    finished = pyqtSignal()
    __inquire_token: str

    def set_token(self, token: str):
        self.__inquire_token = token

    def run(self):
        api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'\
            .format(self.__inquire_token)
        response = requests.get(api_url, headers={'X-Api-Key': f'{my_api_key}'})
        self.got_response.emit(response)
        self.finished.emit()


class ThesaurusDictWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thesaurus")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea |
                             Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setMinimumWidth(200)

        entry_layout = QHBoxLayout()
        self.__entry_widget = QLineEdit()
        self.__entry_widget.setPlaceholderText("Your word here...")
        entry_layout.addWidget(self.__entry_widget)

        self.__inquiry_btn = QPushButton("Inquire")
        entry_layout.addWidget(self.__inquiry_btn)

        synonyms_layout = QVBoxLayout()
        synonyms_layout.addWidget(QLabel("Synonyms"))
        self.__synonyms_result = QPlainTextEdit("")
        self.__synonyms_result.setReadOnly(True)
        synonyms_layout.addWidget(self.__synonyms_result)

        antonyms_layout = QVBoxLayout()
        antonyms_layout.addWidget(QLabel("Antonyms"))
        self.__antonyms_result = QPlainTextEdit("")
        self.__antonyms_result.setReadOnly(True)
        antonyms_layout.addWidget(self.__antonyms_result)

        wrap_layout = QVBoxLayout()
        wrap_layout.addLayout(entry_layout)
        wrap_layout.addLayout(synonyms_layout)
        wrap_layout.addLayout(antonyms_layout)
        wrap_widget = QWidget()
        wrap_widget.setLayout(wrap_layout)
        self.setWidget(wrap_widget)

        self.__inquiry_btn.clicked.connect(self.__inquiry_handler)
        self.__entry_widget.returnPressed.connect(self.__inquiry_handler)

        # Create thread: QThread, worker: QObject
        self.__async_thread = QThread()
        self.__async_worker = ThesaurusDictWorker()

    def __inquiry_handler(self):
        token = self.__entry_widget.text()
        if len(token) == 0:
            QMessageBox.warning(self, "Error",
                                f"Error: No input.")
            return None
        self.inquire_async(token)

    def inquire_async(self, token: str):
        if self.__async_thread.isRunning():
            QMessageBox.warning(self, "Info",
                                "The thesaurus is busy.\n"
                                "Please try again later.")
            return

        # Disable/Disconnect Related UI
        self.__entry_widget.setEnabled(False)
        self.__inquiry_btn.setEnabled(False)

        # Load worker into thread
        self.__async_worker.moveToThread(self.__async_thread)

        # Assign input parameters
        self.__async_worker.set_token(token)

        # Connect thread.started -> worker.run
        self.__async_thread.started.connect(self.__async_worker.run)

        # Connect Worker.got_response -> self.async_stop with response: Response
        self.__async_worker.got_response.connect(self.__inquire_async_receive_response)

        # Connect worker.finish -> thread.quit
        self.__async_worker.finished.connect(self.__async_thread.quit)

        # Start Async Thread
        self.__async_thread.start()

    def __inquire_async_receive_response(self, response: requests.Response):
        self.__process_response(response)
        self.__entry_widget.setEnabled(True)
        self.__inquiry_btn.setEnabled(True)

    def __process_response(self, response: requests.Response):
        if response.status_code != requests.codes.ok:
            QMessageBox.warning(self, "Error",
                                f"Error {response.status_code}: {response.text}")
            return None
        result = response.json()

        def build_str_from_list(str_list: list[str]):
            result_str = ""
            for i, str_token in enumerate(str_list):
                if len(str_token) == 0:
                    continue
                elif i < len(str_list) - 1:
                    result_str += str_token + ', '
                else:
                    result_str += str_token
            if len(result_str) == 0:
                result_str = "No Results"
            return result_str

        self.__synonyms_result.clear()
        self.__synonyms_result.appendPlainText(build_str_from_list(result["synonyms"]))

        self.__antonyms_result.clear()
        self.__antonyms_result.appendPlainText(build_str_from_list(result["antonyms"]))

        return result

    def inquire_blocking(self, token: str):
        self.__entry_widget.setEnabled(False)
        self.__inquiry_btn.setEnabled(False)

        api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(token)
        response = requests.get(api_url, headers={'X-Api-Key': f'{my_api_key}'})
        self.__process_response(response)

        self.__entry_widget.setEnabled(True)
        self.__inquiry_btn.setEnabled(True)

    def toggle_show_hide(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QTextEdit)
    from PyQt6.QtCore import Qt

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("Dictionary Demo")

    main_window.setCentralWidget(QTextEdit())

    thesaurus_dict = ThesaurusDictWidget()
    main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                              thesaurus_dict)

    main_window.show()
    sys.exit(app.exec())
