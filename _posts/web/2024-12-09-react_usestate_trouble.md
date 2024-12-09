---
title: "useState를 썼는데 값이 바뀌지 않는다"
excerpt: ""
category: 
  - web
  - react
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - web
  - react
  - 이터널 리턴
  - 밸런스 게임
toc: true
toc_sticky: true
last_modified_at: 2024-12-09T00:00:00+09:00
---

# 상황
이터널 리턴 밸런스게임을 만들던 도중, 질문 테이블의 id(`questionId`) 값을 상태로 관리하고 있었다.

백엔드에 GET 요청을 보내면 질문에 대한 정보를 응답으로 받는데, 이때 `setState(questionId)`로 `questionId` 값을 저장했다.

그런데 자꾸만 `questionId`에는 초기 값인 0이 들어가있었고, 새로고침을 해도 자꾸만 0이 할당되어 있었다.

# 원인
원인을 알기 위해 GPT의 도움을 받았다.  
GPT의 설명은 아래와 같았다.

> console.log(questionId)가 계속 0으로 출력되는 이유는 상태 업데이트(setQuestionId)가 비동기로 처리되기 때문입니다.  
> React에서 상태 업데이트는 즉각적으로 반영되지 않고, 컴포넌트의 다음 렌더링에서 반영됩니다.  
> 따라서 setQuestionId(data.id)를 호출한 직후에는 questionId가 업데이트되기 이전의 값을 유지합니다.

게다가 여러 상태에 변화가 생긴다면 이를 배치 작업으로 수행한다니, `setState()`가 많이 실행되던 해당 부분에서는 상대적으로 `questionId`의 업데이트가 느렸을 것이다.

그렇다고 사용자가 "어? 화면 나왔다" 하고 무언가를 클릭했는데, `questionId`가 처리되지 않아 에러가 발생하면 곤란했기에 다른 방법을 찾아야 했다.

# 해결
## `useRef` 사용
`questionId`는 렌더링 이후 클릭 이벤트 시, 백엔드에 요청보낼 때 사용할 파라미터였다. 따라서 렌더링과는 아무런 관련이 없었고, 이때 사용하기에 적합한 것으로 GPT는 `useRef`를 추천해주었다.

`useRef`는 렌더링에 관여하지 않는 값을 참조할 수 있는 리액트 훅으로, 자세한 설명은 [여기](https://velog.io/@hyoribogo/react-useref)를 참고.

사용하는 위치도 `useEffect` 내의 비동기 함수 내부이고, 다른 컴포넌트의 렌더링에 영향을 주거나 하는 것도 아니기 때문에 `useRef`를 사용했다.

```typescript
/**
 * 백엔드 API를 호출하여 다음 질문을 가져옵니다.
 */
async function callGetQuestionAPI() {
  const response = await fetch(...);
  if (response.ok) {
    const data = await response.json();
    setQuestion(data.questionText);
    questionIdRef.current = data.id; // 여기!
    setChoiceA(data.choiceA);
    setChoiceB(data.choiceB);
  }
}

```

프론트엔드 어렵다...
