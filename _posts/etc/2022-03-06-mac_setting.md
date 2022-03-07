---
title: "맥 세팅"
excerpt: ""
category: 
  - etc
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 맥
  - 깃
toc: true
toc_sticky: true
last_modified_at: 2022-03-07T00:00:00+09:00
---
맥북을 새로 사서 웬만한 개발 관련된 건 이제 여기서 하려고 한다. 

# iTerm 설치
42서울에서 iTerm을 사용한 기억이 있어서 iTerm을 설치하려고 했다. 다운로드 사이트는 [여기](https://iterm2.com/)이다. 그냥 다운받고 압축 풀고 application 폴더로 옮겼다.  
테마 설치 같은 것도 있던데 난 불편하지 않은 이상 터미널은 터미널대로 냅두는 걸 좋아해서... 나중에 플러그인 더 설치하게 되면 추가로 적겠다.  
그리고 왜인지는 몰랐는데 iTerm을 설치하니까 바로 깃을 쓸 수 있었다. 알고보니 깃 플러그인도 설치되어 있는 것 같았다.

# 루비 세팅
## Ruby permission 에러
세팅을 하는데 깃허브 블로그를 클론하고 별 생각 없이 gem install jekyll을 했다.

![ruby_error](/assets/images/page/etc/2022-03-06_ruby_error.png)

```
You don't have write permission for the /Library/Ruby/Gems/2.6.0 directory.
```
그러니까 루비 디렉토리에 쓰기 권한이 없다는 건데, 이게 무슨 일이지?

알고보니까 나는 저걸 iterms에서 작업했는데, 거기서 루비의 환경이 시스템 ruby로 되어있었던 것이다. 그래서 root 권한으로 실행하면 설치가 되기는 하는데, 보안의 이유로 바람직한 방법은 아니라고 한다.  
그래서 rbenv를 설치하여 루비의 환경을 새로 추가해서, 현재 루비의 환경으로 지정해주는 작업을 했다. 아마 rbenv는 ruby environment의 약자인 것 같다.

자, 루비 환경을 만들어 주기 위해 한 링크를 찾아서 거기서 명시한 대로 하려고 하는데, brew를 사용했다. brew가 뭐지 하고 찾아봤는데, 맥의 패키지 매니저인 homebrew의 명령어였다. 그래서 어차피 깔아야 할 거, homebrew도 같이 설치했다.

## Homebrew 설치
설치 방법은 간단했다. 우선 [homebrew 다운로드](https://brew.sh/index_ko)에 들어가서 명령어를 터미널에 붙여넣기 해서 실행하면 그만이다.

![homebrew_homepage](/assets/images/page/etc/2022-03-06_install_brew1.png)

터미널에서 해당 명령어를 실행하면 맥 계정 비밀번호 입력하고, brew에서 뭘 설치할 건지 목록을 쭉 보여준 이후에 enter를 누르면 된다.  
return을 눌러서 계속하라길래 처음에 별 생각 없이 백스페이스 눌렀다가, 설마 carriage return의 return인가 해서 엔터를 눌렀다.

![install_brew1](/assets/images/page/etc/2022-03-06_install_brew2.png)

설치가 끝나면 다음과 같은 내용이 터미널에 나온다. Installation successful!

![install_brew2](/assets/images/page/etc/2022-03-06_install_brew3.png)

## Ruby permission 에러 해결
내가 참고한 사이트는 <https://jojoldu.tistory.com/288>이다. 그래도 다시 정리를 하자면

1. rbenv 설치하기
```zsh
brew update  
brew install rbenv ruby-build
```

2. rbenv 설치 확인. 설치된 루비의 버전들이 리스트로 표시된다.
```zsh
rbenv versions
```

3. 설치할 수 있는 루비의 버전 확인
```zsh
rbenv install -l
```

4. 원하는 루비의 버전을 선택하여 설치
```zsh
rbenv install [루비 버전]
```

5. rbenv로 글로벌 버전 변경
```zsh
rbenv global [루비 버전]
```

6. 쉘 설정 파일(나의 경우에는 .zshrc)에 rbenv 설정 추가
```zsh
[[ -d ~/.rbenv  ]] && \
  export PATH=${HOME}/.rbenv/bin:${PATH} && \
  eval "$(rbenv init -)"
```

7. source 명령어로 위의 코드 적용
```zsh
source ~/.zshrc
```

8. gem install 수행
```zsh
gem install bundler
```

참고로 2번에서 rbenv의 버전만 확인하고 싶으면
```zsh
rbenv -v
```
를 실행하면 된다.

# 기타 어플리케이션 설치
## rectangle (무료)
윈도우를 쓰면서 애용했던 기능이 화면 분할이다. 왼쪽으로 창을 끌어서 모서리에 마우스 포인터가 부딪히면 딱 화면의 반 정도 되는 크기로 왼쪽에 정렬되는 그런 기능(이름이 기억이 안 난다). 맥에서는 특별히 설치한 게 없으면 전체화면으로 반반씩 나눠쓰는 그런 식으로 해야하는 것 같았다.  
그래서 찾아본 게 [rectangle](https://rectangleapp.com/)이다.

기능은 아래 이미지와 같다.
![rectangle_function](/assets/images/page/etc/2022-03-06_rectangle_func.png)

키보드로 할 수 있을 뿐만 아니라 마우스로 끌어다가 사용하는 것도 된다.  
비슷한 어플리케이션으로 spectacle도 있는데, 업데이트를 안 한지가 꽤 됐다고 하고, spectacle의 확장 버전이 rectangle이라고 해서 선택했다.

# 맥, iTerm 세팅

> 참조 링크: https://subicura.com/mac/

위 링크엔 맥에 대한 기본과 iTerm 세팅, 여러 플러그인 설치 등의 가이드가 적혀있다. 터미널은 터미널인 채로 냅두고 싶었던 생각이 바뀔 정도로 iTerm 세팅이 다양하다는 걸 봐서 결국엔 세팅을 바꿨다.  
oh my zsh를 설치하고 .zshrc 설정이 뭔가 꼬였는지 iTerm 우측 하단에 `uname -m` 정보가 뜨지 않았다. 그래서 다시 삭제하고 재설치...

## brew install vs brew install --cask
위의 링크에서 뭔가 프로그램을 설치할 때 `brew install --cask` 명령어를 쓴다. 이게 그냥 `brew install`과 무슨 차이가 있는지 알아봤다.  
cask는 brew의 확장 개념으로, GUI 기반 어플리케이션(ex. 크롬)까지도 설치할 수 있게 해준다고 한다. 그래서 뒤에 나오는 docker라든가, keka같은 GUI 프로그램을 설치할 때 `brew install --cask` 명령어를 쓴 것이다. 예전에는 `brew cask install`라고 썼다고 한다.

# 세팅 후
▼ iTerm
![iTerm](/assets/images/page/etc/2022-03-07_zsh.png)

▼ SpaceVim
![SpaceVim](/assets/images/page/etc/2022-03-07_spacevim.png)

참고로 oh my zsh는 vscode에서 연 터미널에도 유효하다.