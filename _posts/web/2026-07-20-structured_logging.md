---
title: "백엔드 로깅을 구조화하며 좋았던 설계"
excerpt: "MR !92에서 백엔드 로깅을 Pino 기반 구조화 로그로 정리하며 좋았던 정책과 아키텍처"
category:
  - web
author_profile: true
sidebar:
  - nav: "main"
tag:
  - web
  - backend
  - logging
  - pino
  - nextjs
toc: true
toc_sticky: true
last_modified_at: 2026-07-20T00:00:00+09:00
---

# 백엔드 로깅을 손봐야겠다고 생각한 이유
이번에 upstream MR !92에서 백엔드 로깅을 구조화하는 작업을 했다.

> 기존 프로젝트에는 백엔드 로깅 정책이나 공통 로깅 구조가 따로 없었다.  
> 그래서 이번 MR에서 내가 직접 Pino 기반 구조화 로깅을 도입하고, 요청 단위로 추적할 수 있는 형태로 정리했다.

처음에는 단순히 `console.error`를 Pino로 바꾸는 정도라고 생각할 수도 있는데, 실제로는 그보다 훨씬 마음에 드는 형태로 정리됐다.  
좋았던 점은 로그 라이브러리를 도입했다는 사실보다, **로그를 어디서 남길지, 어떤 정보를 담을지, 비즈니스 코드와 어떻게 분리할지**가 꽤 분명해졌다는 점이다.

기존 라우트 핸들러는 대체로 이런 모양이었다.

```ts
const GET = async () => {
  try {
    const res = await getSensors();
    return jsonResponse(CnSensorResponseSchema.array(), res);
  } catch (error) {
    return handleErrorResponse(error);
  }
};
```

각 라우트마다 `try/catch`가 있고, 실패하면 `handleErrorResponse`로 넘긴다.  
동작 자체는 문제없지만 라우트가 많아질수록 같은 코드가 계속 반복된다.  
그리고 요청이 언제 들어왔는지, 어떤 도메인의 어떤 라우트인지, 얼마나 걸렸는지, 어떤 요청과 어떤 DB 쿼리가 관련 있는지를 한 번에 따라가기 어렵다.

이번 작업의 방향은 이 반복을 줄이는 데서 끝나지 않았다.  
**라우트 핸들러는 도메인 로직만** 갖고, **요청 로깅과 에러 응답 변환은 공통 진입점에서 처리**하도록 바꾸었다.

```ts
const ROUTE = '/api/current/sensor';
const DOMAIN = 'cn-sensor';

const GET = createRoute({ domain: DOMAIN, route: ROUTE }, async () => {
  const res = await getSensors();
  return jsonResponse(CnSensorResponseSchema.array(), res);
});
```

이 형태가 마음에 들었다.  
핸들러 안에는 "센서 목록을 가져와 응답한다"는 코드만 남고, 로깅과 에러 핸들링은 라우트의 공통 정책으로 빠졌다.

# 정책이 먼저 있어야 한다
로깅을 붙일 때 제일 애매한 부분은 "무엇을 로그로 남길 것인가"라고 생각한다.

이번 작업에서는 정책이 꽤 명확했다.

- 프로덕션 로그는 stdout JSON으로 남긴다.
- 개발 환경에서는 `pino-pretty`로 사람이 읽기 좋게 본다.
- 로그 레벨은 `LOG_LEVEL` 환경 변수를 우선하고, 없으면 프로덕션은 `info`, 개발은 `debug`로 둔다.
- 요청마다 `reqId`를 부여한다.
- 클라이언트가 `x-request-id`를 보냈다면 이어받고, 없다면 서버에서 새로 만든다.
- 응답 헤더에도 `x-request-id`를 실어 돌려준다.
- 라우트 로그에는 `reqId`, HTTP method, route pattern, domain을 공통 필드로 붙인다.
- 5xx는 `error`, 4xx는 `warn`, 나머지는 `info`로 남긴다.
- 시크릿, 자격증명, `process.env` 전체, 쿼리 파라미터 값, 이벤트 payload 본문은 로그에 담지 않는다.

이런 규칙이 있으면 로그를 남기는 코드가 취향의 문제가 아니라 운영 정책이 된다.

특히 `reqId`를 응답 헤더에 돌려주는 부분이 좋았다.  
사용자가 "방금 요청이 실패했다"고 했을 때, 프론트나 네트워크 탭에서 확인한 `x-request-id` 하나로 백엔드 로그를 추적할 수 있기 때문이다.

# Pino 싱글톤
기반 로거는 `lib/logger.ts`에 모았다.

```ts
const isProd = process.env.NODE_ENV === 'production';
const level = process.env.LOG_LEVEL ?? (isProd ? 'info' : 'debug');

const globalForLogger = globalThis as unknown as { logger?: pino.Logger };

const logger = globalForLogger.logger ?? createLogger();

if (!isProd) globalForLogger.logger = logger;
```

Next.js 개발 환경에서는 HMR 때문에 모듈이 여러 번 초기화될 수 있다.  
이때 logger transport가 중복으로 생기지 않도록 `globalThis`에 캐시했다.  
Prisma client를 전역 캐시하는 것과 같은 종류의 문제다.

그리고 프로덕션에서는 별도 pretty transport를 붙이지 않고 JSON을 stdout으로 흘린다.  
애플리케이션은 로그를 표준 출력으로 내보내고, 수집/검색/알림은 인프라가 가져가게 하는 쪽이 단순하다.

# 요청 컨텍스트를 AsyncLocalStorage로 묶기
이번 구조에서 가장 중요한 장치는 `AsyncLocalStorage`였다.

요청이 들어오면 `withRequestLogging`이 `reqId`와 child logger를 만들고, `runWithRequestContext`로 요청 컨텍스트에 넣는다.

```ts
type RequestContext = { reqId: string; log: Logger };

const storage = new AsyncLocalStorage<RequestContext>();

const runWithRequestContext = <T>(context: RequestContext, fn: () => T): T =>
  storage.run(context, fn);

const getRequestLog = (): Logger => storage.getStore()?.log ?? logger;
const getReqId = (): string | undefined => storage.getStore()?.reqId;
```

이 구조의 장점은 파라미터 드릴링을 하지 않아도 된다는 점이다.  
라우트 핸들러, 에러 핸들러, 데이터 계층이 서로를 직접 알 필요 없이 같은 요청의 logger를 꺼내 쓸 수 있다.

예를 들어 에러 응답을 만드는 코드는 로깅 래퍼를 몰라도 된다.

```ts
const withErrorHandling = <C>(handler: Handler<C>) => {
  return async (request: NextRequest, ctx: C): Promise<NextResponse> => {
    try {
      return await handler(request, ctx);
    } catch (error) {
      return handleErrorResponse(error, getRequestLog());
    }
  };
};
```

여기서 `getRequestLog()`는 현재 요청의 child logger를 반환한다.  
컨텍스트 밖에서 호출되면 base logger로 폴백한다. 그래서 백그라운드 작업이나 아직 래핑되지 않은 코드에서도 최소한 로그는 남길 수 있다.

# createRoute라는 단일 진입점
로깅 래퍼와 에러 핸들링 래퍼를 각각 만들었지만, 모든 라우트에서 매번 직접 합성하게 두지는 않았다.

```ts
const createRoute = <C>(config: RouteOptions, handler: RouteHandler<C>) =>
  withRequestLogging(config, withErrorHandling(handler));
```

이 한 줄이 생각보다 중요하다.

래퍼는 독립되어 있지만, 실제 라우트에서는 `createRoute`만 쓰면 된다.  
덕분에 라우트별로 합성 순서를 잘못 쓰거나, 어떤 라우트에는 로깅을 붙이고 어떤 라우트에는 빠뜨리는 실수를 줄일 수 있다.

합성 순서도 의미가 있다.

- 바깥쪽 `withRequestLogging`은 요청 시작 시점에 `reqId`와 child logger를 만든다.
- 안쪽 `withErrorHandling`은 핸들러에서 발생한 예외를 HTTP 응답으로 바꾼다.
- 다시 바깥쪽 `withRequestLogging`은 최종 응답 상태 코드를 보고 완료/실패 로그를 한 번 남긴다.

즉, 핸들러가 예외를 던져도 요청 로그는 "이 요청은 몇 ms 걸렸고, 최종 status가 무엇이었다"는 형태로 남는다.  
에러 상세는 `handleErrorResponse`가 현재 요청 logger로 남긴다.

# 에러 응답과 서버 로그를 분리하기
에러 응답 처리도 더 좋아졌다.

클라이언트에게 알려도 되는 에러와 서버 로그에만 남겨야 하는 에러를 구분했다.  
예를 들어 요청 검증 실패는 400과 함께 필드별 `issues`를 내려줄 수 있다. 반대로 응답 계약 위반은 서버 버그에 가깝기 때문에 클라이언트에는 일반적인 서버 오류 메시지만 내려주고, 자세한 `issues`는 서버 로그에 남긴다.

```ts
if (error instanceof ResponseValidationError) {
  log.error({ err: error, issues: error.issues }, 'response contract violation');
  return NextResponse.json({ message: '서버 오류가 발생했습니다' }, { status: 500 });
}

log.error({ err: error }, 'unhandled error');
return NextResponse.json({ message: '서버 오류가 발생했습니다' }, { status: 500 });
```

예전의 `console.error`보다 좋은 점은 로그가 문자열 덩어리가 아니라는 것이다.  
`err`, `issues`, `reqId`, `route`, `domain`, `status`, `durationMs`가 각각 필드로 남는다. 나중에 검색할 때도 "특정 route의 5xx", "특정 reqId의 에러", "response contract violation"처럼 좁혀 볼 수 있다.

# DB 쿼리도 같은 요청으로 따라가기
Prisma client에도 쿼리 이벤트 로그를 붙였다.  
다만 모든 쿼리를 다 남기는 방식은 아니다. 200ms 이상 걸린 슬로우 쿼리만 `warn`으로 기록한다.

```ts
const SLOW_QUERY_MS = 200;

client.$on('query', (e) => {
  if (e.duration >= SLOW_QUERY_MS) {
    getRequestLog().warn({ query: e.query, durationMs: e.duration }, 'slow query');
  }
});
```

여기서도 `getRequestLog()`를 쓴다.  
그래서 특정 HTTP 요청에서 느린 쿼리가 발생하면 요청 로그와 슬로우 쿼리 로그가 같은 `reqId`로 묶인다.

이 부분에서 정책상 마음에 들었던 건 다음과 같다.

- 슬로우 쿼리만 남긴다.
- duration은 남긴다.
- query 문은 남긴다.
- params는 남기지 않는다.

DB 쿼리 로그는 조금만 방심해도 민감한 값이 섞일 수 있다.  
그래서 "무엇을 남길지"만큼 "무엇을 절대 남기지 않을지"가 중요했다.

# SSE는 createRoute를 쓰지 않았다
이렇게 만든 로거를 사용할 수 없었던 예외도 있다.  
`/api/notification` SSE 라우트는 `createRoute`를 쓰지 않았다.

처음 보면 모든 라우트를 같은 방식으로 감싸고 싶어진다.  
그런데 SSE는 일반적인 HTTP 요청/응답과 성격이 다르다.  

`ReadableStream`을 반환하는 장수명 연결이라서, `withRequestLogging`이 측정하는 `durationMs`는 실제 연결 유지 시간이 아니라 스트림 응답을 만드는 데 걸린 시간에 가까워진다.

또 스트림 콜백은 핸들러가 응답을 반환한 뒤에 실행된다.  
즉, `AsyncLocalStorage` 컨텍스트가 기대한 방식으로 이어지지 않을 수 있다.

그래서 SSE는 연결 단위 child logger를 직접 만들고, 그 logger를 클로저로 들고 간다.

```ts
const reqId = request.headers.get('x-request-id') ?? crypto.randomUUID();
const log = logger.child({ reqId, method: 'GET', route: ROUTE, domain: DOMAIN });
const start = performance.now();
const elapsedMs = () => Math.round(performance.now() - start);
```

그리고 연결 열림, 연결 닫힘, keepalive 실패, enqueue 실패, 처리하지 않는 url skip 같은 이벤트를 별도로 남긴다.

```ts
log.info({ channel }, 'sse connection opened');
log.info({ durationMs: elapsedMs(), reason }, 'sse connection closed');
log.error({ err, url: payload.url }, 'notification dropped: enqueue failed');
```

이 결정이 특히 마음에 들었다.  
공통화를 위해 억지로 모든 것을 같은 래퍼에 넣지 않고, 요청의 수명 모델이 다른 SSE는 별도 정책으로 다뤘다.  
공통화보다 관찰 가능성의 의미를 우선한 셈이다.

# 라우트 적용 방식
MR에는 Pino 기반 도입 이후 각 API 라우트에 `createRoute`를 적용하는 커밋들이 순서대로 들어갔다.

- Pino 구조화 로깅 기반 도입
- 요청 컨텍스트(ALS), 로깅 래퍼, 에러 래퍼, `createRoute` 도입
- Prisma 슬로우 쿼리 로깅에 `reqId` 상관관계 부여
- `current/sensor` 라우트에 파일럿 적용
- codes, code-types, containments, core, locations 라우트로 확장
- current/predefined 계열 라우트로 확장
- notification SSE 구조화 로깅 적용
- README에 로깅 구조 반영

파일럿을 먼저 만들고, 같은 패턴을 다른 라우트로 넓힌 점도 우아한 구조 같아서 마음에 들었다.

# 좋았던 점 정리
이번 로깅 구조에서 좋았던 부분은 크게 다섯 가지였다.

첫째, 라우트 핸들러가 깨끗해졌다.  
핸들러는 요청을 파싱하고 서비스를 호출하고 응답을 검증하는 데 집중한다. `try/catch`, 요청 완료 로그, 에러 상세 로그는 공통 정책으로 빠졌다.

둘째, 로그 필드가 검색 가능한 데이터가 됐다.  
문자열 로그가 아니라 `reqId`, `method`, `route`, `domain`, `status`, `durationMs` 같은 필드가 남는다.

셋째, 요청과 DB 쿼리가 같은 `reqId`로 묶인다.  
장애를 볼 때 HTTP 요청 로그와 슬로우 쿼리 로그를 따로 추측해서 맞추지 않아도 된다.

넷째, 민감 정보에 대한 기준이 있었다.  
로그는 디버깅을 위해 자세해야 하지만, 운영 환경에서는 남기지 말아야 할 값이 더 중요할 때가 많다. 이번 정책은 query params나 payload 값을 무작정 남기지 않는 쪽으로 정리됐다.

다섯째, 예외를 예외로 인정했다.  
SSE는 일반 라우트와 다르기 때문에 `createRoute` 공통 래퍼를 쓰지 않았다. 이건 단순한 코드 통일보다 실제 동작 모델을 우선한 결정이라 마음에 들었다.

# 마무리
이번 작업을 하고 나서 로깅은 "에러가 났을 때 출력하는 것"보다 넓은 문제라는 생각이 더 강해졌다.

좋은 로그는 나중에 운영자가 읽는 글이기도 하고, 시스템이 검색할 데이터이기도 하다.  
그래서 로그 메시지 하나하나보다 중요한 것은 일관된 정책과 구조다.

이번 MR !92에서 마음에 들었던 부분도 그 지점이었다.  
Pino를 도입한 것보다, 요청 단위 컨텍스트를 만들고, 라우트의 단일 진입점을 만들고, 에러 응답과 서버 로그를 분리하고, SSE 같은 예외는 별도 정책으로 다룬 구조가 좋았다.

다음에 비슷한 작업을 하게 된다면 처음부터 이 질문을 먼저 해볼 것 같다.

- 이 로그는 누가, 언제, 어떤 문제를 풀기 위해 볼까?
- 검색해야 하는 필드는 무엇인가?
- 절대 남기면 안 되는 값은 무엇인가?
- 모든 요청에 공통으로 적용할 정책과 예외로 둘 흐름은 무엇인가?

그 질문에 답이 있으면, 로깅 코드는 단순한 부가 기능이 아니라 백엔드 아키텍처의 일부가 된다.
