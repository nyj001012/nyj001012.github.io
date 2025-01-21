---
title: "Datadog 설정"
excerpt: ""
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - web
  - datadog
  - 이터널 리턴
  - 밸런스 게임
toc: true
toc_sticky: true
last_modified_at: 2025-01-21T00:00:00+09:00
---

# Datadog이란
Datadog은 애플리케이션 성능 모니터링(APM), 로그 관리를 위한 플랫폼으로, 시스템과 애플리케이션을 전체적으로 모니터링하고 성능 데이터를 실시간으로 수집하여 분석하는 도구이다.

# Datadog 설정 방법 (Docker 사용)
## 에이전트 설치
> Datadog 에이전트 호스트에서 실행되는 소프트웨어입니다. 호스트로부터 이벤트와 메트릭을 수집하여 모니터링 및 성능 데이터를 분석할 수 있는 Datadog으로 보냅니다. Datadog 에이전트는 오픈 소스이며 해당 소스 코드는 GitHub(DataDog/datadog-agent)에서 사용할 수 있습니다.

[공식문서](https://docs.datadoghq.com/ko/agent/?tab=Linux&site=us)에 가보면 여러 플랫폼을 설정할 수 있는데, 나는 예전에 프로메테우스를 42 서울 과제에서 사용해 본 적 있었고 그것처럼 Datadog를 별도의 컨테이너로 만들어 사용하고 싶었다.

### 컨테이너 구성
> 참고: <https://myops.medium.com/monitor-your-server-and-docker-containers-with-datadog-for-free-317b553c8530>

Datadog의 이미지를 생성할 때 별도의 Dockerfile을 생성하기 보다는 기존의 이미지를 사용하고, 대신 환경 변수만 세팅했다.

```yaml
datadog-agent:
  image: gcr.io/datadoghq/agent:7
  container_name: datadog-agent
  env_file:
    - .env
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - /proc:/host/proc:ro
    - /sys/fs/cgroup:/host/sys/fs/cgroup:ro
    - /var/lib/docker/containers:/var/lib/docker/containers:ro
  networks:
    - er_bal_network
```

`.env`에는 `DD_SITE`, `DD_API_KEY`가 적혀있다.  `DD_SITE`는 Datadog의 사이트인데 미국, 유럽, 일본에 있다.  
그나마 가까운 일본의 경우, 값이 `ap1.datadoghq.com` 이렇게 되어있다([공식 문서](https://docs.datadoghq.com/ko/getting_started/site/)).  
`DD_API_KEY`는 Datadog API Key인데, 회원가입을 하고 나면 발급받을 수 있다.  
그 외에는 각종 Datadog 설정 옵션([공식 문서](https://docs.datadoghq.com/containers/docker/apm/?tab=linux#docker-apm-agent-environment-variables))들을 적어두었다.

그리고 하나 더 추가를 해야하는게, 백엔드 컨테이너와 datadog-agent를 연결 해줘야 한다.  
그래서 백엔드 컨테이너의 호스트로 datadog-agent를 지정해줬다.

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: backend
  ports:
    - "8080:8080"
  environment:
    ...
    DD_AGENT_HOST: datadog-agent
    DD_TRACE_AGENT_PORT: 8126
```

# Datadog 설정하다 발생한 에러들
## API Key invalid, dropping transaction
### 에러 본문
```
2025-01-21 05:39:00 UTC | CORE | ERROR | (comp/forwarder/defaultforwarder/transaction/transaction.go:433 in internalProcess) | API Key invalid, dropping transaction for https://7-61-0-app.agent.datadoghq.com/intake/
```

### 해결
> 참고: [Datadog: API Key invalid dropping transaction when installing Datadog agent
](https://stackoverflow.com/questions/74441381/datadog-api-key-invalid-dropping-transaction-when-installing-datadog-agent)

위의 에러의 경우, 원인이 두 가지 경우로 나뉜다.

#### `DD_SITE` 값이 잘못된 경우
`DD_SITE`가 공식 문서에 기재되지 않은 형식으로 작성되거나, 내가 지정한 국가가 아닌 곳의 `DD_SITE`를 지정하면 저런 에러가 발생한다.

나는 저때 따로 `DD_SITE`를 작성하지 않았고 기본 값인 `datadoghq.com`가 세팅된 상태였는데, 이는 미국의 `DD_SITE`였다.  
따라서 일본의 `DD_SITE`로 작성했다.

#### DD_API_KEY 값이 잘못된 경우
이 경우에도 해당 에러가 발생한다.

처음엔 `Datadog 대시보드 > Integrations > Agent > Docker > Select API Key`로 확인할 수 있는 API Key가 아니라, `Personal Settings > Application Keys`에서 별도로 생성한 Key를 가지고 `DD_API_KEY` 값을 지정했다가 마주친 에러였다.

그래서 올바른 키 값을 주어 해결했다.
