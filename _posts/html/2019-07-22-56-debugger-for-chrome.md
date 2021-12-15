---
title: "56_VS CODE에서 DEBUGGER FOR CHROME 이용하여 디버그하기"
excerpt: "live server를 사용할 때 debugger for chrome을 사용하는 방법 정리"
category: 
  - html
author_profile: true
sidebar:
  - nav: "main" 
---
1. DEBUGGER FOR CHROME 설치하기<br>
![](/assets/images/page/html/vsc_chrome_debug1.png)<br>
확장: 마켓 플레이스에서 Debugger for Chrome을 찾아 설치한다.
<br><br>
2. DEBUGGER FOR CHROME 설정하기<br>
왼쪽 메뉴에 보면 디버그 항목이 있는데, 왼쪽 윗부분에 톱니바퀴 아이콘을 눌러 launch.json 파일을 연다.
![](/assets/images/page/html/vsc_chrome_debug2.png)<br>
"url"에서 http://localhost:(localhost 번호)/(열려는 파일 이름)에 맞춰 작성한다.<br>
localhost가 몇인지는 live server를 열면 오른쪽 하단에 뜨는 창으로 알 수 있었다.<br>
열려는 파일은 숫자야구 페이지의 main.html 파일이었기 때문에 위와 같이 썼다.<br><br>
3. 디버그하기<br>
이제 자바스크립트 파일로 돌아가서 중단점을 표시하자.<br>
중단점은 코드 창에서 몇 째 줄인지 나타내는 숫자의 바로 왼편에 있는 공백 부분을 클릭하여 표시할 수 있고,
중단점을 찍을 줄에서 F9를 눌러 표시할 수 있다.<br>
F5를 눌러 디버그를 시작하면 위의 경우, html 페이지가 뜬다.<br>
![](/assets/images/page/html/vsc_chrome_debug3.png)<br>
디버그 콘솔 창에서는 기존 chrome의 개발자 도구에서 console에 출력하던 내용들이 출력된다.<br>
F10을 눌러 한 단계씩 디버그를 실행할 수 있다.<br>
![](/assets/images/page/html/vsc_chrome_debug4.png)<br>
왼쪽에서는 변수는 어떻게 바뀌는지와 조사식, 어떤 것들이 호출되었는지, 중단점은 어디에 찍혀있는지를 알려준다.
