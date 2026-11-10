# -*- coding: utf-8 -*-
"""PR8: QAbstractButton / QButtonGroup demo."""
from __future__ import annotations
import sys
from dataclasses import dataclass
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QRadioButton, QCheckBox, QComboBox,
    QListWidget, QTreeWidget, QTreeWidgetItem, QTabWidget, QGroupBox, QButtonGroup,
    QStatusBar, QToolBar, QMessageBox, QFrame, QSplitter, QAbstractButton,
)

S_TITLE = "EM Client - \u043f\u0440\u043e\u0435\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 UI"
S_SAVE = "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c"
S_FILE = "\u0424\u0430\u0439\u043b"
S_HELP = "\u0421\u043f\u0440\u0430\u0432\u043a\u0430"
S_NEW = "\u041d\u043e\u0432\u0430\u044f \u0437\u0430\u043f\u0438\u0441\u044c"
S_EXIT = "\u0412\u044b\u0445\u043e\u0434"
S_ABOUT = "\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435"
S_CLEAR = "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c"
S_ABOUT_BTN = "\u041e \u043a\u043d\u043e\u043f\u043a\u0430\u0445"
S_ACTIONS = "\u041e\u0441\u043d\u043e\u0432\u043d\u044b\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f"
S_ACTIVE = "\u0410\u043a\u0442\u0438\u0432\u0435\u043d"
S_VACATION = "\u0412 \u043e\u0442\u043f\u0443\u0441\u043a\u0435"
S_FIRED = "\u0423\u0432\u043e\u043b\u0435\u043d"
S_VIEW = "\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440"
S_EDIT = "\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435"
S_QUERY = "\u0417\u0430\u043f\u0440\u043e\u0441"
S_DEPT1 = "\u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
S_DEPT2 = "\u041c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433"
S_DEPT3 = "\u041f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430"
S_DEPT4 = "\u0424\u0438\u043d\u0430\u043d\u0441\u044b"
S_E1N = "\u0418\u0432\u0430\u043d\u043e\u0432\u0430 \u041c\u0430\u0440\u0438\u044f"
S_E1R = "\u0410\u043d\u0430\u043b\u0438\u0442\u0438\u043a"
S_E2N = "\u041f\u0435\u0442\u0440\u043e\u0432 \u0410\u043b\u0435\u043a\u0441\u0435\u0439"
S_E2R = "\u0418\u043d\u0436\u0435\u043d\u0435\u0440"
S_E3N = "\u0421\u0438\u0434\u043e\u0440\u043e\u0432\u0430 \u0410\u043d\u043d\u0430"
S_E3R = "\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440"
S_E4N = "\u041a\u043e\u0437\u043b\u043e\u0432 \u0418\u0433\u043e\u0440\u044c"
S_E4R = "\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442"
S_E5N = "\u041e\u0440\u043b\u043e\u0432\u0430 \u0415\u043b\u0435\u043d\u0430"
S_E5R = "\u0411\u0443\u0445\u0433\u0430\u043b\u0442\u0435\u0440"
S_NOTIFY = "\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f"
S_ARCHIVE = "\u0410\u0440\u0445\u0438\u0432\u043d\u0430\u044f \u043a\u043e\u043f\u0438\u044f"
S_LOAD = "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043f\u0440\u0438\u043c\u0435\u0440"
S_DELETE = "\u0423\u0434\u0430\u043b\u0438\u0442\u044c"
S_QUESTION = "\u0412\u043e\u043f\u0440\u043e\u0441:"
S_ANSWER = "\u041e\u0442\u0432\u0435\u0442:"
S_CODE = "\u041a\u043e\u0434:"
S_FIO = "\u0424\u0418\u041e:"
S_ROLE = "\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c:"
S_DEPT = "\u041e\u0442\u0434\u0435\u043b:"
S_NOTES = "\u0417\u0430\u043c\u0435\u0442\u043a\u0438:"
S_STATUS0 = "\u0413\u043e\u0442\u043e\u0432\u043e. \u0414\u0435\u043c\u043e\u043d\u0441\u0442\u0440\u0430\u0446\u0438\u044f QAbstractButton \u0438 QButtonGroup (\u0430\u043d\u0430\u043b\u043e\u0433 Swing AbstractButton / ButtonGroup)."
S_HERO_TITLE = "\u0423\u0447\u0435\u0431\u043d\u044b\u0439 \u043a\u043b\u0438\u0435\u043d\u0442 EM - \u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430"
S_HERO_SUB = "\u0412\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 \u043d\u0430\u0441\u043b\u0435\u0434\u0443\u044e\u0442\u0441\u044f \u043e\u0442 QAbstractButton (Swing - AbstractButton); \u0432\u0437\u0430\u0438\u043c\u043e\u0438\u0441\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0438\u0439 \u0432\u044b\u0431\u043e\u0440 \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0438\u0432\u0430\u0435\u0442 QButtonGroup (Swing - ButtonGroup)."
S_NAV = "\u041d\u0430\u0432\u0438\u0433\u0430\u0446\u0438\u044f (QTreeWidget)"
S_NAV_HEADER = "\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 / \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a"
S_TAB_CARD = "\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430"
S_TAB_FILTERS = "\u0424\u0438\u043b\u044c\u0442\u0440\u044b \u0438 \u0433\u0440\u0443\u043f\u043f\u0430 \u043a\u043d\u043e\u043f\u043e\u043a"
S_TAB_THEORY = "\u0422\u0435\u043e\u0440\u0438\u044f: \u043a\u043d\u043e\u043f\u043a\u0438 \u0438 ButtonGroup"
S_DATA = "\u0414\u0430\u043d\u043d\u044b\u0435 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430"
S_PH_NOTES = "\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 / \u0441\u043b\u0443\u0436\u0435\u0431\u043d\u0430\u044f \u0437\u0430\u043c\u0435\u0442\u043a\u0430..."
S_CMD_BOX = "\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 (\u043d\u0430\u0441\u043b\u0435\u0434\u043d\u0438\u043a\u0438 QAbstractButton)"
S_TYPE_FMT = "\u0422\u0438\u043f \u043a\u043d\u043e\u043f\u043a\u0438 \u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c: {t} -> \u0431\u0430\u0437\u043e\u0432\u044b\u0439 \u043a\u043b\u0430\u0441\u0441 \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0445 \u043a\u043d\u043e\u043f\u043e\u043a: {b}"
S_STATUS_BOX = "\u0421\u0442\u0430\u0442\u0443\u0441 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430 - QButtonGroup (\u0432\u0437\u0430\u0438\u043c\u043e\u0438\u0441\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0438\u0439 \u0432\u044b\u0431\u043e\u0440)"
S_MODE_BOX = "\u0420\u0435\u0436\u0438\u043c \u0440\u0430\u0431\u043e\u0442\u044b \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430 (\u0435\u0449\u0451 \u043e\u0434\u043d\u0430 \u0433\u0440\u0443\u043f\u043f\u0430)"
S_OPTS = "\u041d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u044b\u0435 \u0444\u043b\u0430\u0433\u0438 (QCheckBox \u0442\u043e\u0436\u0435 QAbstractButton, \u043d\u043e \u0432\u043d\u0435 \u0433\u0440\u0443\u043f\u043f\u044b)"
S_LIST_BOX = "\u0421\u043f\u0438\u0441\u043e\u043a \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u043e\u0432 (\u0432\u044b\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435)"
S_HINT = "QButtonGroup \u043d\u0435 \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0432\u0438\u0437\u0443\u0430\u043b\u044c\u043d\u044b\u043c \u0432\u0438\u0434\u0436\u0435\u0442\u043e\u043c: \u043e\u043d \u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u0438 \u0441\u0432\u044f\u0437\u044b\u0432\u0430\u0435\u0442 \u043a\u043d\u043e\u043f\u043a\u0438 (\u043a\u0430\u043a ButtonGroup \u0432 Swing)."
S_SAMPLE_NOTE = "\u041f\u0440\u0438\u043c\u0435\u0440 \u0437\u0430\u043f\u0438\u0441\u0438 \u0434\u043b\u044f \u0434\u0435\u043c\u043e\u043d\u0441\u0442\u0440\u0430\u0446\u0438\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430."
S_CLEARED = "\u0424\u043e\u0440\u043c\u0430 \u043e\u0447\u0438\u0449\u0435\u043d\u0430. \u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u043c \u0448\u0430\u0433\u043e\u043c."
S_WARN_TITLE = "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0432\u0432\u043e\u0434\u0430"
S_WARN_MSG = "\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u0424\u0418\u041e \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430."
S_WARN_STATUS = "\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435 \u043e\u0442\u043c\u0435\u043d\u0435\u043d\u043e."
S_SAVED_TITLE = "\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043e"
S_SAVED_BODY = "\u0417\u0430\u043f\u0438\u0441\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430 (\u0443\u0447\u0435\u0431\u043d\u044b\u0439 \u0440\u0435\u0436\u0438\u043c)."
S_SAVED_STATUS = "\u041e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c: \u0437\u0430\u043f\u0438\u0441\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430."
S_CONFIRM = "\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435"
S_CONFIRM_MSG = "\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u0437\u0430\u043f\u0438\u0441\u044c?"
S_DELETED = "\u0417\u0430\u043f\u0438\u0441\u044c \u0443\u0434\u0430\u043b\u0435\u043d\u0430."
S_ABOUT_BODY = "\u041f\u0440\u0430\u043a\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430 8\n\u041f\u0440\u043e\u0435\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430\nAbstractButton / ButtonGroup\n\u041a\u043b\u0438\u0435\u043d\u0442: PySide6 (Qt)"
S_BTN_THEORY_TITLE = "\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438"
S_BTN_THEORY_BODY = "\u0412 Swing \u0432\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 \u043d\u0430\u0441\u043b\u0435\u0434\u0443\u044e\u0442\u0441\u044f \u043e\u0442 AbstractButton.\nButtonGroup \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0438\u0432\u0430\u0435\u0442 \u0432\u0437\u0430\u0438\u043c\u043e\u0438\u0441\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0438\u0439 \u0432\u044b\u0431\u043e\u0440.\n\n\u0412 PySide6:\n- \u0431\u0430\u0437\u043e\u0432\u044b\u0439 \u043a\u043b\u0430\u0441\u0441: {b}\n- \u0433\u0440\u0443\u043f\u043f\u0430: {g}"
S_Q_TEXT = "\u041e\u0442 \u043a\u0430\u043a\u043e\u0433\u043e \u0431\u0430\u0437\u043e\u0432\u043e\u0433\u043e \u043a\u043b\u0430\u0441\u0441\u0430 \u043d\u0430\u0441\u043b\u0435\u0434\u0443\u044e\u0442\u0441\u044f \u0432\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 \u0438 \u043a\u0430\u043a\u0443\u044e \u0444\u0443\u043d\u043a\u0446\u0438\u044e \u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442 \u043a\u043b\u0430\u0441\u0441 ButtonGroup?"
S_A_TEXT = "\u0412\u0441\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 \u043d\u0430\u0441\u043b\u0435\u0434\u0443\u044e\u0442\u0441\u044f \u043e\u0442 \u0430\u0431\u0441\u0442\u0440\u0430\u043a\u0442\u043d\u043e\u0433\u043e \u043a\u043b\u0430\u0441\u0441\u0430 AbstractButton. \u041a\u043b\u0430\u0441\u0441 ButtonGroup \u043e\u0431\u044a\u0435\u0434\u0438\u043d\u044f\u0435\u0442 \u043d\u0430\u0431\u043e\u0440 \u043a\u043d\u043e\u043f\u043e\u043a (\u043e\u0431\u044b\u0447\u043d\u043e JRadioButton) \u0432 \u0433\u0440\u0443\u043f\u043f\u0443 \u0432\u0437\u0430\u0438\u043c\u043e\u0438\u0441\u043a\u043b\u044e\u0447\u0430\u044e\u0449\u0435\u0433\u043e \u0432\u044b\u0431\u043e\u0440\u0430. \u0412 Qt/PySide6 \u0430\u043d\u0430\u043b\u043e\u0433\u0438: QAbstractButton \u0438 QButtonGroup."

STYLE = (
    "QMainWindow, QWidget { background-color:#f4f7fb; color:#1f2a37; font-family:'Segoe UI'; font-size:13px; }"
    "QGroupBox { border:1px solid #d5dee8; border-radius:10px; margin-top:12px; padding:12px; background:#ffffff; font-weight:600; }"
    "QGroupBox::title { subcontrol-origin:margin; left:12px; padding:0 6px; color:#0f3d68; }"
    "QLineEdit, QComboBox, QTextEdit, QListWidget, QTreeWidget { border:1px solid #c9d5e3; border-radius:8px; padding:6px 8px; background:#ffffff; }"
    "QPushButton { background-color:#1a6fb5; color:white; border:none; border-radius:8px; padding:8px 16px; font-weight:600; }"
    "QPushButton:hover { background-color:#155a94; }"
    "QPushButton:pressed { background-color:#0f446f; }"
    "QPushButton#SecondaryButton { background-color:#e8eef5; color:#1f2a37; }"
    "QPushButton#SecondaryButton:hover { background-color:#d7e2ee; }"
    "QPushButton#DangerButton { background-color:#c0392b; }"
    "QPushButton#DangerButton:hover { background-color:#a93226; }"
    "QRadioButton, QCheckBox { spacing:8px; padding:4px; color:#1f2a37; }"
    "QTabWidget::pane { border:1px solid #d5dee8; border-radius:10px; background:#ffffff; top:-1px; }"
    "QTabBar::tab { background:#e8eef5; border:1px solid #d5dee8; border-bottom:none; border-top-left-radius:8px; border-top-right-radius:8px; padding:8px 16px; margin-right:4px; }"
    "QTabBar::tab:selected { background:#ffffff; color:#0f3d68; font-weight:700; }"
    "QStatusBar { background:#0f3d68; color:white; }""QStatusBar QLabel { color:white; background:transparent; }"
    "QToolBar { background:#ffffff; border-bottom:1px solid #d5dee8; spacing:6px; padding:4px; }"
    "QFrame#HeroCard { background-color:#0f3d68; background:qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0f3d68, stop:1 #1a6fb5); border-radius:14px; }"
    "QLabel#HeroTitle, QLabel#HeroText { color:#ffffff; background:transparent; }""QFrame#HeroCard QLabel { color:#ffffff; background:transparent; }"
    "QLabel#HeroTitle { font-size:18px; font-weight:700; }"
)

@dataclass
class Employee:
    code: str
    name: str
    dept: str
    role: str
    status: str

FICTIONAL_EMPLOYEES = [
    Employee("E-1001", S_E1N, S_DEPT1, S_E1R, S_ACTIVE),
    Employee("E-1002", S_E2N, S_DEPT1, S_E2R, S_ACTIVE),
    Employee("E-1003", S_E3N, S_DEPT2, S_E3R, S_VACATION),
    Employee("E-1004", S_E4N, S_DEPT3, S_E4R, S_ACTIVE),
    Employee("E-1005", S_E5N, S_DEPT4, S_E5R, S_ACTIVE),
]

class EmployeeManagerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(S_TITLE)
        self.resize(980, 680)
        self.setMinimumSize(860, 600)
        self._build_menu()
        self._build_toolbar()
        self._build_central()
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(S_STATUS0)

    def _build_menu(self) -> None:
        menu = self.menuBar()
        file_menu = menu.addMenu(S_FILE)
        help_menu = menu.addMenu(S_HELP)
        act_new = QAction(S_NEW, self)
        act_new.setShortcut("Ctrl+N")
        act_new.triggered.connect(self.clear_form)
        file_menu.addAction(act_new)
        act_save = QAction(S_SAVE, self)
        act_save.setShortcut("Ctrl+S")
        act_save.triggered.connect(self.save_record)
        file_menu.addAction(act_save)
        file_menu.addSeparator()
        act_exit = QAction(S_EXIT, self)
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)
        act_about = QAction(S_ABOUT, self)
        act_about.triggered.connect(self.show_about)
        help_menu.addAction(act_about)

    def _build_toolbar(self) -> None:
        tb = QToolBar(S_ACTIONS)
        tb.setIconSize(QSize(16, 16))
        tb.setMovable(False)
        self.addToolBar(tb)
        b1 = QPushButton(S_SAVE)
        b1.clicked.connect(self.save_record)
        tb.addWidget(b1)
        b2 = QPushButton(S_CLEAR)
        b2.setObjectName("SecondaryButton")
        b2.clicked.connect(self.clear_form)
        tb.addWidget(b2)
        b3 = QPushButton(S_ABOUT_BTN)
        b3.setObjectName("SecondaryButton")
        b3.clicked.connect(self.show_button_theory)
        tb.addWidget(b3)

    def _build_central(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)
        hero = QFrame()
        hero.setObjectName("HeroCard")
        hl = QVBoxLayout(hero)
        hl.setContentsMargins(18, 14, 18, 14)
        t = QLabel(S_HERO_TITLE)
        t.setObjectName("HeroTitle")
        s = QLabel(S_HERO_SUB)
        s.setObjectName("HeroText")
        s.setWordWrap(True)
        hl.addWidget(t)
        hl.addWidget(s)
        layout.addWidget(hero)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter, 1)
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 8, 0)
        tree_box = QGroupBox(S_NAV)
        tl = QVBoxLayout(tree_box)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([S_NAV_HEADER])
        self._fill_tree()
        self.tree.itemClicked.connect(self.on_tree_clicked)
        tl.addWidget(self.tree)
        ll.addWidget(tree_box)
        splitter.addWidget(left)
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(8, 0, 0, 0)
        tabs = QTabWidget()
        self.tabs = tabs
        tabs.addTab(self._build_card_tab(), S_TAB_CARD)
        tabs.addTab(self._build_filters_tab(), S_TAB_FILTERS)
        tabs.addTab(self._build_theory_tab(), S_TAB_THEORY)
        rl.addWidget(tabs)
        splitter.addWidget(right)
        splitter.setSizes([280, 680])

    def _fill_tree(self) -> None:
        self.tree.clear()
        depts = {}
        for emp in FICTIONAL_EMPLOYEES:
            if emp.dept not in depts:
                depts[emp.dept] = QTreeWidgetItem(self.tree, [emp.dept])
            child = QTreeWidgetItem(depts[emp.dept], [f"{emp.code} - {emp.name}"])
            child.setData(0, Qt.ItemDataRole.UserRole, emp.code)
        self.tree.expandAll()

    def _build_card_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        form_box = QGroupBox(S_DATA)
        form = QFormLayout(form_box)
        self.code_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.role_edit = QLineEdit()
        self.dept_combo = QComboBox()
        self.dept_combo.addItems([S_DEPT1, S_DEPT2, S_DEPT3, S_DEPT4])
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(S_PH_NOTES)
        self.notes_edit.setFixedHeight(80)
        form.addRow(S_CODE, self.code_edit)
        form.addRow(S_FIO, self.name_edit)
        form.addRow(S_ROLE, self.role_edit)
        form.addRow(S_DEPT, self.dept_combo)
        form.addRow(S_NOTES, self.notes_edit)
        layout.addWidget(form_box)
        actions_box = QGroupBox(S_CMD_BOX)
        actions = QHBoxLayout(actions_box)
        self.btn_save = QPushButton(S_SAVE)
        self.btn_save.clicked.connect(self.save_record)
        self.btn_load = QPushButton(S_LOAD)
        self.btn_load.setObjectName("SecondaryButton")
        self.btn_load.clicked.connect(self.load_sample)
        self.btn_delete = QPushButton(S_DELETE)
        self.btn_delete.setObjectName("DangerButton")
        self.btn_delete.clicked.connect(self.delete_record)
        actions.addWidget(self.btn_save)
        actions.addWidget(self.btn_load)
        actions.addWidget(self.btn_delete)
        layout.addWidget(actions_box)
        type_info = QLabel(S_TYPE_FMT.format(t=type(self.btn_save).__name__, b=QAbstractButton.__name__))
        type_info.setWordWrap(True)
        layout.addWidget(type_info)
        layout.addStretch(1)
        return page

    def _build_filters_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        status_box = QGroupBox(S_STATUS_BOX)
        status_layout = QVBoxLayout(status_box)
        self.status_group = QButtonGroup(self)
        self.status_group.setExclusive(True)
        self.rb_active = QRadioButton(S_ACTIVE)
        self.rb_vacation = QRadioButton(S_VACATION)
        self.rb_fired = QRadioButton(S_FIRED)
        self.rb_active.setChecked(True)
        for i, rb in enumerate((self.rb_active, self.rb_vacation, self.rb_fired)):
            self.status_group.addButton(rb, i)
            status_layout.addWidget(rb)
        self.status_group.idClicked.connect(self.on_status_changed)
        layout.addWidget(status_box)
        mode_box = QGroupBox(S_MODE_BOX)
        mode_layout = QHBoxLayout(mode_box)
        self.mode_group = QButtonGroup(self)
        self.mode_group.setExclusive(True)
        self.rb_view = QRadioButton(S_VIEW)
        self.rb_edit = QRadioButton(S_EDIT)
        self.rb_query = QRadioButton(S_QUERY)
        self.rb_edit.setChecked(True)
        for i, rb in enumerate((self.rb_view, self.rb_edit, self.rb_query)):
            self.mode_group.addButton(rb, i)
            mode_layout.addWidget(rb)
        self.mode_group.idClicked.connect(self.on_mode_changed)
        layout.addWidget(mode_box)
        opts_box = QGroupBox(S_OPTS)
        opts_layout = QHBoxLayout(opts_box)
        self.cb_notify = QCheckBox(S_NOTIFY)
        self.cb_archive = QCheckBox(S_ARCHIVE)
        self.cb_notify.setChecked(True)
        opts_layout.addWidget(self.cb_notify)
        opts_layout.addWidget(self.cb_archive)
        layout.addWidget(opts_box)
        list_box = QGroupBox(S_LIST_BOX)
        list_layout = QVBoxLayout(list_box)
        self.list_widget = QListWidget()
        for emp in FICTIONAL_EMPLOYEES:
            self.list_widget.addItem(f"{emp.code} | {emp.name} | {emp.dept} | {emp.status}")
        self.list_widget.currentTextChanged.connect(
            lambda t: self.statusBar().showMessage(("Selected: " + t) if t else "")
        )
        list_layout.addWidget(self.list_widget)
        layout.addWidget(list_box, 1)
        hint = QLabel(S_HINT)
        hint.setWordWrap(True)
        layout.addWidget(hint)
        return page

    def _build_theory_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(
            "<h3>" + S_TAB_THEORY + "</h3>"
            "<p><b>" + S_QUESTION + "</b> " + S_Q_TEXT + "</p>"
            "<p><b>" + S_ANSWER + "</b> " + S_A_TEXT + "</p>"
            "<p>" + S_HERO_SUB + "</p>"
        )
        layout.addWidget(text)
        return page

    def on_tree_clicked(self, item, _column):
        code = item.data(0, Qt.ItemDataRole.UserRole)
        if not code:
            return
        for emp in FICTIONAL_EMPLOYEES:
            if emp.code == code:
                self._apply_employee(emp)
                break

    def _apply_employee(self, emp):
        self.code_edit.setText(emp.code)
        self.name_edit.setText(emp.name)
        self.role_edit.setText(emp.role)
        self.dept_combo.setCurrentText(emp.dept)
        mapping = {S_ACTIVE: self.rb_active, S_VACATION: self.rb_vacation, S_FIRED: self.rb_fired}
        mapping.get(emp.status, self.rb_active).setChecked(True)
        self.statusBar().showMessage(f"{emp.code} - {emp.name}")

    def load_sample(self):
        self._apply_employee(FICTIONAL_EMPLOYEES[0])
        self.notes_edit.setText(S_SAMPLE_NOTE)

    def clear_form(self):
        self.code_edit.clear()
        self.name_edit.clear()
        self.role_edit.clear()
        self.notes_edit.clear()
        self.dept_combo.setCurrentIndex(0)
        self.rb_active.setChecked(True)
        self.statusBar().showMessage(S_CLEARED)

    def save_record(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, S_WARN_TITLE, S_WARN_MSG)
            self.statusBar().showMessage(S_WARN_STATUS)
            return
        status_btn = self.status_group.checkedButton()
        status = status_btn.text() if status_btn else "-"
        QMessageBox.information(
            self, S_SAVED_TITLE,
            S_SAVED_BODY + f"\n{self.code_edit.text()} - {self.name_edit.text()}\n{status}",
        )
        self.statusBar().showMessage(S_SAVED_STATUS)

    def delete_record(self):
        reply = QMessageBox.question(self, S_CONFIRM, S_CONFIRM_MSG)
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_form()
            self.statusBar().showMessage(S_DELETED)

    def on_status_changed(self, button_id: int):
        btn = self.status_group.button(button_id)
        if btn:
            self.statusBar().showMessage(f"QButtonGroup: {btn.text()}")

    def on_mode_changed(self, button_id: int):
        editable = button_id == 1
        for w in (self.code_edit, self.name_edit, self.role_edit, self.notes_edit):
            w.setEnabled(editable or button_id == 2)
        self.dept_combo.setEnabled(editable or button_id == 2)
        btn = self.mode_group.button(button_id)
        if btn:
            self.statusBar().showMessage(btn.text())

    def show_about(self):
        QMessageBox.about(self, S_ABOUT, S_ABOUT_BODY)

    def show_button_theory(self):
        QMessageBox.information(
            self, S_BTN_THEORY_TITLE,
            S_BTN_THEORY_BODY.format(b=QAbstractButton.__name__, g=QButtonGroup.__name__),
        )

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    window = EmployeeManagerWindow()
    window.show()
    window.load_sample()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
