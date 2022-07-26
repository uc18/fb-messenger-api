from fastapi import FastAPI

from routes import login, logout, contacts

app = FastAPI()

app.include_router(login.router)
app.include_router(logout.router)
app.include_router(contacts.router)
