---
title: "copytruncate 유실 없애기: 앱 출력을 FIFO로 받아 rename으로 회전하기"
excerpt: "감수하기로 했던 copytruncate의 유실을 실측해 보니 생각보다 컸다. 앱 대신 전용 syslog-ng가 로그 파일을 열도록 바꾸고, logrotate를 rename/create + reopen 방식으로 바꾼 과정을 정리한다."
category:
  - web
author_profile: true
sidebar:
  - nav: "main"
tag:
  - web
  - devops
  - logging
  - logrotate
  - syslog-ng
  - systemd
  - loki
  - alloy
toc: true
toc_sticky: true
last_modified_at: 2026-11-18T00:00:00+09:00
---

# 감수하기로 했던 유실

[Loki + Alloy 적용기](https://nyj001012.github.io/web/loki_alloy/)에서 앱 로그 회전에 `copytruncate`를 썼다.  
앱 유닛이 `StandardOutput=append:`로 로그 파일을 열고 systemd가 연 파일 디스크립터를 그대로 앱에 넘기기 때문이다.  
일반적인 rename 방식으로 회전하면 앱은 이름이 바뀐 옛 파일(inode)에 계속 쓰고 새 `app.log`는 비어 있게 된다.  
`copytruncate`는 내용을 복사한 뒤 원래 파일을 비우므로 inode가 그대로라 앱이 계속 쓸 수 있다.  

이 방법에는 한계가 있는데, 복사와 비우기 사이에 들어온 줄은 사라진다는 것이다.  
당시에는 하루 로그가 수십 KB 수준이라 "한두 줄 정도려나"라고 생각했다.  
그러다 지레짐작 대신 실제로 로그 유실이 얼마나 일어나는지 시뮬레이션해 보니 생각보다 큰 문제였다.  

> 이 글의 경로·유닛 이름은 실제 이름 대신 `[앱]`, `app-log-*`처럼 일반화했다.

# copytruncate가 잃는 두 곳

1. **파일에서 잃는 줄**: 복사가 끝난 뒤 비우기 전까지 앱이 쓴 로그는 복사본에도, 비워진 원본에도 남지 않는다.
2. **Loki로 못 가는 줄**: 파일을 비우는 순간 Alloy가 아직 읽지 못한 끝부분은 복사본에는 남아 있어도 Alloy가 다시 읽지 않는다.

두 번째는 처음 결정할 때 생각하지 못한 부분이었다.  
파일 백업만 보면 멀쩡한데 Grafana에서 조회하면 줄이 빠져 있는 상황이 생긴다.  

얼마나 잃는지 더미 로그로 먼저 재 봤다.  
발생률별로 로그를 쓰면서 강제 회전을 20번씩 걸고 빠진 줄을 셌다.  
1년치 보관 파일 365개와 100MiB짜리 현재 파일을 미리 깔아 두어 회전이 실제처럼 무거운 상태에서 쟀다.  

| 발생률 | 누락 / 전체 | 누락률 |
| --- | --- | --- |
| 100건/초 | 129 / 471 | 27.4% |
| 1,000건/초 | 552 / 4,020 | 13.7% |
| 6,000건/초 | 3,406 / 25,020 | 13.6% |

회전 순간에 몰려 있는 유실이라 하필 그때 난 장애의 로그가 빠질 수도 있다.  
회전을 일부러 자주 걸었으니 이 수치만큼 유실된다고 볼 수는 없지만, 해결해야 한다는 건 분명했다.  

# 로그 파일을 여는 주체를 바꾸기

rename 방식을 못 쓴 이유는 앱(정확히는 systemd가 넘겨준 FD)이 로그 파일을 직접 열고 있어서였다.  
회전한 뒤 새 파일을 다시 열라고 알리려면 앱 코드에 재오픈 처리를 넣거나 회전할 때마다 앱을 재시작해야 한다.  
앱이 로그 파일을 직접 열어 쓰도록 바꾸는 방법도 있지만, 지금은 pino가 stdout으로 내보내고 systemd가 그 출력을 파일에 붙이는 구조라 로거 설정과 배포 구조까지 손대는 대공사가 된다.  
그래서 앱은 그대로 두고, 앱과 파일 사이에 다른 프로세스를 하나 두기로 했다.  

앱은 FIFO(이름 있는 파이프)에 쓰고 전용 syslog-ng가 FIFO를 읽어 `app.log`에 쓴다.  
syslog-ng는 `syslog-ng-ctl reopen`으로 파일을 다시 열 수 있으니 회전을 rename 방식으로 바꿀 수 있다.  
`app.log` 경로, Alloy 수집 설정, 회전 주기·보관 개수는 전부 그대로다.  

```text
앱 stdout ─ /run/app-log/stdout.fifo ─┐
                                      ├─ app-log-writer(syslog-ng) ─ /var/log/[앱]/app.log ─ Alloy
앱 stderr ─ /run/app-log/stderr.fifo ─┘
            └ PID1이 두 FIFO를 열어 둔다(소켓 유닛 2개 + keeper)
```

## FIFO는 PID1이 열어 둔다

FIFO를 읽는 쪽이 하나도 없으면 쓰는 쪽은 `EPIPE`를 받는다.  
writer가 재시작하는 1초 사이에 앱이 로그를 쓰다 오류를 받으면 안 되므로, FIFO를 systemd 소켓 유닛으로 만들었다.  

```ini
[Socket]
ListenFIFO=/run/app-log/stdout.fifo
SocketMode=0600
# 정지·재시작 때 쌓인 데이터를 버리거나 FIFO를 지우지 않는다.
FlushPending=no
RemoveOnStop=no
Service=app-log-keeper.service
```

`ListenFIFO`로 만든 FIFO는 PID1(systemd)이 읽기·쓰기 모드로 열어 둔다.  
읽는 쪽이 항상 하나는 있는 셈이라 writer가 죽어도 앱의 쓰기는 끊기지 않고, 그동안의 데이터는 커널 파이프 버퍼(64KiB)에 남는다.  

소켓의 활성화 대상은 writer가 아니라 아무 일도 하지 않는 oneshot 서비스(keeper)로 따로 두었다.  
writer를 대상으로 두면 writer가 반복 장애로 시작 제한에 걸릴 때 소켓 유닛까지 실패로 끌려가기 때문이다.  

## writer와 앱 유닛

writer는 OS의 `syslog-ng.service`와 별개로 앱 계정으로 도는 전용 인스턴스다.  

```text
source app_input {
    pipe("/run/app-log/stdout.fifo" flags(no-parse, empty-lines));
    pipe("/run/app-log/stderr.fifo" flags(no-parse, empty-lines));
};
destination app_file {
    file("/var/log/[앱]/app.log" template("${MESSAGE}\n") perm(0640));
};
log { source(app_input); destination(app_file); flags(flow-control); };
```

- `no-parse`와 `template("${MESSAGE}\n")`: 헤더나 시각을 붙이지 않고 받은 줄 그대로 쓴다. Alloy는 전과 똑같이 Pino JSON을 읽는다.
- stdout·stderr를 FIFO 하나로 합치면 두 스트림의 줄이 중간에서 섞일 수 있어 둘로 나눴다.
- `flow-control`: 파일 쓰기가 밀리면 FIFO 읽기를 늦춰 메시지를 버리지 않게 한다.

앱 유닛은 원본을 고치지 않고 drop-in으로 출력 대상만 바꿨다.  

```ini
[Unit]
Wants=app-log-writer.service
After=app-log-writer.service

[Service]
StandardOutput=file:/run/app-log/stdout.fifo
StandardError=file:/run/app-log/stderr.fifo
```

`Requires`가 아니라 `Wants`로 둔 건 로그 경로를 손보느라 writer를 내려도 앱까지 멈추면 안 되기 때문이다.  

# 회전 규칙: rename → create → reopen

크기·보관·압축 설정은 그대로 두고 회전 방식만 바꿨다.  

```diff
 /var/log/[앱]/app.log {
     su <앱 계정> <앱 계정>
     daily
     maxsize 100M
     rotate 14
     missingok
     notifempty
     compress
     delaycompress
-    copytruncate
+    create 0640 <앱 계정> <앱 계정>
+    postrotate
+        /usr/sbin/syslog-ng-ctl --control=/run/app-log/writer.ctl reopen > /dev/null 2>&1 ||
+            /usr/bin/systemctl restart app-log-writer.service
+    endscript
 }
```

logrotate가 `app.log`를 `app.log.1`로 이름을 바꾸고 새 파일을 만든 뒤 writer에게 다시 열게 한다.  
reopen이 실패하면 writer를 재시작하는데, FIFO는 PID1이 열어 두고 있으니 앱은 영향을 받지 않는다.  

그리고 파일이 비워지는 게 아니라 이름만 바뀌므로 Alloy는 옮겨진 파일을 끝까지 읽은 뒤 새 파일로 넘어간다.  
따라서 두 번째 유실 문제도 해결된다.  

# 실제 부하에서 비교하기

실제 웹 요청과 DB 부하를 걸고 두 방식을 비교했다.  
요청마다 `x-request-id`를 붙이면 앱이 그 값을 로그의 `reqId`로 남기므로 보낸 요청과 로그 줄을 1:1로 맞출 수 있다.  
웹 요청 약 57,000건과 PostgreSQL 문장 로그 약 167,000줄을 흘리면서 5초마다 강제 회전을 걸었다.  

| 항목 | FIFO + rename | 기존 copytruncate |
| --- | --- | --- |
| 파일 누락 | 0 / 38,164 | 1 / 38,042 |
| Loki 도달 | 38,163 / 38,164 | 36,773 / 38,041 |
| 회전당 Loki 누락 | 약 0.04줄 | 약 53줄 |

기존 copytruncate 방식에서 파일에서 잃은 줄은 1줄뿐이었지만 Loki로 못 간 줄은 1,268줄이었다.  
FIFO + rename 방식에서는 이 숫자가 1줄로 줄었다.  

다만 writer의 긴 장애나 디스크 고갈처럼 파이프 버퍼 64KiB를 넘는 상황까지 무손실을 보장하지는 않는다.  
우선순위 버퍼 같은 2차 개선은 실제 누락이 확인되면 다시 꺼내기로 하고 미뤘다.  

# 마치며

처음 `copytruncate`를 고를 때 "한두 줄은 괜찮다"고 판단한 건 틀린 결정이 아니었다.  

하지만 직접 재 보니 생각했던 것보다 유실량이 많았고, 무엇보다 파일이 아니라 Loki 쪽에서 더 크게 일어나고 있었다.  

이 문제는 앱이 로그 파일 FD를 직접 갖고 있어서 생긴 제약이니, 파일을 여는 주체를 바꿈으로써 개선했다.
