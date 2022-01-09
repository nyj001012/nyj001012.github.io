---
title: "깃허브 블로그 리뉴얼 (jekyll)"
excerpt: "근 2년 동안 써 온 블로그를 갈아엎게 되는데..."
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag: 
  - jekyll
  - jekyll customize
toc: true
toc_sticky: true
last_modified_at: 2022-01-09T00:00:00+09:00
---
![image](/assets/images/page/web/before_renewal.png)
> 블로그 폰트 나눔고딕으로 바꾸고 싶은데 구글링 한 지킬(jekyll) 폴더 구조랑 다르네..? 어? 이상하다?

때는 어제, 즉 2021년 12월 14일. 긴 잠복기를 끝내고 슬슬 다시 블로그에 글을 올리려는데 글씨체가 마음에 안 들었던 나는 폰트를 바꾸기로 했다.

구글링을 해보니 구글에서 웹폰트 ```@import문```을 복사해서 ```main.scss```에 넣으라는데, ```main.scss```가 어딨지?

그제서야 깨달았다. "내가 깃허브 블로그를 잘못 사용하고 있었구나."

이전에는 블로그 글을 어떻게 쓰고 있었냐면, 그냥 깡으로 마크다운 파일을 깃허브 페이지에서 직접 일일이 쓰고 있었다.   
그러다보니 실제 웹에서 페이지가 어떻게 보이는지를 전부 커밋을 하면서 확인할 수 밖에 없었고, 그 과정에서 쓸데없는 커밋 내역이 늘어나게 되었다.

게다가 블로그 글 작성할 때 vscode로 작성한다는 말을 듣고 심각하게 이건 정말 잘못되었다고 느껴서 급하게 블로그를 리뉴얼하게 되었다.  

여기저기서 지킬 블로그를 어떻게 구성하고 커스터마이즈하는 데 

아래는 내가 지킬을 새로 다운받아 리뉴얼하기까지 어떤 과정을 겪었는지, 어떤 url을 참고했는지를 정리했다.  

## 1. Minimal-mistakes를 다운받자
1. <https://github.com/mmistakes/minimal-mistakes>에 접속해서 코드를 전부 다운 받아 블로그 폴더에 압축을 푼다.  

## 2. Ruby, 지킬을 설치하자
1. <https://rubyinstaller.org/downloads>에 접속해서 WITH DEVKIT 중에 (x86) 실행파일을 다운받는다. 이유는 jekyll이 32비트 기반이라 Ruby를 64비트로 설치하면 에러가 날 수 있다고 한다.
2. 설치를 하고 나면 블로그 폴더에서 cmd를 켜고
```ruby
gem install jekyll
gem install minima
gem install bundler
gem install jekyll-feed
gem install tzinfo-data
```
를 실행해준다.
3. 위의 사항이 끝나면 아래의 명령어로 jekyll을 로컬에서 실행할 수 있는데
```ruby
jekyll serve
```
이 명령어를 실행하고 뭔가 required인데 없어서 저 명령 실행 못 한다거나 하는 에러가 뜨면 필요한 것들 ```gem install``` 명령으로 전부 설치해주면 된다.
4. ```jekyll serve``` 명령어가 실행되면 Server address를 알려주는데, 그곳으로 접속하면 로컬에서 jekyll의 모습을 확인할 수 있다. 접속을 하면 minimal-mistakes의 ```index.html``` 페이지로 이동한다.

## 3. Minimal-mistakes를 커스터마이즈하자
처음 ```index.html```의 모습을 보면 내가 흔히 봐오던 github 블로그의 모습이 아니다. 우리가 블로그를 꾸며야 한다.  
아래는 내가 참고했던 사이트들의 링크를 적어놓은 것이다.

### 3.1. minimal-mistakes 스킨 샘플
<https://mmistakes.github.io/minimal-mistakes/docs/configuration/#dirt-skin-dirt>

### 3.2. 부제목으로 작성 일자 추가, 포스트 제목 밑줄 제거
<https://livlikwav.github.io/etc/blog-revision-1/>

### 3.3. 왼쪽 사이드 바에 카테고리 보여주기
<https://seungwubaek.github.io/blog/left_sidebar/>

### 3.4. 카테고리 별 포스트 개수 나타내기
<https://lakshmanbasnet.com/how-to/display-jekyll-post-count/>

#### 3.4.1. 카테고리 별 포스트 개수 보여주기
이건 내가 ['3.4. 카테고리 별 포스트 개수 나타내기'](#34-카테고리-별-포스트-개수-나타내기)에서 카테고리 별 포스트 개수를 나타내기 위해 어떤 과정이 있었는지를 적은 것이다.  

위의 참조 링크에서 Post in category 부분을 보면 {% raw %}```{{ site.categories.CAT | size }}```{% endraw %}를 사용하면 된다고 하는데 작동을 하지 않았고, 구글링 해도 별 다른 성과가 없어서 따로 작성했다. 

1. 일단 어디서 nav를 수정할 수 있는지 파악하자.
![nav 태그 위치](/assets/images/page/web/2021-12-18_show_category_count1.png)
nav에 우클릭을 하여 '검사'를 클릭하면 해당 엘리먼트에 대해 크롬 개발자도구로 내용을 바로 확인할 수 있는데, 보면 ```nav__list > nav__items > li > a > span```에 카테고리 이름이 나타나는 것을 볼 수 있다. 따라서 nav가 포함된 ```_includes > sidebar.html```을 살펴보기로 했다.  

2. ```sidebar.html```에서 nav를 확인하자.
![sidebar.html](/assets/images/page/web/2021-12-18_show_category_count2.png){% raw %}  
```liquid  
{% if s.nav %}{% include nav_list nav=s.nav %}{% endif %}
```
{% endraw %}내가 Liquid는 처음 써봤지만 ```{ page.sidebar }```의 ```nav```가 존재하면 ```nav=s.nav```로 nav_list에 포함하라는 것 같다.  
그렇다면 nav에 대해 자세한 정보는 ```nav_list```에 있을테니 ```_includes > nav_list```를 살펴보자.  

3. ```nav_list```를 수정하자.
![nav_list](/assets/images/page/web/2021-12-18_show_category_count3.png){% raw %}  
```liquid  
<a href="{{ nav.url | relative_url }}"><span class="nav__sub-title">{{ nav.title }}</span></a>
```
{% endraw %}이 부분이 nav에 어떤 정보를 표시해줄지 결정하는 곳인 것 같다. 코드를 보면 ```navigation```의 요소를 순회하면서 ```nav```의 ```title```속성을 가져오는 것 같은데, 이 속성은 어디서 정의한 걸까? 바로 ```_data > navigation.yml```이다.

4. ```navigation.yml```에 속성을 추가하자.
![navigation.yml](/assets/images/page/web/2021-12-18_show_category_count4.png)
직감적으로 ```navigation.yml```에서 ```title```에 해당하는 부분이 ```nav_list```의 ```nav.title```의 값일 거라 생각했다.  
따라서 일반적인 객체의 프로퍼티라 생각하고 ```name```을 추가했다.  
그리고 sidebar의 카테고리를 클릭하면 url이 ```localhost:4000/web/```으로 이동하기 때문에 ```name```에는 url의 카테고리 부분을 나타내는 ```web```만 적었다.

1. ```nav_list```를 수정하자.
![nav_list](/assets/images/page/web/2021-12-18_show_category_count5.png)  
{% raw %}```{{ site.categories.CAT | size }}```{% endraw %}에서 나는 ```site.categories```를 ```navigation.yml```에서 정의했기에, 처음에는 ```site.categories```의 속성값이자 ```navigation.yml```에서 정의했던 ```name```을 이용했다.{% raw %}  
```liquid  
<a href="{{ nav.url | relative_url }}"><span class="nav__sub-title">{{ nav.title }}</span></a>
```
{% endraw %} 이 부분을{% raw %}  
```liquid  
<a href="{{ nav.url | relative_url }}"><span class="nav__sub-title">{{ nav.title }} ({{ site.categories.nav.name | size }})</span></a>
```
{% endraw %}이렇게 바꿔보았는데...
![first-try](/assets/images/page/web/2021-12-18_show_category_count6.png)
전부 0으로 나타나는 맙소사한 상황이 나타났다.  
찾아보니까 ```site.categories```를 쓸 때는 내가 위에서 적은 ```site.categories.nav.name```이 아니라, ```site.categories[nav.name]``` 방식으로 적어야 한다고 한다([참조 링크](https://stackoverflow.com/questions/22441281/jekyll-site-categories-variable)).  
따라서 이렇게 바꿨다.{% raw %}  
```liquid  
<a href="{{ nav.url | relative_url }}"><span class="nav__sub-title"> ({{ site.categories[nav.name] | size }})</span></a>
```
{% endraw %}그리고 결과물은 이렇다. 짠☆
![end](/assets/images/page/web/2021-12-18_show_category_count8.png)  

늘 그렇지만, 역시 코드를 작성할 때 변수 명이나 파일, 클래스 명 등등을 직관적이고 명시적으로 표기하는 게 중요한 거 같다. 덕분에 이런 파일은 여기 있겠고 이건 무슨 역할을 하겠다는 게 바로 눈에 들어왔으니까.

### 3.5. 카테고리 별 페이지 만들기 및 태그 등록하기
<https://devinlife.com/howto%20github%20pages/category-tag/>

### 3.6. Utterances로 댓글 기능 추가하기
자, 내가 블로그를 만들어서 가장 하고 싶었던 일은 피드백을 받는 건데, 그러려면 댓글 기능을 이용하는 게 제일 편할 것 같았다.  
그래서 가장 많이 봐왔던 disqus를 쓰려고 했는데 ["disqus를 버리자"](https://blueshw.github.io/2020/05/20/disqus-to-utterances/)를 읽고 생각이 바뀌었다.  
구글링을 좀 해보니까 Utterances가 깔끔하고 가벼워서 이 블로그의 댓글을 구현할 오픈소스로 선택하였다. 깃허브에 로그인해야만 댓글을 달 수 있지만, 막말로 요즘 누가 아직도 깃허브 아이디가 없나?

["mmistakes - utterances comments"](https://mmistakes.github.io/minimal-mistakes/docs/configuration/#utterances-comments)
에서 하라는 대로 하면 되는데... 역시나 한 번에 될 리는 없지.  

#### 3.6.1. comments div는 어디에?
돌아온 분해 시간. 이번에도 mmistakes의 폴더 구조를 파헤쳐보겠다. 먼저 댓글 기능이 html 내 어디에 있는지를 확인하기 위해 다른 분의 블로그에서 댓글 영역을 크롬 개발자 도구로 확인하였다. 그 결과
![comments_div](/assets/images/page/web/2021-12-20_utterances1.png)  {% raw %}  
```liquid  
{% if jekyll.environment == 'production' and site.comments.provider and page.comments %}
  {% include comments.html %}
{% endif %}
```
{% endraw %}
```_layouts > single.html```의 이 부분인 것을 확인했다. 봤을 때 ```jekyll.envorionment == 'production``` 이면서 ```site.comments.provider```, ```page.comments ```가 빈 값이 아니어야 한다.

##### 3.6.1.1. ```jekyll.envorionment != 'production```이다?
["jekyll - Environment"](https://jekyllrb.com/docs/configuration/environments/)를 읽어보면, 지킬의 environment를 'production'과 'development'로 구성할 수 있고 기본값은 'development'라고 한다. 사실 이게 정답이다. 로컬에서 실행할 때에는 'development' 방식이지만, 깃허브에 푸시하고 난 다음인 nyj001012.github.io에는 'production'으로 돌아가는 거같다.  
["Utterance comment does not appear working locally to me."](https://github.com/mmistakes/minimal-mistakes/issues/2457)를 봐도 "모든 환경 변수는 ```production```에서 세팅된다.(It sets all sorts of environmental variables when in ```production```)"이라고 mmistakes owner가 issue에 답을 달았다.  
답은 나왔지만 나머지 경우도 보자.

##### 3.6.1.2. ```not site.comments.provider || not page.comments```이다?
개인적으로 이건 말이 안 된다고 생각했던 게, ```site.comments.provider```는 ```config.yml```에서 이미 ```utterances```로 지정해줬다. 그리고 ```page.comments```가 아예 없다면, 즉 페이지에 댓글이 아예 없어도 댓글창은 있어야 한다 해서 이건 문제될 게 없다 생각했다.  

2번 글을 유심히 본 사람이라면 저기서 잘못된 것이 있음을 알아챘을 것이다. 그건 이따 설명하겠다.

#### 3.6.2. 푸시해서 nyj001012.github.io에서 확인해보자?
대망의 확인 시간, 일단 모든 변경 사항을 스테이징하고 전부 커밋 후 푸시했다. 몇 분 지나고 블로그를 확인해보는데... 댓글창이 없네?ㅎ  
그럴 수 있지 하면서 다시 파일을 살펴봤다.

#### 3.6.3. ```_config.yml```을 수정하자
아 역시, 한참 동안 repo 주소가 잘못됐나 뭘 빼먹었나, 오타가 났나 하면서 약 30-40분을 구글링과 함께 뒤져보다가 어이없는 실수를 발견했다.
나는 ```_post``` 설정을 ```_page```와 분리했는데, 여기서 ```_post``` 설정 중, ```comments: false```로 해놓은 것이었다. 댓글창 나타내는 걸 false라 해놓으니 당연히 댓글이 안 보이지. 그런데 이 변수명 낯이 익은데..?  
그렇다. 앞의 ['3.6.1.2. ```not site.comments.provider || not page.comments```이다?'](#3612-not-sitecommentsprovider--not-pagecomments이다)에서 ```if ... page.comments``` 부분이 바로 이 설정과 관련된 것이었다. 나는 저 page를 흔히 생각하는 일반적인 page로 생각했지, 저걸 사이트의 변수로 생각하지 않았다. 이런 댕청한.  
```_config.yml > _post```의 설정은 아래와 같이 변경했다.
```yml  
#Defaults
defaults:
  # _posts
  - scope:
      path: "_posts"
      type: posts
    values:
      layout: single
      author_profile: true
      comments: true # updated, default: false
      ...
```

#### 3.6.4. ```single.html```을 수정하자
```_config.yml```의 댓글 설정을 변경해줬으니 이걸 포스트의 주요 레이아웃인 ```single.html```에 적용하겠다.
!["single.html with comments"](/assets/images/page/web/2021-12-20_utterances2.png)
```html
---
layout: default
author_profile: true
sidebar:
  -nav: "main"
comments: true <!-- added -->
---
```

#### 3.6.5. nyj001012.github.io에서 확인하자
수정을 끝내고 내 깃허브 블로그에 가보면 댓글창이 잘 열린 걸 확인할 수 있다.
!["with comments"](/assets/images/page/web/2021-12-20_utterances3.png)

#### 3.6.6. 댓글창이 안 나올 때
출근을 하고 심심해서 내 블로그 포스트가 잘 올라갔나 하고 보는데 포스트에 댓글창이 없다?  
혹시 다른 포스트도 다 댓글창이 없나 싶어서 살펴보니까 어제 올린 오직 ['성장에 한계를 느끼는 순간, 스스로 돌파구를 찾는 개발자가 되려면'](../lecture/2021-12-21-돌파구를%20찾는%20개발자가%20되려면.md) 포스트에서 '댓글 남기기'라는 문구만 남아있었다.

뭐 만들다 보면 오류 만나는 건 심심치 않아서 당황하지 않고, 혹시나 콘솔에 로그가 찍혀있나 싶어서 바로 크롬의 개발자 도구를 켰다.  
역시 콘솔에는 에러 로그가 찍혀 있었다.

![utterances_error](/assets/images/page/web/2021-12-22_utterances_error.png)
맨 처음 GET으로 시작하는 에러 로그의 링크를 클릭해보니, 왼쪽 박스의 ```issues?q=%...```가 눈에 띄었다. 딱봐도 느낌이 ```issues```는 내 레포지토리의 issues와 연결시켜주는 역할을 하는 것 같고, ```q```는 쿼리 스트링 같았다.  
해당 내용을 자세히 살펴보자.
```json
errors:
  code: "invalid"
  field: "q"
  message: "The search is longer than 256 characters."
  resource: "Search"
```
저게 무슨 내용일지 느낌이 온다. 내가 집중해서 본 부분은 다음과 같다.  
'search가 256글자보다 길다.'  
'resource는 "Search"고, field는 "q"다'
즉, 쿼리를 담당하는 'q'의 길이가 너무 길어서 utterances를 불러오는 데 문제가 생긴 것 같다.

나는 "아니 왜 저 파일 명이 얼마나 길다고 256자를 넘어가?" 했는데 다 이유가 있었다.  
지금 내 블로그의 url을 보면 거의 한글로 되어 있는데, 이걸 쿼리 스트링으로 만드는 과정에서 바이트로 변환되는 것 같았다. 밑에는 정상적인 포스트의 'q' 필드 값이다.
```json
"total_count": 1,
"incomplete_results": false,
"items": [
  {
    "url": "https://api.github.com/repos/nyj001012/nyj001012.github.io/issues/4",
    "repository_url": "https://api.github.com/repos/nyj001012/nyj001012.github.io",
    ...
    "title": "web/%EA%B9%83%ED%97%88%EB%B8%8C-%EB%B8%94%EB%A1%9C%EA%B7%B8-%EB%A6%AC%EB%89%B4%EC%96%BC-(jekyll)/",
    ...
  }
...
]
```
저 포스트는 현재 포스트의 ```issues```인데, ```"title"```을 보면 영어 부분은 그대로고 한글만 변환되어 있는 것을 볼 수 있다.  
저러니 256자가 넘어가지.  
희한한 건 '-'나 '()'는 그대로 표현됐고, 앞에 내가 붙여놓은 날짜는 생략됐다는 것이다.  

어쨌든 이번 일로 **파일 제목을 절대 한글로 지으면 안 된다**는 것을 깨달았다. 원래 코딩할 때는 영어로 지었는데, 포스팅 할 때도 영향을 줄 줄은 몰랐다.

### 3.7. 업데이트 날짜 추가하기
근본적으로는 각 포스트의 .md 파일에 ```last_modified_at```을 추가하면 된다. 그런데 나는 업데이트 날짜에 대해 다음과 같은 기능이 필요했다.

- 각 포스트의 페이지에서 ```last_modified_at```을 푸시를 하는 순간 자동으로 입력될 것
- 카테고리 페이지에서 업데이트 날짜를 보여줄 것
- 업데이트 한 날짜를 기준으로 카테고리 페이지에서 포스트들을 정렬할 것

첫 번째 것은 실패했는데 (이런저런 시도를 해봐도 방법을 도저히 못 찾겠다.) 나머지는 내가 직접 튜닝을 해서, 그걸 적어보도록 하겠다.

#### 3.7.1. 카테고리 페이지에서 업데이트 날짜 보여주기
우선 'web' 카테고리의 레이아웃에서 어떤 부분이 날짜를 표시하는지를 봤다.
![update_date1](/assets/images/page/web/2022-01-01_align_post1.png)

```category.html```은 ```posts-category.html```을 include하였고, 

![update_date2](/assets/images/page/web/2022-01-01_align_post2.png)

```posts-category.html```에서는 ```archive-single.html```을 include, 

![update_date3](/assets/images/page/web/2022-01-01_align_post3.png)

```archive-single.html```에서 ```page__meta.html```을 include했다.

![update_date4](/assets/images/page/web/2022-01-01_align_post4.png)

그리고 드디어 ```page__meta.html```에서 날짜를 표시하는 부분을 찾았다.  
코드를 보아하니 각 post를 document에 할당하고, document의 작성일(date)을 date라는 변수에 할당한 것 같았다. 그래서 나는 할당할 때 수정 날짜를 할당하면 되겠지 싶어서 5번 라인을 다음과 같이 변경하였다.{% raw %}
```liquid
{% if document.last_modified_at %} <!-- 수정일이 있으면, 수정일을 보여준다. -->
  {% assign date = document.last_modified_at %}
{% else %}
  {% assign date = document.date %}
{% endif %}
```
{% endraw %}

![update_date5](/assets/images/page/web/2022-01-01_align_post5.png)

카테고리 페이지에서 블로그 리뉴얼 포스트의 날짜가 성공적으로 바뀌었다. 나는 확인차 해당 포스트 내의 페이지에도 들어가봤는데

![update_date6](/assets/images/page/web/2022-01-01_align_post6.png)

작성일자가 업데이트 날짜로 바뀐 대참사가 일어났다. 확인해보니까 포스트 내의 작성일과 카테고리 페이지 내의 날짜는 같은 양식을 공유한다. 즉, 같은 ```page__meta.html```을 include하고 있기 때문에 따로따로 날짜를 지정해주려면 파일을 따로 include해야 했다.  

이에 나는 포스트 내의 업데이트 날짜를 작성일로, 카테고리 페이지와 포스트 내의 작성일을 업데이트 날짜로 바꿔치기를 하려고 했다.  
포스트 내의 작성일자를 다루는 파일은 ```single.html```에서 include한 ```page__date.html```이다.

![update_date7](/assets/images/page/web/2022-01-01_align_post7.png)

위에서는 포스트의 수정일자가 있는지 없는지에 따라 보여줄 내용을 구분했는데, 나는 이걸 빨간 박스 부분을 아예 제거해서, 수정일자가 아니라 작성일만 보여주도록 했다.
{% raw %}
```liquid
{% assign date_format = site.date_format | default: "%B %-d, %Y" %}
<p class="page__date"><strong><i class="fas fa-fw fa-calendar-alt" aria-hidden="true"></i> {{ "최초작성:" }}</strong> <time class="dt-published" datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: date_format }}</time></p>
```
{% endraw %}

이렇게 하면 하단의 '업데이트: 업데이트 날짜' 였던 부분이 '최초작성: 작성일'로 바뀐다.(카테고리랑 열 너비 맞추고 싶어서 일부러 띄어쓰기 안 했다.) 포스트의 최초 작성일보다 업데이트 날짜를 중시하는 나에게는 저게 맞는 방법이었다. 

다음에는 이 업데이트 날짜를 토대로 카테고리 페이지를 정렬해보자.  

### 3.8. favicon.ico 추가하기
![favicon_error](/assets/images/page/web/2022-01-09_favicon1.png)

"아 알았어 favicon 추가해주면 될 거 아냐."  
매번 개발자 도구를 켤 때마다 저 오류가 뜨는 게 상당히 거슬려서 일단 favicon 먼저 추가해주기로 했다.

#### 3.8.1. 마음에 드는 아이콘을 찾자
![flaticon](/assets/images/page/web/2022-01-09_favicon2.png)

위의 사이트는 무료 아이콘으로 유명한 flaticon의 사이트이다. ['The noun project'](https://thenounproject.com/)도 유명한데, 여기는 유료 회원이 아니면 흑백 밖에 못 써서 flaticon으로 정했다.  

아이콘은 삐약이에 맞는 병아리로 다운받았다.

#### 3.8.2. 어디에 favicon을 추가할까?
![custom.html](/assets/images/page/web/2022-01-09_favicon3.png)

favicon은 `custom.html`에 추가하면 된다.

이 파일에서 favicon을 삽입하는 데, <https://realfavicongenerator.net/>을 사용하라고 한다.

#### 3.8.3. favicon을 생성하자
![favicon_generator1](/assets/images/page/web/2022-01-09_favicon4.png)

위의 사이트에 들어가서 아까 flaticon에서 다운받은 병아리 이미지를 등록해주면 위와 같은 사이트로 이동한다. 내 favicon이 각 브라우저에서, 디바이스에서 어떻게 보일지를 미리 알려준다.

위의 내용을 쭉 훑어보고 'Generate Your Favicons and HTML code'를 눌러서 favicon을 생성하자. 그러면

![favicon_generator2](/assets/images/page/web/2022-01-09_favicon5.png)

이와 같은 HTML 코드가 생성된다. 'Install your favicon'의 내용은 다음과 같다.

1. 'Favicon package' 버튼을 클릭해서 패키지를 다운받는다.
2. 웹사이트 폴더에 압축 파일을 푼다. (나는 /assets/images/favicon.ico/chick에 압축 파일의 내용물을 넣었다. apple-touch-icon은 chick-icon으로 바꿨다.)  
   ![favicon_folder](/assets/images/page/web/2022-01-09_favicon6.png)
3. ```<head>``` 섹션에 생성된 HTML 코드를 넣는다.

#### 3.8.4. favicon HTML을 추가하자
![custom.html](/assets/images/page/web/2022-01-09_favicon7.png)

아까 `custom.html`에서 favicon에 대한 내용을 다룬다고 했는데, favicon generator에서 생성된 HTML코드를 이곳에 넣는다.

단, 나처럼 favicon의 경로를 임의로 수정한 경우에는 `<link href>`를 수정해줘야 한다.

#### 3.8.5. 적용된 favicon을 확인해보자
![favicon1](/assets/images/page/web/2022-01-09_favicon8.png)
![favicon2](/assets/images/page/web/2022-01-09_favicon9.png)

favicon이 제대로 적용된 것을 확인할 수 있다(귀엽다). 이건 어쩌다 알게 된 건데, 연결에 오류가 생겨 사이트에 접속하지 못했을 경우의 favicon도 생성이 되어 있었다.

PC에서뿐만 아니라, 모바일에 맞춰진 favicon도 확인할 수 있다.