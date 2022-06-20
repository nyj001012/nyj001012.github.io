---
title: "[Hello Coding 알고리즘] 이진 탐색; Binary Search"
excerpt: ""
category: 
  - algorithm
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - Hello Coding 알고리즘
toc: true
toc_sticky: true
use_math: true
last_modified_at: 2022-06-20T00:00:00+09:00
---

> 이 포스트는 ["Hello Coding 그림으로 개념을 이해하는 알고리즘, 아디트야 바르가바"](https://www.google.com/search?gs_ssp=eJwBUACv_woNL2cvMTFieXZjeWZ3ZjABSj1oZWxsbyBjb2Rpbmcg6re466a87Jy866GcIOqwnOuFkOydhCDsnbTtlbTtlZjripQg7JWM6rOg66as7KaYt2krKw&q=hello+coding+%EA%B7%B8%EB%A6%BC%EC%9C%BC%EB%A1%9C+%EA%B0%9C%EB%85%90%EC%9D%84+%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94+%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98&rlz=1C5CHFA_enKR995KR995&oq=hello+coding+%EA%B7%B8%EB%A6%BC%EC%9C%BC%EB%A1%9C+&aqs=chrome.1.69i57j46i512j0i512.5576j0j7&sourceid=chrome&ie=UTF-8)를 읽고 작성하였습니다.

# 이진 탐색
## 개념
이진 탐색의 예시로 업다운 게임을 들어보겠다. 1부터 100까지의 수 중, 당신이 만약 숫자 47을 골랐고 내가 그걸 맞춘다고 해보자. 나는 먼저 1부터 100까지의 반절인 50을 제시할 것이다. 50은 47보다 큰 수이므로, 당신은 "다운"이라고 말할 것이다. 그러면 나는 1부터 49까지의 수 중, 가운데 수인 25를 말할 것이다. 그러면 25는 47보다 작은 수이므로, 당신은 "업"이라고 말할 것이다. 그러면 나는 26부터 49까지의 수 중, 또다시 가운데 수인 37을 말하고, 이와 같이 진행하다보면 나는 47이라는 수를 찾을 것이다.  
이와 같은 방법이면 1부터 100까지의 수를 찾을 때, 최대 7번만에 원하는 수를 찾을 수 있다(100 → 50 → 25 → 13 → 7 → 4 → 2 → 1).

## 시간 복잡도
이진 탐색의 시간 복잡도는 $O(\log{n})$ 이다.

# 구현
책에서는 숫자를 가지고 이진 탐색을 구현했다. 그런데 나는 쉘에서 문자열들을 입력받아, `args[0]`을 `args[1 ~ (args.length - 1)]`에서 찾을 것이다. 추가적으로 에러 메시지와 소요 시간, 어느 인덱스에 찾고 싶은 요소(문자열)가 있는지를 출력하게 했다. 전체적인 코드는 다음과 같다.

## 코드
{% highlight java linenos %}
public class binarySearch {
    public static void main(String[] args) {
        int low = 1;
        int high = args.length - 1;
        int mid = 0;
        long startTime = System.currentTimeMillis();
        long endTime = 0;

        System.out.println("==================== Binary Search ====================");
        if (high < 0)
            System.out.println("-> Error: not enough arguments");
        else {
            System.out.println("-> Start Search");
            while (low <= high) {
                mid = (low + high) / 2;
                if (args[0].compareTo(args[mid]) == 0) {
                    endTime = System.currentTimeMillis();
                    System.out.println("-> End Search: element in " + (mid - 1) + " (" + (endTime - startTime) + "ms)");
                    return;
                }
                else if (args[0].compareTo(args[mid]) > 0)
                    low = mid + 1;
                else
                    high = mid - 1;
            }
            endTime = System.currentTimeMillis();
            System.out.println("-> End Search: (" + (endTime - startTime) + "ms)");
            System.out.println(args[0] + " is not found.");
        }
        return;
    }
}
{% endhighlight %}

- 변수
  - `int low`: `args[]` 인덱스의 최소값. 찾을 범위는 무조건 인덱스가 1부터 시작이므로 초기값을 1로 세팅
  - `int high`: `args[]` 인덱스의 최대값
  - `int mid`: `low`와 `high`의 중간 인덱스
  - `long startTime`: 실행 시작 시각
  - `long endTime`: 실행 종료 시각

- 설명
  - 10 ~ 11: 만약 `args.length < 2`이라면 `high < 1`이고, 이는 찾을 문자열만 입력했다는 의미이므로 에러로 처리했다.
  - 14 ~ 25:
    - 만약 `args[0]`의 아스키 값이 `args[mid]`의 값과 같다면, 실행에 걸린 시간과 해당 인덱스를 출력한다.
    - 만약 `args[0]`의 아스키 값이 `args[mid]`의 값보다 크다면, 찾으려는 문자열은 `mid`번째보다 뒤쪽에 있다. 따라서 찾으려는 인덱스 범위의 최소값인 `low`를 `mid + 1`로 할당함으로써 `mid` 바로 다음 번째 문자열부터 `high`까지 찾게 한다.
    - 만약 `args[0]`의 아스키 값이 `args[mid]`의 값보다 작다면, 찾으려는 문자열은 `mid`번째보다 앞쪽에 있다. 따라서 찾으려는 인덱스 범위의 최대값인 `high`를 `mid - 1`로 할당함으로써 `low`부터 `mid` 바로 전 문자열까지 찾게 한다.
  - 26 ~ 28: `low > high`라는 것은 원하는 문자열을 찾지 못했다는 뜻이므로, 탐색이 종료되었음과 수행 시간, 안내 문구를 출력한다.

### 실행 결과
```bash
~/dev/algorithm/src ❯ java binarySearch "b" "b"        
==================== Binary Search ====================
-> Start Search
-> End Search: element in 0 (1ms)

~/dev/algorithm/src ❯ java binarySearch "ㅊ" "a" "b" "c"
==================== Binary Search ====================
-> Start Search
-> End Search: (1ms)
ㅊ is not found.

~/dev/algorithm/src ❯ java binarySearch "c" "a" "b" "c"  
==================== Binary Search ====================
-> Start Search
-> End Search: element in 2 (1ms)

~/dev/algorithm/src ❯ java binarySearch "c" "a" "b" "c" "134"
==================== Binary Search ====================
-> Start Search
-> End Search: element in 2 (0ms)
```

## 추가
여기서 약간의 장난을 쳐보도록 하겠다. 만약 입력 문자열이 정렬되어 있지 않다면?

```bash
~/dev/algorithm/src ❯ java binarySearch "abc" "cba" "bac" "acb" "abc" "cab" "bca"
==================== Binary Search ====================
-> Start Search
-> End Search: (0ms)
abc is not found.
```

결과는 정상적으로 동작하지 않는다.

**이진 탐색은 데이터(배열)가 정렬되어 있음을 전제로 한다.**  
전화번호부도, 1부터 100까지의 수도 전부 정렬이 되어있는 상태이다. 따라서 코드를 약간 바꿔서 입력 데이터의 순서가 뒤죽박죽이어도 찾을 수 있게끔 수정을 해보겠다. 이의 경우에는 몇 번째 위치에서 문자열을 찾았는지는 중요하지 않을 것이기 때문에, 해당 부분은 출력하지 않도록 했다.

{% highlight java linenos %}
import java.util.Arrays;

public class binarySearchSort {
    public static void main(String[] args) {
        int low = 0;
        int high = args.length - 2;
        int mid = 0;
        long startTime = System.currentTimeMillis();
        long endTime = 0;
        String[] sortedArgs;

        System.out.println("==================== Binary Search ====================");
        if (high < 1)
            System.out.println("-> Error: not enough arguments");
        else {
            sortedArgs = Arrays.copyOfRange(args, 1, args.length);
            Arrays.sort(sortedArgs);
            System.out.println("-> Start Search");
            while (low <= high) {
                mid = (low + high) / 2;
                if (args[0].compareTo(sortedArgs[mid]) == 0) {
                    endTime = System.currentTimeMillis();
                    System.out.println("-> End Search: " + sortedArgs[mid] + " exists! (" + (endTime - startTime) + "ms)");
                    return;
                }
                else if (args[0].compareTo(sortedArgs[mid]) > 0)
                    low = mid + 1;
                else
                    high = mid - 1;
            }
            endTime = System.currentTimeMillis();
            System.out.println("-> End Search: " + args[0] + " doesn't exist " + "(" + (endTime - startTime) + "ms)");
        }
        return;
    }
}
{% endhighlight %}

- 변수
  - `sortedArgs`: `args`의 0번째 요소를 제외하고 복사한 후, 정렬한 문자열 배열

- 설명
  - 6: 이번 탐색에서는 `args[0]`과 `sortedArgs[mid]`를 비교할 것인데, `low`와 `high`는 `sortedArgs`의 인덱스 범위를 나타낸다. `sortedArgs.length = args.length - 1`이므로, `high`는 기존 `args.length - 1`보다 1 작아야 `sortedArgs`의 마지막 요소의 인덱스를 나타낸다.
  - 16: `args`를 1번째부터 `args.length` 전까지 복사하여 `sortedArgs`에 할당한다.
  - 17: `sortedArgs`를 오름차순으로 정렬한다.

### 실행 결과
```bash
~/dev/algorithm/src ❯ java binarySearchSort "b" "a" "c" "b"
==================== Binary Search ====================
-> Start Search
-> End Search: b exists! (1ms)

~/dev/algorithm/src ❯ java binarySearchSort "word" "This" "is" "word" "sentence" "true" "apple"
==================== Binary Search ====================
-> Start Search
-> End Search: word exists! (1ms)

~/dev/algorithm/src ❯ java binarySearchSort "not" "This" "should" "print" "not found"
==================== Binary Search ====================
-> Start Search
-> End Search: not doesn\'t exist (0ms)

~/dev/algorithm/src ❯ java binarySearchSort                                                    
==================== Binary Search ====================
-> Error: not enough arguments

~/dev/algorithm/src ❯ java binarySearchSort "find"                                             
==================== Binary Search ====================
-> Error: not enough arguments
```