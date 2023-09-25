---
title: "[Inception] 평가 대비 알아두면 좋은 것들"
excerpt: "Inception을 평가 받을 때 알아두면 좋을 것들"
category: 
  - 42_seoul
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - 42서울
toc: true
toc_sticky: true
last_modified_at: 2023-09-25T00:00:00+09:00
---

# ssh 설정
# 호스트 파일(로컬)을 원격 환경(VM)으로 옮기기
> 참고: [리눅스 scp 명령어 사용법 ( 파일 전송 프로토콜 / 파일 보내기 /파일 받기 )](https://wlsvud84.tistory.com/11)
```
scp -P PORT -r FILE_NAME REMOTE_ID@REMOTE_IP:PATH_TO
```
