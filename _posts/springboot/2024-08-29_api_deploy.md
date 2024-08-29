---
title: "Rest Docs를 자동배포 해보자!"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
  - 문서화
toc: true
toc_sticky: true
last_modified_at: 2024-08-29T00:00:00+09:00
---

Rest Docs를 나만 보면 되지 않나 했는데, 이건 공개하자는 의견이 있어 해당 API 문서는 공개하기로 했다.  
html 파일들을 일일이 올리기는 싫었던지라, 해당 파일들을 자동으로 배포하려 한다.

# 아이디어
## 1. 깃허브 위키에 올리자
처음에는 깃허브 위키에 올리는 방법을 생각했다.  
프로세스는 gradle이 빌드를 하면서 API 문서를 만들면, 그때 깃허브 위키에 업로드 하는 방식이었다.  
그러기 위해서는 깃허브 위키에 gradle로 접근하는 방법이 필요했고, 그 과정에서 wiki 리포지토리에 git으로 push하는 방법을 gradle로 하는 방법을 알아냈다.

```gradle
exec {
    commandLine 'git', 'commit', '-m', '이런 식으로'
}
```

그런데 하다보니 든 생각이, "위키에서 html을 지원하나? 마크다운 문법 아닌가?" 였다. 물론 html을 쓸 수는 있는데, 페이지네이션이나 링크는 어떻게 되는건가 싶었다.  
그래서 두 번째 방법을 고안했다.

## 2. 깃허브 페이지에 올리자
이 블로그처럼 깃허브 페이지를 이용하는 방법이다. 우선 깃허브 페이지를 만들고 거기에 `index.html`을 비롯한 다른 API 문서들을 올리기로 했다.  
그러기 위해서는 또 두 가지 방법이 떠올랐는데, 하나는 "새로운 폴더에서 API 리포지토리에 연결" 이고, 또다른 하나는 "기존 폴더에서 API 리포지토리에 연결" 이었다.  
이미 `BOOT-INF`와 `static/docs`에 같은 html 파일이 올라가있는 상황에 또 똑같은 파일을 복사해서 쓰고 싶지 않았기 때문에, 기존의 리포지토리에서 서브 트리로 API 리포지토리에 연결하기로 했다.

이 과정에서 서브트리를 처음 써봤는데, 기존 리포지토리의 서브 트리인 `static/docs` 내의 파일들은 API 리포지토리에 연결되어 거기서만 관리하고, 기존 리포지토리에서는 추적하지 않는 것 같았다.  
서브트리를 만들고 연결하는 건 쉬웠는데 문제는 이걸 gradle 스크립트로 짜야 한다는 거... 

처음에는 통짜로 무조건 `static/docs`에 있는 파일들은 그냥 add, commit, push하고 에러가 발생하면 `ignoreExitValue = true` 를 이용했다.  
물론 제대로 동작하지도 않기도 하거니와 이건 너무 비효율적이지 않나 싶어서 오직 `static/docs`에 변경 사항이 있으면 그것만 push 하도록 하고 싶었다. 그리고 여기부터 고난과 역경이 시작되었다.

### 에러 발생: `cause execcommand == null!`
이건 지나고보니 단순한 에러였다. gradle task를 register할 때, `tasks.register('작업', Exec)` 이런 식으로 했었는데, 막상 내부에 실행하는 부분이 없어서 발생한 에러다.  
그래서 뒷부분에 task type을 지정해주는 `Exec`를 제거하여 해결했다.

### 에러 발생: 왜 `static/docs`의 status가 아니라 모든 status를 훑어보니?
분명히 `commandLine 'git', 'status', apiDir`로 줬는데, 왜 자꾸 루트 폴더에 있는 `build.gradle`의 변경사항을 알려주는지 의문이었다. 저때 당시에 `def apiDir = src/main/resources/static/docs`였는데 이후에 `file()`로 감싸줬더니 의도대로 동작했다.  
생각해보면 파일 경로를 줘야 하는 게 맞으니까 이거에 대해서는 해결하는 데 오래 걸리지 않았다.

### 고난: `exec {}`의 결과를 가져오고 싶어!
내가 검색을 잘못한 건지는 모르겠는데, 구글도 그렇고 AI들도 그렇고 exec 값을 가져오는데 자꾸 `toString().trim()`을 쓰라길래 그거 썼다가 `null`에는 `toString()` 못 쓴다라는 충격적인 에러를 뱉었다.  
이게 왜 충격이었냐면, `git status`를 한 결과를 가져오는 건데 그 결과가 `null`이니까 `toString()`을 못 쓴다는 거 아닌가 했다. 알고보니 `exec {...}.StandardOutput어쩌구` 하면서 결과를 가져오는 방식이 잘못되었고, 이건 기존의 표준 출력을 변수에 담아둠으로써 `git status`의 표준 출력 결과물을 변수에 담아 이용하는 식으로 해결했다.

```gradle
// 변경 사항 확인
def changes = new ByteArrayOutputStream()
exec {
    commandLine 'git', 'status', '--porcelain', apiDir
    standardOutput = changes
}

// 변경 사항이 없으면 커밋하지 않음
if (changes.toString().isEmpty()) ...
```

### 에러 발생: 왜 push 때마다 에러가 발생할까...
여기가 진짜 원인 찾을때도, 해결할 때에도 혈압올랐었다.  
자꾸 `git pull`하라길래 기존 `git pull`을 하자니 지금 작업 중인 `build.gradle` 파일이 덮어씌워지고, 애초에 "서브트리면 기존 리포지토리 영역은 건드리지 않아야 하는 거 아닌가" 했다.  
심지어는 `git subtree pull`도 이미 최신이라고 출력돼서 `git pull`의 문제가 아니란 걸 깨달았다.

그리고 자꾸 `BOOT-INF`에 빌드하고나면 html 파일이 생성되는데 깃에서 이걸 추적중이어서 추적을 끊어버렸다. 어차피 `jar` 파일만 배포하면 되는데 굳이 깃에서 추적해야하나 했다.  

사투 끝에 원인은 기존 리포지토리에 변경사항이 있기 때문에 그거 먼저 업데이트 하고 서브트리 내용을 push 하란 것이었는데, 이러면 기존 것을 커밋했는지도 강제된다.  
테스트도 강제, 커밋도 강제되는 건 좀 아니지 않나 했는데 뭐... 커밋도 중요하니까.

### 승리
> 전리품: <https://eternal-return-user-creator.github.io/er-bal-api.github.io/>

```
BUILD SUCCESSFUL in 31s
10 actionable tasks: 8 executed, 2 up-to-date
오후 5:52:35: Execution finished 'build --stacktrace'.
```

Makefile도 그렇고 DockerFile이나 요즘 들어 이런저런 스크립트들도 다뤄보는 것 같다... 다음엔 더 잘할 수 있을 거야.