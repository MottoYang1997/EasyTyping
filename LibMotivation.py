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
    QWizard, QWizardPage, QDockWidget, QWidget,
    QComboBox, QSlider, QCheckBox, QLineEdit, QPlainTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QLabel
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from LibEmoji import emoji_dict, Emoji
import json

# Reference: https://hbr.org/2018/12/how-to-motivate-yourself-to-do-things-you-dont-want-to-do
benefit_list = ["Lower your anxiety.",
                "Benefit someone who you care about.",
                "Lead to financial gain.",
                "Avoid a negative consequence.",
                "Make you feel good about yourself.",
                "Clear your mind.",
                "Align with your values.",
                "Reduce stress."]


class MotivationData:
    __feeling: Emoji
    __benefits: list[str]

    def __init__(self):
        self.__feeling = Emoji()
        self.__benefits = []

    def set_feeling(self, emoji: str):
        self.__feeling.set_emoji(emoji)

    def get_feeling(self):
        return self.__feeling

    def set_benefits(self, benefits: list[str]):
        self.__benefits.clear()
        self.__benefits.extend(benefits)

    def append_benefit(self, benefit: str):
        self.__benefits.append(benefit)

    def get_benefits(self):
        return self.__benefits

    def get_json_str(self):
        dict_data = {"feeling": self.__feeling.get_emoji(), "benefits": self.__benefits}
        return json.dumps(dict_data)

    def from_json_str(self, data: str):
        result = json.loads(data)
        self.set_feeling(result["feeling"])
        self.set_benefits(result["benefits"])


# noinspection PyUnresolvedReferences
class MotivationWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.__data = MotivationData()
        self.setWindowTitle("Find your writing motivation.")
        self.setWindowIcon(QIcon("Resources/yellow_star.jpeg"))
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.addPage(self.__create_feeling_page())
        self.addPage(self.__create_benefit_page())
        self.addPage(self.__create_conclusion_page())

    def __create_feeling_page(self):
        page = QWizardPage()
        page.setTitle("Know your feeling.")
        page.setSubTitle("It's important to know and accept you feelings to deal with the writing task.")

        feeling_group_selection_layout = QVBoxLayout()
        feeling_group_selection_layout.addWidget(QLabel("Please select a group of feeling."))
        self.__feeling_group_combox = QComboBox()
        self.__feeling_group_combox.setMinimumWidth(300)
        for category in emoji_dict:
            self.__feeling_group_combox.addItem(category)
        feeling_group_selection_layout.addWidget(self.__feeling_group_combox)

        select_emoji_layout = QVBoxLayout()
        select_emoji_layout.addWidget(QLabel("Please select how strong you feel."))
        self.__feel_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.__feel_intensity_slider.setMinimum(0)
        self.__feel_intensity_slider.setMaximum(99)
        select_emoji_layout.addWidget(self.__feel_intensity_slider)

        preview_emoji_layout = QHBoxLayout()
        preview_emoji_layout.addWidget(QLabel("Your feeling: "))
        self.__preview_feeling_label = QLabel(self.__data.get_feeling().get_emoji())
        self.__preview_feeling_label.setFont(QFont("Arial", 24))
        preview_emoji_layout.addWidget(self.__preview_feeling_label)

        wrap_layout = QVBoxLayout()
        wrap_layout.addLayout(feeling_group_selection_layout)
        wrap_layout.addLayout(select_emoji_layout)
        wrap_layout.addLayout(preview_emoji_layout)
        page.setLayout(wrap_layout)

        self.__feeling_group_combox.currentIndexChanged.connect(self.__update_feeling_page)
        self.__feeling_group_combox.currentIndexChanged.connect(self.__update_conclusion_page)
        self.__feel_intensity_slider.valueChanged.connect(self.__update_feeling_page)
        self.__feel_intensity_slider.valueChanged.connect(self.__update_conclusion_page)

        return page

    def __update_feeling_page(self):
        feeling_category = self.__feeling_group_combox.currentText()
        intensity = self.__feel_intensity_slider.value()

        n_emoji = len(emoji_dict[feeling_category])
        i_emoji = int(intensity / 100 * (n_emoji - 1) + 0.5)
        selected_emoji = emoji_dict[feeling_category][i_emoji]

        self.__preview_feeling_label.setText(selected_emoji)

    def __create_benefit_page(self):
        page = QWizardPage()
        page.setTitle("Find benefits.")
        page.setSubTitle("After you know your feeling, you can try finding what you can benefit from the task.")

        selection_layout = QVBoxLayout()
        self.__benefit_checkboxes = list(map(lambda benefit: QCheckBox(benefit), benefit_list))
        for checkbox in self.__benefit_checkboxes:
            selection_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.__update_conclusion_page)

        user_entry_layout = QHBoxLayout()
        self.__user_entry_checkbox = QCheckBox()
        self.__user_entry_checkbox.setChecked(False)
        self.__user_entry_line_edit = QLineEdit()
        self.__user_entry_line_edit.setPlaceholderText("Your insight.")
        self.__user_entry_line_edit.setEnabled(False)
        self.__user_entry_line_edit.setMaxLength(256)
        user_entry_layout.addWidget(self.__user_entry_checkbox)
        user_entry_layout.addWidget(self.__user_entry_line_edit)

        wrap_layout = QVBoxLayout()
        wrap_layout.addLayout(selection_layout)
        wrap_layout.addLayout(user_entry_layout)
        page.setLayout(wrap_layout)

        self.__user_entry_checkbox.stateChanged.connect(self.__update_benefit_page)
        self.__user_entry_checkbox.stateChanged.connect(self.__update_conclusion_page)
        self.__user_entry_line_edit.textChanged.connect(self.__update_conclusion_page)

        return page

    def __update_benefit_page(self):
        if self.__user_entry_checkbox.isChecked():
            self.__user_entry_line_edit.setEnabled(True)
        else:
            self.__user_entry_line_edit.setEnabled(False)

    def __create_conclusion_page(self):
        page = QWizardPage()
        page.setTitle("Conclusion")
        page.setSubTitle("Please review your motivation about the writing task.")

        feeling_layout = QHBoxLayout()
        feeling_layout.addWidget(QLabel("My feeling about the task:"))
        self.__conclusion_feeling_label = QLabel(self.__preview_feeling_label.text())
        self.__conclusion_feeling_label.setFont(QFont("Arial", 24))
        feeling_layout.addWidget(self.__conclusion_feeling_label)

        motivation_layout = QVBoxLayout()
        motivation_layout.addWidget(QLabel("You can benefit the followings from the task."))
        motivation_items = []
        for checkbox in self.__benefit_checkboxes:
            if checkbox.isChecked():
                motivation_items.append(checkbox.text())
        if self.__user_entry_checkbox.isChecked():
            motivation_items.append(self.__user_entry_line_edit.text())
        self.__motivation_preview = QPlainTextEdit('\n'.join(motivation_items))
        self.__motivation_preview.setReadOnly(True)
        motivation_layout.addWidget(self.__motivation_preview)

        wrap_layout = QVBoxLayout()
        wrap_layout.addLayout(feeling_layout)
        wrap_layout.addSpacing(5)
        wrap_layout.addLayout(motivation_layout)
        page.setLayout(wrap_layout)

        return page

    def __update_conclusion_page(self):
        self.__conclusion_feeling_label.setText(self.__preview_feeling_label.text())
        motivation_items = []
        for checkbox in self.__benefit_checkboxes:
            if checkbox.isChecked():
                motivation_items.append(checkbox.text())
        if self.__user_entry_checkbox.isChecked():
            motivation_items.append(self.__user_entry_line_edit.text())
        self.__motivation_preview.clear()
        self.__motivation_preview.appendPlainText('\n'.join(motivation_items))
        self.__update_data()

    def __update_data(self):
        self.__data.set_feeling(self.__preview_feeling_label.text())
        motivation_list = []
        for checkbox in self.__benefit_checkboxes:
            if checkbox.isChecked():
                motivation_list.append(checkbox.text())
        if self.__user_entry_checkbox.isChecked():
            motivation_list.append(self.__user_entry_line_edit.text())
        self.__data.set_benefits(motivation_list)

    def get_data(self):
        return self.__data


# noinspection PyUnresolvedReferences
class MotivationWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Motivation")
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea |
                             Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.BottomDockWidgetArea)

        self.__data = MotivationData()

        feeling_layout = QHBoxLayout()
        feeling_layout.addWidget(QLabel("My feeling about the task:"))
        self.__conclusion_feeling_label = QLabel(self.__data.get_feeling().get_emoji())
        self.__conclusion_feeling_label.setFont(QFont("Arial", 24))
        feeling_layout.addWidget(self.__conclusion_feeling_label)

        motivation_layout = QVBoxLayout()
        motivation_layout.addWidget(QLabel("You can benefit the followings from the task."))
        self.__motivation_preview = QPlainTextEdit('\n'.join(self.__data.get_benefits()))
        self.__motivation_preview.setReadOnly(True)
        motivation_layout.addWidget(self.__motivation_preview)

        self.__edit_motivation_btn = QPushButton("Edit Motivation")
        self.__edit_motivation_btn.clicked.connect(self.__edit_motivation_wizard)

        wrap_layout = QVBoxLayout()
        wrap_layout.addLayout(feeling_layout)
        wrap_layout.addSpacing(5)
        wrap_layout.addLayout(motivation_layout)
        wrap_layout.addWidget(self.__edit_motivation_btn)
        wrap_widget = QWidget()
        wrap_widget.setLayout(wrap_layout)
        self.setWidget(wrap_widget)

        self.wizard = MotivationWizard()

    def __edit_motivation_wizard(self):
        self.wizard.restart()
        self.wizard.exec()
        self.load_data(self.wizard.get_data())

    def load_data(self, data: MotivationData):
        self.__data = data
        self.__conclusion_feeling_label.setText(self.__data.get_feeling().get_emoji())
        self.__motivation_preview.clear()
        self.__motivation_preview.appendPlainText('\n'.join(self.__data.get_benefits()))

    def get_data(self):
        return self.__data

    def toggle_show_hide(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit

    motivation = MotivationData()
    motivation.set_feeling("🤤")
    motivation.append_benefit("Become Happier.")
    motivation.append_benefit("Reduce stress.")
    motivation.from_json_str(motivation.get_json_str())
    print(motivation.get_json_str())
    print(motivation.get_feeling().get_emoji())

    app = QApplication([])
    w = QMainWindow()
    w.setWindowTitle("Motivation Demo")
    w.setCentralWidget(QTextEdit())
    motivation_widget = MotivationWidget()
    w.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,
                    motivation_widget)
    w.show()
    sys.exit(app.exec())
