from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QListWidget, QListWidgetItem, QLabel, QFileDialog, 
    QMessageBox, QSizePolicy, QFrame, QSplitter, QMenu
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QColor

from config.colors import Colors
from config.constants import DEFAULT_VOLUME
from repositories.playlist_repository import PlaylistRepository
from services.playlist_service import PlaylistService
from managers.mpv_manager import MPVManager
from managers.thread_manager import ThreadManager
from controllers.player_controller import PlayerController
from controllers.playlist_controller import PlaylistController
from controllers.search_controller import SearchController
from controllers.settings_controller import SettingsController
from controllers.fullscreen_controller import FullscreenController
from controllers.keyboard_controller import KeyboardController
from ui.styles.stylesheet import get_modern_stylesheet
from ui.widgets.custom_widgets import (
    ChannelListWidget, GradientButton, ChannelNameOverlay, 
    ModernSlider, SettingsPopup
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPTV Player - Modern Edition")
        self.resize(1400, 780)
        self.setMinimumSize(1000, 650)
        
        # 1. Instantiate Repositories & Services
        self.repo = PlaylistRepository()
        self.playlist_service = PlaylistService(self.repo)
        
        # 2. Instantiate Managers
        self.mpv_manager = MPVManager()
        self.thread_mgr = ThreadManager()
        
        # 3. Instantiate Controllers (Dependency Injection)
        self.player_ctrl = PlayerController(self.mpv_manager, self.repo)
        self.playlist_ctrl = PlaylistController(self.playlist_service, self.repo, self.thread_mgr)
        self.search_ctrl = SearchController(self.repo)
        self.settings_ctrl = SettingsController(self.mpv_manager)
        self.fullscreen_ctrl = FullscreenController()
        
        # 4. Build UI
        self.init_ui()
        
        # 5. Inject UI elements into Keyboard Controller
        self.keyboard_ctrl = KeyboardController(
            self.player_ctrl, self.playlist_ctrl, self.settings_ctrl, 
            self.fullscreen_ctrl, self.volume_slider
        )
        
        # 6. Wire Signals
        self._connect_signals()
        
        # 7. Initialize MPV with the Window ID
        self.mpv_manager.initialize(int(self.video_container.winId()))
        self.mpv_manager.error_occurred.connect(
            lambda msg: QMessageBox.critical(self, "MPV Error", f"Failed to initialize MPV:\n{msg}")
        )

    def init_ui(self):
        self.setStyleSheet(get_modern_stylesheet())
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # ========== LEFT PANEL (Sidebar) ==========
        self.left_panel = QFrame()
        self.left_panel.setObjectName("sidebarFrame")
        self.left_panel.setMinimumWidth(450)
        self.left_panel.setMaximumWidth(600)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(14)

        left_layout.addWidget(QLabel("📺 Channel List", styleSheet=f"font-size: 18px; font-weight: 700; color: {Colors.PRIMARY}; margin-bottom: 5px;"))
        
        load_file_btn = GradientButton("📂 Load M3U", gradient_start=Colors.GRADIENT_BUTTON_START, gradient_end=Colors.GRADIENT_BUTTON_END)
        load_file_btn.setFixedHeight(34)
        load_file_btn.clicked.connect(self._load_file_dialog)
        left_layout.addWidget(load_file_btn)

        url_frame = QFrame()
        url_frame.setObjectName("cardFrame")
        url_layout = QHBoxLayout(url_frame)
        url_layout.setContentsMargins(4, 4, 4, 4)
        url_layout.setSpacing(6)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter M3U URL or direct stream link...")
        self.url_input.setFixedHeight(28)
        load_url_btn = QPushButton("▶")
        load_url_btn.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d4ff, stop:1 #0099ff); color: #0a0e1a; border: none; border-radius: 8px; font-weight: 700; font-size: 14px; } QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #33ddff, stop:1 #00aaff); }")
        load_url_btn.setMaximumWidth(44)
        load_url_btn.setMinimumHeight(10)
        load_url_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_url_btn.clicked.connect(lambda: self.playlist_ctrl.load_url(self.url_input.text().strip()))
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(load_url_btn)
        left_layout.addWidget(url_frame)

        sep1 = QFrame()
        sep1.setObjectName("separator")
        sep1.setFrameShape(QFrame.Shape.HLine)
        left_layout.addWidget(sep1)

        search_frame = QFrame()
        search_frame.setObjectName("cardFrame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(12, 6, 12, 6)
        search_layout.addWidget(QLabel("🔍", styleSheet="font-size: 16px;"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Channels...")
        self.search_input.setFixedHeight(28)
        self.search_input.setStyleSheet("border: none; background: transparent;")
        search_layout.addWidget(self.search_input)
        left_layout.addWidget(search_frame)

        self.list_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.list_splitter.setHandleWidth(4)
        self.category_list = QListWidget()
        self.channel_list = ChannelListWidget()
        self.channel_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_splitter.addWidget(self.category_list)
        self.list_splitter.addWidget(self.channel_list)
        self.list_splitter.setSizes([180, 270])
        left_layout.addWidget(self.list_splitter, stretch=1)

        self.channel_count_label = QLabel("0 channels loaded", styleSheet=f"color: {Colors.TEXT_MUTED}; font-size: 11px; padding: 5px;")
        left_layout.addWidget(self.channel_count_label)

        # ========== RIGHT PANEL (Video + Controls) ==========
        self.right_panel = QFrame()
        self.right_panel.setObjectName("cardFrame")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.video_container = QWidget()
        self.video_container.setStyleSheet(f"background-color: {Colors.BG_DARK}; border-radius: 12px;")
        self.video_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_container.setMinimumHeight(420)
        video_layout = QVBoxLayout(self.video_container)
        video_layout.setContentsMargins(0, 0, 0, 0)

        self.black_overlay = QLabel()
        self.black_overlay.setStyleSheet(f"background-color: {Colors.BG_DARK}; border-radius: 12px;")
        self.black_overlay.hide()
        video_layout.addWidget(self.black_overlay)

        self.channel_name_overlay = ChannelNameOverlay(self.video_container)
        self.channel_name_overlay.setGeometry(20, 20, 400, 50)

        self.loading_label = QLabel("LOADING STREAM...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        video_layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_exit_fs = QPushButton("✕ Exit Fullscreen")
        self.btn_exit_fs.setStyleSheet("QPushButton { background: #ff5252; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 600; } QPushButton:hover { background: #ff1744; }")
        self.btn_exit_fs.setMaximumWidth(140)
        self.btn_exit_fs.hide()
        exit_fs_layout = QVBoxLayout()
        exit_fs_layout.setContentsMargins(15, 15, 15, 0)
        exit_fs_layout.addWidget(self.btn_exit_fs, alignment=Qt.AlignmentFlag.AlignRight)
        video_layout.addLayout(exit_fs_layout)
         
        right_layout.addWidget(self.video_container, stretch=1)

        self.status_bar = QLabel("Ready | Played: 0s | Buffered: 0% | Cache: 0.0 MB")
        self.status_bar.setObjectName("statusLabel")
        right_layout.addWidget(self.status_bar)

        # ========== VIDEO TOOLBAR ==========
        self.toolbar_widget = QFrame()
        self.toolbar_widget.setObjectName("cardFrame")
        toolbar_layout = QVBoxLayout(self.toolbar_widget)
        toolbar_layout.setContentsMargins(16, 12, 16, 12)
        toolbar_layout.setSpacing(10)

        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        self.time_label = QLabel("00:00", styleSheet="color: #8ba4b8; font-size: 12px; font-family: 'Consolas', monospace; min-width: 50px;")
        progress_layout.addWidget(self.time_label)
        self.progress_slider = ModernSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimumHeight(20)
        progress_layout.addWidget(self.progress_slider, stretch=1)
        self.duration_label = QLabel("00:00", styleSheet="color: #8ba4b8; font-size: 12px; font-family: 'Consolas', monospace; min-width: 50px;")
        progress_layout.addWidget(self.duration_label)
        toolbar_layout.addLayout(progress_layout)

        controls_row = QHBoxLayout()
        controls_row.setSpacing(12)
        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(6)
        self.volume_icon = QLabel("◉", styleSheet="font-size: 16px; background: transparent; border: none;")
        self.volume_slider = ModernSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(DEFAULT_VOLUME)
        self.volume_slider.setMaximumWidth(120)
        volume_layout.addWidget(self.volume_icon)
        volume_layout.addWidget(self.volume_slider)
        controls_row.addLayout(volume_layout)
        controls_row.addStretch()

        play_controls = QHBoxLayout()
        play_controls.setSpacing(8)
        btn_style = "QPushButton { background: #1a2332; color: #e8f4f8; border: 1px solid #1e3048; border-radius: 10px; font-size: 16px; min-width: 44px; min-height: 44px; } QPushButton:hover { border-color: #00d4ff; color: #00d4ff; }"
        
        self.btn_prev = QPushButton("⏮")
        self.btn_prev.setStyleSheet(btn_style)
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_play_pause = QPushButton("▶")
        self.btn_play_pause.setStyleSheet("QPushButton { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d4ff, stop:1 #0099ff); color: #0a0e1a; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; min-width: 52px; min-height: 52px; } QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #33ddff, stop:1 #00aaff); }")
        self.btn_play_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_next = QPushButton("⏭")
        self.btn_next.setStyleSheet(btn_style)
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        
        play_controls.addWidget(self.btn_prev)
        play_controls.addWidget(self.btn_play_pause)
        play_controls.addWidget(self.btn_next)
        controls_row.addLayout(play_controls)
        controls_row.addStretch()

        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setStyleSheet(btn_style)
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_fullscreen = QPushButton("⛶")
        self.btn_fullscreen.setStyleSheet(btn_style)
        self.btn_fullscreen.setCursor(Qt.CursorShape.PointingHandCursor)
        
        controls_row.addWidget(self.btn_settings)
        controls_row.addWidget(self.btn_fullscreen)
        toolbar_layout.addLayout(controls_row)
        right_layout.addWidget(self.toolbar_widget)

        self.settings_popup = SettingsPopup(self)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([450, 950])
        main_layout.addWidget(self.splitter)

    def _connect_signals(self):
        # Player Signals
        self.player_ctrl.loading_state_changed.connect(self._handle_loading)
        self.player_ctrl.status_update.connect(self._handle_status_update)
        self.player_ctrl.channel_name_requested.connect(self.channel_name_overlay.show_channel_name)
        
        # Playlist Signals
        self.playlist_ctrl.playlist_loaded.connect(self._handle_playlist_loaded)
        self.playlist_ctrl.categories_updated.connect(self._handle_categories_updated)
        self.playlist_ctrl.channels_updated.connect(self._handle_channels_updated)
        self.playlist_ctrl.loading_state_changed.connect(self._handle_loading)
        self.playlist_ctrl.error_occurred.connect(lambda msg: QMessageBox.warning(self, "Error", msg))
        
        # Search Signals
        self.search_ctrl.search_results.connect(self._handle_search_results)
        self.search_input.textChanged.connect(self._on_search_text_changed)
        
        # MPV Track List Signals
        self.mpv_manager.track_list_changed.connect(
            lambda tl: self.settings_ctrl.process_track_list(
                tl, self.settings_popup.audio_combo, 
                self.settings_popup.sub_combo, self.settings_popup.quality_combo
            )
        )
        
        # Fullscreen Signals
        self.fullscreen_ctrl.fullscreen_state_changed.connect(self._apply_fullscreen_state)
        
        # UI Events to Controllers
        self.btn_play_pause.clicked.connect(self.player_ctrl.toggle_play_pause)
        self.btn_next.clicked.connect(self.player_ctrl.play_next)
        self.btn_prev.clicked.connect(self.player_ctrl.play_prev)
        self.progress_slider.valueChanged.connect(self.player_ctrl.seek)
        self.volume_slider.valueChanged.connect(self.player_ctrl.set_volume)
        self.volume_slider.valueChanged.connect(self._update_volume_icon)
        
        self.btn_fullscreen.clicked.connect(self.fullscreen_ctrl.toggle)
        self.btn_exit_fs.clicked.connect(self.fullscreen_ctrl.toggle)
        self.btn_settings.clicked.connect(self._toggle_settings_popup)
        
        self.category_list.itemClicked.connect(self._on_category_selected)
        self.channel_list.itemClicked.connect(self._on_channel_item_clicked)
        self.channel_list.customContextMenuRequested.connect(self._show_channel_context_menu)
        
        # Settings Events
        self.settings_popup.audio_combo.currentIndexChanged.connect(lambda: self.settings_ctrl.change_audio(self.settings_popup.audio_combo))
        self.settings_popup.sub_combo.currentIndexChanged.connect(lambda: self.settings_ctrl.change_sub(self.settings_popup.sub_combo))
        self.settings_popup.quality_combo.currentIndexChanged.connect(
            lambda: self.settings_ctrl.change_quality(
                self.settings_popup.quality_combo, 
                lambda: self.player_ctrl.current_url, 
                self.player_ctrl.play_channel
            )
        )

    # ==========================================
    # VIEW EVENT HANDLERS (No Business Logic)
    # ==========================================
    def _load_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select M3U File", "", "M3U Files (*.m3u *.m3u8);;All Files (*.*)")
        if file_path: 
            self.playlist_ctrl.load_file(file_path)

    def _handle_loading(self, show: bool):
        if show:
            self.black_overlay.show()
            self.loading_label.show()
            self.loading_label.raise_()
            self.black_overlay.raise_()
        else:
            self.loading_label.hide()
            self.black_overlay.hide()

    def _handle_status_update(self, data: dict):
        self.status_bar.setText(data["text"])
        self.time_label.setText(data["time_label"])
        self.duration_label.setText(data["duration_label"])
        if data["progress"] != -1:
            self.progress_slider.blockSignals(True)
            self.progress_slider.setValue(data["progress"])
            self.progress_slider.blockSignals(False)

    def _handle_playlist_loaded(self, count: int):
        if count == -1:
            self.player_ctrl.play_channel(self.playlist_ctrl.get_pending_url())
        else:
            self.channel_count_label.setText(f"{count} channels loaded")

    def _handle_categories_updated(self, cat_list: list):
        self.category_list.clear()
        self.channel_list.clear()
        self.category_list.setUpdatesEnabled(False)
        for cat in cat_list:
            item = QListWidgetItem(f"◉ {cat['name']}    ({len(cat['channels'])})")
            item.setData(Qt.ItemDataRole.UserRole, (cat['name'], cat['channels']))
            item.setSizeHint(QSize(0, 36))
            self.category_list.addItem(item)
        self.category_list.setUpdatesEnabled(True)
        placeholder = QListWidgetItem("Select a category from the left.")
        placeholder.setFlags(placeholder.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
        self.channel_list.addItem(placeholder)

    def _handle_channels_updated(self, channels: list, is_search: bool, match_count: int):
        self.channel_list.clear()
        self.channel_list.setUpdatesEnabled(False)
        for ch in channels:
            name = ch["name"]
            stream_count = len(ch.get("streams", []))
            if stream_count > 1: name += f" ({stream_count})"
            item = QListWidgetItem(f"📺 {name}")
            item.setData(Qt.ItemDataRole.UserRole, ch)
            item.setSizeHint(QSize(0, 32))
            self.channel_list.addItem(item)
        if is_search:
            info = QListWidgetItem(f"🔍 Found {match_count} channels.")
            info.setForeground(QColor(Colors.ACCENT_BLUE))
            info.setFlags(info.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEnabled)
            self.channel_list.insertItem(0, info)
        self.channel_list.setUpdatesEnabled(True)

    def _on_search_text_changed(self, text: str):
        base_channels = self.playlist_ctrl.current_category_channels if self.playlist_ctrl.current_category_name else self.repo.get_channels()
        self.search_ctrl.set_query(text, base_channels)

    def _handle_search_results(self, filtered: list, count: int):
        self._handle_channels_updated(filtered, is_search=True, match_count=count)

    def _on_category_selected(self, item):
        role_data = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(role_data, tuple):
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
            self.playlist_ctrl.select_category(role_data[0], role_data[1])

    def _on_channel_item_clicked(self, item):
        channel = item.data(Qt.ItemDataRole.UserRole)
        if not channel or not isinstance(channel, dict): return
        streams = channel.get("streams", [])
        if streams:
            self.player_ctrl.play_channel(streams[0]["url"])
            channels = self.repo.get_channels()
            for idx, ch in enumerate(channels):
                if ch is channel: 
                    self.player_ctrl.current_channel_index = idx
                    break

    def _show_channel_context_menu(self, pos):
        item = self.channel_list.itemAt(pos)
        if not item: return
        channel = item.data(Qt.ItemDataRole.UserRole)
        if not channel or not isinstance(channel, dict): return
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background: #111827; color: #e8f4f8; border: 1px solid #1e3048; border-radius: 8px; padding: 5px; } QMenu::item { padding: 8px 20px; border-radius: 4px; } QMenu::item:selected { background: #00d4ff; color: #0a0e1a; }")
        streams = channel.get("streams", [])
        if len(streams) > 1:
            stream_menu = menu.addMenu("🎬 Select Stream")
            for i, stream in enumerate(streams):
                action = stream_menu.addAction(f"Stream {i+1}")
                action.triggered.connect(lambda checked, url=stream["url"]: self.player_ctrl.play_channel(url))
        menu.exec(self.channel_list.mapToGlobal(pos))

    def _update_volume_icon(self, value):
        if value == 0: self.volume_icon.setText("🔇")
        elif value < 30: self.volume_icon.setText("🔈")
        elif value < 70: self.volume_icon.setText("🔉")
        else: self.volume_icon.setText("🔊")

    def _toggle_settings_popup(self):
        if self.settings_popup.isVisible():
            self.settings_popup.hide()
        else:
            btn_pos = self.btn_settings.mapToGlobal(QPoint(0, 0))
            x = btn_pos.x() + self.btn_settings.width() - self.settings_popup.width()
            y = btn_pos.y() - self.settings_popup.height() - 10
            self.settings_popup.move(x, y)
            self.settings_popup.show()
            self.settings_popup.raise_()
            self.settings_popup.activateWindow()

    def _apply_fullscreen_state(self, is_fs: bool):
        if is_fs:
            self.left_panel.hide()
            self.toolbar_widget.hide()
            self.status_bar.hide()
            self.btn_exit_fs.show()
            self.splitter.setContentsMargins(0, 0, 0, 0)
            self.showFullScreen()
        else:
            self.left_panel.show()
            self.toolbar_widget.show()
            self.status_bar.show()
            self.btn_exit_fs.hide()
            self.splitter.setContentsMargins(12, 12, 12, 12)
            self.showNormal()

    def keyPressEvent(self, event):
        if not self.keyboard_ctrl.handle_key(event):
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.thread_mgr.cleanup_all()
        self.mpv_manager.terminate()
        event.accept()