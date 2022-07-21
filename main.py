from fastapi import FastAPI

from routes import login, contacts

app = FastAPI()

app.include_router(login.router)
app.include_router(contacts.router)