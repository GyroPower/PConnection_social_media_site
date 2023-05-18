import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.base import api_route as api
from app.web_apps.base import api_router

# we need RealDictCursor just to give us the name of the columns when we make a sql query
# without it that just give us the values but not the columns where that belong
# this class make what we recived in a python dictionary wit key-value pair

# if we want to give a user feedback of an error we use a http status code
# to use that in a simple way we use Response class from fastapi package

# Other way to raise an http status code we can use httpexception, to make it simpler

"""class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
"""


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/media", StaticFiles(directory="media/"), name="media")

if not os.path.exists("media/"):
    os.mkdir("media/")

# this function what makes it's to get a session to our database, and the session
# object it's responsable to comunicate with our database
# every time we send a request we will get a session, and when we make our sql commands we
# close the session
# every time we make a request to our endpoints we will make a session and then close then
# when we finish


"""while True:

    try:
        conn = psycopg2.connect(dbname='FastAPI',password="16062016JustifyMy",
        user="postgres",host='localhost',cursor_factory=RealDictCursor,port=5432)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("error")
        print(error)
        time.sleep(2)
"""

"""@app.get("/main/{model_name}")
async def root(model_name:ModelName):
    #comparing if the model name is equal to the content of alexnet attribute
    if model_name is ModelName.alexnet:
        return {"Model name" : model_name,"message": "Deep Learning FTW!"}

    if model_name.value == "resnet":
        return {"Model name" : model_name,"message": "LeCNN all the images"}

    return {"Model name" : model_name, "message": "Have some residuals"}
"""
