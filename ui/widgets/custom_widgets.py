from PyQt6.QtWidgets import (QListWidget, QFrame, QPushButton, QWidget, QLabel, QSlider, QVBoxLayout, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QColor, QPainter, QPen, QLinearGradient as QLinearGradientGui, QPainterPath, QBrush, QFont
from config.colors import Colors

class ChannelListWidget(QListWidget):
    def __init__(self, parent=None): super().__init__(parent)

class GradientButton(QPushButton):
    def __init__(self, text: str, parent=None, gradient_start=None, gradient_end=None):
        super().__init__(text, parent)
        self.gradient_start = QColor(gradient_start or Colors.GRADIENT_BUTTON_START)
        self.gradient_end = QColor(gradient_end or Colors.GRADIENT_BUTTON_END)
        self.hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(42)
        self.setStyleSheet("QPushButton { background: transparent; border: none; color: #0a0e1a; font-weight: 700; font-size: 13px; border-radius: 10px; padding: 0 20px; }")

    def enterEvent(self, event): self.hovered = True; self.update(); super().enterEvent(event)
    def leaveEvent(self, event): self.hovered = False; self.update(); super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 10, 10)
        gradient = QLinearGradientGui(self.rect().topLeft().x(), self.rect().topLeft().y(), self.rect().bottomRight().x(), self.rect().bottomRight().y())
        gradient.setColorAt(0, self.gradient_start.lighter(20) if self.hovered else self.gradient_start)
        gradient.setColorAt(1, self.gradient_end.lighter(20) if self.hovered else self.gradient_end)
        painter.fillPath(path, QBrush(gradient))
        painter.setPen(QPen(QColor(Colors.BORDER_FOCUS), 1))
        painter.drawPath(path)
        painter.setPen(QPen(QColor("#0a0e1a")))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

class ChannelNameOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.channel_name = ""
        self.opacity = 0.0
        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self._fade_out)
        self.hide()

    def show_channel_name(self, name: str):
        self.channel_name = name; self.opacity = 1.0; self.show(); self.raise_(); self.fade_timer.start(2000)

    def _fade_out(self):
        self.fade_timer.stop(); self.opacity = max(0, self.opacity - 0.05); self.update()
        if self.opacity <= 0: self.hide()

    def paintEvent(self, event):
        if not self.channel_name: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, int(150 * self.opacity)))
        painter.drawRoundedRect(self.rect(), 8, 8)
        painter.setPen(QPen(QColor(255, 255, 255, int(255 * self.opacity))))
        painter.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.channel_name)

class ModernSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("QSlider::groove:horizontal { border: none; height: 6px; background: #1e3048; border-radius: 3px; } QSlider::handle:horizontal { background: #00d4ff; border: none; width: 16px; height: 16px; margin: -5px 0; border-radius: 8px; } QSlider::sub-page:horizontal { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #0099ff); border-radius: 3px; } QSlider::add-page:horizontal { background: #1e3048; border-radius: 3px; }")

class SettingsPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(280, 320)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("color: #00d4ff; font-size: 16px; font-weight: 700; padding-bottom: 8px; border-bottom: 1px solid #1e3048;")
        layout.addWidget(title)
        
        combo_style = "QComboBox { background: #111827; color: #e8f4f8; border: 1px solid #1e3048; border-radius: 8px; padding: 8px 12px; font-size: 12px; } QComboBox:hover { border-color: #00d4ff; }"
        for lbl_text in ["🔊 Audio Quality", "📝 Subtitles", "🎬 Playback Quality"]:
            layout.addWidget(QLabel(lbl_text, styleSheet="color: #8ba4b8; font-size: 12px; font-weight: 600;"))
            combo = QComboBox()
            combo.addItem("Auto" if "Quality" in lbl_text else "No Subtitle")
            combo.setStyleSheet(combo_style)
            layout.addWidget(combo)
            if "Audio" in lbl_text: self.audio_combo = combo
            elif "Sub" in lbl_text: self.sub_combo = combo
            else: self.quality_combo = combo
        layout.addStretch()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 12, 12)
        gradient = QLinearGradientGui(self.rect().topLeft().x(), self.rect().topLeft().y(), self.rect().bottomRight().x(), self.rect().bottomRight().y())
        gradient.setColorAt(0, QColor("#111827")); gradient.setColorAt(1, QColor("#1a2332"))
        painter.fillPath(path, QBrush(gradient))
        painter.setPen(QPen(QColor("#1e3048"), 1))
        painter.drawPath(path)