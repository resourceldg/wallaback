from fastapi import FastAPI
from routes.user import user

app =  FastAPI(
    title="Walatic Backend",
    description='This is where everything happens...',
    version="0.0.1",
    #terms_of_service="http://example.com/terms/",
    contact={
        "name": "Resourceldg",
        "url": "http://walatic.com",
        "email": "resourceld@gmail.com",
    
    },
    tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },]
    
)
app.include_router(user)