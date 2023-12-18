# 프로젝트 목표
- 로그인, 로그아웃 기능, 사용자별 ToDo 리스트 CRUD 기능만을 지원하는 API 백엔드 서버를 구축한다.
- FastAPI를 체험한다.
# 사용 Tools
- FastAPI
# 구현 목표
- [x] ToDo 목록 전송
- [x] ToDo 상세 내용 전송
- [x] ToDo 작성 수행
- [x] ToDo 수정 수행
- [x] ToDo 삭제 수행
- [x] 회원 가입 수행
- [x] 로그인 JWT 토큰 전송
- [x] JWT 토큰 검증 (라이브러리)
# 실행방법
- 터미널에서 아래의 명령어 입력
```bash
alembic init migrations
```
- `./alembic.ini` 에서 `sqlalchemy.url`를 아래와 같이 변경
```
sqlalchemy.url = sqlite:///./todo.sqlite
```
- `./migrations/env.py` 에서 아래의 내용 추가
```
import models
```
- `./migrations/env.py` 에서 `target_metadata`를 아래와 같이 변경
```
target_metadata = models.Base.metadata
```
- 터미널에서 아래의 명령어 입력
```bash
alembic revision --autogenerate
alembic upgrade head
```
- 터미널에서 아래의 명령어 입력
```bash
uvicorn main:app --reload
```