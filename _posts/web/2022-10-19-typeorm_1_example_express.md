---
title: "[TypeORM] Example using TypeORM with Express"
excerpt: "공식 문서와 함께하는 간단한 사용법"
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
last_modified_at: 2022-10-19T00:00:00+09:00
---

# Type Script: TypeORM
> 공식 문서: <https://typeorm.io/>

## Getting Started 번역
[원문 보기](https://typeorm.io/)

TypeORM은 NodeJS, Browser, Cordova, PhoneGap, Ionic, React Native, NativeScript, Expo 및 전자 플랫폼에서 동작 가능하고 TypeScript와 JavaScript (ES5, ES6, ES7, ES8)에서 사용 가능한 ORM 입니다. 목표는 최신 Javascript를 항상 지원하고, 몇 안 되는 테이블을 가진 작은 프로그램부터 다수의 데이터베이스를 가진 대규모 기업용 프로그램까지 데이터베이스를 사용하는 어떠한 종류의 프로그램이라도 개발할 수 있게끔 도와주는 부가적인 부분까지 지원하는 것입니다.

TypeORM은 현재 존재하는 다른 모든 JavaScript ORM들과는 다르게, [Active Record 패턴과 Data Mapper 패턴](https://velog.io/@koreanhole/Active-Record%ED%8C%A8%ED%84%B4%EA%B3%BC-Data-Mapper-%ED%8C%A8%ED%84%B4) 모두를 지원합니다. 이는 **높은 퀄리티의, 느슨하게 연결된, 확장 가능한, 지속 가능한 프로그램을 가장 생산적인 방식으로 작성**할 수 있음을 의미합니다.

## Example using TypeORM with Express
패키지 매니저로 **yarn**을, DB로 **MySQL2**를, DBMS로 **MySQL Workbench**를, 그리고 **express**를 사용하여 튜토리얼을 진행하도록 하겠다. 특별히 이와 같이 구성한 이유는 
내가 현재 42 서울에서 활동하고 있는 집현전에서 위와 같은 세팅으로 개발을 하고 있기 때문이다.

### 초기 설정
우선 프로젝트 폴더에 yarn을 설치하고, `package.json`을 생성, 이후 타입 스크립트를 설치했다.
```bash
brew install yarn
yarn init -y
yarn add typescript --save-dev
```

타입 스크립트 설치까지 끝났으면, 타입 스크립트를 초기화하는 명령어를 실행하여 설정 파일인 `tsconfig.json`을 생성한다.
```bash
tsc -init
```

그러면 이와 같은 메시지가 터미널에 출력되고, 타입 스크립트 설정 파일이 생성된다.

```bash
Created a new tsconfig.json with:                                                                                       
                                                                                                                     TS 
  target: es2016
  module: commonjs
  strict: true
  esModuleInterop: true
  skipLibCheck: true
  forceConsistentCasingInFileNames: true


You can learn more at https://aka.ms/tsconfig
```

이후 `tsconfig.json`의 파일 내용 중, 나는 `compilerOptions` 중에 튜토리얼과는 다르게 일부만 변경했다.

```json
{
    "compilerOptions": {
        ...
        "emitDecoratorMetadata": true,
        "experimentalDecorators": true
        ...
    }
}
```

저 속성들은 처음엔 주석 처리가 되어 있을 건데, 저걸 true로 안 해주면 나중에 `@Entity` 같은 TypeORM의 [데코레이터](https://m.blog.naver.com/pjt3591oo/222120496022)를 
쓸 때 에러가 난다. 그래서 다른 건 몰라도 저 둘만큼은 꼭 true로 변경하기!

이제 타입 스크립트의 `src`폴더와 `app.ts`파일을 생성한다. 직접 폴더와 파일을 만들어도 되고, 아니면 밑에 있는 터미널 명령어를 실행하자.

```bash
mkdir src
touch src/app.ts
```

그리고 아까 만든 `src/app.ts`에 아래와 같은 코드를 추가하고 직접 실행해볼 것이다.

```ts
console.log("Application is up and running :)");
```

`src/app.ts`에 코드를 다 작성했으면 해당 파일을 자바 스크립트 파일로 컴파일한다.
```bash
tsc
```
컴파일하면 `src/app.js`가 생성된다. 이렇게 컴파일된 자바 스크립트 파일을 아래의 명령어로 실행한다. 그 결과로 아까 `src/app.ts`에 작성한 
"Application is up and running :)"이 출력되면 정상적으로 동작한 것이다.

```bash
node src/app.js
```

### Adding Express to the application
이제 TypeORM과 타입 스크립트의 준비가 되었으니 `express`를 프로젝트에 추가해보도록 하겠다. 일단 express를 아래의 명령어로 설치한다.

```bash
yarn add express @types/express --save
```

- `express`: express 엔진. 웹 API를 작성할 수 있게 해준다.
- `@types/express`: express의 타입 정의에 대한 패키지이다.

이제 `src/app.ts`에 express 스타일의 로직을 아래와 같이 구현해보자.

```ts
import express from "express"
import { Request, Response } from "express"

// create and setup express app
const app = express()
app.use(express.json())

// register routes

app.get("/users", function (req: Request, res: Response) {
    // here we will have logic to return all users
})

app.get("/users/:id", function (req: Request, res: Response) {
    // here we will have logic to return user by id
})

app.post("/users", function (req: Request, res: Response) {
    // here we will have logic to save a user
})

app.put("/users/:id", function (req: Request, res: Response) {
    // here we will have logic to update a user by a given user id
})

app.delete("/users/:id", function (req: Request, res: Response) {
    // here we will have logic to delete a user by a given user id
})

// start express server
app.listen(3000)
```

이제 프로젝트를 컴파일하고 실행해보면 된다. express 서버로 라우팅도 할 수 있다. 그런데, 전부 아무것도 반환하지는 않는다.

### Adding TypeORM to the application
이번엔 TypeORM을 추가해보자. 위에서 적어놨듯 튜토리얼에서는 mysql을 사용했지만, 나는 `mysql2`를 사용하여 진행하도록 하겠다. 튜토리얼에서도 다른 드라이버들도 셋업 
프로세스는 비슷하다고 나와있다.

아래의 명령어를 실행하여 typeorm, mysql2를 설치하자.

```bash
yarn add typeorm mysql2 reflect-metadata --save
```

- `reflect-metadata`: 데코레이터가 적절히 동작하게 한다.

다 설치했으면 초기 데이터베이스 연결 옵션을 설정하는 역할인 `app-data-source.ts` 를 작성하자.

```ts
import { DataSource } from "typeorm"

export const myDataSource = new DataSource({
    type: "mysql", // mysql2도 type을 mysql로 지정한다.
    host: "localhost",
    port: 3306,
    username: "ormtest",
    password: "password",
    database: "test",
    entities: ["src/entity/*.js"],
    logging: true,
    synchronize: true,
})
```

> [더 많은 Data Source Option 보러가기](https://typeorm.io/data-source-options#)

그 다음으로 `src/entity`에 `user.entity.ts`라는 엔티티 파일을 작성하자.

```ts
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm"

@Entity()
export class User {
    @PrimaryGeneratedColumn()
    id!: number

    @Column()
    firstName!: string

    @Column()
    lastName!: string
}
```

이때 튜토리얼 대로 작성하면 `속성 'id'은(는) 이니셜라이저가 없고 생성자에 할당되어 있지 않습니다.ts(2564)`라는 에러가 발생하는 경우가 있다. 
생성자를 추가해주면 해당 에러를 없앨 수 있지만, 간단하게 `!` 연산자를 추가하여 **해당 변수에는 무조건 값이 있음을 보장**한다고 
표시해주면 이 방법도 에러를 없앨 수 있다. 대신 남용하는 것은 좋지 않을 것 같다...

엔티티 파일까지 전부 작성했으면 `src/app.ts`를 CRUD에 맞게 아래와 같이 작성한다. 참고로 공식 문서의 튜토리얼에서 
일부를 수정했기 때문에, 공식 문서에서 제시한 코드와는 약간 다르다.

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
	const myRepo = myDataSource.getRepository(User);
	const user = await myRepo.create([
		{
			firstName: "이름",
			lastName: "성"
		},
		{
			firstName: "glish",
			lastName: "En"
		}
	]);
	const results = await myRepo.save(user);
	return res.json(results);
});

app.get("/users/update/:id", async function (req: Request, res: Response) {
	const user = await myDataSource.getRepository(User).findOneBy({
		id: Number(req.params.id),
	});
	if (user) {
		myDataSource.getRepository(User).merge(user, { "firstName": "Lover" },
		{ "lastName": "Espresso" });
		const results = await myDataSource.getRepository(User).save(user);
		return res.send(results);
	}
	else
		return res.statusMessage = 'Getting Repository Failed';
});

app.get("/users/leave/:id", async function (req: Request, res: Response) {
	const results = await myDataSource.getRepository(User).delete(req.params.id);
	return res.send(results);
});

app.get("/users/:id", async function (req: Request, res: Response) {
	const results = await myDataSource.getRepository(User).findOneBy({
		id: Number(req.params.id),
	});
	return res.send(results);
});

app.get("/users", async function (req: Request, res: Response) {
	const users = await myDataSource.getRepository(User).find();
	res.json(users);
});

// start express server
app.listen(3000);

```

자, 위처럼 파일을 작성하고 서버를 돌려보면 아무것도 안 나올 것이다! 왜냐하면 데이터베이스를 만들지 않았기 때문이다.  
튜토리얼 페이지에서는 따로 데이터베이스를 만드는 부분을 생략했는데, 나는 이 부분까지 함께 작성하도록 하겠다.

### 데이터베이스 구성: MySQL2
여기서 필요한 데이터베이스는 `user`라는 테이블로, 컬럼들은 `src/entity/user.entity.ts`의 내용을 토대로 생성할 것이다.  
컬럼은 순서대로

- id: INT, PK
- firstName: CHAR
- lastName: CHAR

이다. 이를 SQL문으로 작성하면 아래와 같다.

```sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    firstName NCHAR(10) NOT NULL,
    lastName NCHAR(2) NOT NULL
);
```
(사실 SQL 안 쓰고 워크벤치에서 GUI 써서 생성해도 되기는 한다)

그리고 데이터를 아래와 같이 넣어주도록 하겠다.

```sql
INSERT INTO user (firstName, lastName)
VALUES ('예진', '나');
INSERT INTO user (firstName, lastName)
VALUES ('코코', '모');
```

이제 `SELECT`문을 이용하여 `user` 테이블에 값이 잘 들어갔는지를 확인하도록 하겠다.

```sql
SELECT * FROM user;
```

![select_result](../../assets/images/page/web/2022-10-17_select_result.png){: width="45%"}

이후 `node src/app.js` 명령어를 터미널에 입력하여 실행하면 터미널에 아래와 같은 메시지가 출력된다.

```bash
~/dev/TypeORM_Tutorial/with_express ❯ node src/app.js

query: SELECT VERSION() AS `version`
query: START TRANSACTION
query: SELECT DATABASE() AS `db_name`
query: SELECT `TABLE_SCHEMA`, `TABLE_NAME` FROM `INFORMATION_SCHEMA`.`TABLES` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'user'
query: 
                SELECT
                    *
                FROM
                    `INFORMATION_SCHEMA`.`COLUMNS`
                WHERE
                    `TABLE_SCHEMA` = 'test'
                    AND
                    `TABLE_NAME` = 'user'
... (중략) ...
query: COMMIT
Data Source has been initialized!
```

`Data Source has been initialized!`라는 문구가 출력되면, 데이터베이스와의 연결이 성공했다는 뜻이다!

### 핵심 함수와 실행 화면 및 생성된 쿼리문
이번에는 각 라우터에 따라 어떤 결과가 나오는지를 확인해보자. 라우터마다 조회, 삽입, 수정, 삭제 동작을 하게 했는데, 
해당 동작에 어떤 함수가 쓰였는지를 적었다. 그리고 각 라우터마다의 실행 화면과 그에 따라 생성된 쿼리문이 터미널에 어떻게 출력되었는지를 정리하였다.

#### `find()`: 한 테이블의 전체 조회 결과 가져오기
- 사용 라우터: `/users`

- 실행 화면  
![users](/assets/images/page/web/2022-10-17_users.png){: width="80%"}

- 생성된 쿼리문
```bash
query: SELECT `User`.`id` AS `User_id`, `User`.`firstName` AS `User_firstName`, `User`.`lastName` AS `User_lastName` FROM `user` `User`
```

#### `findOneBy()`: 한 테이블의 조회 결과 1개 행만 가져오기
- 사용 라우터: `/users/:id`

- 실행 화면  
![users_id](/assets/images/page/web/2022-10-17_users_id.png){: width="45%"}

- 생성된 쿼리문
```bash
query: SELECT `User`.`id` AS `User_id`, `User`.`firstName` AS `User_firstName`, `User`.`lastName` AS `User_lastName` FROM `user` `User` WHERE (`User`.`id` = ?) LIMIT 1 -- PARAMETERS: [2]
```
참고로 `LIMIT 1`이 자동으로 들어간 이유는 해당 라우터 내의 `findOneBy()`함수 때문이다. 해당 함수는 한 개의 결과만 가져오는 역할을 한다(자세한 내용은 공식 문서의 [Query Builder](https://typeorm.io/select-query-builder) 파트를 참고하자).

#### `create()`: 새로운 인스턴스를 생성한다.
- 사용 라우터: `/users/register`

- 실행 화면  
![users_regiser](/assets/images/page/web/2022-10-18_users_register.png){: width="80%"}

- 생성된 쿼리문
```bash
query: START TRANSACTION
query: INSERT INTO `user`(`id`, `firstName`, `lastName`) VALUES (DEFAULT, ?, ?) -- PARAMETERS: ["이름","성"]
query: INSERT INTO `user`(`id`, `firstName`, `lastName`) VALUES (DEFAULT, ?, ?) -- PARAMETERS: ["glish","En"]
query: COMMIT
```

사실 `insert()`를 써서 같은 동작을 하도록 만들 수 있다. 그리고 신기한 점은 그냥 깡으로 insert를 할 줄 알았는데, 트랜잭션 처리를 한다는 점이었다. 그렇다면 rollback 함수도 있으려나 싶어서 찾아봤는데, `beforeTransactionRollback()`, `afterTransactionRollback()` 등의 트랜잭션 관련 콜백 함수를 재정의하여 사용할 수 있었다. 이것도 나중에 잘 사용하면 매우 유용할 것 같다.

#### `merge()`: 여러 엔티티를 하나의 엔티티로 합친다.
- 사용 라우터: `/users/update/:id`

- 실행 화면  
![users_update](/assets/images/page/web/2022-10-18_users_update.png){: width="45%"}

- 생성된 쿼리문
```bash
query: START TRANSACTION
query: UPDATE `user` SET `firstName` = ?, `lastName` = ? WHERE `id` IN (?) -- PARAMETERS: ["Lover","Espresso",1]
query: COMMIT
```

여기서 하나 특이한 점이 있다. 바로 내가 처음 `user` 테이블을 만들 때, 스키마를 정의하는 과정에서 firstName은 10글자, lastName은 2글자로 글자수 제한을 걸어뒀었다. 그런데 어떻게 그보다 더 긴 길이의 데이터가 insert 되었을까? 바로 `app-data-source.ts`에서 지정한 `synchronize: true` 속성 때문이다.  

`synchronize` 옵션은 어플리케이션을 작동할 때마다 데이터베이스 스키마를 자동으로 생성해야 할지를 결정한다. 그래서인지 공식문서에서는 디버그와 개발 중에는 유용하게 쓸 수 있지만, 프로덕션 모드(in production)에서는 사용에 주의를 요한다고 적혀있다. 그 대안으로 CLI와 run schema:sync 커맨드를 쓸 수 있다고 한다.

그리고 데이터베이스를 확인해보니까 `synchronize: true` 속성에 의해 firstName과 lastName의 스키마에서 데이터 타입 부분이 전부 varchar(255)로 바뀌어있었다. 그런데 "/users/register" 에서는 칼같이 insert를 막았다. 아무래도 insert 명령으로는 스키마가 바뀌지 않도록 해놓은 듯 하다.

추가로 `synchronize: false`로 두고 위의 라우터를 실행하면 데이터가 너무 길다는 에러가 뜬다.

#### `delete()`: 주어진 조건에 맞는 엔티티를 삭제한다.
- 사용 라우터: `/users/leave/:id`

- 실행 화면  
![users_delete](/assets/images/page/web/2022-10-18_users_delete.png){: width="45%"}

- 생성된 쿼리문
```bash
query: DELETE FROM `user` WHERE `id` IN (?) -- PARAMETERS: ["2"]
```
