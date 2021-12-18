---
title: "깃허브 블로그 리뉴얼 (jekyll)"
excerpt: "근 2년 동안 써 온 블로그를 갈아엎게 되는데..."
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
toc: true
toc_sticky: true
last-modified-at:
    date-format: '%d-%b-%y'
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
