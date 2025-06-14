from fastapi import FastAPI


from src.api.router import router as bot_router

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


app.include_router(bot_router)
