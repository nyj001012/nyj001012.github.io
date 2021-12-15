---
title: "66_IntelliJ Spring Boot 세팅 참고 url"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
---
<h3>
  초기 세팅
</h3>
<h4 style="line-height: 1.8rem">
  <p>
    <b>IntelliJ Community 용 spring boot initialiser 사이트</b>
    <ul>
      <li>웹 프로젝트 용도면 Dependancy에 Spring Web 체크할 것</li>
      <li>압축파일 풀고 나서 원하는 폴더에 옮기고 IntelliJ로 열기</li>
      <li><a href="https://start.spring.io/">https://start.spring.io/</a></li>
  </ul>
  </p>
  <p>
    <b>JDK 설치</b>
    <ul>
      <li>File > Project Structure > SDK 드롭다운 클릭 > Add SDK > Download JDK</li>
    </ul>
  </p>
  <p>
    <b>SDK 버전 변경</b>
    <ul>
      <li>File > Project Structure > SDK 드롭다운에서 선택</li>
      <li>버전을 변경하고 나면 바로 밑의 Language Level과 맞는지 체크하자</li>
      <li>모든 변경이 끝나면 gradle rebuild 해줘야 변경사항이 적용된다</li>
    </ul>
  </p>
  <p>
    <b>Lombok 설정</b>
    <ul>
      <li><a href="https://azurealstn.tistory.com/41">Lombok 설정부터 테스트 코드 오류 시 해결</a></li>
    </ul>
  </p>
</h4>
<h3>
  오류
</h3>
<h4 class="line-height: 1.8rem">
  <p>
    <b>Cause: invalid source release: 11</b>
    <ul>
      <li>SDK 버전과 gradle에 명시된 버전이 맞는지를 확인한다</li>
    </ul>
  </p>
  <p>
    <b>Getmapping import error: Cannot resolve...</b>
    <ul>
      <li>내가 만든 프로젝트가 <strong>Spring Web Project</strong>인지 확인한다</li>
      <li>그냥 Spring Project로 만들면 저 에러 뜬다</li>
    </ul>
  </p>
  <p>
    <b>Can't finish Github sharing process</b>
    <ul>
      <li>Github 설치하고 내 이메일을 등록해 준 적 없으면 뜨는 에러</li>
      <li>해결 방법은 git에서 명령어를 쳐도 되지만, IntelliJ에서도 계정 등록이 된다.</li>
      <li><a href="https://pika-chu.tistory.com/89">명령어 방식 링크</a></li>
      <li><a href="https://suyeoniii.tistory.com/41">IntelliJ 계정 등록 링크</a></li>
    </ul>
  </p>
</h4>
