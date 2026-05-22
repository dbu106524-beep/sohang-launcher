import customtkinter as ctk
import minecraft_launcher_lib
from minecraft_launcher_lib.microsoft_account import (
    authenticate_with_xbl,
    authenticate_with_xsts,
    authenticate_with_minecraft,
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)
ICON_PATH = os.path.join(RESOURCE_DIR, "sohangicon-transparent.png")
WINDOWS_ICON_PATH = os.path.join(RESOURCE_DIR, "sohangicon.ico")
MINECRAFT_DIR = os.path.join(os.path.expanduser("~"), ".minecraft_asteroid")
MODS_DIR = os.path.join(MINECRAFT_DIR, "mods")
AVATAR_CACHE_DIR = os.path.join(MINECRAFT_DIR, "avatars")
AUTH_CACHE_FILE = os.path.join(MINECRAFT_DIR, "auth_cache.json")
LAUNCHER_SETTINGS_FILE = os.path.join(MINECRAFT_DIR, "launcher_settings.json")
LAUNCHER_LOG_FILE = os.path.join(MINECRAFT_DIR, "launcher-game.log")
INSTALL_STATE_FILE = os.path.join(MINECRAFT_DIR, "install_state.json")
KEYCHAIN_SERVICE = "SohangLauncher"
KEYCHAIN_ACCOUNT = "minecraft-refresh-token"
APP_VERSION = "1.04"
UPDATE_API_URL = "https://api.github.com/repos/dbu106524-beep/sohang-launcher/releases/latest"
UPDATE_PAGE_URL = "https://github.com/dbu106524-beep/sohang-launcher/releases/latest"
LAUNCHER_WINDOWS_ASSET_NAME = "SohangLauncher.exe"
LAUNCHER_MAC_ASSET_NAMES = (
    "SohangLauncher-mac-arm64.zip",
    "SohangLauncher-mac-x64.zip",
    "SohangLauncher-mac.zip",
    "SohangLauncher.dmg",
)
MC_VERSION = "1.21.1"
SERVER_IP = "dinbu.kro.kr"
SERVER_PORT = "25565"
SERVER_ADDRESS = f"{SERVER_IP}:{SERVER_PORT}"
SERVER_NAME = "소행성 서버"
SERVER_PROTOCOL_VERSION = 767
NEOFORGE_VERSION = "21.1.228"
CLIENT_ID = "0ab5ff14-0b50-4a22-a26b-def8c460b422" #"0ab5ff14-0b50-4a22-a26b-def8c460b422"
DEVICE_CODE_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
MICROSOFT_SCOPE = "XboxLive.signin offline_access"
DEFAULT_OLD_CLIENT_ID = "00000000402b5328"
MRPACK_PATH = ""
MRPACK_URL = "https://github.com/dbu106524-beep/sohang-launcher/releases/latest/download/Createdin.mrpack"
MRPACK_FILE = os.path.join(MINECRAFT_DIR, "server-pack.mrpack")
MRPACK_META_FILE = os.path.join(MINECRAFT_DIR, "server-pack-meta.json")

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
        self.geometry("780x560")
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
        self._launch_status_after_id = None
        self._last_launch_status_message = None
        self._load_images()
        self._build_ui()
        self._refresh_server_status()
        self._try_auto_login()
        self._check_launcher_update()

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
                         font=ctk.CTkFont(size=48)).pack()
        ctk.CTkLabel(logo_frame, text="소행성",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=SPACE_STAR).pack()
        ctk.CTkLabel(logo_frame, text="마인크래프트 소행성 서버",
                     font=ctk.CTkFont(size=10),
                     text_color=SPACE_MUTED).pack(pady=(2, 0))

        ctk.CTkFrame(sidebar, height=1, fg_color=SPACE_ACCENT2).pack(
            fill="x", padx=20, pady=15)

        self.login_btn = ctk.CTkButton(
            sidebar, text="Microsoft 로그인",
            command=self._login, width=180, height=38,
            fg_color=SPACE_ACCENT2, hover_color="#6d28d9",
            font=ctk.CTkFont(size=13, weight="bold")
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
            font=ctk.CTkFont(size=11)
        )
        self.remember_login_checkbox.pack(pady=(0, 5), padx=20, anchor="w")

        self.update_btn = ctk.CTkButton(
            sidebar, text="런처가 최신버전이에요!",
            command=self._install_launcher_update,
            width=180, height=30,
            state="disabled",
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.update_btn.pack(pady=(4, 5), padx=20)

        self.account_label = ctk.CTkLabel(
            sidebar, text="로그인이 필요해요",
            font=ctk.CTkFont(size=11),
            text_color=SPACE_MUTED
        )
        self.account_label.pack(pady=3)

        self.avatar_label = ctk.CTkLabel(sidebar, text="")
        self.avatar_label.pack(pady=(8, 0))

        ctk.CTkLabel(sidebar, text="").pack(expand=True)
        ctk.CTkLabel(sidebar, text=f"✦ Minecraft {MC_VERSION}",
                     font=ctk.CTkFont(size=11),
                     text_color=SPACE_MUTED).pack(pady=5)
        ctk.CTkLabel(sidebar, text=f"✦ NeoForge {NEOFORGE_VERSION}",
                     font=ctk.CTkFont(size=11),
                     text_color=SPACE_MUTED).pack(pady=(0, 20))

        main = ctk.CTkFrame(self, corner_radius=0, fg_color=SPACE_BG)
        main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main, text="✦ 우주로 떠날 준비가 됐나요?",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=SPACE_STAR).pack(anchor="w", pady=(0, 15))

        status_card = ctk.CTkFrame(main, fg_color=SPACE_CARD,
                                   corner_radius=12,
                                   border_width=1, border_color=SPACE_MUTED)
        status_card.pack(fill="x", pady=(0, 12))

        status_header = ctk.CTkFrame(status_card, fg_color="transparent")
        status_header.pack(fill="x", padx=15, pady=(12, 8))

        ctk.CTkLabel(status_header, text="서버 상태",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=SPACE_STAR).pack(side="left")

        self.status_refresh_btn = ctk.CTkButton(
            status_header, text="새로고침",
            command=self._refresh_server_status,
            width=78, height=26,
            fg_color=SPACE_MUTED, hover_color="#374151",
            font=ctk.CTkFont(size=11)
        )
        self.status_refresh_btn.pack(side="right")

        self.server_status_label = ctk.CTkLabel(
            status_card, text="확인 중...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=SPACE_MUTED
        )
        self.server_status_label.pack(anchor="w", padx=15)

        self.server_detail_label = ctk.CTkLabel(
            status_card, text=f"{SERVER_IP}:{SERVER_PORT}",
            font=ctk.CTkFont(size=11),
            text_color=SPACE_MUTED
        )
        self.server_detail_label.pack(anchor="w", padx=15, pady=(2, 12))

        mem_card = ctk.CTkFrame(main, fg_color=SPACE_CARD,
                                 corner_radius=12,
                                 border_width=1, border_color=SPACE_MUTED)
        mem_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(mem_card, text="🖥  메모리 할당",
                     font=ctk.CTkFont(size=13, weight="bold"),
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
                                       font=ctk.CTkFont(size=13, weight="bold"))
        self.mem_label.pack(side="right")

        self.start_btn = ctk.CTkButton(
            main, text="🚀  발사!",
            height=50,
            font=ctk.CTkFont(size=17, weight="bold"),
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
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=SPACE_STAR).pack(anchor="w", padx=15, pady=(12, 4))

        self.log_box = ctk.CTkTextbox(
            log_card, height=120,
            font=ctk.CTkFont(family="Consolas", size=11),
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
            with open(LAUNCHER_SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)
            memory_gb = int(settings.get("memory_gb", 4))
            return max(2, min(16, memory_gb))
        except Exception:
            return 4

    def _save_memory_setting(self):
        try:
            os.makedirs(MINECRAFT_DIR, exist_ok=True)
            settings = {}
            if os.path.exists(LAUNCHER_SETTINGS_FILE):
                with open(LAUNCHER_SETTINGS_FILE, "r", encoding="utf-8") as file:
                    settings = json.load(file)
            settings["memory_gb"] = self.memory_gb
            with open(LAUNCHER_SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(settings, file, ensure_ascii=False, indent=2)
        except Exception as e:
            self._log(f"메모리 설정 저장 실패: {e}")

    def _log(self, msg):
        if threading.current_thread() is not self._main_thread:
            self.after(0, lambda: self._log(msg))
            return

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"› {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

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
            preferred_names = (LAUNCHER_WINDOWS_ASSET_NAME,)
            fallback_suffixes = (".exe",)
        elif sys.platform == "darwin":
            preferred_names = LAUNCHER_MAC_ASSET_NAMES
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

        if sys.platform != "win32":
            self._log("macOS에서는 릴리즈 페이지에서 새 앱을 받아 교체해 주세요.")
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
if exist "%BACKUP%" del "%BACKUP%" >nul 2>nul
if exist "%TARGET%" move /Y "%TARGET%" "%BACKUP%" >nul
set "TRY=0"
:copy
set /A TRY+=1
copy /Y "%SOURCE%" "%TARGET%" >nul
if exist "%TARGET%" goto copied
if %TRY% GEQ 10 goto failed
timeout /t 1 /nobreak >nul
goto copy
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
            self.after(0, lambda: self._set_server_status(
                "오프라인",
                f"{SERVER_IP}:{SERVER_PORT}  |  {e}",
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
            account_request = authenticate_with_minecraft(userhash, xsts_token)
            if "access_token" not in account_request:
                error_message = account_request.get("errorMessage", account_request)
                if isinstance(error_message, str) and "Invalid app registration" in error_message:
                    raise RuntimeError(
                        "Azure 앱이 아직 Minecraft API 사용 승인을 받지 못했어요. "
                        "https://aka.ms/mce-reviewappid 에서 앱 ID 승인을 신청한 뒤 승인될 때까지 기다려야 합니다."
                    )
                raise RuntimeError(error_message)

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
            self._log(f"로그인 실패: {e}")
            self.after(0, lambda: self.login_btn.configure(
                state="normal", text="Microsoft 로그인"))

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
            if self._is_initial_mod_setup_done():
                self._log("모드팩은 이미 준비되어 있어요. 개인 모드와 설정은 건드리지 않습니다.")
                return
            self._install_mrpack()
            self._mark_initial_mod_setup_done()
            return

        os.makedirs(MODS_DIR, exist_ok=True)
        server_mods = self._get_server_mods()

        if not server_mods:
            self._log("서버 모드 목록이 비어 있어요. SERVER_MODS에 모드 URL을 추가해 주세요.")
            return

        if self._is_initial_mod_setup_done():
            self._log("서버 모드는 이미 준비되어 있어요. 개인 모드는 건드리지 않습니다.")
            return

        self._log("서버 모드 확인 중...")
        for mod in server_mods:
            self._download_server_mod(mod)
        self._mark_initial_mod_setup_done()
        self._log("서버 모드 준비 완료!")

    def _install_mrpack(self):
        mrpack_path = self._prepare_mrpack()
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

    def _is_initial_mod_setup_done(self):
        if self._has_user_mod_files():
            if not self._load_install_state().get("initial_mod_setup_done"):
                self._mark_initial_mod_setup_done()
            return True

        return False

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

    def _mark_initial_mod_setup_done(self):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        state = self._load_install_state()
        state["initial_mod_setup_done"] = True
        state["updated_at"] = int(time.time())
        state["preserve_user_mods"] = True
        with open(INSTALL_STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)

    def _install_mrpack_dependencies(self, mrpack_path, callback):
        dependencies = self._get_mrpack_dependencies(mrpack_path)
        minecraft_version = dependencies.get("minecraft")
        if not minecraft_version:
            raise RuntimeError("mrpack에 Minecraft 버전 정보가 없어요.")

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

            loader = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)
            self._log(f"{loader.get_name()} {loader_version} 설치 확인 중...")
            loader.install(
                minecraft_version,
                MINECRAFT_DIR,
                loader_version=loader_version,
                callback=callback,
                java=java_path
            )

    def _ensure_java_runtime(self, minecraft_version, callback):
        runtime_info = minecraft_launcher_lib.runtime.get_version_runtime_information(
            minecraft_version, MINECRAFT_DIR)
        if runtime_info is None:
            return "java"

        runtime_name = runtime_info["name"]
        self._log(f"Java 런타임 {runtime_name} 확인 중...")
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

    def _get_mrpack_dependencies(self, mrpack_path):
        with zipfile.ZipFile(mrpack_path, "r") as pack:
            index = json.loads(pack.read("modrinth.index.json"))
            return index.get("dependencies", {})

    def _prepare_mrpack(self):
        if MRPACK_URL:
            return self._download_or_update_mrpack()

        if MRPACK_PATH:
            if not os.path.exists(MRPACK_PATH):
                raise RuntimeError(f"mrpack 파일을 찾을 수 없어요: {MRPACK_PATH}")
            return MRPACK_PATH

        raise RuntimeError("MRPACK_URL 또는 MRPACK_PATH가 설정되어 있지 않아요.")

    def _download_or_update_mrpack(self):
        os.makedirs(MINECRAFT_DIR, exist_ok=True)
        meta = self._load_mrpack_meta()
        headers = {}
        if os.path.exists(MRPACK_FILE):
            if meta.get("etag"):
                headers["If-None-Match"] = meta["etag"]
            if meta.get("last_modified"):
                headers["If-Modified-Since"] = meta["last_modified"]

        self._log("Modrinth 모드팩 업데이트 확인 중...")
        temp_path = MRPACK_FILE + ".part"
        with requests.get(MRPACK_URL, stream=True, timeout=30, headers=headers) as response:
            if response.status_code == 304 and os.path.exists(MRPACK_FILE):
                self._log("모드팩이 최신 버전입니다.")
                return MRPACK_FILE

            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "html" in content_type.lower():
                raise RuntimeError("모드팩 대신 HTML 페이지를 받았어요. GitHub asset URL을 확인해 주세요.")

            self._log("새 모드팩 다운로드 중...")
            with open(temp_path, "wb") as pack_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        pack_file.write(chunk)

        self._validate_mrpack_file(temp_path)
        os.replace(temp_path, MRPACK_FILE)
        self._save_mrpack_meta({
            "url": MRPACK_URL,
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
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

        neoforge_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
        neoforge_id = neoforge_loader.get_installed_version(MC_VERSION, NEOFORGE_VERSION)
        installed = [v["id"] for v in
                     minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIR)]

        if neoforge_id not in installed:
            self._log("NeoForge 설치 중...")
            neoforge_id = neoforge_loader.install(
                MC_VERSION,
                MINECRAFT_DIR,
                loader_version=NEOFORGE_VERSION,
                callback={
                    "setStatus": lambda s: self._log(s),
                    "setProgress": lambda c: None,
                    "setMax": lambda m: None,
                }
            )
            self._log("NeoForge 설치 완료!")

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
            }

            self._log("🚀 소행성 서버 목록 준비 완료!")
            cmd = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version, MINECRAFT_DIR, options)
            cmd = self._fix_java_vm_option_order(cmd)
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
