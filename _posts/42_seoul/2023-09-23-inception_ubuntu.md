---
title: "[Inception] 결국 Ubuntu로 갈아타다..!"
excerpt: "Ubuntu 설치"
category: 
  - 42_seoul
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 42서울
  - Inception
toc: true
toc_sticky: true
last_modified_at: 2023-09-23T00:00:00+09:00
---

# 왜 Ubuntu로 갈아탔는가?
원래는 알파인 리눅스를 고수하려 했으나... Docker 이미지를 지우고 만들고 테스트하고를 반복하던 중, 볼륨에 문제가 생겼는지 로컬 볼륨을 도커 볼륨으로 마운트하는 과정에서 난리가 났다. 집현전의 구원자분께 찾아가 조언을 구하려 했으나 그분도 포기한 문제였기에 VM을 갈아엎기로 했다. 하려면 할 수는 있겠지만, 블랙홀이 50여일 남은 시점에 그것까지 하기는 무리라 생각했다.

알파인 리눅스에는 기본적으로 데스크탑 환경이 아니었기 때문에 내가 이전에 작성해둔 포스팅처럼 직접 GUI 환경을 마련해줘야하는 귀찮음이 있었다. 그걸 감수하고 이번에는 새로운 GUI 환경인 Plasma와 Gnome을 사용해보려 했다. 그러나 Plasma는 로그인 할 때 먹통이 되고 Gnome은 부팅할 때 자꾸 crash가 나는 열받는 상황이 발생했다.  
이걸 옆에서 보고 계시던 또다른 집현전 구세주께서 우분투를 추천하시길래 찍먹하러 공식 홈페이지를 갔다. 공홈도 가보고 이것저것 둘러본 결과 생각보다 UI도 예뻤고(이게 제일 중요했다) 자료도 알파인보다는 많았던 것 같았다. 알파인에서는 뭔가 문제가 생기면 주로 영어로 검색했는데, 우분투는 한국어로 검색해도 자료가 잘 나왔다.

알파인 리눅스도 굉장히 좋은 OS 같지만, 일단 여기서 + 트렌센던스 과제에서는 우분투로 하는 걸로...

# 설치
> 참고 자료: [M1 Mac 가상머신(UTM) 설치 - Ubuntu 20.04 for ARM 설치해보기 + ssh 연결](https://velog.io/@zhy2on/Ubuntu-20.04-for-ARM-%EC%84%A4%EC%B9%98%ED%95%B4%EB%B3%B4%EA%B8%B0)

참고로 amd의 경우, 그냥 공식 홈페이지 [Download Ubuntu Desktop](https://ubuntu.com/download/desktop) 가서 넣고 돌리면 된다. 그런데 내 맥북은 슬프게도 arm이기 때문에 Ubuntu Server를 다운받아 그 안에서 Desktop을 설치하는 수 밖엔 없었다. 이래도 알파인보다는 설치하는 게 덜 귀찮다.
