---
title: "인터넷 속도가 안 나와!"
excerpt: ""
category: 
  - etc
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - KT
  - 인터넷 속도
toc: true
toc_sticky: true
last_modified_at: 2022-01-29T00:00:00+09:00
---

# 문제 인식
어느 순간부터 인터넷이 느려진 거 같다는 생각이 들어 속도 테스트를 해봤다. 처음에는 <https://www.speedtest.net/>에서 테스트를 했다. 결과가 97mbps 정도 나오면서 100mbps 조금 안 되는 수준의 결과가 나오자 통신사 테스트는 다를 까 싶어 [kt 인터넷 속도 테스트](http://speed.kt.com/speed/speedtest/introduce.asp) 페이지에서도 테스트를 했다. 그랬는데 500mbps 지원인 인터넷의 100mbps도 안 나오는 속도를 보고 기가 찼다(와 라임!).

![speedtest](/assets/images/page/etc/2022-01-13_speed_test2.png)

# 해결 시도
- ~~이더넷 링크속도 확인~~
- ~~명령 프롬프트 창에 가서 DNS 캐시 플러시~~
- ~~명령 프롬프트 창에서 수신 창 자동 조정 수준 highlyrestricted로 변경~~
- 랜 선 변경

## 랜 선 변경
Buddy(KT의 증폭기)와 컴퓨터를 연결하는 랜선은 내가 예에에에에ㅔㅔ전에 쓰던, 낡은 랜선이고, Buddy와 랜포트를 연결하는 랜선은 CAT.5E였다. CAT.5E가 딱 1gbps를 지원하기 때문에 이걸 컴퓨터에 연결해야 했었다. 그런데 내가 본체를 손 볼 일이 생겨서 선을 다 뽑아버렸는데, 다시 꽂는 과정에서 뒤바뀐 것 같았다.

랜선도 크로스 케이블, 다이렉트 케이블이 있는데 요즘 공유기에서는 Auto MDI-X라는 게 있어서 아무거나 써도 상관없다고 한다. 나는 장도 볼 겸 그냥 이마트 가서 크로스 케이블 가져왔다.

참고: [생선스프, 'UTP 크로스와 다이렉트 케이블의 차이'](https://sengsung.tistory.com/39)

# 결과
하.. 초반에 470mbps찍고 좋았는데, 갑자기 다시 97mbps 정도로 떨어졌다. 

![speed_test](/assets/images/page/etc/2022-01-13_speed_test1.png)

나한테 왜그래...

# 현재는?
이제보니까 랜선을 꽂았다가 뺀 직후, Buddy의 인터넷 LED에 파란 불이 들어오면 거의 500mbps에 달하는 속도가 나온다. 그런데 LED에 노란 불이 들어오니까 100mbps에 조금 못 미치는 속도가 나온다. 이전에 기사님께서 SLA 품질보증 이의신청 내역을 보고 연락을 주셨을 때, 그때 당시에는 속도가 괜찮아서 다음에 이런 현상이 또 발생하면 연락드리기로 했다. 이제는 연락을 드려야겠다. 매번 랜뽑할 수도 없고...
