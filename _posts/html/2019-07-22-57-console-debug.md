---
title: "57_개발자 도구에서 디버그하기"
excerpt: "chrome의 개발자 도구에서 콘솔 디버그하기"
category: 
  - html
author_profile: true
sidebar:
  - nav: "main" 
---
1. 개발자 도구를 열어 중단점 체크하기<br>
F12를 눌러 개발자 도구를 연 후, 중단점을 찍고 싶은 줄의 왼쪽 부분 공백을 클릭하여 중단점을 표시해준다.
<br><br>
2. EVENT LISTENER BREAKPOINT 설정<br>
event listner breakpoint에서 디버그할 부분에 해당하는 이벤트를 체크한다.<br>
![](/assets/images/page/html/console_debug_breakpoint.jpg)<br>
이번의 경우, 난수를 만드는 함수를 디버그 할 건데, 이 함수는 숫자를 설정하는 버튼을 클릭해야
동작하므로 mouse > click에 체크했다. 이렇게 하면 click의 이벤트를 받는 부분에 대해 디버그가 이루어진다.
<br><br>
1. 디버그 실행<br>
숫자 설정 및 초기화 버튼을 클릭하면 디버그가 실행되며 F10을 눌러 진행할 수 있다.<br>
![](/assets/images/page/html/console_debug_run.jpg)<br>
호출 스택, 중단점이 있고, 그 오른쪽의 scope에선 변수가 어떻게 변하는지를 볼 수 있다.<br>
아래의 console 창에서는 console.log에 해당하는 부분이 출력된다.<br>
난수 생성이 완료되면, console 창에 난수가 출력된 후, 디버그는 종료된다.<br>
![](/assets/images/page/html/console_debug_stop.jpg)<br>
중단점을 비활성화 시키고(Ctrl + F8) 버튼을 누르면 위의 과정 없이 콘솔에 결과만 출력된다. scope에는 Not paused라고 나온다.
