---
title: "JDBC 템플릿"
excerpt: ""
category: 
  - springboot
author_profile: true
sidebar:
  - nav: "main" 
tag:
  - spring boot
toc: true
toc_sticky: true
last_modified_at: 2024-04-15T00:00:00+09:00
---

> 이 포스트는 김영한님의 ['스프링 입문 - 코드로 배우는 스프링 부트, 웹 MVC, DB 접근 기술'](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EC%9E%85%EB%AC%B8-%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8/dashboard)을 수강하고 작성하였습니다.

# JDBC 템플릿
이전에 JDBC를 쓰면서 데이터를 조회할 때

1. DB와 연결
2. 쿼리문 작성
3. 쿼리문으로 `prepareStatement` 생성
4. 조회 결과 하나씩 가져오기
5. `Member` 객체에 값 매핑
6. 조회 결과 반환

위의 일련의 과정들을 거쳐왔다. JDBC 템플릿은 이런 과정을 간단하게 해준다.

# `JDBCTemplateMemberRepository` 구현
```java
package hello.hellospring.repository;

// import 생략

@Repository
public class JDBCTemplateMemberRepository implements MemberRepository {
    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public JDBCTemplateMemberRepository(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Override
    public Member save(Member member) {
        SimpleJdbcInsert jdbcInsert = new SimpleJdbcInsert(jdbcTemplate);
        jdbcInsert.withTableName("member").usingGeneratedKeyColumns("id");

        Map<String, Object> parameters = new HashMap<String, Object>();
        parameters.put("name", member.getName());

        Number key = jdbcInsert.executeAndReturnKey(new MapSqlParameterSource(parameters));
        member.setId(key.longValue());
        return member;
    }

    @Override
    public Optional<Member> findById(Long id) {
        List<Member> memberList = jdbcTemplate.query("select * from member where id = ?", memberRowMapper(), id);
        return memberList.stream().findAny();
    }

    @Override
    public Optional<Member> findByName(String name) {
        List<Member> memberList = jdbcTemplate.query("select * from member where name = ?", memberRowMapper(), name);
        return memberList.stream().findAny();
    }

    @Override
    public List<Member> findAll() {
        return jdbcTemplate.query("select * from member", memberRowMapper());
    }

    private RowMapper<Member> memberRowMapper() {
        return (resultSet, row) -> {
            Member member = new Member();
            member.setId(resultSet.getLong("id"));
            member.setName(resultSet.getString("name"));
            return member;
        };
    }
}
```

`JdbcTemplate`을 이용하면 순수 JDBC만 사용했을 때보다 훨신 간편하다.  
여기서 `query()` 메서드로 조회하려면 조회 결과와 객체를 매핑할 함수가 필요하다는 것 정도이며, 이 함수의 매개변수로 `ResultSet`과 `row` 가 전달된다.

이 클래스가 잘 동작하는지는 `SpringConfig`에서 스프링 컨테이너에 등록할 리포지토리를 위의 리포지토리로 지정하고, 통합 테스트를 실행해보면 확인할 수 있다.
