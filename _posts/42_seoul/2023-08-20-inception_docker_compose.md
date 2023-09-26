---
title: "[Inception] docker-compose 작성"
excerpt: "docker-compose 작성법"
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
last_modified_at: 2023-08-20T00:00:00+09:00
---

# docker-compose
> 공식 문서: <https://docs.docker.com/compose/gettingstarted/>

## 파일 구성
> 공식 문서: <https://docs.docker.com/compose/compose-file/compose-file-v3/>

docker-compose의 파일 예시를 봤는데, 궁금한 점이 있어서 찾아보고 정리했다.

### version
.yml 파일 보면 맨 첫 줄에 항상

```yml
version: '3.8'
```

이런 식으로 적혀 있는 걸 봤는데, 이는 compose 파일의 버전이다. 도커 버전에 맞는 compose 파일의 버전을 명시해야 하며, version 1.x와 2.x, 3.x가 구성 파일의 매개 변수가 삭제되었거나 추가된 것들이 있다. 해당 내용은 [Docker Compose와 버전별 특징
](https://meetup.nhncloud.com/posts/277)을 참고하면 좋을 것 같다.

### services
compose 파일은 서비스 이름의 문자열 표현을 키로, 서비스 정의를 값으로 하는 맵으로 선언되어야 한다. 서비스 정의에는 각 서비스 컨테이너에 적용되는 구성이 포함된다.

각 서비스에는 반드시 서비스의 도커 이미지를 어떻게 생성할지를 정의한 `build` 섹션이 있어야 한다.

그 외에 services에 정의할 수 있는 섹션은 아래와 같다.
- build: [Compose Build Specification](https://docs.docker.com/compose/compose-file/build/)에 정의된 대로 소스를 컨테이너 이미지로 만들기 위한 빌드 설정을 정의한다.

이 내용들과 Docker hub에서 패키지들의 "... via docker-compose or docker stack deploy" 섹션을 토대로 작성한 내용은 다음과 같았다.

```yml
version: '3.8'

services:
  nginx:
    image: nginx
    volumes:
      - ./templates:/etc/nginx/templates
    ports:
      - 8080:80
    environment:
      - NGINX_HOST=foobar.com
      - NGINX_PORT=80
  
  mariadb:
    image: mariadb
    restart: always
    environment:
      MARIADB_ROOT_PASSWORD: example

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 8000:80
    environment:
      WORDPRESS_DB_HOST: mariadb
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
```

그리고 `docker-compose up`을 해 보니 이미지 생성은 전부 잘 됐다.

### volumes

### .env
