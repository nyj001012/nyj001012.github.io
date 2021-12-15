---
title: "55_숫자야구 코드"
excerpt: "숫자야구 페이지 만든 후, 코드 내용 업로드"
category: 
  - html
author_profile: true
sidebar:
  - nav: "main" 
---
<script src="https://gist.github.com/nyj001012/d3b1a5424673e3bc3afda1ecc91c5942.js"></script>
<h4>
난수 생성:<br>
0~9까지의 수가 있는 배열을 만든 후, 그 배열에서 각각 천의 자리, 백의 자리, 십의 자리, 일의 자리에 해당하는 수를 뽑는 방식.<br><br>
판정:<br>
사용자가 입력한 수를 각각 분리하여 하나의 배열로 만듦, 컴퓨터가 만든 수도 동일(charAt을 쓰려 하니 문자열로 바꿨어야 했음).
이후 두 배열의 인덱스가 일치할 때, 그 인덱스에 해당하는 값이 같을 경우 S, 인덱스는 다르지만 해당하는 값이 같은 경우가 있으면 B, 값이 아예 없으면 O를
출력하게 함.
</h4>
