from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Article(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=256)
    description = fields.CharField(max_length=512)

    class PydanticMeta:
        pass


Article_Pydantic = pydantic_model_creator(Article, name="Article")
Article_Pydantic_In = pydantic_model_creator(Article, name="ArticleIn",
                                             exclude_readonly=True)

