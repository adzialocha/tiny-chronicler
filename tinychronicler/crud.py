from sqlalchemy import delete, insert, select, update

from . import models, schemas
from .database import database


async def create_chronicle(chronicle: schemas.ChronicleIn):
    query = insert(models.Chronicle).values(
        title=chronicle.title, description=chronicle.description
    )
    return await database.execute(query)


async def get_chronicle(chronicle_id: int):
    query = select([models.Chronicle]).where(
        models.Chronicle.id == chronicle_id
    )
    return await database.fetch_one(query)


async def get_chronicles():
    query = select([models.Chronicle])
    return await database.fetch_all(query)


async def update_chronicle(chronicle_id: int, chronicle: schemas.ChronicleIn):
    query = (
        update(models.Chronicle)
        .where(models.Chronicle.id == chronicle_id)
        .values(title=chronicle.title, description=chronicle.description)
    )
    return await database.execute(query)


async def delete_chronicle(chronicle_id: int):
    query = delete(models.Chronicle).where(models.Chronicle.id == chronicle_id)
    return await database.execute(query)


async def create_file(file: schemas.FileIn):
    query = insert(models.File).values(
        name=file.name,
        path=file.path,
        mime=file.mime,
        thumb_name=file.thumb_name,
        thumb_path=file.thumb_path,
    )
    return await database.execute(query)
