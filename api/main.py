from typing import List

from fastapi import FastAPI, HTTPException, status
from .models import Article, Article_Pydantic, Article_Pydantic_In
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

class Status(BaseModel):
    message:str

app = FastAPI()

@app.get("/articles", response_model=List[Article_Pydantic])
async def get_articles():
    return await Article_Pydantic.from_queryset(
        Article.all()
    )

@app.get("/articles/{id}", response_model=Article_Pydantic, responses={
    404: {"model": HTTPNotFoundError}
})
async def get_article_detail(id:int):
    return await Article_Pydantic.from_queryset_single(
        Article.get(id=id)
    )

@app.put("/articles/{id}", response_model=Article_Pydantic, responses={
    404: {"model": HTTPNotFoundError}
})
async def update_article(id:int, body:Article_Pydantic_In):
    await Article.filter(id=id).update(**body.dict(exclude_unset=True))
    return await Article_Pydantic.from_queryset_single(
        Article.get(id=id)
    )

@app.post("/articles", response_model=Article_Pydantic)
async def insert_article(body:Article_Pydantic_In):
    article_obj = await Article.create(**body.dict(exclude_unset=True))
    return await Article_Pydantic.from_tortoise_orm(article_obj)


@app.delete("/articles/{id}", response_model=Status, responses={
    404: {"model": HTTPNotFoundError}
})
async def delete_article(id:int):
    article = await Article.filter(id=id).delete()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User id not found.")
    return Status(message="Article was deleted.")


register_tortoise(app,
                  db_url="postgres://developer:secret@localhost:5432"
                         "/tortoise",
                  modules={'models': ['api.models']},
                  generate_schemas=True,
                  add_exception_handlers=True
                  )