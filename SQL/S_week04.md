# SQL_ADVANCED 4주차 정규 과제 

📌SQL_ADVANCED 정규과제는 매주 정해진 분량의 『*혼자 공부하는 SQL*』 을 읽고 학습하는 것입니다. 이번주는 아래의 **SQL_ADVANCED_4th_TIL**에 나열된 분량을 읽고 공부하시면 됩니다.

아래의 문제를 풀어보며 학습 내용을 점검하세요. 문제를 해결하는 과정에서 개념을 스스로 정리하고, 필요한 경우 제시된 강의를 참고하여 보완하는 것이 좋습니다.

<!-- 강의 링크는 아래와 같습니다.
https://www.youtube.com/watch?v=DMNpkj_bZIs&list=PLVsNizTWUw7GCfy5RH27cQL5MeKYnl8Pm&index=13
https://www.youtube.com/watch?v=BUHj-behLyc&list=PLVsNizTWUw7GCfy5RH27cQL5MeKYnl8Pm&index=14
https://www.youtube.com/watch?v=JrXWxku7ZIM&list=PLVsNizTWUw7GCfy5RH27cQL5MeKYnl8Pm&index=15
-->

**교재 실습 예제 파일은 08_SQL_ADVANCED_Template 레포지토리의 src 폴더에 업로드되어 있습니다. market_db 파일도 해당 폴더에 함께 포함되어 있으니 참고하시기 바랍니다.**

**👀(수행 인증샷은 필수입니다.)** 

## SQL_ADVANCED_4th_TIL

### 5장 테이블과 뷰
#### 01. 테이블 만들기
#### 02. 제약조건으로 테이블을 견고하게
#### 03. SQL 가상의 테이블: 뷰 


## Study Schedule

| 주차  | 공부 범위     | 완료 여부 |
| ----- | ------------- | --------- |
| 1주차 | p.24~99    | ✅         |
| 2주차 | p.102~155   | ✅         |
| 3주차 | p.158~213  | ✅         |
| 4주차 | p.216~271 | ✅         |
| 5주차 | p.274~327 | 🍽️         |
| 6주차 | p.330~369 | 🍽️         |
| 7주차 | p.372~407 | 🍽️         |


<br>

<!-- 여기까진 그대로 둬 주세요-->

---

# 1️⃣ 학습 내용 정리

## 1. 테이블 만들기 

````markdown
## 1. 테이블 만들기

### 테이블 기본 개념

* **테이블(Table)**: 데이터를 표 형태로 저장하는 구조
* **행(Row)**: 하나의 데이터 → **레코드(Record)**
* **열(Column)**: 데이터의 속성 → **필드(Field)**
* MySQL에서는 GUI와 SQL 모두 테이블 생성 가능하며, 실무에서는 **SQL 방식**을 많이 사용

---

### 데이터베이스 생성

```sql
CREATE DATABASE naver_db;
USE naver_db;
````

* **`CREATE DATABASE`**: 데이터베이스 생성
* **`USE`**: 사용할 데이터베이스 선택

```sql
DROP DATABASE IF EXISTS naver_db;
```

* **`IF EXISTS`**: 데이터베이스가 존재할 경우에만 삭제

---

### CREATE TABLE

* **`CREATE TABLE`**: 새로운 테이블 생성
* 테이블 생성 시 **열 이름 + 데이터 형식 + 제약조건** 지정

```sql
CREATE TABLE 테이블명 (
    열이름 데이터형식 제약조건,
    ...
);
```

---

### NULL / NOT NULL

* **`NULL`**: 값이 없어도 허용
* **`NOT NULL`**: 반드시 값을 입력해야 함

```sql
mem_name VARCHAR(10) NOT NULL,
phone1 CHAR(3) NULL
```

---

### PRIMARY KEY

* **`PRIMARY KEY`**: 각 행을 구분하는 **기본 키**
* 값이 **중복될 수 없고 NULL도 사용할 수 없음**

```sql
mem_id CHAR(8) NOT NULL PRIMARY KEY
```

---

### AUTO_INCREMENT

* **`AUTO_INCREMENT`**: 숫자를 1부터 자동으로 증가시켜 입력
* 주로 기본 키와 함께 사용

```sql
num INT AUTO_INCREMENT NOT NULL PRIMARY KEY
```

---

### FOREIGN KEY

* **`FOREIGN KEY`**: 다른 테이블의 기본 키를 참조하는 **외래 키**
* 두 테이블 사이의 관계를 연결할 때 사용
* 참조하는 테이블에 존재하지 않는 값은 입력할 수 없음

```sql
FOREIGN KEY(mem_id) REFERENCES member(mem_id)
```

**관계**

`member.mem_id (PK)` → `buy.mem_id (FK)`

---

### UNSIGNED

* **`UNSIGNED`**: 음수를 제외하고 **0 이상의 값만 저장**

```sql
price INT UNSIGNED,
amount SMALLINT UNSIGNED
```

---

### 회원 테이블 생성

```sql
DROP TABLE IF EXISTS member;

CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    mem_number TINYINT NOT NULL,
    addr CHAR(2) NOT NULL,
    phone1 CHAR(3) NULL,
    phone2 CHAR(8) NULL,
    height TINYINT UNSIGNED NULL,
    debut_date DATE NULL
);
```

---

### 구매 테이블 생성

```sql
DROP TABLE IF EXISTS buy;

CREATE TABLE buy (
    num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    mem_id CHAR(8) NOT NULL,
    prod_name CHAR(6) NOT NULL,
    group_name CHAR(4) NULL,
    price INT UNSIGNED NOT NULL,
    amount SMALLINT UNSIGNED NOT NULL,
    FOREIGN KEY(mem_id) REFERENCES member(mem_id)
);
```

---

### 핵심 정리

* **`CREATE TABLE`**: 테이블 생성
* **`NOT NULL`**: 빈 값 허용 X
* **`PRIMARY KEY`**: 행을 구분하는 기본 키
* **`AUTO_INCREMENT`**: 번호 자동 증가
* **`FOREIGN KEY`**: 다른 테이블의 기본 키 참조
* **`UNSIGNED`**: 음수 사용 X




## 2. 제약조건으로 테이블을 견고하게 

### 제약조건

* **제약조건(Constraint)**: 데이터의 무결성을 지키기 위해 데이터를 제한하는 조건
* 대표적인 제약조건
  * `PRIMARY KEY`
  * `FOREIGN KEY`
  * `UNIQUE`
  * `CHECK`
  * `DEFAULT`
  * `NULL / NOT NULL`

---

### 기본 키 제약조건 (PRIMARY KEY)

* **`PRIMARY KEY`**: 각 행을 구분하는 기본 키
* 값이 **중복될 수 없고 `NULL`도 허용하지 않음**
* 한 테이블에 **1개만 지정 가능**

```sql
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL
);
````

* 테이블 마지막에 따로 지정하는 것도 가능

```sql
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL,
    PRIMARY KEY (mem_id)
);
```

---

### ALTER TABLE로 기본 키 추가

* **`ALTER TABLE`**: 이미 만들어진 테이블의 구조를 변경

```sql
ALTER TABLE member
    ADD CONSTRAINT
    PRIMARY KEY (mem_id);
```

---

### 외래 키 제약조건 (FOREIGN KEY)

* **`FOREIGN KEY`**: 두 테이블 사이의 관계를 연결하는 외래 키
* 외래 키가 있는 테이블 → **참조 테이블**
* 외래 키가 참조하는 테이블 → **기준 테이블**
* 외래 키 값은 기준 테이블의 **기본 키 또는 고유 키에 존재하는 값**이어야 함

```sql
FOREIGN KEY(mem_id) REFERENCES member(mem_id)
```

* `buy.mem_id` → `member.mem_id` 참조

```sql
CREATE TABLE buy (
    num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    mem_id CHAR(8) NOT NULL,
    prod_name CHAR(6) NOT NULL,
    FOREIGN KEY(mem_id) REFERENCES member(mem_id)
);
```

---

### ALTER TABLE로 외래 키 추가

```sql
ALTER TABLE buy
    ADD CONSTRAINT
    FOREIGN KEY(mem_id)
    REFERENCES member(mem_id);
```

---

### 외래 키와 데이터 변경

* 참조 중인 기본 키는 마음대로 **수정하거나 삭제할 수 없음**
* 기준 테이블의 값을 변경하면 참조 관계 때문에 오류 발생 가능

```sql
UPDATE member
SET mem_id = 'PINK'
WHERE mem_id = 'BLK';
```

---

### ON UPDATE CASCADE / ON DELETE CASCADE

* **`ON UPDATE CASCADE`**: 기준 테이블의 값이 변경되면 참조 테이블의 값도 자동 변경
* **`ON DELETE CASCADE`**: 기준 테이블의 행이 삭제되면 관련된 참조 테이블의 행도 자동 삭제

```sql
ALTER TABLE buy
    ADD CONSTRAINT
    FOREIGN KEY(mem_id) REFERENCES member(mem_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

---

### 고유 키 제약조건 (UNIQUE)

* **`UNIQUE`**: 중복되지 않는 유일한 값을 저장
* `PRIMARY KEY`와 달리 **NULL 허용 가능**
* 한 테이블에 여러 개 설정 가능

```sql
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL,
    email CHAR(30) NULL UNIQUE
);
```

---

### 체크 제약조건 (CHECK)

* **`CHECK`**: 입력되는 값이 지정한 조건을 만족하는지 검사

```sql
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL CHECK (height >= 100)
);
```

* 여러 값 중 하나만 입력하도록 제한 가능

```sql
ALTER TABLE member
    ADD CONSTRAINT
    CHECK (phone1 IN ('02', '031', '032', '054', '055', '061'));
```

---

### 기본값 정의 (DEFAULT)

* **`DEFAULT`**: 값을 입력하지 않았을 때 자동으로 입력되는 기본값

```sql
CREATE TABLE member (
    mem_id CHAR(8) NOT NULL PRIMARY KEY,
    mem_name VARCHAR(10) NOT NULL,
    height TINYINT UNSIGNED NULL DEFAULT 160,
    phone1 CHAR(3) NULL
);
```

* 기존 열에 기본값 설정

```sql
ALTER TABLE member
    ALTER COLUMN phone1 SET DEFAULT '02';
```

* 기본값을 사용하려면 `DEFAULT` 입력

```sql
INSERT INTO member
VALUES ('SPC', '우주소녀', DEFAULT, DEFAULT);
```

---

### NULL / NOT NULL

* **`NULL`**: 값이 없어도 됨
* **`NOT NULL`**: 반드시 값을 입력해야 함
* `PRIMARY KEY`로 지정된 열은 자동으로 `NOT NULL`

```
```


> **확인문제: 다음 보기 중에서 각 문항이 설명하는 것을 고르세요.**

보기는 아래와 같습니다.
```
CHECK / DEFAULT / PRIMAY KEY / UNIQUE / NOT NULL / FOREIGN KEY
```

```
여기에 답과 그 이유를 적어주세요!
1. 입력되는 데이터가 조건에 맞는지 검사하는 기능:
2. 값을 입력하지 않으면 자동으로 들어갈 값:
3. 빈 값을 입력하는 것을 허용하지 않음: 
```


## 3. 가상의 테이블: 뷰 

````markdown
## 3. 가상의 테이블: 뷰

### 뷰(View)

* **뷰(View)**: 실제 데이터를 저장하지 않고, `SELECT` 문의 결과를 테이블처럼 사용하는 **가상의 테이블**
* 실제 데이터는 원본 테이블에 존재
* 뷰에 접근하면 내부의 `SELECT` 문이 실행되어 결과를 보여줌
* 일반 테이블처럼 `SELECT`, `WHERE` 등을 사용할 수 있음

---

### 뷰 생성

* **`CREATE VIEW`**: 새로운 뷰 생성

```sql
CREATE VIEW 뷰_이름
AS
    SELECT 문;
````

```sql
CREATE VIEW v_member
AS
    SELECT mem_id, mem_name, addr
    FROM member;
```

* 생성한 뷰는 일반 테이블처럼 조회

```sql
SELECT * FROM v_member;
```

---

### 뷰에서 조건 사용

```sql
SELECT mem_name, addr
FROM v_member
WHERE addr IN ('서울', '경기');
```

* 뷰에서도 `WHERE` 등 일반적인 조회 기능 사용 가능

---

### 뷰를 사용하는 이유

* **보안(Security)**: 필요한 열만 보여주어 중요한 데이터 접근 제한
* **복잡한 SQL 단순화**: 복잡한 쿼리를 뷰로 만들어 간단하게 재사용

```sql
CREATE VIEW v_memberbuy
AS
    SELECT B.mem_id, M.mem_name, B.prod_name, M.addr,
           CONCAT(M.phone1, M.phone2) AS '연락처'
    FROM buy B
        INNER JOIN member M
        ON B.mem_id = M.mem_id;
```

```sql
SELECT *
FROM v_memberbuy
WHERE mem_name = '블랙핑크';
```

---

### 뷰의 열 이름 지정

* 뷰 생성 시 **별칭(`AS`)**을 사용하여 열 이름 변경 가능
* 열 이름에 공백이 있으면 **백틱(``)** 사용

```sql
CREATE VIEW v_viewtest1
AS
    SELECT B.mem_id AS `Member ID`,
           M.mem_name AS `Member Name`,
           B.prod_name AS `Product Name`
    FROM buy B
        INNER JOIN member M
        ON B.mem_id = M.mem_id;
```

---

### 뷰 수정

* **`ALTER VIEW`**: 기존 뷰 수정

```sql
ALTER VIEW v_viewtest1
AS
    SELECT B.mem_id AS `회원 아이디`,
           M.mem_name AS `회원 이름`,
           B.prod_name AS `제품 이름`
    FROM buy B
        INNER JOIN member M
        ON B.mem_id = M.mem_id;
```

---

### 뷰 삭제

* **`DROP VIEW`**: 뷰 삭제

```sql
DROP VIEW v_viewtest1;
```

---

### CREATE OR REPLACE VIEW

* **`CREATE OR REPLACE VIEW`**: 뷰가 없으면 생성, 있으면 기존 뷰를 덮어씀

```sql
CREATE OR REPLACE VIEW v_viewtest2
AS
    SELECT mem_id, mem_name, addr
    FROM member;
```

---

### 뷰 정보 확인

* **`DESCRIBE`**: 뷰의 열 구조 확인

```sql
DESCRIBE v_viewtest2;
```

* **`SHOW CREATE VIEW`**: 뷰를 생성한 SQL 확인

```sql
SHOW CREATE VIEW v_viewtest2;
```

---

### 뷰를 통한 데이터 수정

* 뷰를 통해 원본 테이블의 데이터를 수정할 수 있음

```sql
UPDATE v_member
SET addr = '부산'
WHERE mem_id = 'BLK';
```

* 단, 뷰의 구조에 따라 **INSERT / UPDATE / DELETE가 제한될 수 있음**
* 뷰에 없는 필수 열이 `NOT NULL`이면 데이터 입력 시 오류 발생 가능

---

### WITH CHECK OPTION

* **`WITH CHECK OPTION`**: 뷰에 설정된 조건에 맞는 데이터만 입력·수정 가능

```sql
CREATE VIEW v_height167
AS
    SELECT *
    FROM member
    WHERE height >= 167
    WITH CHECK OPTION;
```

* `height < 167`인 데이터 입력 → 오류
* 뷰의 조건을 벗어나는 데이터 입력 방지

---

### 뷰와 원본 테이블

* 뷰는 실제 데이터를 가지고 있지 않으므로 **원본 테이블에 의존**
* 원본 테이블이 삭제되면 해당 뷰를 정상적으로 사용할 수 없음

```sql
CHECK TABLE v_height167;
```

* **`CHECK TABLE`**: 뷰가 정상적으로 사용 가능한지 확인

---

### 핵심 정리

* **`CREATE VIEW`**: 뷰 생성
* **`ALTER VIEW`**: 뷰 수정
* **`DROP VIEW`**: 뷰 삭제
* **`CREATE OR REPLACE VIEW`**: 뷰 생성 또는 교체
* **`DESCRIBE`**: 뷰 구조 확인
* **`SHOW CREATE VIEW`**: 뷰 생성 SQL 확인
* **`WITH CHECK OPTION`**: 뷰 조건에 맞는 데이터만 입력·수정
* **`CHECK TABLE`**: 뷰 상태 확인

```
```


> **확인문제: 다음은 뷰의 특징입니다. 거리가 먼 것을 하나 고르세요.**

보기는 아래와 같습니다.
```
1️⃣ 뷰에는 테이블의 모든 열을 포함시켜야 합니다.
2️⃣ 뷰는 복잡한 SQL을 단순하게 만드는 효과가 있습니다.
3️⃣ 뷰는 보안에 도움이 됩니다.
4️⃣ 일부 사용자가 테이블에는 접근하지 못하게 하고, 뷰에만 접근하도록 설정할 수 있습니다.
```

```
여기에 답과 그 이유를 적어주세요!
```


---

# 2️⃣ 실습과제

## 1. 데이터베이스 구축

아래 코드를 MySQL Workbench에 붙여넣은 후,  
**전체 드래그 → 실행 (Ctrl + Shift + Enter)** 하여 데이터베이스를 생성하세요.

```sql
CREATE DATABASE IF NOT EXISTS week4_db;
USE week4_db;
```

## 2. 실습문제

1. 다음 조건을 만족하는 `users` 테이블을 생성하시오.
```
- user_id는 INT이며 **기본키(Primary Key)**로 설정합니다.
- name은 VARCHAR(20)이며 NULL을 허용하지 않습니다.
- email은 VARCHAR(50)이며 중복을 허용하지 않습니다.
- signup_date는 DATE 타입으로 설정합니다.
- grade는 INT이며 기본값(Default)을 1로 설정합니다.
```

2. 다음 조건을 만족하는 `orders` 테이블을 생성하시오.
```
- order_id는 INT이며 기본키(Primary Key)로 설정합니다.
- user_id는 INT이며 NULL을 허용하지 않습니다.
- amount는 INT이며 0보다 커야 합니다.
- order_date는 DATE 타입으로 설정합니다.
```

3. 다음 조건을 만족하여 데이터를 삽입하시오.
```
- users 테이블에 3명 이상의 데이터를 직접 INSERT 하시오. (단, user 중 본인이 포함돼야 함)
- orders 테이블에 3건 이상의 데이터를 직접 INSERT 하시오.
```

4. users와 orders 테이블을 활용하여 다음 컬럼을 보여주는 뷰 user_order_view를 생성하시오.
```
- user_id
- name
- amount
```

5. 생성한 user_order_view를 조회하시오.

## 3. 제출 방법

1. 각 문제의 실행 결과가 보이도록 화면을 캡처합니다.
2. 테이블 생성 결과, 데이터 삽입 결과, 뷰 생성 및 조회 결과가 모두 보이도록 제출합니다.

<!-- 이 부분을 지우고 인증사진을 제출해주세요.-->

### 🎉 수고하셨습니다.






