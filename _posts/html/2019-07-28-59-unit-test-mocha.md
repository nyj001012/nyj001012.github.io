---
title: "59_MOCHA로 UNIT TEST하기"
excerpt: "MOCHA로 UNIT TEST하는 방법 정리"
category: 
  - html
author_profile: true
sidebar:
  - nav: "main" 
---
1. mocha 설치하기<br>
mocha를 설치하는 데에는 npm install mocha --global로 전역설치하는 방법과 npm install mocha --save-dev로 
package.json &gt; devDependecies에 mocha를 추가하는 방법이 있다.<br><br>
2. 테스트 할 함수 내보내기<br>
module.export를 이용하여 테스트를 진행할 함수를 내보낸다. 아래의 코드는 samples.js라는 자바 스크립트 파일에
입력받은 수에 따라 한글을 출력하는 함수와 두 수를 곱하는 함수를 포함한다.
<script src="https://gist.github.com/nyj001012/a2a03ea0bbff5a35dc2f7fff3b46c677.js"></script>
오른쪽의 printHangul은 함수 이름이고, 왼쪽의 printHangul은 프로퍼티로 작용한다.<br><br>
3. 테스트 코드 작성<br>
samples.js의 테스트 코드를 작성할 samples.spec.js 파일을 만들었다.
<script src="https://gist.github.com/nyj001012/f3c488eeea7874c1321ae9ed5fef3c7c.js"></script>
require()는 무언가를 불러올 때 쓰는데, 위의 require('assert');는 node.js에 내장된 assert 모듈을 불러오고, 
require('../samples.js').printHangul;은 현재 test폴더의 상위 폴더에서 samples.js 파일의 printHangul이라는 프로퍼티를
불러오는 역할을 한다.<br>
describe()부분의 'Samples.js printHangul Test'는 테스트의 이름이고, it() 안에는 테스트의 로직이 들어간다. .
이후 assert.equal로 printHangul(1)이 "가"와 같은 지를 확인한다. 여기서는 엄격한 비교(===)가 아니기 때문에, '가'를 썼을 때와 
'가'를 썼을 때의 차이는 없다. ('use strict'는 jslint를 고려하여 쓴 것으로, 테스트 코드와는 관련이 없음.)
이후 터미널에 mocha를 입력하여 테스트를 진행한다.
![](/assets/images/page/html/mocha_test_01.png)
결과는 몇 개의 테스트가 통과(passing)했는지, 걸린 시간이 몇 밀리초인지를 함께 보여준다.<br>
또한 한 describe 안에 여러 개의 it을 쓰거나, 여러 describe를 중복해서 쓰는 것도 가능하다.
아래는 describe 안에 또다른 describe를 중복해서 쓴 코드이다.
<script src="https://gist.github.com/nyj001012/1ffc3c9f70b255c083122d56f7e11a03.js"></script>
테스트 결과는 다음과 같다.
![](/assets/images/page/html/mocha_test_02.png)
여기서 코드를 살짝 바꿔보자. 'multipleNumbers Test'의 assert.equal의 18을 15로 바꿨을 때 나오는 결과는 다음과 같다.
![](/assets/images/page/html/mocha_test_03.png)
AssertionError라는 말과 함께 18 == 15가 출력되었다. 코드 상 계산결과는 18인데, 그것을 15와 같다고(equal)
주장했기 때문에(assert) 에러가 생겼다.
