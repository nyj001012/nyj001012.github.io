---
title: "[Inception] Inception을 진행하며 맞닥뜨린 에러들"
excerpt: "Inception을 진행하며 맞닥뜨린 에러들을 해결하기 위해 삽질한 이야기"
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
last_modified_at: 2023-09-25T00:00:00+09:00
---

에러 하나하나만 보면 개수는 적은데 의외로 시간이 많이 걸렸다. 몇몇 에러는 시간 단위로 붙잡고 있었는데 이제보니 별 거 아닌 것 같기도 하다..?

# Docker compose
## Docker compose up 시, no such device 문제 (로컬 볼륨 없음)
> error response from daemon: failed to mount local volume: mount /home/yena/data/wordpress:/var/lib/docker/volumes/srcs_wordpress_data/_data: no such device

상당히 간단하다. 알려준 대로 `/home/yena/data/wordpress`라는 로컬 볼륨을 도커에 마운트하는 데 실패했다는 뜻이다. 사유는 그런 장치가 없기 때문(no such device). 그렇다면 그냥 로컬 볼륨을 생성해주면 된다.

```
mkdir -p /home/yena/data/wordpress
```

그런데 만약 로컬 볼륨도 존재하는데 저런 에러가 뜬다면..?

## [미해결] Docker compose up 시, no such device 문제 (로컬 볼륨 존재)
에러 내용은 로컬 볼륨이 없을 때와 같다. 원인은 대충 [Mounting a docker volume fails with 'no such device' error](https://serverfault.com/questions/1127151/mounting-a-docker-volume-fails-with-the-no-such-device-error)에 적힌대로 같았다. 내용대로라면 도커에서 로컬 볼륨을 두 곳에 마운트하려는 것 같았다. 머리가 아팠던 게, docker compose 파일의 볼륨 경로를 바꿔줘도 계속 기존 경로로 인식하고 있었다. 이를 위해 시도해 본 몇 가지 방법이 있었다.

### 0. docker 재시작
컴퓨터가 이상하면 재부팅이 80%는 해결해주듯 도커를 껐다 켜봤다. 그래도 그대로였다.

### 1. docker volume 생성
일단 위에서 적힌 답변대로 사이즈를 지정하여 볼륨을 생성하고, 그 볼륨으로 로컬 볼륨을 마운트하도록 시도했다. 그러나 효과는 없었다..!

### 2. docker volume 삭제
```
docker volume ls          # docker volume 확인
docker volume rm VOLUME   # VOLUME 삭제
```
위의 명령어로 도커 내의 볼륨을 삭제했다. 그러면 기존 도커 볼륨에 마운트할 로컬 볼륨의 정보가 갱신되지 않을까 하는 바람이 있었다. 그러나 여전했다.

### 3. 로컬 볼륨 경로 변경
가장 쉽게 docker compose 파일에 정의한 로컬 볼륨의 경로를 변경해봤다. 그러나 이것도 그대로였다.

### 4. 결국 갈아엎다...
이 문제로 미리 이 길을 걸어가신 선배님께 여쭤봤으나... 결국 답을 찾지 못하고 갈아엎었다. 이때가 알파인 리눅스에서 우분투로 갈아탔을 때다. 선배 카뎃 말씀으로는 도커 이미지를 만들고 올리고 내리고 삭제하고 하다보면 도커 내부에서 뭔가 꼬이는 것 같다 하셨다.  

아무리 구글링을 해도 이 문제에 대해 자료가 많이 나오지 않는 걸 보면 이유가 있지 않을까..? GPT도 모르던데.

## listen tcp 0.0.0.0:3306:bind:address already in use
> 참고: [Error starting userland proxy: listen tcp 0.0.0.0:3306: bind: address already in use](https://stackoverflow.com/questions/37896369/error-starting-userland-proxy-listen-tcp-0-0-0-03306-bind-address-already-in)
이건 3306 포트를 누가 이미 점유하고 있다는 에러다. 해결 방법은 3306 포트를 누가 쓰고 있는지를 확인한 후, 그 프로세스를 종료시키면 된다.

### 방법 1. lsof 이용
```
lsof -i :3306
kill PID
```

### 방법 2. netstat 이용
```
sudo netstat -nlpt | grep 3306
kill PID
```

### 방법 3. mysql 종료
```
sudo service mysql stop
```

# Docker image
## nginx 이미지를 만드는데 자꾸 pull layer를 한다
내가 docker image를 만드는데 자꾸 Dockerfile의 COPY 명령어도 제대로 수행이 안 되고, 터미널에 pull layer [1/8...] 이런 식으로 레이어를 pull한다는 내용이 출력되었다. 그래서 원인을 찾아 나섰는데, 이유는 docker compose 파일에 있었다.

docker compose 파일에 nginx 부분을 내가

```yml
  nginx:
    ...
    build: requirements/nginx
    image: nginx:alpine
    ...
```

이렇게 작성해놨다. 이게 무슨 문제냐? 나는 `requirements/nginx`에 있는 `Dockerfile`을 가지고 빌드한 이미지 `nginx:alpine`을 가지고 컨테이너를 띄우란 의도로 작성했는데, 도커는 이걸 docker hub에 있는 `nginx:alpine`을 pull해서 띄우면 되겠다고 이해한 것이다. 그러니 내가 작성한 Dockerfile은 싹다 무시하지...

재밌는 점은 내가 nginx 뿐만 아니라 wordpress, mariadb에도 이미지를 정의해뒀는데, 걔네는 내가 지정한 빌드 경로로 잘 찾아가서 이미지를 빌드했다. 알고보니 alpine 태그가 달린 이미지가 도커에는 없었나보다.

# yena.42.fr
## 안전하지 않은 연결입니다
이건 에러라고 하기 뭐한데 내가 보고 당황했던 거라 일단 넣었다. 현재 Inception에서는 openssl로 만든 인증서를 사용하고 있다. 이건 내가 인증서에 서명한 거라 공신력 있는 기관으로부터 발급받은 인증서가 아닌, 한마디로 야매 인증서다. 그러다보니 아무리 https라 해도 안전하지 않은 연결이라고 뜰 수 밖에 없었다.

## 403 Forbidden
403은 접근 권한이 없는 사람이 리소스에 접근하려 할 때 뜨는 에러다. 왜 접근 권한이 없을까? 나의 경우는 wordpress의 페이지를 넣어두는 폴더의 권한과 nginx의 config 파일이 잘못 설정되어 있었다(오타라든가 오타라든가 오타라든가).

이 에러가 나면 권한 한 번 체크해보길 바란다.

# Ubuntu
## 우분투 터미널/화면 먹통 현상 해결법
> 원글: [우분투 터미널/화면 먹통 현상 해결법](https://inpa.tistory.com/entry/LINUX-%F0%9F%93%9A-%EC%9A%B0%EB%B6%84%ED%88%AC-%ED%84%B0%EB%AF%B8%EB%84%90%ED%99%94%EB%A9%B4-%EB%A8%B9%ED%86%B5-%ED%98%84%EC%83%81-%ED%95%B4%EA%B2%B0-%EC%A0%95%EB%A6%AC)

1. 우분투 부팅 시, `Shift` 연타하여 GRUB 메뉴 진입
2. Ubuntu 선택 후, e키 누르기
3. 맨 밑으로 가서 `$vt_handoff` 옆에 `nomodeset` 추가
