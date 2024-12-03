from fastapi import FastAPI   , APIRouter
from .routes import posts , users , login , votes

app = FastAPI()

@app.get("/")
def root():
    return { "message" : "working" }

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(votes.router)