from typing import Union

from fastapi import FastAPI

from models.mail import Mail, fetchMails
from mysqldb import SqlConection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/mails")
def RefreshDB_mails():
    sql = SqlConection()
    listMails = fetchMails()
    for mail in listMails:
        sql.insertMail(mail)
    return {""}

@app.get("/mails")
def RefreshDB_mails():
    sql = SqlConection()
    mailsList = sql.listMails()
    return mailsList
