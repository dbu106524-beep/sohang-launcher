# 소행성 런처 배포 / 모드팩 업데이트 가이드

이 문서는 GitHub Releases에 `Createdin.mrpack`과 런처 exe를 올리고, 유저 런처가 자동으로 최신 모드팩과 런처 업데이트를 받게 하는 방법을 정리한 것입니다.

## 현재 런처 설정

`launcher.py`는 아래 주소에서 최신 모드팩을 다운로드합니다.

```python
MRPACK_PATH = ""
MRPACK_URL = "https://github.com/dbu106524-beep/sohang-launcher/releases/latest/download/Createdin.mrpack"
```

즉, 유저가 런처에서 `발사!` 버튼을 누르면 GitHub 최신 릴리즈의 `Createdin.mrpack`을 확인하고, 새 파일이면 자동으로 다운로드합니다.

## 처음 릴리즈 만들기

1. GitHub 저장소 `sohang-launcher`로 이동합니다.
2. 오른쪽 또는 상단의 `Releases`를 클릭합니다.
3. `Draft a new release` 또는 `Create a new release`를 클릭합니다.
4. `Choose a tag`에 버전을 입력합니다.
   - 예: `1.0`
5. Release title도 같은 식으로 입력합니다.
   - 예: `Sohang Launcher 1.0`
6. 아래 `Attach binaries by dropping them here or selecting them` 영역에 파일을 올립니다.
   - 모드팩: 반드시 `Createdin.mrpack` 이름으로 업로드합니다.
   - 런처 exe: 가능하면 `SohangLauncher.exe` 이름으로 업로드합니다.
7. `Publish release`를 클릭합니다.

## 모드팩 업데이트 방법

모드팩을 바꿨다면 아래 순서로 진행합니다.

1. Modrinth에서 새 `.mrpack`을 export합니다.
2. 파일 이름을 반드시 아래처럼 맞춥니다.

```text
Createdin.mrpack
```

3. GitHub 저장소의 `Releases`로 이동합니다.
4. 새 릴리즈를 만듭니다.
   - 예: 기존이 `1.0`이면 새 태그는 `1.1`
5. 새 릴리즈에 `Createdin.mrpack`을 업로드합니다.
6. `Publish release`를 누릅니다.

이렇게 하면 `releases/latest/download/Createdin.mrpack` 주소가 새 릴리즈의 파일을 가리키게 됩니다.

## 유저 런처에서는 어떻게 적용되나요?

유저가 런처에서 `발사!`를 누르면:

1. 처음 실행이거나 `mods` 폴더에 모드가 없을 때만 `Createdin.mrpack`을 다운로드하고 설치합니다.
2. 한 번 설치된 뒤에는 `mods`, `config`, `options.txt`, `servers.dat` 같은 유저 개인 설정을 건드리지 않습니다.
3. 유저가 직접 넣은 미니맵 모드, 한글채팅 모드, 키 설정, 미니맵 설정은 유지됩니다.
4. `options.txt`에 언어 설정이 아직 없을 때만 한국어(`ko_kr`)를 기본값으로 넣습니다.
5. `servers.dat` 파일이 없을 때만 `소행성 서버` / `dinbu.kro.kr:25565`를 등록합니다.

초기 설치 완료 상태는 아래 파일에 저장됩니다.

```text
C:\Users\<사용자>\.minecraft_asteroid\install_state.json
```

## 게임 실행 문제 확인

런처에서 `게임 프로세스를 시작했어요`가 뜬 뒤에도 게임 창이 안 보이면 먼저 기다려 주세요. 첫 실행은 모드가 많아서 1~3분 정도 로딩될 수 있습니다.

런처는 Minecraft 실행 출력을 아래 파일에 저장합니다.

```text
C:\Users\<사용자>\.minecraft_asteroid\launcher-game.log
```

Minecraft 자체 로그는 아래 위치에 생깁니다.

```text
C:\Users\<사용자>\.minecraft_asteroid\logs\latest.log
C:\Users\<사용자>\.minecraft_asteroid\logs\debug.log
```

게임이 바로 꺼지면 런처 로그에 종료 코드가 표시되고, `launcher-game.log`에서 원인을 확인할 수 있습니다.

`G1NewSizePercent is experimental` 오류가 나지 않도록 런처가 Java 실행 직전에 `-XX:+UnlockExperimentalVMOptions` 옵션을 실험 옵션보다 앞쪽으로 자동 정렬합니다.

발사 버튼을 누른 뒤에는 우주 컨셉 문구가 3초마다 무작위로 바뀝니다.

자동 접속 인자는 사용하지 않습니다. 대신 런처가 `.minecraft_asteroid\servers.dat`에 `소행성 서버`를 등록해서 Minecraft 멀티플레이 서버 목록에 보이게 합니다.

마지막으로 선택한 메모리 할당량은 아래 설정 파일에 저장됩니다. 예를 들어 6GB로 바꿨다면 런처를 다시 켜도 6GB로 시작합니다.

```text
C:\Users\<사용자>\.minecraft_asteroid\launcher_settings.json
```

Windows에서는 가능한 경우 `java.exe` 대신 `javaw.exe`로 Minecraft를 실행하고, 런처 콘솔과 별도 프로세스로 분리합니다. 그래서 게임이 정상 실행된 뒤 CMD 창을 닫아도 Minecraft가 같이 종료되지 않도록 처리합니다.

## 꼭 지켜야 하는 것

- 릴리즈 asset 파일명은 반드시 `Createdin.mrpack`이어야 합니다.
- GitHub 저장소가 private이면 유저 런처가 다운로드하지 못합니다. public 저장소 또는 public release asset이어야 합니다.
- Google Drive, OneDrive 공유 링크는 자동 다운로드에 부적합합니다.
- 모드팩을 바꿨는데 적용이 안 되면 새 릴리즈가 `Latest`인지 확인합니다.

## 런처 자체 자동 업데이트

현재 런처는 GitHub latest release tag를 확인해서 새 버전이 있으면 사이드바에 업데이트 버튼을 표시합니다.

```python
APP_VERSION = "1.04"
UPDATE_API_URL = "https://api.github.com/repos/dbu106524-beep/sohang-launcher/releases/latest"
LAUNCHER_WINDOWS_ASSET_NAME = "SohangLauncher.exe"
```

런처 코드 자체를 수정했다면:

1. `APP_VERSION`을 올립니다.
   - 예: `1.0` -> `1.1`
2. Windows용 exe를 새로 빌드합니다.
3. GitHub Releases에 새 태그로 릴리즈를 만듭니다.
4. 릴리즈 asset에 exe를 업로드합니다.
   - 추천 파일명: `SohangLauncher.exe`
   - 다른 `.exe` 파일명이어도 런처가 첫 번째 `.exe` asset을 찾아 자동 설치를 시도합니다.
5. 유저 런처가 새 버전을 감지하면 `런처 업데이트 vX.X` 버튼이 활성화됩니다.
6. 유저가 버튼을 누르면 exe를 다운로드하고, 별도 updater 배치 파일이 기존 exe를 교체한 뒤 런처를 재실행합니다.

주의:

- 자동 교체는 패키징된 Windows exe에서 동작합니다.
- `python launcher.py`로 실행하는 개발 모드에서는 자동 교체하지 않고 릴리즈 페이지를 엽니다.
- macOS에서는 업데이트를 감지하면 릴리즈 페이지를 열어 새 `.app`/`.dmg`를 받도록 안내합니다.
- Windows 자동 업데이트는 기존 런처가 완전히 종료될 때까지 기다린 뒤 기존 exe를 백업하고 새 exe를 복사합니다.
- `Failed to load Python DLL ... _MEI...` 오류가 난 버전에서는 한 번만 GitHub Release에서 `SohangLauncher.exe`를 직접 받아 교체해 주세요. 교체 후 다음 버전부터는 수정된 updater가 동작합니다.
- 보안상 더 단단하게 하려면 exe 코드 서명 또는 SHA-256 체크섬 asset을 추가하는 것을 추천합니다.

## Windows exe 빌드

현재 Windows용 실행 파일은 아래 경로에 생성됩니다.

```text
dist/SohangLauncher.exe
```

빌드 명령 예시:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed `
  --name SohangLauncher `
  --icon sohangicon.ico `
  --add-data "sohangicon-transparent.png;." `
  --add-data "sohangicon.ico;." `
  launcher.py
```

새 런처 버전을 배포할 때는:

1. `launcher.py`의 `APP_VERSION`을 올립니다.
2. `SohangLauncher.exe`를 다시 빌드합니다.
3. GitHub Releases에 새 태그로 릴리즈를 만듭니다.
4. asset으로 `SohangLauncher.exe`와 `Createdin.mrpack`을 올립니다.

## macOS 배포 메모

Windows에서 만든 `.exe`는 macOS에서 실행되지 않습니다. macOS용 앱은 Mac에서 따로 빌드해야 합니다.

맥북이 없어도 GitHub Actions가 macOS 앱을 대신 빌드할 수 있도록 아래 워크플로우를 추가해 두었습니다.

```text
.github/workflows/build-macos.yml
```

GitHub Actions 자동 빌드 방법:

1. `launcher.py`, `README.md`, `.github/workflows/build-macos.yml`, 아이콘 파일들을 GitHub 저장소에 올립니다.
2. GitHub 저장소의 `Actions` 탭에서 `Build macOS Launcher`를 선택합니다.
3. `Run workflow`를 누릅니다.
4. 빌드가 끝나면 `Artifacts`에서 아래 두 파일을 받을 수 있습니다.

```text
SohangLauncher-mac-arm64.zip
SohangLauncher-mac-x64.zip
```

권장 배포:

- `SohangLauncher-mac-arm64.zip`: Apple Silicon 맥용입니다. M1, M2, M3, M4 맥북 사용자는 이 파일을 받으면 됩니다.
- `SohangLauncher-mac-x64.zip`: Intel 맥용입니다.
- GitHub Release를 발행하면 워크플로우가 두 zip 파일을 릴리즈 asset으로 자동 업로드합니다.

워크플로우가 실패한 뒤 파일을 수정했다면 해당 실행 화면 오른쪽 위의 `Re-run jobs` 또는 Actions 탭의 `Run workflow`로 다시 실행합니다.

macOS 아이콘 생성은 `sohangicon-transparent.png`, `sohangicon.png`, `sohangicon.ico` 순서로 시도합니다. 이미지 파일을 GitHub에 잘못 올렸거나 macOS가 읽지 못해도 임시 아이콘으로 빌드가 계속되도록 처리되어 있습니다.

macOS 코드 호환성:

- 경로는 `os.path` 기반이라 Windows/macOS 모두 대응합니다.
- 자동 로그인 토큰은 macOS에서 Keychain을 사용하도록 되어 있습니다.
- 런처 이미지 리소스는 PyInstaller 번들 경로(`sys._MEIPASS`)를 지원합니다.
- macOS에서는 업데이트 감지 후 릴리즈 페이지 안내 방식으로 운영합니다.
- macOS용 릴리즈 asset 이름은 `SohangLauncher-mac-arm64.zip`, `SohangLauncher-mac-x64.zip`, `SohangLauncher-mac.zip`, `SohangLauncher.dmg`를 인식합니다.

macOS 빌드 예시:

```bash
python3 -m pip install pyinstaller customtkinter minecraft-launcher-lib requests
python3 -m PyInstaller --noconfirm --clean --windowed --name SohangLauncher \
  --add-data "sohangicon-transparent.png:." \
  --add-data "sohangicon.ico:." \
  launcher.py
```

빌드 후 `dist/SohangLauncher.app`을 압축해서 릴리즈에 올립니다.

```bash
cd dist
zip -r SohangLauncher-mac.zip SohangLauncher.app
```

릴리즈 asset 예시:

```text
SohangLauncher.exe
SohangLauncher-mac-arm64.zip
SohangLauncher-mac-x64.zip
Createdin.mrpack
```

## 추천 릴리즈 버전 규칙

- 모드팩만 바꿔도 릴리즈 버전을 올리는 것을 추천합니다.
- 예시:

```text
1.0   첫 배포
1.1   모드팩 업데이트
1.2   모드팩 업데이트
2.0   런처 구조 변경 또는 큰 업데이트
```

## 빠른 체크리스트

배포 전 확인:

- [ ] `Createdin.mrpack` 파일명이 정확한가?
- [ ] `SohangLauncher.exe`를 새 릴리즈 asset으로 업로드했는가?
- [ ] GitHub 릴리즈에 asset으로 업로드했는가?
- [ ] 새 릴리즈가 latest 상태인가?
- [ ] 런처에서 `MRPACK_URL`이 `releases/latest/download/Createdin.mrpack`인가?
- [ ] 런처 실행 후 로그에 모드팩 업데이트 확인이 뜨는가?


