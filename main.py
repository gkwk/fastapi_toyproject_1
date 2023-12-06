from fastapi import FastAPI

# uvicorn main:{변수명} --reload ex) uvicorn main:app --reload
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}