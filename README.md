# 소행성 런처 배포 / 모드팩 업데이트 가이드

이 문서는 GitHub Releases에 `Createdin.mrpack`과 런처 exe를 올리고, 유저 런처가 자동으로 최신 모드팩과 런처 업데이트를 받게 하는 방법을 정리한 것입니다.

## 현재 런처 설정

`launcher.py`는 아래 주소에서 최신 모드팩을 다운로드합니다.

```python
APP_VERSION = "1.16"
MC_VERSION = "26.1.2"
NEOFORGE_VERSION = "26.1.2.65-beta"
REQUIRED_JAVA_MAJOR = 25
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
   - 런처 exe: 가능하면 `SohangLauncher-버전.exe` 이름으로 업로드합니다. 예: `SohangLauncher-1.16.exe`
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

현재 런처는 `Createdin.mrpack` 안의 Minecraft / NeoForge 버전이 런처 설정과 다르면 실행을 멈추고 로그에 오류를 표시합니다. 서버를 `26.1.2` / `26.1.2.65-beta`로 올린 뒤에는 Modrinth에서 같은 버전으로 다시 export한 `Createdin.mrpack`을 릴리즈에 올려야 합니다.

## 유저 런처에서는 어떻게 적용되나요?

유저가 런처에서 `발사!`를 누르면:

1. 처음 실행이거나 `mods` 폴더에 모드가 없을 때 `Createdin.mrpack`을 다운로드하고 설치합니다.
2. 런처에 기록된 Minecraft / NeoForge / Java 버전이 바뀌면 새 서버 모드팩을 한 번 다시 적용합니다.
3. 같은 서버 버전이어도 GitHub latest의 `Createdin.mrpack`이 바뀌면 서버 기본 모드를 다시 적용합니다.
4. 서버 모드팩에 포함된 `.jar`는 파일명이 같아도 먼저 지우고 다시 설치해서 내용 변경분이 확실히 반영됩니다.
5. 이전 런처가 설치했던 서버 기본 모드 중 새 모드팩에서 빠진 `.jar`만 제거합니다.
6. 유저가 직접 넣은 추가 `.jar`, `config`, `options.txt`, `servers.dat` 같은 개인 설정은 건드리지 않습니다.
7. 유저가 직접 넣은 미니맵 모드, 한글채팅 모드, 키 설정, 미니맵 설정은 유지됩니다.
8. `options.txt`에 언어 설정이 아직 없을 때만 한국어(`ko_kr`)를 기본값으로 넣습니다.
9. `servers.dat` 파일이 없을 때만 `소행성 서버` / `dinbu.kro.kr:25565`를 등록합니다.

초기 설치 완료 상태는 아래 파일에 저장됩니다.

```text
C:\Users\<사용자>\.minecraft_asteroid\install_state.json
```

## 개인 모드 검색과 추가

런처 오른쪽의 `Modrinth 모드` 패널에서 개인 모드를 검색하고 추가할 수 있습니다.

현재 지원 범위:

- Modrinth 검색
- Minecraft `26.1.2` 필터
- `neoforge` 로더 필터
- 클라이언트 사용 가능 모드 검색
- 검색어가 없으면 인기 모드 기본 표시
- 인기순, 관련순, 업데이트순, 최신순 정렬
- 20개씩 페이지 이동
- 모드 아이콘, 설명, 다운로드 수 표시
- 검색 결과 클릭 시 Modrinth 모드 페이지 열기
- `mods` 폴더에 `.jar` 다운로드
- 이미 같은 파일이 있으면 덮어쓰지 않음
- Modrinth 필수 의존성 자동 설치
- `내 모드` 탭에서 기본 서버 모드팩에 없는 추가 모드 목록 표시
- 추가 모드 삭제
- UI 글꼴은 `fonts` 폴더에 포함된 Paperlogy를 사용합니다.
- 작은 글씨도 최소 11pt 이상으로 표시합니다.

CurseForge는 아직 지원하지 않습니다. CurseForge는 API key가 필요해서 배포 런처에 넣기 전에 별도 보안 설계가 필요합니다.

주의:

- 유저가 직접 추가한 모드는 런처가 자동 삭제하지 않습니다.
- 서버 접속에 문제가 생기면 사용자가 직접 추가한 모드와 서버 모드 호환성을 확인해야 합니다.
- Modrinth API 요청에는 런처 식별용 `User-Agent`를 사용합니다.

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

`Version 26.1.2 is not supported`처럼 `minecraft-launcher-lib`의 NeoForge 지원 판정이 새 버전을 따라가지 못하는 경우에는 런처가 NeoForge Maven installer를 직접 다운로드해서 설치합니다. 이때 installer가 요구하는 `launcher_profiles.json`이 없으면 런처가 빈 프로필 파일을 먼저 생성합니다.

`G1NewSizePercent is experimental` 오류가 나지 않도록 런처가 Java 실행 직전에 `-XX:+UnlockExperimentalVMOptions` 옵션을 실험 옵션보다 앞쪽으로 자동 정렬합니다.

발사 버튼을 누른 뒤에는 우주 컨셉 문구가 3초마다 무작위로 바뀝니다.

자동 접속 인자는 사용하지 않습니다. 대신 런처가 `.minecraft_asteroid\servers.dat`에 `소행성 서버`를 등록해서 Minecraft 멀티플레이 서버 목록에 보이게 합니다.

마지막으로 선택한 메모리 할당량은 아래 설정 파일에 저장됩니다. 예를 들어 6GB로 바꿨다면 런처를 다시 켜도 6GB로 시작합니다.

서버 상태 카드의 `해상도 설정` 버튼에서 게임 해상도와 전체화면 시작 여부도 바꿀 수 있습니다. 저장한 해상도, 전체화면/창모드 설정은 런처를 껐다 켜도 유지됩니다.

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
APP_VERSION = "1.16"
UPDATE_API_URL = "https://api.github.com/repos/dbu106524-beep/sohang-launcher/releases/latest"
LAUNCHER_WINDOWS_ASSET_NAME = "SohangLauncher.exe"
```

런처 왼쪽 사이드바와 시스템 로그에는 현재 실행 중인 런처 버전과 실제 실행 파일 경로가 표시됩니다. 새로 설치했는데도 업데이트 버튼이 계속 뜨면, 사이드바의 `런처 vX.X`와 로그의 `실행 파일:` 경로를 먼저 확인하세요. 대부분 예전 exe/app를 다시 실행하고 있는 경우입니다.

런처 코드 자체를 수정했다면:

1. `APP_VERSION`을 올립니다.
   - 예: `1.0` -> `1.1`
2. Windows용 exe를 새로 빌드합니다.
3. GitHub Releases에 새 태그로 릴리즈를 만듭니다.
4. 릴리즈 asset에 exe를 업로드합니다.
   - 추천 파일명: `SohangLauncher-버전.exe`
   - 예: `SohangLauncher-1.16.exe`
   - 다른 `.exe` 파일명이어도 런처가 첫 번째 `.exe` asset을 찾아 자동 설치를 시도합니다.
5. 유저 런처가 새 버전을 감지하면 `런처 업데이트 vX.X` 버튼이 활성화됩니다.
6. 유저가 버튼을 누르면 exe를 다운로드하고, 별도 updater 배치 파일이 기존 exe를 교체한 뒤 런처를 재실행합니다.

주의:

- 자동 교체는 패키징된 Windows exe에서 동작합니다.
- `python launcher.py`로 실행하는 개발 모드에서는 자동 교체하지 않고 릴리즈 페이지를 엽니다.
- macOS에서는 zip asset을 찾으면 런처가 직접 다운로드한 뒤 현재 `.app`을 교체하고 다시 실행합니다. dmg만 있거나 앱 경로를 찾지 못하면 릴리즈 페이지를 엽니다.
- Windows 자동 업데이트는 기존 런처가 완전히 종료될 때까지 기다린 뒤 기존 exe를 백업하고 새 exe를 복사합니다. 기존 exe가 잠겨 있으면 최대 30초 동안 재시도합니다.
- `Failed to load Python DLL ... _MEI...` 오류가 난 버전에서는 한 번만 GitHub Release에서 `SohangLauncher.exe`를 직접 받아 교체해 주세요. 교체 후 다음 버전부터는 수정된 updater가 동작합니다.
- 보안상 더 단단하게 하려면 exe 코드 서명 또는 SHA-256 체크섬 asset을 추가하는 것을 추천합니다.

1.15 변경점:

- Minecraft Services `login_with_xbox` 인증 실패 시 HTTP 상태 코드와 응답 내용을 더 자세히 표시합니다.
- 로그인 실패 시 자동 로그인 캐시를 삭제해서 꼬인 refresh token으로 계속 실패하는 상황을 줄입니다.
- NeoForge patched client jar가 깨진 경우 손상된 NeoForge 파일을 삭제하고 재설치합니다.

1.16 변경점:

- Minecraft Services 인증 서버가 HTTP 429/5xx 또는 일시 네트워크 오류를 반환하면 3회 자동 재시도합니다.
- 최종 실패 시 HTTP 상태 코드를 로그에 표시합니다.

## Windows exe 빌드

현재 Windows용 실행 파일은 아래 경로에 생성됩니다.

```text
dist/SohangLauncher-1.16.exe
```

빌드 명령 예시:

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed `
  --name SohangLauncher-1.16 `
  --icon sohangicon.ico `
  --add-data "sohangicon-transparent.png;." `
  --add-data "sohangicon.ico;." `
  --add-data "fonts;fonts" `
  launcher.py
```

새 런처 버전을 배포할 때는:

1. `launcher.py`의 `APP_VERSION`을 올립니다.
2. `SohangLauncher-버전.exe`를 다시 빌드합니다.
3. GitHub Releases에 새 태그로 릴리즈를 만듭니다.
4. asset으로 `SohangLauncher-버전.exe`와 `Createdin.mrpack`을 올립니다.

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
SohangLauncher-1.16-mac-arm64.zip
SohangLauncher-1.16-mac-x64.zip
```

권장 배포:

- `SohangLauncher-1.16-mac-arm64.zip`: Apple Silicon 맥용입니다. M1, M2, M3, M4 맥북 사용자는 이 파일을 받으면 됩니다.
- `SohangLauncher-1.16-mac-x64.zip`: Intel 맥용입니다.
- GitHub Release를 발행하면 워크플로우가 두 zip 파일을 릴리즈 asset으로 자동 업로드합니다.

워크플로우가 실패한 뒤 파일을 수정했다면 해당 실행 화면 오른쪽 위의 `Re-run jobs` 또는 Actions 탭의 `Run workflow`로 다시 실행합니다.

macOS 아이콘 생성은 `sohangicon-transparent.png`, `sohangicon.png`, `sohangicon.ico` 순서로 시도합니다. 이미지 파일을 GitHub에 잘못 올렸거나 macOS가 읽지 못해도 임시 아이콘으로 빌드가 계속되도록 처리되어 있습니다.

macOS에서 새 버전으로 교체하는 방법:

1. 실행 중인 `SohangLauncher` 또는 `SohangLauncher-버전` 앱을 완전히 종료합니다.
2. `Applications` 폴더나 다운로드 폴더에 남아 있는 이전 `SohangLauncher*.app`를 휴지통으로 보냅니다.
3. 새 `SohangLauncher-버전-mac-arm64.zip` 또는 `SohangLauncher-버전-mac-x64.zip`을 풉니다.
4. 새 `SohangLauncher-버전.app`을 `Applications` 폴더로 옮깁니다.
5. 앱을 열고 왼쪽 사이드바의 `런처 vX.X`가 릴리즈 버전과 같은지 확인합니다.

macOS 코드 호환성:

- 경로는 `os.path` 기반이라 Windows/macOS 모두 대응합니다.
- 자동 로그인 토큰은 macOS에서 Keychain을 사용하도록 되어 있습니다.
- 런처 이미지 리소스는 PyInstaller 번들 경로(`sys._MEIPASS`)를 지원합니다.
- Paperlogy 폰트 파일은 `fonts` 폴더로 번들에 포함합니다.
- macOS에서는 zip asset 기반 자동 교체를 시도하고, 실패하면 릴리즈 페이지 안내 방식으로 운영합니다.
- macOS용 릴리즈 asset 이름은 `SohangLauncher-버전-mac-arm64.zip`, `SohangLauncher-버전-mac-x64.zip`, `SohangLauncher-mac-arm64.zip`, `SohangLauncher-mac-x64.zip`, `SohangLauncher-mac.zip`, `SohangLauncher.dmg`를 인식합니다.

macOS 빌드 예시:

```bash
python3 -m pip install pyinstaller customtkinter minecraft-launcher-lib requests
python3 -m PyInstaller --noconfirm --clean --windowed --name SohangLauncher-1.16 \
  --add-data "sohangicon-transparent.png:." \
  --add-data "sohangicon.ico:." \
  --add-data "fonts:fonts" \
  launcher.py
```

빌드 후 `dist/SohangLauncher-1.16.app`을 압축해서 릴리즈에 올립니다.

```bash
cd dist
zip -r SohangLauncher-1.16-mac.zip SohangLauncher-1.16.app
```

릴리즈 asset 예시:

```text
SohangLauncher-1.16.exe
SohangLauncher-1.16-mac-arm64.zip
SohangLauncher-1.16-mac-x64.zip
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
- [ ] `SohangLauncher-버전.exe`를 새 릴리즈 asset으로 업로드했는가?
- [ ] GitHub 릴리즈에 asset으로 업로드했는가?
- [ ] 새 릴리즈가 latest 상태인가?
- [ ] 런처에서 `MRPACK_URL`이 `releases/latest/download/Createdin.mrpack`인가?
- [ ] 런처 실행 후 로그에 모드팩 업데이트 확인이 뜨는가?


