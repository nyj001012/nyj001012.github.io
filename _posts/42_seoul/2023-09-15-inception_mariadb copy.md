---
title: "[Inception] nginx 세팅"
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

> 참고: [nginx의 Dockerfile
](https://github.com/nginxinc/docker-nginx/blob/1a8d87b69760693a8e33cd8a9e0c2e5f0e8b0e3c/stable/alpine-slim/Dockerfile)

# openssl
## 버전 확인
```shell
openssl version
```

## TLS v1.3 확인
```shell
openssl s_client -connect sgstatsdemo.com:443 -tls1_3
```

# TLS v1.3
# nginx
