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

from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
import re


class WriteProgressBar(QtWidgets.QWidget):
    height = 8
    progress = 0.0
    bar_color = "black"

    def __init__(self):
        super().__init__()
        self.setFixedHeight(self.height)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )
        self.setContentsMargins(0, 0, 0, 0)

    def sizeHint(self):
        return QtCore.QSize(self.width(), self.height)

    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()

        brush.setColor(QtGui.QColor("white"))
        brush.setStyle(Qt.BrushStyle.SolidPattern)

        background_rect = a0.rect()
        painter.fillRect(background_rect, brush)

        (bar_x0, bar_y0, _, _) = background_rect.getRect()
        bar_width = int(background_rect.width() *
                        self.progress)
        bar_rect = QtCore.QRect(bar_x0, bar_y0,
                                bar_width, self.height)

        brush.setColor(QtGui.QColor(self.bar_color))
        painter.fillRect(bar_rect, brush)

        painter.end()


class MyPlainTextEdit(QtWidgets.QPlainTextEdit):
    focus_lost = QtCore.pyqtSignal()
    focus_got = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

    def focusOutEvent(self, e: QtGui.QFocusEvent | None) -> None:
        self.focus_lost.emit()
        return super().focusOutEvent(e)

    def focusInEvent(self, e: QtGui.QFocusEvent | None) -> None:
        self.focus_got.emit()
        return super().focusInEvent(e)


class MainEdit(QtWidgets.QWidget):
    max_row_characters = 45
    font = QtGui.QFont("Arial", 18)
    n_goal_words = 150
    n_fail_seconds = 5
    n_warning_seconds = 2

    succeeded = QtCore.pyqtSignal()
    failed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.bar = WriteProgressBar()
        self.edit = MyPlainTextEdit()
        self.edit.setFont(self.font)
        edit_width = int(self.max_row_characters *
                         self.edit.font().pointSize() * 0.74 + 0.5)
        self.edit.setMinimumWidth(edit_width)

        layout = QtWidgets.QVBoxLayout()
        l, _, r, _ = layout.getContentsMargins()
        layout.setContentsMargins(l, 0, r, 0)
        layout.setSpacing(0)
        layout.addWidget(self.bar)
        layout.addWidget(self.edit)
        layout.setAlignment(self.edit,
                            Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

        self.__init_state_machine()

        self.timer = QtCore.QTimer()
        self.timer_tick_interval_s = 0.1
        self.timer.setInterval(int(self.timer_tick_interval_s *
                                   1000))
        self.idle_seconds = 0.0

        self.connect_slots()

    def __init_state_machine(self):
        self.idle_state = EditorIdleState()
        self.typing_state = EditorTypingState()
        self.warning_state = EditorWarningState()
        self.failed_state = EditorFailedState()
        self.succeeded_state = EditorSucceededState()

        self.current_state = self.idle_state

    def connect_slots(self):
        self.edit.textChanged.connect(self.__editor_typed)
        self.edit.focus_lost.connect(self.__pause_timer)
        self.edit.focus_got.connect(self.__resume_timer)
        self.timer.timeout.connect(self.__timer_tick)

    def disconnect_slots(self):
        self.edit.textChanged.disconnect(self.__editor_typed)
        self.timer.timeout.disconnect(self.__timer_tick)

    def count_words(self):
        text = self.edit.toPlainText()
        length = len(re.findall(r'[A-z|0-9]+|[\u4e00-\u9fa5]', text))
        return length

    def update_progress_bar(self):
        self.bar.progress = self.count_words() / self.n_goal_words
        self.bar.update()

    def set_editor_whiteness(self, b: int):
        self.edit.setStyleSheet(
            f"""
                QPlainTextEdit {{
                    color: rgb({b}, {b}, {b});
                }}
            """
        )

    def __editor_typed(self):
        self.current_state.text_changed(self)

    def __timer_tick(self):
        self.current_state.timer_ticked(self)
    
    def __pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
    
    def __resume_timer(self):
        if not self.timer.isActive():
            self.timer.start()


class EditorAbstractState:
    def __init__(self):
        ...

    def text_changed(self, main_edit: MainEdit):
        ...

    def timer_ticked(self, main_edit: MainEdit):
        ...


class EditorIdleState(EditorAbstractState):
    def text_changed(self, main_edit: MainEdit):
        main_edit.idle_seconds = 0.0
        main_edit.timer.start()
        main_edit.bar.bar_color = "black"
        main_edit.update_progress_bar()
        main_edit.current_state = main_edit.typing_state


class EditorTypingState(EditorAbstractState):
    def text_changed(self, main_edit: MainEdit):
        main_edit.idle_seconds = 0.0
        main_edit.set_editor_whiteness(0)
        main_edit.update_progress_bar()
        if main_edit.count_words() == 0:
            main_edit.timer.stop()
            main_edit.current_state = main_edit.idle_state
        if main_edit.bar.progress >= 1.0:
            main_edit.timer.stop()
            main_edit.bar.bar_color = "Green"
            main_edit.bar.update()
            main_edit.current_state = main_edit.succeeded_state

    def timer_ticked(self, main_edit: MainEdit):
        main_edit.idle_seconds += main_edit.timer_tick_interval_s
        if main_edit.idle_seconds > main_edit.n_warning_seconds:
            main_edit.current_state = main_edit.warning_state


class EditorWarningState(EditorAbstractState):
    def text_changed(self, main_edit: MainEdit):
        main_edit.disconnect_slots()
        main_edit.idle_seconds = 0.0
        main_edit.set_editor_whiteness(0)
        main_edit.current_state = main_edit.typing_state
        main_edit.connect_slots()

    def timer_ticked(self, main_edit: MainEdit):
        main_edit.idle_seconds += main_edit.timer_tick_interval_s
        whiteness = int((main_edit.idle_seconds - main_edit.n_warning_seconds) /
                        (main_edit.n_fail_seconds - main_edit.n_warning_seconds) *
                        255)
        main_edit.set_editor_whiteness(whiteness)
        if main_edit.idle_seconds > main_edit.n_fail_seconds:
            main_edit.disconnect_slots()
            main_edit.timer.stop()
            main_edit.set_editor_whiteness(0)
            main_edit.edit.selectAll()
            main_edit.edit.cut()
            main_edit.edit.appendPlainText("Sorry, you haven't typed for a while by now.\n"
                                           "The written texts are saved into clipboard.\n"
                                           "You can type anything to restart the challenge.")
            main_edit.current_state = main_edit.failed_state
            main_edit.connect_slots()


class EditorFailedState(EditorAbstractState):
    def text_changed(self, main_edit: MainEdit):
        main_edit.disconnect_slots()
        main_edit.edit.clear()
        main_edit.bar.progress = 0.0
        main_edit.bar.update()
        main_edit.current_state = main_edit.idle_state
        main_edit.connect_slots()


class EditorSucceededState(EditorAbstractState):
    def text_changed(self, main_edit: MainEdit):
        if main_edit.count_words() == 0:
            main_edit.disconnect_slots()
            main_edit.bar.bar_color = "black"
            main_edit.update_progress_bar()
            main_edit.current_state = main_edit.idle_state
            main_edit.connect_slots()
