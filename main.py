from typing import Union
from fastapi import FastAPI
from controller import Controller
from models import *

app = FastAPI()
controller = Controller()


@app.get("/apply")
def apply(userType: str, price: int):
    applicantItem = ApplicantItem(UserType(userType), price)
    return controller.respond(applicantItem)
