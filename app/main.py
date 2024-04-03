from fastapi import FastAPI, Response, status, HTTPException,Depends

from sqlalchemy.orm import Session
from .config import settings

from app import auth
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user,vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
#Hashing user password

app=FastAPI()

origins=[
  "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return{"message":"Welcome to my simple API for social media kind of application"}







# try:
#         conn= psycopg2.connect("host='localhost' dbname='fastapi' user='postgres' password='#botiz'", cursor_factory=RealDictCursor )
#         cursor=conn.cursor()
#         print("Database was connected successfully!")
# except Exception as error:
#         print("Database connection failed")
#         print(error)
  



# def find_post(id):
#     cursor.execute("SELECT * FROM posts WHERE id= %s", (id,))
#     post=cursor.fetchone()
#     return post 

    
           
       
# def find_post_index(id):
#     for i, post in enumerate(my_posts):
#         if post['id']== id:
#             return i
#         else:
#             print("Post not found with ID:", id)
    
      





     



    
        


