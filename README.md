# 소행성 런처 배포 / 모드팩 업데이트 가이드

이 문서는 GitHub Releases에 `Createdin.mrpack`을 올리고, 런처가 자동으로 최신 모드팩을 받게 하는 방법을 정리한 것입니다.

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
   - 반드시 `Createdin.mrpack` 이름으로 업로드합니다.
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

1. GitHub의 최신 `Createdin.mrpack`을 확인합니다.
2. 기존 모드팩과 다르면 새로 다운로드합니다.
3. 다운로드한 파일이 진짜 Modrinth `.mrpack`인지 검사합니다.
4. 기존 `mods` 폴더에서 빠진 모드를 정리합니다.
5. 새 모드팩 기준으로 모드와 NeoForge를 설치합니다.
6. `dinbu.kro.kr` 서버로 자동 접속합니다.

## 꼭 지켜야 하는 것

- 릴리즈 asset 파일명은 반드시 `Createdin.mrpack`이어야 합니다.
- GitHub 저장소가 private이면 유저 런처가 다운로드하지 못합니다. public 저장소 또는 public release asset이어야 합니다.
- Google Drive, OneDrive 공유 링크는 자동 다운로드에 부적합합니다.
- 모드팩을 바꿨는데 적용이 안 되면 새 릴리즈가 `Latest`인지 확인합니다.

## 런처 자체 업데이트

현재 런처는 GitHub latest release tag를 확인해서 새 버전이 있으면 로그에 알려줍니다.

```python
APP_VERSION = "1.0"
UPDATE_API_URL = "https://api.github.com/repos/dbu106524-beep/sohang-launcher/releases/latest"
```

런처 코드 자체를 수정했다면:

1. `APP_VERSION`을 올립니다.
   - 예: `1.0` -> `1.1`
2. 새 exe 또는 새 런처 파일을 빌드합니다.
3. GitHub Releases에 새 태그로 업로드합니다.
4. 유저는 로그에 뜬 업데이트 안내를 보고 새 런처를 받으면 됩니다.

완전 자동으로 exe를 자기 자신이 덮어쓰는 기능은 아직 넣지 않았습니다. 이 기능은 별도 updater 프로그램으로 구현하는 것이 안전합니다.

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
- [ ] GitHub 릴리즈에 asset으로 업로드했는가?
- [ ] 새 릴리즈가 latest 상태인가?
- [ ] 런처에서 `MRPACK_URL`이 `releases/latest/download/Createdin.mrpack`인가?
- [ ] 런처 실행 후 로그에 모드팩 업데이트 확인이 뜨는가?
