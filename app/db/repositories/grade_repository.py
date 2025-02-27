

import asyncpg
from app.db.models.grade_model import GradeType
from app.db.repositories.utils import generate_insert_query


async def get_grade_types_from_db(class_id: int, conn: asyncpg.Connection):
    """Fetches all grade_types of a class from db given its id."""

    res = await conn.fetch("SELECT * FROM grade_types WHERE class_id = $1", class_id)
    return res

async def get_assessments(class_id: int, type_name: str, conn: asyncpg.Connection):
    """Fetches all assessments of type type_name in a class given its id."""

    # Try to get grade type id
    res = await get_grade_type_id(class_id, type_name, conn)

    if not res:
        return None

    id = dict(res)["grade_type_id"] 
    assessments = await conn.fetch("SELECT * FROM assessments WHERE class_id = $1 AND grade_type_id = $2", class_id, id)
    
    return assessments
    
    
async def get_grade_type_id(class_id: int, type_name: str, conn: asyncpg.Connection):
    """Fetches the id of a grade type from a class."""

    id = await conn.fetchrow("SELECT grade_type_id FROM grade_types WHERE LOWER(type_name) = LOWER($1) AND class_id = $2;", type_name, class_id)
    return id

async def insertDB_grade_type(grade_type: GradeType, conn):
    """Inserts a grade type in the db. The class_id is included in the request body."""

    grade_type_dict = grade_type.model_dump()

    query = generate_insert_query(grade_type_dict, "grade_types", "grade_type_id")

    return await conn.fetchrow(query, *grade_type_dict.values())

async def deleteDB_grade_type(class_id: int, type_id: int, conn: asyncpg.Connection):
    """Deletes a grade type given its id on a class."""
    return await conn.fetchval("DELETE FROM grade_types WHERE class_id = $1 AND grade_type_id = $2 RETURNING grade_type_id", class_id, type_id)