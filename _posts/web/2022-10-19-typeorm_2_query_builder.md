---
title: "[TypeORM] Advanced: Query Builder"
excerpt: "Query Builder 사용법"
category: 
  - web
author_profile: true
sidebar:
  - nav: "main"
tag:
  - ORM
  - TypeORM
toc: true
toc_sticky: true
last_modified_at: 2022-10-19T01:00:00+09:00
---

> [1편. [TypeORM] Example using TypeORM with Express](../typeorm_1_example_express)와 이어집니다.

# 시작하기 전에
TypeORM에서는 Repository API와 Query Builder를 이용하여 SQL을 구성할 수 있다. 그런데 "아니 Repository API 사용해서 동작 가능하게 만들었으면 됐지, 웬 Query Builder냐?" 할 수 있다. 이 둘은 명백한 차이가 있고, 각각의 특징이 있기 때문에 상황에 맞춰서 잘 사용하면 좋을 것 같아서 Repository 뿐만 아니라 Query Builder로도 어떻게 TypeORM을 사용하는지를 작성하도록 하겠다.

Query Builder를 이용하는 방법은 크게 DataSource, entity manager, repository를 이용한 방법이 있는데, repository를 이용하는 방법은 이미 해봤으니 이번엔 DataSource를 사용해보도록 하겠다.

# Repository API vs Query Builder
- Repository API
  - 사용하기 쉬움
  - 릴레이션을 가져오는 데 친화적
    - 데코레이션으로부터 eager/lazy 릴레이션들이 파싱됨
    - join을 일일이 열거할 필요 없음
- Query Builder
  - 매우 강력하고 SQL문에 가까운 형태
  - 복잡한 SQL문도 구성 가능
  - join을 명시해야 함
    - 그렇지 않으면 메인 테이블의 내용만 가져옴

# app.ts with DataSource + Query Builder
이전에 Repository API를 이용하여 만든 `app.ts`를 Query Builder를 이용한 코드로 바꾸면 다음과 같다.

```typescript
import express from "express"
import { Request, Response } from "express"
import { User } from "./entity/user.entity"
import { myDataSource } from "../app-data-source"

// 데이터베이스 연결
myDataSource
	.initialize()
	.then(() => {
		console.log("Data Source has been initialized!")
	})
	.catch((err) => {
		console.error("Error during Data Source initialization:", err)
	});

// express 생성 및 설정
const app = express();
app.use(express.json());

// 라우터
app.get("/users/register", async function (req: Request, res: Response) {
	const values = [
		{
			firstName: "이름",
			lastName: "성"
		},
		{
			firstName: "glish",
			lastName: "En"
		}
	];
	myDataSource.createQueryBuilder()
		.insert()
		.into(User)
		.values(values)
		.execute();
	return res.redirect("/users");
});

app.get("/users/update/:id", async function (req: Request, res: Response) {
	const id = req.params.id;
	myDataSource.createQueryBuilder()
		.update(User)
		.set({ "firstName": "Updated" })
		.where("id = :id", { id: id })
		.execute();
	return res.redirect("/users/" + id);
});

app.get("/users/leave/:id", async function (req: Request, res: Response) {
	await myDataSource.createQueryBuilder()
			.delete()
			.from(User)
			.where("id = :id", { id: req.params.id })
			.execute();
	return res.redirect("/users");
});

app.get("/users/count", async function (req: Request, res: Response) {
	const count = await myDataSource.createQueryBuilder()
					.select()
					.from(User, "user")
					.getCount();
	return res.json(count);
});

app.get("/users/:id", async function (req: Request, res: Response) {
	const name = await myDataSource.createQueryBuilder()
					.select(["user.firstName", "user.lastName"])
					.from(User, "user")
					.where("user.id = :id", { id: req.params.id })
					.getOne();
	return res.json(name);
});

app.get("/users", async function (req: Request, res: Response) {
	const users = await myDataSource.createQueryBuilder()
					.select()
					.from(User, "user")
					.orderBy("user.id", "DESC")
					.getRawMany();
	return res.json(users);
});

// start express server
app.listen(3000);

```

~~줄맞춤 악랄한 거 보소~~

여기서는 Repository API를 사용했을 때와 비슷한 동작을 하기 때문에, 실행 화면과 쿼리문은 건너뛰겠다. 대신 쓰인 함수에 대해서만 간략하게 적어놓도록 하겠다.

- `createQueryBuilder()`: SQL 쿼리를 구성하는 데 쓰이는 쿼리 builder를 생성한다.
- `select()`: SELECT문을 만든다. 괄호 안에는 함수(ADD, SUM 같은), 컬럼 등 일반적인 SELECT와 FROM 사이에 들어갈 수 있는 구문들이 들어갈 수 있다.
- `from()`: SELECT, DELETE문에서의 from 역할. 데이터를 매핑할 엔티티 클래스와 테이블의 별칭을 인자로 받는다.
- `where()`: WHERE 조건문 역할. 조건을 추가하고 싶으면 `andWhere()`나 `orWhere()`를 써도 된다.
- `orderBy()`: ORDER BY 역할. 정렬의 기준이 되는 컬럼과 정렬 방식을 인자로 받는다.
- `getRawMany()`: builder SQL을 실행하여 반환된 모든 raw result를 가져온다.
- `getOne()`: builder SQL을 실행하여 반환된 엔티티 한 개를 가져온다.
- `getCount()`: builder SQL을 실행하여 반환된 엔티티의 개수를 가져온다.
- `insert().into(Entity Class, columns).values(values)`: = INSERT INTO table (columns) VALUES (values)
- `update(Entity Class).set(values)`: = UPDATE table SET values
- `delete().from(Entity Class)`: = DELETE FROM table
