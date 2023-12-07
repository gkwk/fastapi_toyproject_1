from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from domain.todo import todo_route

# uvicorn main:{변수명} --reload ex) uvicorn main:app --reload
app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(todo_route.router)