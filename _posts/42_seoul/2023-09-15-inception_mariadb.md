---
title: "[Inception] mariadb 설치"
excerpt: ""
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
last_modified_at: 2023-09-15T00:00:00+09:00
---
> 참고 자료: [How to install MariaDB on Alpine Linux
](https://www.librebyte.net/en/data-base/how-to-install-mariadb-on-alpine-linux/)

# 설치
## mariadb 설치
```shell
apk add mariadb
```

## mariadb 초기 세팅
```shell
/etc/init.d/mariadb setup
```
- 초기 루트 계정: root@localhost
- 초기 루트 PW: 없음

명령어 실행 결과 로그 잘 찾아보면 위와 같은 내용이 나온다. 또한 부트 시에 mariadb를 시작하고 싶다면, `support-files mariadb.service`를 적절한 곳에 복사하라고 한다.

mariadb daemon도 함께 시작하고 싶다면, `cd '/usr' ; /usr/bin/mariadb-safe --datadir='/var/lib/mysql`을 실행하면 된다.

## mariadb 동작 확인
```shell
rc-service mariadb status
```

## mariadb 실행
```shell
rc-service mariadb start
```

## 재부팅 시, mariadb 자동 시작
```shell
rc-update add mariadb default
```

## mariadb 종료
```shell
rc-service mariadb stop
```

# 연결
## mariadb-client 설치
```shell
apk add mariadb-client
```

## 루트 계정으로 접속
```shell
mysql -u root
```

## 보안 설정
```shell
mariadb-secure-installation
```
이 명령어를 사용하면 루트 계정 원격 로그인 가능 여부 등의 보안 관련 세팅을 할 수 있다.

## 루트 계정 비밀번호 변경 
```sql
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('새로운 비밀번호'); # 비밀번호 변경

FLUSH PRIVILIEGES; # 변경사항 바로 적용
```
