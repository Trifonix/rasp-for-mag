# bank_dashboard_gui.py
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QSize
import sys


class BankDashboardGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личный кабинет банка — Практическая работа GUI")
        self.setMinimumSize(900, 550)
        self.setStyleSheet("background-color: #F4F4F4;")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Левая панель навигации ---
        nav_frame = QFrame()
        nav_frame.setStyleSheet("background-color: #2C3E50;")
        nav_frame.setFixedWidth(200)
        nav_layout = QVBoxLayout()
        nav_layout.setContentsMargins(10, 20, 10, 10)
        nav_layout.setSpacing(15)

        # Кнопки навигации с иконками
        nav_buttons = [
            ("Главная", "home.png"),
            ("Инструкция", "info.png"),
            ("Регистрация", "register.png"),
            ("Платежи и переводы", "payment.png"),
            ("Счета", "accounts.png"),
            ("Персональные настройки", "settings.png"),
        ]

        self.stack = QStackedWidget()

        for i, (text, icon_path) in enumerate(nav_buttons):
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setFont(QFont("Segoe UI", 10))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                """
                QPushButton {
                    color: white;
                    background-color: transparent;
                    text-align: left;
                    padding: 8px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
                QPushButton:pressed {
                    background-color: #1ABC9C;
                }
                """
            )
            btn.clicked.connect(lambda checked, index=i: self.stack.setCurrentIndex(index))
            nav_layout.addWidget(btn)

            # Добавим пустую страницу в стек
            page = QLabel(f"Содержимое страницы: {text}")
            page.setAlignment(Qt.AlignCenter)
            page.setFont(QFont("Segoe UI", 14))
            page.setStyleSheet("color: #2C3E50;")
            self.stack.addWidget(page)

        nav_layout.addStretch()
        nav_frame.setLayout(nav_layout)
        main_layout.addWidget(nav_frame)

        # --- Основная рабочая область ---
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #ECF0F1; border-radius: 10px;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.addWidget(self.stack)
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankDashboardGUI()
    window.show()
    sys.exit(app.exec())
