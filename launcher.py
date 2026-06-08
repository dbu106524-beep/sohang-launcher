import customtkinter as ctk
import minecraft_launcher_lib
from minecraft_launcher_lib.microsoft_account import (
    authenticate_with_xbl,
    authenticate_with_xsts,
    get_profile
)
import subprocess
import threading
import os
import webbrowser
import time
import requests
import hashlib
import urllib.parse
import zipfile
import json
import socket
import struct
import tkinter as tk
import sys
import base64
import ctypes
import tempfile
import random
import platform
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)
ICON_PATH = os.path.join(RESOURCE_DIR, "sohangicon-transparent.png")
WINDOWS_ICON_PATH = os.path.join(RESOURCE_DIR, "sohangicon.ico")
FONT_DIR = os.path.join(RESOURCE_DIR, "fonts")
MINECRAFT_DIR = os.path.join(os.path.expanduser("~"), ".minecraft_asteroid")
MODS_DIR = os.path.join(MINECRAFT_DIR, "mods")
AVATAR_CACHE_DIR = os.path.join(MINECRAFT_DIR, "avatars")
AUTH_CACHE_FILE = os.path.join(MINECRAFT_DIR, "auth_cache.json")
LAUNCHER_SETTINGS_FILE = os.path.join(MINECRAFT_DIR, "launcher_settings.json")
LAUNCHER_LOG_FILE = os.path.join(MINECRAFT_DIR, "launcher-game.log")
INSTALL_STATE_FILE = os.path.join(MINECRAFT_DIR, "install_state.json")
KEYCHAIN_SERVICE = "SohangLauncher"
KEYCHAIN_ACCOUNT = "minecraft-refresh-token"
APP_VERSION = "1.17"
UPDATE_API_URL = "https://api.github.com/repos/dbu106524-beep/sohang-launcher/releases/latest"
UPDATE_PAGE_URL = "https://github.com/dbu106524-beep/sohang-launcher/releases/latest"
LAUNCHER_WINDOWS_ASSET_NAME = "SohangLauncher.exe"
LAUNCHER_WINDOWS_ASSET_NAMES = (
    f"SohangLauncher-{APP_VERSION}.exe",
    LAUNCHER_WINDOWS_ASSET_NAME,
)
LAUNCHER_MAC_ASSET_NAMES = (
    "SohangLauncher-mac-arm64.zip",
    "SohangLauncher-mac-x64.zip",
    "SohangLauncher-mac.zip",
    "SohangLauncher.dmg",
)
MC_VERSION = "26.1.2"
SERVER_IP = "dinbu.kro.kr"
SERVER_PORT = "25565"
SERVER_ADDRESS = f"{SERVER_IP}:{SERVER_PORT}"
SERVER_NAME = "소행성 서버"
SERVER_PROTOCOL_VERSION = 767
NEOFORGE_VERSION = "26.1.2.65-beta"
REQUIRED_JAVA_MAJOR = 25
CLIENT_ID = "0ab5ff14-0b50-4a22-a26b-def8c460b422" #"0ab5ff14-0b50-4a22-a26b-def8c460b422"
DEVICE_CODE_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
MINECRAFT_LOGIN_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"
MICROSOFT_SCOPE = "XboxLive.signin offline_access"
DEFAULT_OLD_CLIENT_ID = "00000000402b5328"
MRPACK_PATH = ""
MRPACK_URL = "https://github.com/dbu106524-beep/sohang-launcher/releases/latest/download/Createdin.mrpack"
MRPACK_FILE = os.path.join(MINECRAFT_DIR, "server-pack.mrpack")
MRPACK_META_FILE = os.path.join(MINECRAFT_DIR, "server-pack-meta.json")
MRPACK_DOWNLOAD_RETRIES = 4
MRPACK_DOWNLOAD_TIMEOUT = (15, 180)
MODRINTH_API_BASE = "https://api.modrinth.com/v2"
MODRINTH_USER_AGENT = f"dbu106524-beep/sohang-launcher/{APP_VERSION} (dinbu.kro.kr)"
MODRINTH_LOADER = "neoforge"
APP_FONT_FAMILY = "Paperlogy 4 Regular"
APP_FONT_BOLD_FAMILY = "Paperlogy 7 Bold"
FONT_FILES = (
    "Paperlogy-1Thin.ttf",
    "Paperlogy-2ExtraLight.ttf",
    "Paperlogy-3Light.ttf",
    "Paperlogy-4Regular.ttf",
    "Paperlogy-5Medium.ttf",
    "Paperlogy-6SemiBold.ttf",
    "Paperlogy-7Bold.ttf",
    "Paperlogy-8ExtraBold.ttf",
    "Paperlogy-9Black.ttf",
)

# 서버 필수 모드 다운로드 목록입니다.
# url에는 직접 다운로드 가능한 .jar 링크를 넣으면 됩니다.
# sha256은 선택 사항이지만, 넣어두면 깨진 파일이나 잘못된 파일을 잡아낼 수 있어요.
SERVER_MODS_MANIFEST_URL = ""
SERVER_MODS = [
    # {
    #     "name": "example-mod",
    #     "url": "https://example.com/mods/example-mod.jar",
    #     "filename": "example-mod.jar",
    #     "sha256": "",
    # },
]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SPACE_BG = "#0a0a1a"
SPACE_CARD = "#0f0f2e"
SPACE_ACCENT = "#4a90d9"
SPACE_ACCENT2 = "#7c3aed"
SPACE_STAR = "#c0caf5"
SPACE_MUTED = "#4a4a6a"
SPACE_GREEN = "#22c55e"
SPACE_RED = "#ef4444"

LAUNCH_STATUS_MESSAGES = [
    "항법 컴퓨터 가동 중...",
    "별자리 좌표 계산 중...",
    "소행성 궤도 맞추는 중...",
    "워프 게이트 예열 중...",
    "우주복 산소 확인 중...",
    "성간 지도 펼치는 중...",
    "엔진 플라즈마 충전 중...",
    "중력장을 안정화하는 중...",
    "서버 궤도로 진입 중...",
    "마지막 별가루 점검 중...",
]
EXPERIMENTAL_JVM_UNLOCK_ARG = "-XX:+UnlockExperimentalVMOptions"
EXPERIMENTAL_JVM_OPTION_PREFIXES = (
    "-XX:G1NewSizePercent",
    "-XX:G1MaxNewSizePercent",
    "-XX:G1MixedGCLiveThresholdPercent",
    "-XX:G1NewSizePercent=",
    "-XX:G1MaxNewSizePercent=",
    "-XX:G1MixedGCLiveThresholdPercent=",
)


class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("소행성 런처")
        self.geometry("1320x660")
        self.resizable(False, False)
        self.configure(fg_color=SPACE_BG)

        self._main_thread = threading.current_thread()
        self.icon_image = None
        self.logo_image = None
        self.avatar_image = None
        self.remember_login_var = ctk.BooleanVar(value=False)
        self.available_launcher_update = None
        self.account = None
        self.memory_gb = self._load_memory_setting()
        self.resolution_width = self._load_resolution_setting("resolution_width", 1280)
        self.resolution_height = self._load_resolution_setting("resolution_height", 720)
        self.fullscreen_enabled = self._load_fullscreen_setting()
        self._launch_status_after_id = None
        self._last_launch_status_message = None
        self.mod_search_window = None
        self.mod_search_results = []
        self.mod_icon_images = {}
        self.mod_search_page = 0
        self.mod_sort_var = tk.StringVar(value="인기순")
        self.mod_search_query = ""
        self._last_mrpack_changed = False
        self.font_family = self._load_app_fonts()
        self._load_images()
        self._build_ui()
        self._log(f"소행성 런처 v{APP_VERSION}")
        self._log(f"실행 파일: {sys.executable}")
        self._refresh_server_status()
        self._try_auto_login()
        self._check_launcher_update()
        self.after(600, self._search_modrinth_mods)

    def _load_images(self):
        if not os.path.exists(ICON_PATH):
            return

        self.icon_image = tk.PhotoImage(file=ICON_PATH)
        self.iconphoto(True, self.icon_image)
        if os.path.exists(WINDOWS_ICON_PATH):
            try:
                self.iconbitmap(WINDOWS_ICON_PATH)
            except tk.TclError:
                pass
        self.logo_image = self.icon_image.subsample(10, 10)

    def _load_app_fonts(self):
        if sys.platform == "win32" and os.path.isdir(FONT_DIR):
            add_font = ctypes.windll.gdi32.AddFontResourceExW
            for filename in FONT_FILES:
                font_path = os.path.join(FONT_DIR, filename)
                if os.path.exists(font_path):
                    add_font(font_path, 0x10, 0)
            return APP_FONT_FAMILY

        if sys.platform == "darwin":
            return APP_FONT_FAMILY

        return APP_FONT_FAMILY

    def _font(self, size, weight="normal"):
        family = APP_FONT_BOLD_FAMILY if weight == "bold" else self.font_family
        return ctk.CTkFont(
            family=family,
            size=max(11, size),
            weight=weight
        )

    def _build_ui(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0,
                                fg_color=SPACE_CARD,
                                border_width=1, border_color=SPACE_ACCENT2)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=(30, 5), padx=15)

        if self.logo_image:
            ctk.CTkLabel(logo_frame, text="", image=self.logo_image).pack()
        else:
            ctk.CTkLabel(logo_frame, text="🪐",
                         font=self._font(48, "bold")).pack()
        ctk.CTkLabel(logo_frame, text="소행성",
                     font=self._font(24, "bold"),
                     text_color=SPACE_STAR).pack()
        ctk.CTkLabel(logo_frame, text="마인크래프트 소행성 서버",
                     font=self._font(11),
                     text_color=SPACE_MUTED).pack(pady=(2, 0))

        ctk.CTkFrame(sidebar, height=1, fg_color=SPACE_ACCENT2).pack(
            fill="x", padx=20, pady=15)

        self.login_btn = ctk.CTkButton(
            sidebar, text="Microsoft 로그인",
            command=self._login, width=180, height=38,
            fg_color=SPACE_ACCENT2, hover_color="#6d28d9",
            font=self._font(14, "bold")
        )
        self.login_btn.pack(pady=8, padx=20)

        self.remember_login_checkbox = ctk.CTkCheckBox(
            sidebar, text="자동 로그인",
            variable=self.remember_login_var,
            command=self._on_remember_login_changed,
            checkbox_width=18, checkbox_height=18,
            fg_color=SPACE_ACCENT2,
            hover_color="#6d28d9",
            text_color=SPACE_STAR,
            font=self._font(12)
        )
        self.remember_login_checkbox.pack(pady=(0, 5), padx=20, anchor="w")

        self.update_btn = ctk.CTkButton(
            sidebar, text="런처가 최신버전이에요!",
            command=self._install_launcher_update,
            width=180, height=30,
            state="disabled",
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=self._font(12, "bold")
        )
        self.update_btn.pack(pady=(4, 5), padx=20)

        ctk.CTkLabel(sidebar, text=f"런처 v{APP_VERSION}",
                     font=self._font(12, "bold"),
                     text_color=SPACE_ACCENT).pack(pady=(2, 5))

        self.account_label = ctk.CTkLabel(
            sidebar, text="로그인이 필요해요",
            font=self._font(12),
            text_color=SPACE_MUTED
        )
        self.account_label.pack(pady=3)

        self.avatar_label = ctk.CTkLabel(sidebar, text="")
        self.avatar_label.pack(pady=(8, 0))

        ctk.CTkLabel(sidebar, text="").pack(expand=True)
        ctk.CTkLabel(sidebar, text=f"✦ Minecraft {MC_VERSION}",
                     font=self._font(12),
                     text_color=SPACE_MUTED).pack(pady=5)
        ctk.CTkLabel(sidebar, text=f"✦ NeoForge {NEOFORGE_VERSION}",
                     font=self._font(12),
                     text_color=SPACE_MUTED).pack(pady=(0, 20))

        content = ctk.CTkFrame(self, corner_radius=0, fg_color=SPACE_BG)
        content.pack(side="right", fill="both", expand=True, padx=18, pady=18)

        main = ctk.CTkFrame(content, width=510, corner_radius=0, fg_color=SPACE_BG)
        main.pack(side="left", fill="both", expand=True, padx=(0, 14))
        main.pack_propagate(False)

        mod_panel = ctk.CTkFrame(
            content,
            width=520,
            fg_color=SPACE_CARD,
            corner_radius=12,
            border_width=1,
            border_color=SPACE_MUTED
        )
        mod_panel.pack(side="right", fill="both")
        mod_panel.pack_propagate(False)
        self._build_mod_search_panel(mod_panel)

        ctk.CTkLabel(main, text="✦ 우주로 떠날 준비가 됐나요?",
                     font=self._font(16, "bold"),
                     text_color=SPACE_STAR).pack(anchor="w", pady=(0, 15))

        status_card = ctk.CTkFrame(main, fg_color=SPACE_CARD,
                                   corner_radius=12,
                                   border_width=1, border_color=SPACE_MUTED)
        status_card.pack(fill="x", pady=(0, 12))

        status_header = ctk.CTkFrame(status_card, fg_color="transparent")
        status_header.pack(fill="x", padx=15, pady=(12, 8))

        ctk.CTkLabel(status_header, text="서버 상태",
                     font=self._font(14, "bold"),
                     text_color=SPACE_STAR).pack(side="left")

        self.status_refresh_btn = ctk.CTkButton(
            status_header, text="새로고침",
            command=self._refresh_server_status,
            width=78, height=26,
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=self._font(12)
        )
        self.status_refresh_btn.pack(side="right")

        self.launch_settings_btn = ctk.CTkButton(
            status_card, text="해상도 설정",
            command=self._open_launch_settings,
            width=110, height=28,
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=self._font(12, "bold")
        )
        self.launch_settings_btn.pack(anchor="e", padx=15, pady=(0, 8))

        self.server_status_label = ctk.CTkLabel(
            status_card, text="확인 중...",
            font=self._font(17, "bold"),
            text_color=SPACE_MUTED
        )
        self.server_status_label.pack(anchor="w", padx=15)

        self.server_detail_label = ctk.CTkLabel(
            status_card, text=f"{SERVER_IP}:{SERVER_PORT}",
            font=self._font(12),
            text_color=SPACE_MUTED
        )
        self.server_detail_label.pack(anchor="w", padx=15, pady=(2, 12))

        mem_card = ctk.CTkFrame(main, fg_color=SPACE_CARD,
                                 corner_radius=12,
                                 border_width=1, border_color=SPACE_MUTED)
        mem_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(mem_card, text="🖥  메모리 할당",
                     font=self._font(14, "bold"),
                     text_color=SPACE_STAR).pack(anchor="w", padx=15, pady=(12, 6))

        mem_row = ctk.CTkFrame(mem_card, fg_color="transparent")
        mem_row.pack(fill="x", padx=15, pady=(0, 12))

        self.mem_slider = ctk.CTkSlider(
            mem_row, from_=2, to=16, number_of_steps=14,
            command=self._update_mem,
            button_color=SPACE_ACCENT, button_hover_color=SPACE_ACCENT2,
            progress_color=SPACE_ACCENT2
        )
        self.mem_slider.set(self.memory_gb)
        self.mem_slider.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.mem_label = ctk.CTkLabel(mem_row, text=f"{self.memory_gb} GB", width=50,
                                       text_color=SPACE_ACCENT,
                                       font=self._font(14, "bold"))
        self.mem_label.pack(side="right")

        self.start_btn = ctk.CTkButton(
            main, text="🚀  발사!",
            height=50,
            font=self._font(18, "bold"),
            command=self._start_game,
            state="disabled",
            fg_color=SPACE_ACCENT2,
            hover_color="#6d28d9",
            corner_radius=12
        )
        self.start_btn.pack(fill="x", pady=(0, 12))

        log_card = ctk.CTkFrame(main, fg_color=SPACE_CARD,
                                  corner_radius=12,
                                  border_width=1, border_color=SPACE_MUTED)
        log_card.pack(fill="both", expand=True)

        ctk.CTkLabel(log_card, text="📡  시스템 로그",
                     font=self._font(14, "bold"),
                     text_color=SPACE_STAR).pack(anchor="w", padx=15, pady=(12, 4))

        self.log_box = ctk.CTkTextbox(
            log_card, height=120,
            font=self._font(11),
            fg_color="#07071a",
            text_color=SPACE_STAR,
            border_width=0
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_box.configure(state="disabled")

    def _update_mem(self, val):
        self.memory_gb = int(val)
        if hasattr(self, "mem_label"):
            self.mem_label.configure(text=f"{self.memory_gb} GB")
        self._save_memory_setting()

    def _load_memory_setting(self):
        try:
            settings = self._load_launcher_settings()
            memory_gb = int(settings.get("memory_gb", 4))
            return max(2, min(16, memory_gb))
        except Exception:
            return 4

    def _load_resolution_setting(self, key, default_value):
        try:
            settings = self._load_launcher_settings()
            value = int(settings.get(key, default_value))
            return max(320, min(7680, value))
        except Exception:
            return default_value

    def _load_fullscreen_setting(self):
        try:
            settings = self._load_launcher_settings()
            return bool(settings.get("fullscreen", False))
        except Exception:
            return False

    def _load_launcher_settings(self):
        if not os.path.exists(LAUNCHER_SETTINGS_FILE):
            return {}

        with open(LAUNCHER_SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_launcher_settings(self, settings):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        with open(LAUNCHER_SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=2)

    def _save_memory_setting(self):
        try:
            settings = self._load_launcher_settings()
            settings["memory_gb"] = self.memory_gb
            self._write_launcher_settings(settings)
        except Exception as e:
            self._log(f"메모리 설정 저장 실패: {e}")

    def _open_launch_settings(self):
        if hasattr(self, "launch_settings_window") and self.launch_settings_window.winfo_exists():
            self.launch_settings_window.focus()
            return

        window = ctk.CTkToplevel(self)
        self.launch_settings_window = window
        window.title("실행 설정")
        window.geometry("330x260")
        window.resizable(False, False)
        window.configure(fg_color=SPACE_BG)
        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="실행 설정",
            font=self._font(18, "bold"),
            text_color=SPACE_STAR
        ).pack(anchor="w", padx=18, pady=(18, 12))

        form = ctk.CTkFrame(
            window,
            fg_color=SPACE_CARD,
            corner_radius=12,
            border_width=1,
            border_color=SPACE_MUTED
        )
        form.pack(fill="x", padx=18, pady=(0, 12))

        self.resolution_width_var = tk.StringVar(value=str(self.resolution_width))
        self.resolution_height_var = tk.StringVar(value=str(self.resolution_height))
        self.fullscreen_var = ctk.BooleanVar(value=self.fullscreen_enabled)

        width_row = ctk.CTkFrame(form, fg_color="transparent")
        width_row.pack(fill="x", padx=14, pady=(14, 8))
        ctk.CTkLabel(width_row, text="가로", width=64,
                     font=self._font(12, "bold"),
                     text_color=SPACE_STAR).pack(side="left")
        ctk.CTkEntry(width_row, textvariable=self.resolution_width_var,
                     height=32, fg_color="#101033",
                     border_color=SPACE_MUTED,
                     text_color=SPACE_STAR,
                     font=self._font(12)).pack(side="right", fill="x", expand=True)

        height_row = ctk.CTkFrame(form, fg_color="transparent")
        height_row.pack(fill="x", padx=14, pady=(0, 10))
        ctk.CTkLabel(height_row, text="세로", width=64,
                     font=self._font(12, "bold"),
                     text_color=SPACE_STAR).pack(side="left")
        ctk.CTkEntry(height_row, textvariable=self.resolution_height_var,
                     height=32, fg_color="#101033",
                     border_color=SPACE_MUTED,
                     text_color=SPACE_STAR,
                     font=self._font(12)).pack(side="right", fill="x", expand=True)

        ctk.CTkCheckBox(
            form,
            text="전체화면으로 시작",
            variable=self.fullscreen_var,
            checkbox_width=18,
            checkbox_height=18,
            fg_color=SPACE_ACCENT2,
            hover_color="#6d28d9",
            text_color=SPACE_STAR,
            font=self._font(12)
        ).pack(anchor="w", padx=14, pady=(0, 14))

        button_row = ctk.CTkFrame(window, fg_color="transparent")
        button_row.pack(fill="x", padx=18)
        ctk.CTkButton(
            button_row, text="취소",
            command=window.destroy,
            width=86, height=34,
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=self._font(12, "bold")
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            button_row, text="저장",
            command=self._save_launch_settings_from_window,
            width=86, height=34,
            fg_color=SPACE_ACCENT2, hover_color="#6d28d9",
            font=self._font(12, "bold")
        ).pack(side="right")

    def _save_launch_settings_from_window(self):
        try:
            width = int(self.resolution_width_var.get())
            height = int(self.resolution_height_var.get())
            if width < 320 or height < 240:
                raise ValueError
            if width > 7680 or height > 4320:
                raise ValueError

            self.resolution_width = width
            self.resolution_height = height
            self.fullscreen_enabled = bool(self.fullscreen_var.get())

            settings = self._load_launcher_settings()
            settings["memory_gb"] = self.memory_gb
            settings["resolution_width"] = self.resolution_width
            settings["resolution_height"] = self.resolution_height
            settings["fullscreen"] = self.fullscreen_enabled
            self._write_launcher_settings(settings)

            mode = "전체화면" if self.fullscreen_enabled else "창모드"
            self._log(f"실행 설정 저장 완료: {self.resolution_width}x{self.resolution_height}, {mode}")
            self.launch_settings_window.destroy()
        except ValueError:
            self._log("해상도는 가로 320~7680, 세로 240~4320 사이 숫자로 입력해 주세요.")
        except Exception as e:
            self._log(f"실행 설정 저장 실패: {e}")

    def _log(self, msg):
        if threading.current_thread() is not self._main_thread:
            self.after(0, lambda: self._log(msg))
            return

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"› {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _build_mod_search_panel(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 8))

        ctk.CTkLabel(
            header,
            text="🔎  Modrinth 모드",
            font=self._font(15, "bold"),
            text_color=SPACE_STAR
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=f"{MC_VERSION} · {MODRINTH_LOADER} 호환 검색",
            font=self._font(11),
            text_color=SPACE_MUTED
        ).pack(anchor="w", pady=(2, 0))

        self.mod_tabview = ctk.CTkTabview(
            parent,
            fg_color="transparent",
            segmented_button_fg_color="#101033",
            segmented_button_selected_color=SPACE_ACCENT2,
            segmented_button_selected_hover_color="#6d28d9",
            segmented_button_unselected_color=SPACE_MUTED,
        )
        self.mod_tabview.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        search_tab = self.mod_tabview.add("검색")
        my_mods_tab = self.mod_tabview.add("내 모드")
        self.mod_tabview.set("검색")
        self.mod_tabview._segmented_button.configure(font=self._font(12, "bold"))

        search_row = ctk.CTkFrame(search_tab, fg_color="transparent")
        search_row.pack(fill="x", padx=4, pady=(6, 8))

        self.mod_search_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="비워두면 인기 모드",
            height=34,
            fg_color="#101033",
            border_color=SPACE_MUTED,
            text_color=SPACE_STAR,
            font=self._font(12)
        )
        self.mod_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.mod_search_entry.bind("<Return>", lambda _event: self._search_modrinth_mods())

        self.mod_search_action_btn = ctk.CTkButton(
            search_row,
            text="검색",
            width=62,
            height=34,
            command=self._search_modrinth_mods,
            fg_color=SPACE_ACCENT2,
            hover_color="#6d28d9",
            font=self._font(12, "bold")
        )
        self.mod_search_action_btn.pack(side="right")

        filter_row = ctk.CTkFrame(search_tab, fg_color="transparent")
        filter_row.pack(fill="x", padx=4, pady=(0, 8))

        self.mod_sort_menu = ctk.CTkOptionMenu(
            filter_row,
            values=["인기순", "관련순", "업데이트순", "최신순"],
            variable=self.mod_sort_var,
            command=lambda _value: self._reset_and_search_modrinth_mods(),
            width=112,
            height=30,
            fg_color=SPACE_MUTED,
            button_color=SPACE_ACCENT2,
            button_hover_color="#6d28d9",
            font=self._font(12),
            dropdown_font=self._font(12),
        )
        self.mod_sort_menu.pack(side="left")

        self.mod_prev_btn = ctk.CTkButton(
            filter_row,
            text="이전",
            width=58,
            height=30,
            command=lambda: self._change_mod_search_page(-1),
            fg_color=SPACE_MUTED,
            hover_color="#374151",
            font=self._font(12)
        )
        self.mod_prev_btn.pack(side="right", padx=(6, 0))

        self.mod_next_btn = ctk.CTkButton(
            filter_row,
            text="다음",
            width=58,
            height=30,
            command=lambda: self._change_mod_search_page(1),
            fg_color=SPACE_MUTED,
            hover_color="#374151",
            font=self._font(12)
        )
        self.mod_next_btn.pack(side="right")

        self.mod_search_status_label = ctk.CTkLabel(
            search_tab,
            text="인기 모드를 불러오는 중...",
            font=self._font(11),
            text_color=SPACE_MUTED,
            wraplength=470,
            justify="left"
        )
        self.mod_search_status_label.pack(anchor="w", padx=4, pady=(0, 8))

        self.mod_results_frame = ctk.CTkScrollableFrame(
            search_tab,
            fg_color="transparent",
            border_width=0,
            corner_radius=0
        )
        self.mod_results_frame.pack(fill="both", expand=True, padx=0, pady=(0, 4))

        my_mods_header = ctk.CTkFrame(my_mods_tab, fg_color="transparent")
        my_mods_header.pack(fill="x", padx=4, pady=(6, 8))
        ctk.CTkLabel(
            my_mods_header,
            text="서버 기본 모드팩에 없는 추가 모드만 표시합니다.",
            font=self._font(11),
            text_color=SPACE_MUTED,
            wraplength=330,
            justify="left"
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            my_mods_header,
            text="새로고침",
            width=78,
            height=30,
            command=self._refresh_user_mod_list,
            fg_color=SPACE_MUTED,
            hover_color="#374151",
            font=self._font(12)
        ).pack(side="right", padx=(8, 0))

        self.user_mod_status_label = ctk.CTkLabel(
            my_mods_tab,
            text="",
            font=self._font(11),
            text_color=SPACE_MUTED,
            wraplength=470,
            justify="left"
        )
        self.user_mod_status_label.pack(anchor="w", padx=4, pady=(0, 6))

        self.user_mods_frame = ctk.CTkScrollableFrame(
            my_mods_tab,
            fg_color="transparent",
            border_width=0,
            corner_radius=0
        )
        self.user_mods_frame.pack(fill="both", expand=True, padx=0, pady=(0, 4))
        self._refresh_user_mod_list()

    def _open_mod_search(self):
        self.mod_search_entry.focus()

    def _reset_and_search_modrinth_mods(self):
        self.mod_search_page = 0
        self._search_modrinth_mods()

    def _change_mod_search_page(self, delta):
        next_page = max(0, self.mod_search_page + delta)
        if next_page == self.mod_search_page:
            return
        self.mod_search_page = next_page
        self._search_modrinth_mods()

    def _search_modrinth_mods(self):
        query = self.mod_search_entry.get().strip()
        if query != self.mod_search_query:
            self.mod_search_page = 0
            self.mod_search_query = query

        self.mod_search_action_btn.configure(state="disabled", text="검색 중")
        self.mod_search_status_label.configure(text="Modrinth에서 검색 중...", text_color=SPACE_MUTED)
        self._clear_mod_search_results()
        threading.Thread(target=self._do_search_modrinth_mods, args=(query,), daemon=True).start()

    def _do_search_modrinth_mods(self, query):
        try:
            facets = json.dumps([
                [f"versions:{MC_VERSION}"],
                [f"categories:{MODRINTH_LOADER}"],
                ["project_type:mod"],
                ["client_side:required", "client_side:optional"],
            ])
            response = requests.get(
                f"{MODRINTH_API_BASE}/search",
                params={
                    "query": query,
                    "facets": facets,
                    "index": self._get_modrinth_sort_index(),
                    "limit": 20,
                    "offset": self.mod_search_page * 20,
                },
                headers=self._modrinth_headers(),
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("hits", [])
            total_hits = data.get("total_hits", 0)
            self.after(0, lambda: self._show_mod_search_results(results, total_hits))
        except Exception as e:
            self.after(0, lambda: self._set_mod_search_error(f"검색 실패: {e}"))

    def _get_modrinth_sort_index(self):
        return {
            "인기순": "downloads",
            "관련순": "relevance",
            "업데이트순": "updated",
            "최신순": "newest",
        }.get(self.mod_sort_var.get(), "downloads")

    def _show_mod_search_results(self, results, total_hits=0):
        self.mod_search_results = results
        self.mod_icon_images = {}
        self.mod_search_action_btn.configure(state="normal", text="검색")
        self.mod_prev_btn.configure(state="normal" if self.mod_search_page > 0 else "disabled")
        has_next_page = (self.mod_search_page + 1) * 20 < total_hits
        self.mod_next_btn.configure(state="normal" if has_next_page else "disabled")

        if not results:
            self.mod_search_status_label.configure(text="검색 결과가 없어요.", text_color=SPACE_MUTED)
            return

        mode = f"'{self.mod_search_query}' 검색" if self.mod_search_query else "인기 모드"
        self.mod_search_status_label.configure(
            text=f"{mode} · {self.mod_search_page + 1}페이지 · {total_hits:,}개 중 {len(results)}개",
            text_color=SPACE_GREEN
        )

        for index, result in enumerate(results):
            self._add_mod_result_row(index, result)

    def _add_mod_result_row(self, index, result):
        project_url = self._get_modrinth_project_url(result)
        row = ctk.CTkFrame(
            self.mod_results_frame,
            fg_color="#101033",
            corner_radius=8,
            border_width=1,
            border_color=SPACE_MUTED
        )
        row.pack(fill="x", padx=8, pady=6)
        row.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))

        title = result.get("title") or result.get("slug") or "이름 없음"
        description = result.get("description") or ""
        downloads = result.get("downloads", 0)
        icon_url = result.get("icon_url")

        icon_label = ctk.CTkLabel(
            row,
            text=self._get_mod_icon_placeholder(title),
            width=56,
            height=56,
            fg_color=SPACE_BG,
            corner_radius=8,
            text_color=SPACE_ACCENT
        )
        icon_label.pack(side="left", padx=(8, 0), pady=8)
        icon_label.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))
        if icon_url:
            threading.Thread(
                target=self._load_mod_icon,
                args=(icon_url, icon_label, index),
                daemon=True
            ).start()

        text_frame = ctk.CTkFrame(row, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        text_frame.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=self._font(14, "bold"),
            text_color=SPACE_STAR
        )
        title_label.pack(anchor="w")
        title_label.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))

        description_label = ctk.CTkLabel(
            text_frame,
            text=description[:150],
            font=self._font(11),
            text_color=SPACE_MUTED,
            wraplength=300,
            justify="left"
        )
        description_label.pack(anchor="w", pady=(2, 2))
        description_label.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))

        meta_label = ctk.CTkLabel(
            text_frame,
            text=f"다운로드 {downloads:,} · {result.get('author', '')}",
            font=self._font(11),
            text_color=SPACE_ACCENT
        )
        meta_label.pack(anchor="w")
        meta_label.bind("<Button-1>", lambda _event, url=project_url: webbrowser.open(url))

        install_btn = ctk.CTkButton(
            row,
            text="추가",
            width=62,
            height=32,
            command=lambda i=index: self._install_selected_modrinth_mod(i),
            fg_color=SPACE_ACCENT2,
            hover_color="#6d28d9",
            font=self._font(12, "bold")
        )
        install_btn.pack(side="right", padx=(4, 8))

    def _get_mod_icon_placeholder(self, title):
        title = (title or "").strip()
        if not title:
            return "?"
        return title[0].upper()

    def _get_modrinth_project_url(self, result):
        slug = result.get("slug") or result.get("project_id")
        return f"https://modrinth.com/mod/{slug}"

    def _load_mod_icon(self, icon_url, label, index):
        try:
            response = requests.get(icon_url, timeout=10, headers=self._modrinth_headers())
            response.raise_for_status()
            icon_bytes = response.content
            self.after(0, lambda: self._set_mod_icon(label, index, icon_bytes))
        except Exception:
            pass

    def _set_mod_icon(self, label, index, icon_bytes):
        try:
            encoded = base64.b64encode(icon_bytes).decode("ascii")
            image = tk.PhotoImage(data=encoded)
            while image.width() > 54 or image.height() > 54:
                image = image.subsample(2, 2)
            self.mod_icon_images[index] = image
            label.configure(image=image, text="")
        except Exception:
            pass

    def _clear_mod_search_results(self):
        for child in self.mod_results_frame.winfo_children():
            child.destroy()

    def _set_mod_search_error(self, message):
        self.mod_search_action_btn.configure(state="normal", text="검색")
        self.mod_search_status_label.configure(text=message, text_color=SPACE_RED)

    def _install_selected_modrinth_mod(self, index):
        if index >= len(self.mod_search_results):
            return

        project = self.mod_search_results[index]
        project_id = project.get("project_id")
        title = project.get("title") or project.get("slug") or project_id
        if not project_id:
            self.mod_search_status_label.configure(text="프로젝트 ID를 찾지 못했어요.", text_color=SPACE_RED)
            return

        self.mod_search_action_btn.configure(state="disabled", text="설치 중")
        self.mod_search_status_label.configure(text=f"{title} 설치 중...", text_color=SPACE_MUTED)
        threading.Thread(
            target=self._do_install_modrinth_mod,
            args=(project_id, title),
            daemon=True
        ).start()

    def _do_install_modrinth_mod(self, project_id, title):
        try:
            installed = []
            self._install_modrinth_project(project_id, installed, set())
            installed_text = ", ".join(installed[:4])
            if len(installed) > 4:
                installed_text += f" 외 {len(installed) - 4}개"
            self.after(0, lambda: self._finish_mod_install(f"{title} 설치 완료: {installed_text}"))
        except Exception as e:
            self.after(0, lambda: self._finish_mod_install(f"설치 실패: {e}", error=True))

    def _install_modrinth_project(self, project_id, installed, visited):
        if project_id in visited:
            return
        visited.add(project_id)

        version = self._get_modrinth_compatible_version(project_id)
        for dependency in version.get("dependencies", []):
            if dependency.get("dependency_type") != "required":
                continue
            dependency_project_id = dependency.get("project_id")
            dependency_version_id = dependency.get("version_id")
            if dependency_project_id:
                self._install_modrinth_project(dependency_project_id, installed, visited)
            elif dependency_version_id:
                dependency_version = self._get_modrinth_version(dependency_version_id)
                self._download_modrinth_version_file(dependency_version, installed)

        self._download_modrinth_version_file(version, installed)

    def _get_modrinth_compatible_version(self, project_id):
        response = requests.get(
            f"{MODRINTH_API_BASE}/project/{project_id}/version",
            params={
                "loaders": json.dumps([MODRINTH_LOADER]),
                "game_versions": json.dumps([MC_VERSION]),
            },
            headers=self._modrinth_headers(),
            timeout=15
        )
        response.raise_for_status()
        versions = response.json()
        if not versions:
            raise RuntimeError(f"{MC_VERSION} {MODRINTH_LOADER} 호환 파일이 없어요.")
        return versions[0]

    def _get_modrinth_version(self, version_id):
        response = requests.get(
            f"{MODRINTH_API_BASE}/version/{version_id}",
            headers=self._modrinth_headers(),
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    def _download_modrinth_version_file(self, version, installed):
        files = version.get("files", [])
        if not files:
            raise RuntimeError(f"{version.get('name', '모드')} 파일이 없어요.")

        file_info = next((file for file in files if file.get("primary")), files[0])
        filename = file_info.get("filename")
        url = file_info.get("url")
        if not filename or not url:
            raise RuntimeError("모드 다운로드 정보를 찾지 못했어요.")

        os.makedirs(MODS_DIR, exist_ok=True)
        target_path = os.path.join(MODS_DIR, filename)
        if os.path.exists(target_path):
            installed.append(f"{filename}(이미 있음)")
            return

        self._download_modrinth_file(url, target_path, file_info)
        installed.append(filename)

    def _download_modrinth_file(self, url, target_path, file_info):
        temp_path = target_path + ".part"
        with requests.get(url, stream=True, timeout=60, headers=self._modrinth_headers()) as response:
            response.raise_for_status()
            with open(temp_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)

        expected_sha1 = file_info.get("hashes", {}).get("sha1")
        if expected_sha1 and self._sha1(temp_path) != expected_sha1.lower():
            os.remove(temp_path)
            raise RuntimeError(f"{os.path.basename(target_path)} 검증 실패")

        os.replace(temp_path, target_path)

    def _finish_mod_install(self, message, error=False):
        self.mod_search_action_btn.configure(state="normal", text="검색")
        self.mod_search_status_label.configure(
            text=message,
            text_color=SPACE_RED if error else SPACE_GREEN
        )
        self._log(message)
        self._refresh_user_mod_list()

    def _refresh_user_mod_list(self):
        if not hasattr(self, "user_mods_frame"):
            return

        for child in self.user_mods_frame.winfo_children():
            child.destroy()

        user_mods = self._get_user_added_mod_files()
        if not user_mods:
            self.user_mod_status_label.configure(
                text="추가 모드가 없어요.",
                text_color=SPACE_MUTED
            )
            return

        self.user_mod_status_label.configure(
            text=f"추가 모드 {len(user_mods)}개",
            text_color=SPACE_GREEN
        )
        for filename in user_mods:
            self._add_user_mod_row(filename)

    def _get_user_added_mod_files(self):
        if not os.path.isdir(MODS_DIR):
            return []

        base_mods = set()
        mrpack_path = MRPACK_PATH or MRPACK_FILE
        if mrpack_path and os.path.exists(mrpack_path):
            try:
                base_mods = self._get_mrpack_mod_filenames(mrpack_path)
            except Exception:
                base_mods = set()

        return sorted(
            filename for filename in os.listdir(MODS_DIR)
            if filename.lower().endswith(".jar")
            and os.path.isfile(os.path.join(MODS_DIR, filename))
            and filename not in base_mods
        )

    def _add_user_mod_row(self, filename):
        row = ctk.CTkFrame(
            self.user_mods_frame,
            fg_color="#101033",
            corner_radius=8,
            border_width=1,
            border_color=SPACE_MUTED
        )
        row.pack(fill="x", padx=8, pady=5)

        path = os.path.join(MODS_DIR, filename)
        size_mb = os.path.getsize(path) / (1024 * 1024)

        text_frame = ctk.CTkFrame(row, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        ctk.CTkLabel(
            text_frame,
            text=filename,
            font=self._font(12, "bold"),
            text_color=SPACE_STAR,
            wraplength=330,
            justify="left"
        ).pack(anchor="w")
        ctk.CTkLabel(
            text_frame,
            text=f"{size_mb:.1f} MB",
            font=self._font(11),
            text_color=SPACE_MUTED
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(
            row,
            text="삭제",
            width=58,
            height=30,
            command=lambda name=filename: self._delete_user_mod(name),
            fg_color="#7f1d1d",
            hover_color="#991b1b",
            font=self._font(12, "bold")
        ).pack(side="right", padx=8)

    def _delete_user_mod(self, filename):
        path = os.path.join(MODS_DIR, filename)
        try:
            if not os.path.isfile(path) or not filename.lower().endswith(".jar"):
                raise RuntimeError("삭제할 모드 파일을 찾지 못했어요.")
            os.remove(path)
            self._log(f"추가 모드 삭제: {filename}")
            self._refresh_user_mod_list()
        except Exception as e:
            self.user_mod_status_label.configure(text=f"삭제 실패: {e}", text_color=SPACE_RED)

    def _modrinth_headers(self):
        return {"User-Agent": MODRINTH_USER_AGENT}

    def _check_launcher_update(self):
        threading.Thread(target=self._do_check_launcher_update, daemon=True).start()

    def _do_check_launcher_update(self):
        try:
            response = requests.get(UPDATE_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            latest = str(data.get("tag_name", "")).lstrip("v")
            if latest and self._is_newer_version(latest, APP_VERSION):
                asset = self._find_launcher_update_asset(data)
                self.available_launcher_update = {
                    "version": latest,
                    "asset": asset,
                    "page_url": data.get("html_url") or UPDATE_PAGE_URL,
                }
                self._log(f"런처 업데이트 사용 가능: v{latest}")
                if asset:
                    self._log("업데이트 버튼으로 자동 설치할 수 있어요.")
                else:
                    self._log(f"업데이트 파일을 찾지 못했어요: {UPDATE_PAGE_URL}")
                self.after(0, lambda: self._set_update_button(True, latest, bool(asset)))
            else:
                self._log(f"런처가 최신버전이에요! v{APP_VERSION}")
                self.after(0, lambda: self._set_update_button(False, APP_VERSION, False))
        except Exception as e:
            self._log(f"런처 업데이트 확인 실패: {e}")
            self.after(0, lambda: self._set_update_button(False, APP_VERSION, False))

    def _find_launcher_update_asset(self, release_data):
        assets = release_data.get("assets", [])

        if sys.platform == "win32":
            release_version = str(release_data.get("tag_name", "")).lstrip("v")
            preferred_names = (
                f"SohangLauncher-{release_version}.exe",
                *LAUNCHER_WINDOWS_ASSET_NAMES,
            )
            fallback_suffixes = (".exe",)
        elif sys.platform == "darwin":
            release_version = str(release_data.get("tag_name", "")).lstrip("v")
            arch = "arm64" if platform.machine().lower() == "arm64" else "x64"
            other_arch = "x64" if arch == "arm64" else "arm64"
            preferred_names = (
                f"SohangLauncher-{release_version}-mac-{arch}.zip",
                f"SohangLauncher-{release_version}-mac-{other_arch}.zip",
                f"SohangLauncher-mac-{arch}.zip",
                f"SohangLauncher-mac-{other_arch}.zip",
                *LAUNCHER_MAC_ASSET_NAMES,
            )
            fallback_suffixes = (".dmg", ".zip")
        else:
            preferred_names = ()
            fallback_suffixes = ()

        for asset in assets:
            if asset.get("name") in preferred_names:
                return asset
        for asset in assets:
            name = asset.get("name", "").lower()
            if name.endswith(fallback_suffixes):
                return asset
        return None

    def _set_update_button(self, update_available, version, can_auto_install):
        if update_available and can_auto_install:
            self.update_btn.configure(
                text=f"런처 업데이트 v{version}",
                state="normal",
                fg_color=SPACE_ACCENT2,
                hover_color="#6d28d9"
            )
        elif update_available:
            self.update_btn.configure(
                text=f"업데이트 v{version}",
                state="normal",
                fg_color=SPACE_MUTED,
                hover_color="#374151"
            )
        else:
            self.update_btn.configure(
                text="런처가 최신버전이에요!",
                state="disabled",
                fg_color=SPACE_MUTED,
                hover_color="#374151"
            )

    def _install_launcher_update(self):
        if not self.available_launcher_update:
            return
        threading.Thread(target=self._do_install_launcher_update, daemon=True).start()

    def _do_install_launcher_update(self):
        update = self.available_launcher_update
        asset = update.get("asset")
        if not asset:
            self._log("자동 설치용 런처 파일이 없어 릴리즈 페이지를 엽니다.")
            webbrowser.open(update.get("page_url") or UPDATE_PAGE_URL)
            return

        if not getattr(sys, "frozen", False):
            self._log("개발 모드에서는 자동 교체를 하지 않습니다. 패키징된 앱에서 동작해요.")
            webbrowser.open(update.get("page_url") or UPDATE_PAGE_URL)
            return

        if sys.platform == "darwin":
            self._do_install_macos_launcher_update(asset, update)
            return

        if sys.platform != "win32":
            self._log("이 운영체제에서는 릴리즈 페이지에서 새 앱을 받아 교체해 주세요.")
            webbrowser.open(update.get("page_url") or UPDATE_PAGE_URL)
            return

        try:
            self.after(0, lambda: self.update_btn.configure(state="disabled", text="다운로드 중..."))
            download_url = asset["browser_download_url"]
            target_exe = sys.executable
            temp_exe = os.path.join(tempfile.gettempdir(), f"sohang-launcher-update-{update['version']}.exe")
            self._download_launcher_asset(download_url, temp_exe)
            script_path = self._write_windows_updater_script(temp_exe, target_exe)
            self._log("업데이트 파일 다운로드 완료. 런처를 재시작합니다.")
            subprocess.Popen(
                ["cmd", "/c", script_path],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            self.after(500, self.destroy)
        except Exception as e:
            self._log(f"런처 자동 업데이트 실패: {e}")
            self.after(0, lambda: self.update_btn.configure(state="normal", text="업데이트 재시도"))

    def _do_install_macos_launcher_update(self, asset, update):
        if not asset.get("name", "").lower().endswith(".zip"):
            self._log("macOS 자동 업데이트는 zip asset만 지원합니다. 릴리즈 페이지를 엽니다.")
            webbrowser.open(update.get("page_url") or UPDATE_PAGE_URL)
            return

        app_path = self._get_current_macos_app_path()
        if not app_path:
            self._log("현재 macOS 앱 경로를 찾지 못해 릴리즈 페이지를 엽니다.")
            webbrowser.open(update.get("page_url") or UPDATE_PAGE_URL)
            return

        try:
            self.after(0, lambda: self.update_btn.configure(state="disabled", text="다운로드 중..."))
            temp_zip = os.path.join(tempfile.gettempdir(), f"sohang-launcher-mac-update-{update['version']}.zip")
            self._download_launcher_asset(asset["browser_download_url"], temp_zip)
            script_path = self._write_macos_updater_script(temp_zip, app_path)
            self._log("업데이트 파일 다운로드 완료. 런처를 재시작합니다.")
            subprocess.Popen(["/bin/bash", script_path])
            self.after(500, self.destroy)
        except Exception as e:
            self._log(f"macOS 런처 자동 업데이트 실패: {e}")
            self.after(0, lambda: self.update_btn.configure(state="normal", text="업데이트 재시도"))

    def _get_current_macos_app_path(self):
        path = os.path.abspath(sys.executable)
        while path and path != os.path.dirname(path):
            if path.endswith(".app"):
                return path
            path = os.path.dirname(path)
        return None

    def _write_macos_updater_script(self, source_zip, target_app):
        script_path = os.path.join(tempfile.gettempdir(), "sohang-launcher-updater.sh")
        extract_dir = os.path.join(tempfile.gettempdir(), f"sohang-launcher-mac-update-{os.getpid()}")
        pid = os.getpid()
        script = f"""#!/bin/bash
set -u
SOURCE_ZIP={source_zip!r}
TARGET_APP={target_app!r}
EXTRACT_DIR={extract_dir!r}
PID={pid}
while kill -0 "$PID" >/dev/null 2>&1; do
  sleep 1
done
rm -rf "$EXTRACT_DIR"
mkdir -p "$EXTRACT_DIR"
ditto -x -k "$SOURCE_ZIP" "$EXTRACT_DIR"
NEW_APP="$(find "$EXTRACT_DIR" -maxdepth 1 -name '*.app' -type d | head -n 1)"
if [ -z "$NEW_APP" ]; then
  open "$(dirname "$TARGET_APP")"
  exit 1
fi
rm -rf "$TARGET_APP"
ditto "$NEW_APP" "$TARGET_APP"
open "$TARGET_APP"
rm -rf "$EXTRACT_DIR" "$SOURCE_ZIP"
rm -f "$0"
"""
        with open(script_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(script)
        os.chmod(script_path, 0o755)
        return script_path

    def _download_launcher_asset(self, url, target_path):
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "html" in content_type.lower():
                raise RuntimeError("런처 파일 대신 HTML 페이지를 받았어요. 릴리즈 asset을 확인해 주세요.")
            with open(target_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)

        if os.path.getsize(target_path) < 1024 * 100:
            raise RuntimeError("다운로드한 런처 파일이 너무 작아요.")

    def _write_windows_updater_script(self, source_exe, target_exe):
        script_path = os.path.join(tempfile.gettempdir(), "sohang-launcher-updater.bat")
        pid = os.getpid()
        target_dir = os.path.dirname(target_exe)
        backup_exe = os.path.join(
            tempfile.gettempdir(),
            f"sohang-launcher-backup-{pid}.exe"
        )
        script = f"""@echo off
setlocal
set "SOURCE={source_exe}"
set "TARGET={target_exe}"
set "TARGET_DIR={target_dir}"
set "BACKUP={backup_exe}"
set "PID={pid}"
:wait
tasklist /FI "PID eq %PID%" | find "%PID%" >nul
if not errorlevel 1 (
  timeout /t 1 /nobreak >nul
  goto wait
)
timeout /t 3 /nobreak >nul
set "TRY=0"
:replace
set /A TRY+=1
if exist "%BACKUP%" del "%BACKUP%" >nul 2>nul
if exist "%TARGET%" move /Y "%TARGET%" "%BACKUP%" >nul 2>nul
if exist "%TARGET%" (
  if %TRY% GEQ 30 goto failed
  timeout /t 1 /nobreak >nul
  goto replace
)
copy /Y "%SOURCE%" "%TARGET%" >nul 2>nul
if exist "%TARGET%" goto copied
if %TRY% GEQ 30 goto failed
timeout /t 1 /nobreak >nul
goto replace
:copied
timeout /t 2 /nobreak >nul
start "" /D "%TARGET_DIR%" "%TARGET%"
del "%SOURCE%" >nul 2>nul
del "%BACKUP%" >nul 2>nul
del "%~f0" >nul 2>nul
exit /b 0
:failed
if exist "%BACKUP%" move /Y "%BACKUP%" "%TARGET%" >nul
echo Update failed. Could not replace launcher.
pause
"""
        with open(script_path, "w", encoding="utf-8") as file:
            file.write(script)
        return script_path

    def _is_newer_version(self, latest, current):
        def normalize(version):
            parts = []
            for part in version.split("."):
                digits = "".join(ch for ch in part if ch.isdigit())
                parts.append(int(digits or 0))
            return parts

        latest_parts = normalize(latest)
        current_parts = normalize(current)
        length = max(len(latest_parts), len(current_parts))
        latest_parts += [0] * (length - len(latest_parts))
        current_parts += [0] * (length - len(current_parts))
        return latest_parts > current_parts

    def _refresh_server_status(self):
        self.server_status_label.configure(text="확인 중...", text_color=SPACE_MUTED)
        self.server_detail_label.configure(text=f"{SERVER_IP}:{SERVER_PORT}")
        self.status_refresh_btn.configure(state="disabled")
        threading.Thread(target=self._check_server_status, daemon=True).start()

    def _check_server_status(self):
        try:
            status = self._ping_minecraft_server(SERVER_IP, int(SERVER_PORT))
            players = status.get("players", {})
            online = players.get("online", 0)
            max_players = players.get("max", 0)
            version = status.get("version", {}).get("name", "알 수 없음")

            self.after(0, lambda: self._set_server_status(
                "온라인",
                f"{SERVER_IP}:{SERVER_PORT}  |  {online}/{max_players}명  |  {version}",
                SPACE_GREEN
            ))
        except Exception as e:
            error_message = str(e)
            self.after(0, lambda: self._set_server_status(
                "오프라인",
                f"{SERVER_IP}:{SERVER_PORT}  |  {error_message}",
                SPACE_RED
            ))

    def _set_server_status(self, status, detail, color):
        self.server_status_label.configure(text=status, text_color=color)
        self.server_detail_label.configure(text=detail)
        self.status_refresh_btn.configure(state="normal")

    def _ping_minecraft_server(self, host, port):
        with socket.create_connection((host, port), timeout=4) as sock:
            sock.settimeout(4)
            handshake = (
                self._encode_varint(SERVER_PROTOCOL_VERSION)
                + self._pack_string(host)
                + struct.pack(">H", port)
                + self._encode_varint(1)
            )
            self._send_packet(sock, 0, handshake)
            self._send_packet(sock, 0)

            self._read_varint(sock)
            packet_id = self._read_varint(sock)
            if packet_id != 0:
                raise RuntimeError("상태 응답이 올바르지 않아요.")

            response_length = self._read_varint(sock)
            response = self._read_exact(sock, response_length).decode("utf-8")
            return json.loads(response)

    def _send_packet(self, sock, packet_id, data=b""):
        packet = self._encode_varint(packet_id) + data
        sock.sendall(self._encode_varint(len(packet)) + packet)

    def _pack_string(self, value):
        encoded = value.encode("utf-8")
        return self._encode_varint(len(encoded)) + encoded

    def _encode_varint(self, value):
        result = bytearray()
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                result.append(byte | 0x80)
            else:
                result.append(byte)
                return bytes(result)

    def _read_varint(self, sock):
        value = 0
        for position in range(5):
            byte = self._read_exact(sock, 1)[0]
            value |= (byte & 0x7F) << (7 * position)
            if not byte & 0x80:
                return value
        raise RuntimeError("서버 응답이 너무 깁니다.")

    def _read_exact(self, sock, length):
        data = bytearray()
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise RuntimeError("서버 연결이 끊겼어요.")
            data.extend(chunk)
        return bytes(data)

    def _login(self):
        self.login_btn.configure(state="disabled", text="연결 중...")
        threading.Thread(target=self._do_login, daemon=True).start()

    def _try_auto_login(self):
        auth_cache = self._load_auth_cache()
        refresh_token = self._get_cached_refresh_token(auth_cache)
        if not refresh_token:
            return

        self.remember_login_var.set(True)
        self.login_btn.configure(state="disabled", text="자동 로그인 중...")
        self._log("저장된 계정으로 자동 로그인 중...")
        threading.Thread(
            target=self._do_auto_login,
            args=(refresh_token,),
            daemon=True
        ).start()

    def _do_auto_login(self, refresh_token):
        try:
            token_data = self._refresh_microsoft_token(refresh_token)
            self._complete_login_from_microsoft_token(token_data)
        except Exception as e:
            self._delete_auth_cache()
            self._log(f"자동 로그인 실패: {e}")
            self.after(0, lambda: self.login_btn.configure(
                state="normal", text="Microsoft 로그인"))

    def _on_remember_login_changed(self):
        if not self.remember_login_var.get():
            self._delete_auth_cache()
            if self.account:
                self._log("자동 로그인을 껐어요. 현재 로그인은 유지됩니다.")
        elif self.account:
            self._save_auth_cache(self.account)
            self._log("자동 로그인을 켰어요.")

    def _refresh_microsoft_token(self, refresh_token):
        response = requests.post(TOKEN_URL, data={
            "client_id": CLIENT_ID,
            "scope": MICROSOFT_SCOPE,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }, timeout=15)
        token_data = response.json()
        if "access_token" not in token_data:
            raise RuntimeError(token_data.get("error_description", token_data))
        return token_data

    def _do_login(self):
        try:
            self._log("마이크로소프트 디바이스 인증을 준비 중...")
            device_data = self._request_device_code()
            user_code = device_data["user_code"]
            verify_url = device_data["verification_uri"]

            self._log(f"브라우저에서 코드 {user_code} 를 입력해 주세요.")
            webbrowser.open(verify_url)
            self.after(0, lambda: self._show_device_code(user_code, verify_url))
            self._process_device_login(device_data)
        except Exception as e:
            self._log(f"오류: {e}")
            self.after(0, lambda: self.login_btn.configure(
                state="normal", text="Microsoft 로그인"))

    def _show_device_code(self, user_code, verify_url):
        ctk.CTkInputDialog(
            text=f"브라우저에서 아래 코드를 입력하고 로그인하세요.\n\n{user_code}\n\n주소: {verify_url}\n\n로그인이 끝나면 이 창은 닫아도 됩니다.",
            title="Microsoft 인증 코드"
        )

    def _request_device_code(self):
        if CLIENT_ID == DEFAULT_OLD_CLIENT_ID:
            raise RuntimeError(
                "현재 CLIENT_ID는 예전 예제용 ID라 새 인증 방식에서 사용할 수 없어요. "
                "Azure Portal에서 만든 앱의 Application (client) ID로 CLIENT_ID를 바꿔 주세요."
            )

        response = requests.post(DEVICE_CODE_URL, data={
            "client_id": CLIENT_ID,
            "scope": MICROSOFT_SCOPE,
        }, timeout=15)
        data = response.json()
        if "device_code" not in data:
            raise RuntimeError(data.get("error_description", data))
        return data

    def _process_device_login(self, device_data):
        interval = int(device_data.get("interval", 5))
        expires_at = time.time() + int(device_data.get("expires_in", 900))

        while time.time() < expires_at:
            time.sleep(interval)
            token_response = requests.post(TOKEN_URL, data={
                "client_id": CLIENT_ID,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_data["device_code"],
            }, timeout=15)
            token_data = token_response.json()

            if token_data.get("error") == "authorization_pending":
                continue
            if token_data.get("error") == "slow_down":
                interval += 5
                continue
            if "access_token" not in token_data:
                raise RuntimeError(token_data.get("error_description", token_data))

            self._complete_login_from_microsoft_token(token_data)
            return

        raise RuntimeError("인증 시간이 만료됐어요. 다시 로그인해 주세요.")

    def _complete_login_from_microsoft_token(self, token_data):
        try:
            self._log("Microsoft 로그인 완료. Xbox Live 인증 중...")

            xbl_request = authenticate_with_xbl(token_data["access_token"])
            if "Token" not in xbl_request:
                raise RuntimeError(self._format_auth_service_error("Xbox Live", xbl_request))
            xbl_token = xbl_request["Token"]
            userhash = xbl_request["DisplayClaims"]["xui"][0]["uhs"]

            self._log("Xbox Live 인증 완료. Minecraft 인증 중...")
            xsts_request = authenticate_with_xsts(xbl_token)
            if "Token" not in xsts_request:
                raise RuntimeError(self._format_auth_service_error("XSTS", xsts_request))
            xsts_token = xsts_request["Token"]

            self._log("Minecraft Java 프로필 확인 중...")
            account_request = self._authenticate_with_minecraft_services(userhash, xsts_token)
            if "access_token" not in account_request:
                raise RuntimeError(self._format_minecraft_auth_error(account_request))

            profile = get_profile(account_request["access_token"])
            if profile.get("error") == "NOT_FOUND":
                raise RuntimeError("이 Microsoft 계정은 Minecraft Java Edition을 소유하고 있지 않아요.")

            profile["access_token"] = account_request["access_token"]
            profile["refresh_token"] = token_data.get("refresh_token")
            self.account = profile
            if self.remember_login_var.get():
                self._save_auth_cache(profile)
            else:
                self._delete_auth_cache()

            name = self.account["name"]
            self._log(f"로그인 성공! 안녕하세요, {name}님 🌟")

            self._load_account_avatar(self.account["id"])
            self.after(0, lambda: self.account_label.configure(
                text=f"✦ {name}", text_color=SPACE_GREEN))
            self.after(0, lambda: self.login_btn.configure(
                text="로그아웃 / 계정 변경", command=self._logout, state="normal",
                fg_color=SPACE_MUTED, hover_color="#374151"))
            self.after(0, lambda: self.start_btn.configure(state="normal"))

        except Exception as e:
            self._delete_auth_cache()
            self._log(f"로그인 실패: {e}")
            self.after(0, lambda: self.login_btn.configure(
                state="normal", text="Microsoft 로그인"))

    def _authenticate_with_minecraft_services(self, userhash, xsts_token):
        last_error = None
        for attempt in range(1, 4):
            try:
                response = requests.post(
                    MINECRAFT_LOGIN_URL,
                    json={"identityToken": f"XBL3.0 x={userhash};{xsts_token}"},
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "User-Agent": MODRINTH_USER_AGENT,
                    },
                    timeout=20
                )
                try:
                    data = response.json()
                except ValueError:
                    data = {"raw": response.text[:500]}

                if response.status_code >= 400:
                    data["_status_code"] = response.status_code
                    data["_url"] = MINECRAFT_LOGIN_URL
                    if response.status_code == 429 or response.status_code >= 500:
                        last_error = data
                        if attempt < 3:
                            self._log(f"Minecraft 인증 서버 응답 불안정 HTTP {response.status_code}. 재시도 {attempt}/3...")
                            time.sleep(2 * attempt)
                            continue
                return data
            except requests.RequestException as e:
                last_error = {
                    "_status_code": "network",
                    "_url": MINECRAFT_LOGIN_URL,
                    "raw": str(e),
                }
                if attempt < 3:
                    self._log(f"Minecraft 인증 서버 연결 실패. 재시도 {attempt}/3...")
                    time.sleep(2 * attempt)
                    continue

        return last_error or {"error": "unknown_minecraft_auth_error"}

    def _format_minecraft_auth_error(self, response):
        status_code = response.get("_status_code")
        error_message = (
            response.get("errorMessage")
            or response.get("message")
            or response.get("error")
            or response.get("raw")
            or response
        )

        if isinstance(error_message, str) and "Invalid app registration" in error_message:
            return (
                "Minecraft API 앱 등록이 거부됐어요. Azure 앱 승인 상태와 CLIENT_ID를 다시 확인해 주세요. "
                "승인받은 앱 ID와 런처 CLIENT_ID가 같아야 합니다."
            )

        if status_code == 401:
            return "Minecraft 인증 실패: Microsoft/Xbox 세션이 만료됐어요. 로그아웃 후 다시 로그인해 주세요."
        if status_code == 403:
            return (
                "Minecraft 인증 실패: Minecraft Services가 이 앱 또는 계정 요청을 거부했어요. "
                "공식 런처/Modrinth가 되는데 우리 런처만 실패하면 Azure App ID 승인 상태를 확인해야 합니다."
            )
        if status_code == 429:
            return "Minecraft 인증 실패: HTTP 429 요청이 너무 많아요. 잠시 후 다시 시도해 주세요."
        if status_code and status_code >= 500:
            return f"Minecraft 인증 서버 오류입니다. HTTP {status_code}. 잠시 후 다시 시도해 주세요."
        if status_code == "network":
            return f"Minecraft 인증 서버에 연결하지 못했어요: {error_message}"

        if isinstance(error_message, dict) and error_message.get("path") == "/authentication/login_with_xbox":
            return (
                "Minecraft 인증 실패: Minecraft Services가 login_with_xbox 요청을 거부했지만 자세한 사유를 주지 않았어요. "
                "공식 런처/Modrinth가 정상이라면 Azure App ID 승인 상태를 다시 확인해 주세요."
            )

        return f"Minecraft 인증 실패: HTTP {status_code or '알 수 없음'} / {error_message}"

    def _format_auth_service_error(self, service_name, response):
        xerr = response.get("XErr")
        if xerr == 2148916233:
            return f"{service_name} 인증 실패: 이 Microsoft 계정에 Xbox 프로필이 없어요. xbox.com에 한 번 로그인한 뒤 다시 시도해 주세요."
        if xerr == 2148916235:
            return f"{service_name} 인증 실패: 이 지역에서는 Xbox Live를 사용할 수 없어요."
        if xerr == 2148916236:
            return f"{service_name} 인증 실패: 보호자 또는 성인 인증이 필요한 계정이에요."
        if xerr == 2148916237:
            return f"{service_name} 인증 실패: 미성년자 계정은 가족 그룹의 보호자 허용이 필요해요."
        if xerr == 2148916238:
            return f"{service_name} 인증 실패: 이 계정은 온라인 멀티플레이 권한이 꺼져 있어요."

        message = response.get("Message") or response.get("error_description") or response
        return f"{service_name} 인증 실패: {message}"

    def _load_auth_cache(self):
        try:
            with open(AUTH_CACHE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _get_cached_refresh_token(self, auth_cache):
        refresh_token = auth_cache.get("refresh_token")
        if not refresh_token:
            return None

        protection = auth_cache.get("token_protection", "plain")
        if protection == "dpapi":
            return self._unprotect_secret(refresh_token)
        if protection == "plain":
            return refresh_token

        self._delete_auth_cache()
        return None

    def _save_auth_cache(self, profile):
        refresh_token = profile.get("refresh_token")
        if not refresh_token:
            return

        protected_token, protection = self._protect_secret(refresh_token)
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        with open(AUTH_CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump({
                "name": profile.get("name"),
                "id": profile.get("id"),
                "refresh_token": protected_token,
                "token_protection": protection,
            }, file)
        try:
            os.chmod(AUTH_CACHE_FILE, 0o600)
        except OSError:
            pass

    def _protect_secret(self, value):
        if sys.platform == "win32":
            return self._dpapi_protect(value), "dpapi"
        if sys.platform == "darwin":
            self._keychain_store(value)
            return KEYCHAIN_ACCOUNT, "keychain"
        return value, "plain"

    def _unprotect_secret(self, value):
        if sys.platform == "win32":
            return self._dpapi_unprotect(value)
        if sys.platform == "darwin":
            return self._keychain_load(value)
        return value

    def _keychain_store(self, value):
        subprocess.run(
            [
                "security", "add-generic-password",
                "-U",
                "-s", KEYCHAIN_SERVICE,
                "-a", KEYCHAIN_ACCOUNT,
                "-w", value,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _keychain_load(self, account):
        result = subprocess.run(
            [
                "security", "find-generic-password",
                "-w",
                "-s", KEYCHAIN_SERVICE,
                "-a", account,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return result.stdout.strip()

    def _keychain_delete(self):
        if sys.platform != "darwin":
            return
        subprocess.run(
            [
                "security", "delete-generic-password",
                "-s", KEYCHAIN_SERVICE,
                "-a", KEYCHAIN_ACCOUNT,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    class _DataBlob(ctypes.Structure):
        _fields_ = [
            ("cbData", ctypes.c_ulong),
            ("pbData", ctypes.POINTER(ctypes.c_char)),
        ]

    def _dpapi_protect(self, value):
        data = value.encode("utf-8")
        in_blob = self._DataBlob(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_char)))
        out_blob = self._DataBlob()
        if not ctypes.windll.crypt32.CryptProtectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)
        ):
            raise ctypes.WinError()
        try:
            protected = ctypes.string_at(out_blob.pbData, out_blob.cbData)
            return base64.b64encode(protected).decode("ascii")
        finally:
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)

    def _dpapi_unprotect(self, value):
        data = base64.b64decode(value.encode("ascii"))
        in_blob = self._DataBlob(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_char)))
        out_blob = self._DataBlob()
        if not ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)
        ):
            raise ctypes.WinError()
        try:
            return ctypes.string_at(out_blob.pbData, out_blob.cbData).decode("utf-8")
        finally:
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)

    def _delete_auth_cache(self):
        self._keychain_delete()
        try:
            os.remove(AUTH_CACHE_FILE)
        except FileNotFoundError:
            pass

    def _load_account_avatar(self, uuid):
        try:
            os.makedirs(AVATAR_CACHE_DIR, exist_ok=True)
            clean_uuid = uuid.replace("-", "")
            avatar_path = os.path.join(AVATAR_CACHE_DIR, f"{clean_uuid}.png")
            avatar_urls = [
                f"https://mc-heads.net/avatar/{clean_uuid}/64",
                f"https://minotar.net/helm/{clean_uuid}/64.png",
                f"https://crafatar.com/avatars/{clean_uuid}?overlay=true&size=64",
            ]

            response = None
            for avatar_url in avatar_urls:
                try:
                    current_response = requests.get(avatar_url, timeout=10)
                    current_response.raise_for_status()
                    if "image" in current_response.headers.get("content-type", ""):
                        response = current_response
                        break
                except requests.RequestException:
                    continue

            if response is None:
                raise RuntimeError("사용 가능한 스킨 아이콘 서버가 없어요.")

            with open(avatar_path, "wb") as file:
                file.write(response.content)

            self.after(0, lambda: self._set_account_avatar(avatar_path))
        except Exception as e:
            self._log(f"스킨 아이콘을 불러오지 못했어요: {e}")

    def _set_account_avatar(self, avatar_path):
        self.avatar_image = tk.PhotoImage(file=avatar_path)
        self.avatar_label.configure(image=self.avatar_image, text="")

    def _logout(self):
        self.account = None
        self._delete_auth_cache()
        self.avatar_image = None
        self.avatar_label.configure(image=None, text="")
        self.account_label.configure(text="로그인이 필요해요", text_color=SPACE_MUTED)
        self.login_btn.configure(
            text="Microsoft 로그인", command=self._login,
            fg_color=SPACE_ACCENT2, hover_color="#6d28d9")
        self.start_btn.configure(state="disabled")
        self._log("로그아웃 완료")

    def _sync_server_mods(self):
        if MRPACK_PATH or MRPACK_URL:
            mrpack_path = self._prepare_mrpack()
            state = self._load_install_state()
            managed_mods = self._get_mrpack_mod_filenames(mrpack_path)
            if self._is_initial_mod_setup_done(state) and not self._last_mrpack_changed:
                self._log("모드팩은 이미 준비되어 있어요. 개인 모드와 설정은 건드리지 않습니다.")
                return

            self._remove_retired_server_mods(managed_mods, state)
            self._remove_existing_server_mods_for_refresh(managed_mods)
            self._install_mrpack(mrpack_path)
            self._mark_initial_mod_setup_done(managed_mods)
            return

        os.makedirs(MODS_DIR, exist_ok=True)
        server_mods = self._get_server_mods()
        managed_mods = self._get_server_mod_filenames(server_mods)
        state = self._load_install_state()

        if not server_mods:
            self._log("서버 모드 목록이 비어 있어요. SERVER_MODS에 모드 URL을 추가해 주세요.")
            return

        if self._is_initial_mod_setup_done(state):
            self._log("서버 모드는 이미 준비되어 있어요. 개인 모드는 건드리지 않습니다.")
            return

        self._remove_retired_server_mods(managed_mods, state)
        self._remove_existing_server_mods_for_refresh(managed_mods)
        self._log("서버 모드 확인 중...")
        for mod in server_mods:
            self._download_server_mod(mod)
        self._mark_initial_mod_setup_done(managed_mods)
        self._log("서버 모드 준비 완료!")

    def _install_mrpack(self, mrpack_path):
        callback = {
            "setStatus": lambda s: self._log(s),
            "setProgress": lambda c: None,
            "setMax": lambda m: None,
        }
        self._log("Modrinth 모드팩 설치 중...")
        minecraft_launcher_lib.mrpack.install_mrpack(
            mrpack_path,
            MINECRAFT_DIR,
            callback=callback,
            mrpack_install_options={"skipDependenciesInstall": True}
        )
        self._install_mrpack_dependencies(mrpack_path, callback)
        self._log("Modrinth 모드팩 설치 완료!")

    def _is_initial_mod_setup_done(self, state=None):
        if state is None:
            state = self._load_install_state()
        if not self._has_user_mod_files():
            return False

        if self._is_install_state_current(state):
            return True

        if state.get("initial_mod_setup_done"):
            old_version = state.get("minecraft_version") or "이전 버전"
            self._log(f"서버 버전 변경 감지: {old_version} -> {MC_VERSION}")
            self._log("새 서버 모드팩을 한 번 적용합니다. 개인 모드와 설정은 유지됩니다.")
        return False

    def _current_install_signature(self):
        return {
            "minecraft_version": MC_VERSION,
            "neoforge_version": NEOFORGE_VERSION,
            "java_major": REQUIRED_JAVA_MAJOR,
            "mod_loader": MODRINTH_LOADER,
        }

    def _is_install_state_current(self, state):
        if not state.get("initial_mod_setup_done"):
            return False

        for key, value in self._current_install_signature().items():
            if state.get(key) != value:
                return False

        return True

    def _has_user_mod_files(self):
        if not os.path.isdir(MODS_DIR):
            return False

        return any(
            filename.lower().endswith(".jar")
            for filename in os.listdir(MODS_DIR)
            if os.path.isfile(os.path.join(MODS_DIR, filename))
        )

    def _load_install_state(self):
        try:
            with open(INSTALL_STATE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _mark_initial_mod_setup_done(self, managed_server_mods=None):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        state = self._load_install_state()
        state["initial_mod_setup_done"] = True
        state["updated_at"] = int(time.time())
        state["preserve_user_mods"] = True
        if managed_server_mods is not None:
            state["managed_server_mods"] = sorted(managed_server_mods)
        state.update(self._current_install_signature())
        with open(INSTALL_STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)

    def _remove_retired_server_mods(self, current_server_mods, state):
        previous_server_mods = set(state.get("managed_server_mods", []))
        if not previous_server_mods or not os.path.isdir(MODS_DIR):
            return

        retired_mods = previous_server_mods - set(current_server_mods)
        for filename in sorted(retired_mods):
            path = os.path.join(MODS_DIR, filename)
            if os.path.isfile(path) and filename.lower().endswith(".jar"):
                os.remove(path)
                self._log(f"이전 서버 모드 제거: {filename}")

    def _remove_existing_server_mods_for_refresh(self, current_server_mods):
        if not os.path.isdir(MODS_DIR):
            return

        for filename in sorted(set(current_server_mods)):
            path = os.path.join(MODS_DIR, filename)
            if os.path.isfile(path) and filename.lower().endswith(".jar"):
                os.remove(path)
                self._log(f"서버 모드 갱신 준비: {filename}")

    def _install_mrpack_dependencies(self, mrpack_path, callback):
        dependencies = self._get_mrpack_dependencies(mrpack_path)
        minecraft_version = dependencies.get("minecraft")
        if not minecraft_version:
            raise RuntimeError("mrpack에 Minecraft 버전 정보가 없어요.")
        if minecraft_version != MC_VERSION:
            raise RuntimeError(
                f"mrpack Minecraft 버전이 런처 설정과 달라요: {minecraft_version} != {MC_VERSION}")

        neoforge_version = dependencies.get("neoforge")
        if neoforge_version and neoforge_version != NEOFORGE_VERSION:
            raise RuntimeError(
                f"mrpack NeoForge 버전이 런처 설정과 달라요: {neoforge_version} != {NEOFORGE_VERSION}")

        self._log(f"Minecraft {minecraft_version} 설치 확인 중...")
        minecraft_launcher_lib.install.install_minecraft_version(
            minecraft_version, MINECRAFT_DIR, callback)

        java_path = self._ensure_java_runtime(minecraft_version, callback)

        loader_map = {
            "forge": "forge",
            "neoforge": "neoforge",
            "fabric-loader": "fabric",
            "quilt-loader": "quilt",
        }
        for dependency_name, loader_id in loader_map.items():
            loader_version = dependencies.get(dependency_name)
            if not loader_version:
                continue

            if loader_id == "neoforge":
                self._ensure_neoforge_installed(
                    minecraft_version,
                    loader_version,
                    callback,
                    java_path
                )
                continue

            loader = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)
            self._log(f"{loader.get_name()} {loader_version} 설치 확인 중...")
            loader.install(
                minecraft_version,
                MINECRAFT_DIR,
                loader_version=loader_version,
                callback=callback,
                java=java_path
            )

    def _get_neoforge_installed_version(self, loader_version):
        return f"neoforge-{loader_version}"

    def _get_neoforge_installer_url(self, loader_version):
        return (
            "https://maven.neoforged.net/releases/net/neoforged/neoforge/"
            f"{loader_version}/neoforge-{loader_version}-installer.jar"
        )

    def _ensure_neoforge_installed(self, minecraft_version, loader_version, callback, java_path):
        installed_version = self._get_neoforge_installed_version(loader_version)
        installed = [v["id"] for v in
                     minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)]
        if installed_version in installed:
            if self._is_neoforge_install_valid(loader_version):
                self._log(f"NeoForge {loader_version} 설치 확인 완료")
                return installed_version

            self._log("NeoForge 설치 파일 손상 감지. NeoForge를 다시 설치합니다.")
            self._remove_neoforge_install(loader_version, installed_version)

        self._log(f"NeoForge {loader_version} 설치 중...")
        try:
            loader = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
            loader.install(
                minecraft_version,
                MINECRAFT_DIR,
                loader_version=loader_version,
                callback=callback,
                java=java_path
            )
        except Exception as e:
            self._log(f"기본 NeoForge 설치 방식 실패: {e}")
            self._install_neoforge_from_installer(loader_version, java_path)

        installed = [v["id"] for v in
                     minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)]
        if installed_version not in installed:
            raise RuntimeError(f"NeoForge 설치 후 버전 정보를 찾을 수 없어요: {installed_version}")
        if not self._is_neoforge_install_valid(loader_version):
            raise RuntimeError("NeoForge 설치 후 patched client jar가 올바르지 않아요.")

        self._log("NeoForge 설치 완료!")
        return installed_version

    def _is_neoforge_install_valid(self, loader_version):
        patched_client_path = self._get_neoforge_patched_client_path(loader_version)
        if not os.path.isfile(patched_client_path):
            return False

        try:
            with zipfile.ZipFile(patched_client_path, "r") as jar:
                return jar.testzip() is None
        except zipfile.BadZipFile:
            return False

    def _get_neoforge_patched_client_path(self, loader_version):
        return os.path.join(
            MINECRAFT_DIR,
            "libraries",
            "net",
            "neoforged",
            "minecraft-client-patched",
            loader_version,
            f"minecraft-client-patched-{loader_version}.jar"
        )

    def _remove_neoforge_install(self, loader_version, installed_version):
        paths = [
            os.path.dirname(self._get_neoforge_patched_client_path(loader_version)),
            os.path.join(MINECRAFT_DIR, "versions", installed_version),
        ]
        for path in paths:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                self._log(f"손상된 NeoForge 파일 제거: {path}")

    def _install_neoforge_from_installer(self, loader_version, java_path):
        installer_url = self._get_neoforge_installer_url(loader_version)
        self._ensure_launcher_profiles_file()
        with tempfile.TemporaryDirectory(prefix="sohang-neoforge-") as temp_dir:
            installer_path = os.path.join(temp_dir, "neoforge-installer.jar")
            self._log("NeoForge installer 다운로드 중...")
            response = requests.get(installer_url, timeout=60)
            response.raise_for_status()
            with open(installer_path, "wb") as file:
                file.write(response.content)

            self._log("NeoForge installer 실행 중...")
            result = subprocess.run(
                [java_path, "-jar", installer_path, "--install-client", MINECRAFT_DIR],
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            if result.returncode != 0:
                if result.stdout:
                    self._log(result.stdout[-800:])
                raise RuntimeError(f"NeoForge installer 실패: 종료 코드 {result.returncode}")

    def _ensure_launcher_profiles_file(self):
        profiles_path = os.path.join(MINECRAFT_DIR, "launcher_profiles.json")
        if os.path.exists(profiles_path):
            return

        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        with open(profiles_path, "w", encoding="utf-8") as file:
            json.dump(
                {"profiles": {}, "settings": {}, "version": 3},
                file,
                ensure_ascii=False,
                indent=4
            )
        self._log("Minecraft launcher profile 준비 완료")

    def _ensure_java_runtime(self, minecraft_version, callback):
        runtime_info = minecraft_launcher_lib.runtime.get_version_runtime_information(
            minecraft_version, MINECRAFT_DIR)
        if runtime_info is None:
            return "java"

        runtime_name = runtime_info["name"]
        self._log(f"Java {REQUIRED_JAVA_MAJOR} 런타임 확인 중... ({runtime_name})")
        minecraft_launcher_lib.runtime.install_jvm_runtime(
            runtime_name, MINECRAFT_DIR, callback=callback)

        java_path = minecraft_launcher_lib.runtime.get_executable_path(
            runtime_name, MINECRAFT_DIR)
        if java_path is None:
            raise RuntimeError(f"Java 런타임 실행 파일을 찾을 수 없어요: {runtime_name}")
        return java_path

    def _clean_mods_for_mrpack(self, mrpack_path):
        if not os.path.isdir(MODS_DIR):
            return

        expected_mods = self._get_mrpack_mod_filenames(mrpack_path)
        if not expected_mods:
            return

        for filename in os.listdir(MODS_DIR):
            path = os.path.join(MODS_DIR, filename)
            if os.path.isfile(path) and filename.lower().endswith(".jar") and filename not in expected_mods:
                os.remove(path)
                self._log(f"이전 모드 제거: {filename}")

    def _get_mrpack_mod_filenames(self, mrpack_path):
        expected_mods = set()
        with zipfile.ZipFile(mrpack_path, "r") as pack:
            index = json.loads(pack.read("modrinth.index.json"))
            for file_info in index.get("files", []):
                path = file_info.get("path", "").replace("\\", "/")
                if path.startswith("mods/") and path.lower().endswith(".jar"):
                    expected_mods.add(os.path.basename(path))

            for zip_name in pack.namelist():
                path = zip_name.replace("\\", "/")
                for prefix in ("overrides/mods/", "client-overrides/mods/"):
                    if path.startswith(prefix) and path.lower().endswith(".jar"):
                        expected_mods.add(os.path.basename(path))

        return expected_mods

    def _get_server_mod_filenames(self, server_mods):
        filenames = set()
        for mod in server_mods:
            filename = mod.get("filename")
            if not filename and mod.get("url"):
                filename = self._filename_from_url(mod["url"])
            if filename and filename.lower().endswith(".jar"):
                filenames.add(filename)
        return filenames

    def _get_mrpack_dependencies(self, mrpack_path):
        with zipfile.ZipFile(mrpack_path, "r") as pack:
            index = json.loads(pack.read("modrinth.index.json"))
            return index.get("dependencies", {})

    def _prepare_mrpack(self):
        if MRPACK_URL:
            return self._download_or_update_mrpack()

        if MRPACK_PATH:
            self._last_mrpack_changed = True
            if not os.path.exists(MRPACK_PATH):
                raise RuntimeError(f"mrpack 파일을 찾을 수 없어요: {MRPACK_PATH}")
            return MRPACK_PATH

        raise RuntimeError("MRPACK_URL 또는 MRPACK_PATH가 설정되어 있지 않아요.")

    def _download_or_update_mrpack(self):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        self._last_mrpack_changed = False
        meta = self._load_mrpack_meta()
        headers = {}
        if os.path.exists(MRPACK_FILE):
            if meta.get("etag"):
                headers["If-None-Match"] = meta["etag"]
            if meta.get("last_modified"):
                headers["If-Modified-Since"] = meta["last_modified"]

        self._log("Modrinth 모드팩 업데이트 확인 중...")
        temp_path = MRPACK_FILE + ".part"
        response = None
        last_error = None
        for attempt in range(1, MRPACK_DOWNLOAD_RETRIES + 1):
            try:
                with requests.get(
                    MRPACK_URL,
                    stream=True,
                    timeout=MRPACK_DOWNLOAD_TIMEOUT,
                    headers=headers
                ) as response:
                    if response.status_code == 304 and os.path.exists(MRPACK_FILE):
                        self._log("모드팩이 최신 버전입니다.")
                        return MRPACK_FILE

                    if response.status_code in (429, 500, 502, 503, 504):
                        raise RuntimeError(f"GitHub 응답 HTTP {response.status_code}")

                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "")
                    if "html" in content_type.lower():
                        raise RuntimeError("모드팩 대신 HTML 페이지를 받았어요. GitHub asset URL을 확인해 주세요.")

                    self._log("새 모드팩 다운로드 중...")
                    with open(temp_path, "wb") as pack_file:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                pack_file.write(chunk)
                    break
            except (requests.RequestException, RuntimeError) as e:
                last_error = e
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
                if attempt < MRPACK_DOWNLOAD_RETRIES:
                    self._log(f"모드팩 다운로드 실패: {e}. 재시도 {attempt}/{MRPACK_DOWNLOAD_RETRIES}...")
                    time.sleep(2 * attempt)
                    continue
                if os.path.exists(MRPACK_FILE):
                    self._log(f"모드팩 업데이트 확인 실패: {e}. 기존 모드팩으로 계속 실행합니다.")
                    return MRPACK_FILE
                raise RuntimeError(
                    "모드팩 다운로드가 실패했어요. GitHub 연결이 불안정하거나 차단됐을 수 있어요. "
                    f"잠시 후 다시 시도해 주세요. ({e})"
                ) from e

        self._validate_mrpack_file(temp_path)
        os.replace(temp_path, MRPACK_FILE)
        self._last_mrpack_changed = True
        self._save_mrpack_meta({
            "url": MRPACK_URL,
            "etag": response.headers.get("ETag") if response else None,
            "last_modified": response.headers.get("Last-Modified") if response else None,
            "downloaded_at": int(time.time()),
        })
        self._log("모드팩 업데이트 완료!")
        return MRPACK_FILE

    def _validate_mrpack_file(self, path):
        try:
            with zipfile.ZipFile(path, "r") as pack:
                if "modrinth.index.json" not in pack.namelist():
                    raise RuntimeError("modrinth.index.json이 없습니다.")
                json.loads(pack.read("modrinth.index.json"))
        except zipfile.BadZipFile as e:
            raise RuntimeError("다운로드한 파일이 올바른 mrpack ZIP이 아니에요.") from e

    def _load_mrpack_meta(self):
        try:
            with open(MRPACK_META_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_mrpack_meta(self, meta):
        with open(MRPACK_META_FILE, "w", encoding="utf-8") as file:
            json.dump(meta, file)

    def _get_launch_version(self):
        if MRPACK_PATH or MRPACK_URL:
            mrpack_path = MRPACK_PATH or MRPACK_FILE
            if os.path.exists(mrpack_path):
                return minecraft_launcher_lib.mrpack.get_mrpack_launch_version(mrpack_path)

        neoforge_id = self._get_neoforge_installed_version(NEOFORGE_VERSION)
        installed = [v["id"] for v in
                     minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)]

        if neoforge_id not in installed:
            callback = {
                "setStatus": lambda s: self._log(s),
                "setProgress": lambda c: None,
                "setMax": lambda m: None,
            }
            java_path = self._ensure_java_runtime(MC_VERSION, callback)
            neoforge_id = self._ensure_neoforge_installed(
                MC_VERSION,
                NEOFORGE_VERSION,
                callback,
                java_path
            )

        return neoforge_id

    def _get_server_mods(self):
        if not SERVER_MODS_MANIFEST_URL:
            return SERVER_MODS

        self._log("서버 모드 목록 다운로드 중...")
        response = requests.get(SERVER_MODS_MANIFEST_URL, timeout=15)
        response.raise_for_status()
        manifest = response.json()
        if isinstance(manifest, dict):
            return manifest.get("mods", [])
        if isinstance(manifest, list):
            return manifest
        raise RuntimeError("모드 목록 JSON 형식이 올바르지 않아요.")

    def _download_server_mod(self, mod):
        url = mod["url"]
        filename = mod.get("filename") or self._filename_from_url(url)
        expected_sha256 = mod.get("sha256")
        target_path = os.path.join(MODS_DIR, filename)

        if os.path.exists(target_path):
            if not expected_sha256 or self._sha256(target_path) == expected_sha256.lower():
                self._log(f"{filename} 이미 준비됨")
                return
            self._log(f"{filename} 해시가 달라 다시 다운로드합니다.")

        self._log(f"{mod.get('name', filename)} 다운로드 중...")
        temp_path = target_path + ".part"
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            with open(temp_path, "wb") as mod_file:
                for chunk in response.iter_content(chunk_size=1024 * 512):
                    if chunk:
                        mod_file.write(chunk)

        if expected_sha256 and self._sha256(temp_path) != expected_sha256.lower():
            os.remove(temp_path)
            raise RuntimeError(f"{filename} 파일 검증 실패: SHA-256이 맞지 않아요.")

        os.replace(temp_path, target_path)
        self._log(f"{filename} 다운로드 완료")

    def _filename_from_url(self, url):
        path = urllib.parse.urlparse(url).path
        filename = os.path.basename(path)
        if not filename:
            raise RuntimeError(f"모드 파일 이름을 알 수 없어요: {url}")
        return filename

    def _sha256(self, path):
        digest = hashlib.sha256()
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _sha1(self, path):
        digest = hashlib.sha1()
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _prepare_minecraft_preferences(self):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        changed = []
        if self._set_minecraft_language("ko_kr"):
            changed.append("한국어")
        if self._write_server_list():
            changed.append("서버 목록")

        if changed:
            self._log(f"Minecraft 기본 설정 준비 완료: {', '.join(changed)}")
        else:
            self._log("Minecraft 개인 설정은 그대로 유지합니다.")

    def _set_minecraft_language(self, language_code):
        options_path = os.path.join(MINECRAFT_DIR, "options.txt")
        lines = []

        if os.path.exists(options_path):
            with open(options_path, "r", encoding="utf-8", errors="replace") as file:
                lines = file.read().splitlines()

        if any(line.startswith("lang:") for line in lines):
            return False

        lines.append(f"lang:{language_code}")
        with open(options_path, "w", encoding="utf-8", newline="\n") as file:
            file.write("\n".join(lines) + "\n")
        return True

    def _write_server_list(self):
        servers_path = os.path.join(MINECRAFT_DIR, "servers.dat")
        if os.path.exists(servers_path):
            return False

        with open(servers_path, "wb") as file:
            self._write_nbt_named_header(file, 10, "")
            self._write_nbt_named_header(file, 9, "servers")
            file.write(struct.pack(">BI", 10, 1))

            self._write_nbt_string_tag(file, "name", SERVER_NAME)
            self._write_nbt_string_tag(file, "ip", SERVER_ADDRESS)
            self._write_nbt_byte_tag(file, "hidden", 0)
            self._write_nbt_byte_tag(file, "acceptTextures", 0)
            file.write(b"\x00")
            file.write(b"\x00")
        return True

    def _write_nbt_named_header(self, file, tag_type, name):
        encoded_name = name.encode("utf-8")
        file.write(struct.pack(">BH", tag_type, len(encoded_name)))
        file.write(encoded_name)

    def _write_nbt_string_tag(self, file, name, value):
        self._write_nbt_named_header(file, 8, name)
        encoded_value = value.encode("utf-8")
        file.write(struct.pack(">H", len(encoded_value)))
        file.write(encoded_value)

    def _write_nbt_byte_tag(self, file, name, value):
        self._write_nbt_named_header(file, 1, name)
        file.write(struct.pack(">b", value))

    def _start_game(self):
        self.start_btn.configure(state="disabled")
        self._start_launch_status_cycle()
        threading.Thread(target=self._install_and_launch, daemon=True).start()

    def _start_launch_status_cycle(self):
        self._stop_launch_status_cycle()
        self._cycle_launch_status()

    def _cycle_launch_status(self):
        message = random.choice(LAUNCH_STATUS_MESSAGES)
        if len(LAUNCH_STATUS_MESSAGES) > 1:
            while message == self._last_launch_status_message:
                message = random.choice(LAUNCH_STATUS_MESSAGES)

        self._last_launch_status_message = message
        self.start_btn.configure(text=f"✦  {message}", state="disabled")
        self._launch_status_after_id = self.after(3000, self._cycle_launch_status)

    def _stop_launch_status_cycle(self):
        if self._launch_status_after_id:
            self.after_cancel(self._launch_status_after_id)
            self._launch_status_after_id = None

    def _install_and_launch(self):
        try:
            self._log("마인크래프트 설치 확인 중...")
            os.makedirs(MINECRAFT_DIR, exist_ok=True)
            callback = {
                "setStatus": lambda s: self._log(s),
                "setProgress": lambda c: None,
                "setMax": lambda m: None,
            }
            installed = [v["id"] for v in
                         minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)]

            if not (MRPACK_PATH or MRPACK_URL) and MC_VERSION not in installed:
                self._log(f"마인크래프트 {MC_VERSION} 다운로드 중... 잠시만요!")
                minecraft_launcher_lib.install.install_minecraft_version(
                    MC_VERSION, MINECRAFT_DIR, callback)
                self._log("마인크래프트 설치 완료!")

            self._prepare_minecraft_preferences()
            self._sync_server_mods()
            launch_version = self._get_launch_version()

            mem_gb = self.memory_gb
            options = {
                "username": self.account["name"],
                "uuid": self.account["id"],
                "token": self.account["access_token"],
                "jvmArguments": [
                    f"-Xmx{mem_gb}G",
                    f"-Xms{mem_gb // 2}G",
                    EXPERIMENTAL_JVM_UNLOCK_ARG,
                    "-XX:+UseG1GC",
                    "-XX:+ParallelRefProcEnabled",
                    "-XX:G1NewSizePercent=20",
                    "-XX:G1ReservePercent=20",
                ],
                "gameDirectory": MINECRAFT_DIR,
                "customResolution": True,
                "resolutionWidth": str(self.resolution_width),
                "resolutionHeight": str(self.resolution_height),
            }
            if self.fullscreen_enabled:
                options["fullscreen"] = True

            self._log("🚀 소행성 서버 목록 준비 완료!")
            cmd = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version, MINECRAFT_DIR, options)
            cmd = self._fix_java_vm_option_order(cmd)
            cmd = self._apply_window_mode_arguments(cmd)
            cmd = self._prefer_windowless_java(cmd)

            log_file = open(LAUNCHER_LOG_FILE, "w", encoding="utf-8", errors="replace")
            popen_options = self._get_minecraft_popen_options(log_file)
            process = subprocess.Popen(
                cmd,
                **popen_options
            )
            threading.Thread(
                target=self._watch_game_process,
                args=(process, log_file),
                daemon=True
            ).start()
            self._log("게임 프로세스를 시작했어요. 첫 실행은 모드 로딩 때문에 1~3분 걸릴 수 있어요.")
            self._log(f"게임 로그: {LAUNCHER_LOG_FILE}")
            self.after(0, lambda: self.start_btn.configure(
                text="✦  게임 로딩 중", state="disabled"))

        except Exception as e:
            self._log(f"오류: {e}")
            self.after(0, lambda: self._reset_start_button("🚀  발사!"))

    def _fix_java_vm_option_order(self, cmd):
        fixed_cmd = [arg for arg in cmd if arg != EXPERIMENTAL_JVM_UNLOCK_ARG]
        experimental_indexes = [
            index for index, arg in enumerate(fixed_cmd)
            if any(arg.startswith(prefix) for prefix in EXPERIMENTAL_JVM_OPTION_PREFIXES)
        ]

        if experimental_indexes:
            fixed_cmd.insert(min(experimental_indexes), EXPERIMENTAL_JVM_UNLOCK_ARG)

        return fixed_cmd

    def _apply_window_mode_arguments(self, cmd):
        if self.fullscreen_enabled and "--fullscreen" not in cmd:
            cmd.append("--fullscreen")

        if "--width" not in cmd:
            cmd.extend(["--width", str(self.resolution_width)])
        if "--height" not in cmd:
            cmd.extend(["--height", str(self.resolution_height)])

        return cmd

    def _prefer_windowless_java(self, cmd):
        if os.name != "nt" or not cmd:
            return cmd

        java_path = cmd[0]
        java_name = os.path.basename(java_path).lower()
        if java_name != "java.exe":
            return cmd

        javaw_path = os.path.join(os.path.dirname(java_path), "javaw.exe")
        if os.path.exists(javaw_path):
            return [javaw_path] + cmd[1:]

        return cmd

    def _get_minecraft_popen_options(self, log_file):
        options = {
            "cwd": MINECRAFT_DIR,
            "stdin": subprocess.DEVNULL,
            "stdout": log_file,
            "stderr": subprocess.STDOUT,
            "text": True,
        }

        if os.name == "nt":
            options["creationflags"] = (
                getattr(subprocess, "DETACHED_PROCESS", 0)
                | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            )
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            options["startupinfo"] = startupinfo
        else:
            options["start_new_session"] = True

        return options

    def _watch_game_process(self, process, log_file):
        exit_code = process.wait()
        log_file.close()

        if exit_code == 0:
            self._log("게임이 종료됐어요.")
        else:
            self._log(f"게임이 비정상 종료됐어요. 종료 코드: {exit_code}")
            self._log(f"자세한 내용은 {LAUNCHER_LOG_FILE} 를 확인해 주세요.")

        self.after(0, lambda: self._reset_start_button("🚀  다시 발사!"))

    def _reset_start_button(self, text):
        self._stop_launch_status_cycle()
        self.start_btn.configure(state="normal", text=text)


if __name__ == "__main__":
    app = Launcher()
    app.mainloop()

