---
title: "깃허브 액션으로 E2E 테스트 자동화하다 맞닥뜨린 에러들"
excerpt: ""
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - web
  - github action
  - 이터널 리턴
  - 밸런스 게임
toc: true
toc_sticky: true
last_modified_at: 2025-01-20T16:00:00+09:00
---

# Github Action으로 자동화
## 프로세스
- 리포지토리 체크아웃
- 파이썬 설치
- 웹 브라우저, 브라우저 드라이버 설치
- Docker Compose 설치
- github secret으로 .env 생성
- docker-compose up
- selenium 테스트를 위한 XVFB(가상 X윈도) 설치
- 파이썬 가상환경 설정 및 패키지 설치
- pytest 실행

## 맞닥뜨린 에러들
### Chrome Driver 버전 관련
selenium에서는 웹 브라우저 드라이버가 있어야 브라우저와 Selenium 사이의 중개 역할을 하기 때문에, 크롬과 크롬 드라이버를 설치해야 한다.

처음에는 무턱대고 stable 버전의 크롬과 크롬 드라이버를 다운 받았고, 이런 에러가 발생했다.

#### 에러
```shell
    @pytest.fixture(scope="module")
    def driver(request):
        browser = request.config.getoption("browser")
>       driver = driver_factory(browser)

test/conftest.py:7:

response = {'status': 500, 'value': '{"value":{"error":"unknown error","message":"unknown error: Chrome failed to start: exited a...\\n#16 0x5651cc55c243 \\u003Cunknown>\\n#17 0x7fbafa49ca94 \\u003Cunknown>\\n#18 0x7fbafa529c3c \\u003Cunknown>\\n"}}'}
```

#### 원인
원인은 구글링을 해보니 크롬과 드라이버의 버전에 주의하라는 내용이 있었다.  
github action의 로그를 살펴보니 크롬은 131, 드라이버는 114의 메이저 버전으로 설치가 되었다.  

정상적으로 동작하려면 크롬과 드라이버의 메이저 버전이 일치해야 했는데, 구글 공식 사이트에서 검색을 해보니 드라이버가 114 버전까지 나왔는데 크롬은 114 버전이 없다는 것을 알았다.

#### 해결
구글링을 더 해보니 테스트 용으로 배포되는 크롬이 있길래 나는 일반적인 크롬이 아닌 chrome-for-testing을 설치하는 방식으로 해결했다.

chrome-for-testing: <https://googlechromelabs.github.io/chrome-for-testing/>

### XVFB 관련
크롬도 설치했겠다, 이제 돌아가겠지 하고 github action을 실행했는데 이번엔 다른 에러가 발생했다.

```shell
E       selenium.common.exceptions.SessionNotCreatedException: Message: session not created: probably user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-dir
```

#### 시도해 본 것
처음에는 에러 로그가 말한대로 `--user-data-dir`을 지정했었다. 이게 알고보니 크롬의 프로필마다 사용자 경험과 관련된 데이터를 저장하는 디렉터리가 있는데, 누구 디렉터리를 사용할 것인지를 설정하는 것 같았다.  
그래서 디렉터리를 지정해봤는데 여전했다.

세션이 계속 열려있는 경우에도 저런다길래 pkill로 크롬도 종료시켜보고, `guest` 옵션도 줘 보고, 우분투 24 버전이라 그렇다길래 22로 낮춰도 보고 등등 여러 가지 해봤는데 계속 저 에러가 발생했다.

#### 해결
원인은 엉뚱한 곳에 있었는데, 답은 `pytest`를 실행하는 `run` 블록과 다른 곳에서 XVFB를 활성화 하고 그 활성화한 블록에서만 상태가 유지되었던 것이다. 즉, `pytest`를 실행하는 `run` 블록에서는 XVFB가 꺼져 있었던 것이다.

그래서 pytest를 실행하는 블록에서 XVFB를 활성화하는 식으로 해결했다.

```shell
xvfb-run --server-args="-screen 0 1280x1024x24" pytest --browser chrome
```

## 아쉬웠던 점
### 하나의 브라우저로 테스트
파이어폭스나 사파리도 같이 테스트하고 싶었는데, 파이어폭스까지 포함하면 테스트 시간이 너무너무 길어졌다.  
Selenium Grid를 사용해서 브라우저마다 컨테이너를 별도로 띄워서 병렬로 테스트하는 방식도 있는 것 같긴 한데, 그건 더 알아보고 시도해봐야겠다.

사파리는 맥 브라우저라서 실행 환경을 아예 다르게 해야 하는 거라 일단은 제외했었다.  
다음엔 사파리로도 테스트 해보고 싶다.
