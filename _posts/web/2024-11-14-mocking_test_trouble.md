---
title: "@WebMvcTest를 사용하며 맞닥뜨린 문제"
excerpt: "@WebMvcTest를 사용하며 겪은 문제와 해결했던 방법"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - test
toc: true
toc_sticky: true
last_modified_at: 2024-11-14T00:00:00+09:00
---

# 컨트롤러 테스트
## WebMvcTest를 사용한 계기
리포지토리 함수야 데이터베이스에 값 잘 들어가는지 확인하고, 서비스 함수야 리포지토리 함수 잘 호출하고 비즈니스 로직 잘 처리하는지만 보면 됐다.  
그 둘의 테스트를 작성할 때에는 문제가 없었는데, 갑자기 컨트롤러 함수에 대한 테스트를 작성하려니 턱 막혔다. 바로 "컨트롤러를 테스트하려면 요청을 보내고 응답을 받아야하지 않나?" 라는 생각 때문이었다.

이어서 들었던 생각은 "그러면 컨트롤러는 서비스, 리포지토리까지 전부 호출하는지를 봐야 하는 건가? 그러면 너무 지저분한 것 같은데. 애초에 요청을 실제로 테스트에서 보내는 게 맞나?" 였다.  
그래서 나는 분명 이에 대해 사람들이 뭔가 만들어 둔 것이 있을 거라 생각하고, 컨트롤러를 테스트하는 방법에 대해 구글링했다.

## WebMvcTest
> @WebMvcTest는 Spring MVC 컨트롤러를 테스트할 때 사용되는 어노테이션으로, 웹 레이어(컨트롤러)만 독립적으로 테스트하고 전체 애플리케이션 컨텍스트를 로드하지 않도록 해줍니다.  
> 즉, 서비스나 레포지토리 등 다른 빈들은 로드되지 않으며, 컨트롤러의 동작만 확인할 수 있습니다.  
> 이 방식은 테스트의 속도를 높이고, 컨트롤러에 집중할 수 있게 해줍니다. ~~GPT 씀~~

옳거니! 사용 방법은 간단했는데, HTTP 요청을 보내고 응답을 확인할 용도의 `MockMvc`를 선언하고 `perform` 함수를 통해 테스트하고자 하는 API로 요청을 보내면 된다.

```java
@WebMvcTest(MyController.class)
public class MyControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MyService myService;  // 서비스 모킹

    @Test
    public void testHandleInternalError() throws Exception {
        mockMvc.perform(get("/example"))
               .andExpect(status().isInternalServerError())  // 500 상태 코드 확인
               .andExpect(content().string("문제가 발생했습니다"));  // 예외 메시지 확인
    }
}
```

# 문제
## Response Body에 자꾸 null이 들어간다
그렇게 http 응답 코드들을 확인하며 잘 동작하는 것을 봤는데, 문제는 response body를 확인하며 발생했다.

rest docs에 response body 값을 작성하는 과정에서, 리소스를 post한 후에 해당 리소스의 id 값을 반환하는 함수였는데 자꾸 response body에 0이 담겨 오는 것이었다.  
id는 DB 상의 id 값으로 1부터 시작하도록 해두었는데 0이 반환된다니 말도 안 되는 일이었다.  

그래서 확인해 본 결과, `getId()`를 호출한 객체가 `null`인 것을 알아냈다.

일단 서비스 객체를 모킹하다보니 실제로 값을 뱉지 않는건가 싶어 구글링을 해 보니 `verify` 함수로 수행 여부를 확인하길래 나도 해 본 결과, **실제 처리되는 Request 객체와 모킹한 Request 객체의 해시코드가 다르다**는 것이 결론이었다.  
그러니 내가 준 Request 객체로 모킹한 서비스 객체의 함수를 호출한 게 아니니, 값이 제대로 반환될 리가 없었다.

# 해결
## mockito
> Mockito는 자바에서 사용되는 모킹 라이브러리로, 주로 **단위 테스트(Unit Test)**에서 외부 의존성(예: 서비스, 데이터베이스, HTTP 클라이언트 등)을 모의(Mock) 하기 위해 사용됩니다.  
> 이를 통해 실제 구현 없이 **가짜 객체(Mock Object)**를 만들어 테스트할 수 있으며, 특정 메서드 호출에 대해 원하는 반환 값을 설정하고, 호출 여부를 검증하는 등의 작업을 할 수 있습니다. ~~갓피티~~

## mockito로 응답을 가짜로 만들어버리자
저 문제를 해결하기 위해 많은 사람들이 mockito로 응답을 만들어두는 것 같았다.  

그래서 나는 서비스에서 반환할 데이터를 `given().willReturn()`의 형식으로 정의하였고, 추가로 서비스 함수를 제대로 수행했는지(특정 서비스 함수를 호출했는가, 몇 번 호출했는가 등) 여부를 `verify` 함수를 통해 검증했다.  
추가로 예외 처리 부분에 있어서도 `given().willThrow()`를 통해 특정 서비스 함수를 호출하면 반드시 의도한 예외를 발생시키도록 했다.

[여기](https://eternal-return-user-creator.github.io/er-bal-api.github.io/#_get_apiquestion) 들어가면 결과를 볼 수 있다..!

# 참고한 블로그들
- [민찬기, [Spring/Test] WebMvcTest에서 Response Body가 Empty일 때](https://velog.io/@devmizz/Spring-WebMvcTest%EC%97%90%EC%84%9C-Response-Body%EA%B0%80-Empty%EC%9D%BC-%EB%95%8C)
- [loose, @WebMvcTest에 대한 올바른 사용법 및 시행착오](https://stir.tistory.com/407)
- [ksb-dev, WebMvcTest Mockito given() Null](https://ksb-dev.tistory.com/326)
