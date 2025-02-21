
# This file contains various resuable sql query functions for Class entity.

import asyncpg

from app.db.models.class_model import ClassModel


async def get_classes_from_db(conn: asyncpg.Connection):
    """Returns a list of classes from the database."""

    # Query from the database
    return await conn.fetch("SELECT * FROM classes;")

async def get_class_from_db(conn: asyncpg.Connection, class_id: int):
    """Returns class data from db given class_id."""

    return await conn.fetchrow("SELECT * FROM classes WHERE class_id = $1", class_id)

async def insert_class_into_db(conn: asyncpg.Connection, new_class: ClassModel):
    """Inserts the a class into db and returns the class_id."""

    new_class_dict = new_class.model_dump()
    
    values = ", ".join(new_class_dict.keys())
    placeholders = ", ".join(f"${i + 1}" for i in range(len(new_class_dict)))

    query = f"""
            INSERT INTO classes ({values}) VALUES ({placeholders}) RETURNING class_id;
            """
    

    return await conn.fetchval(query, *new_class_dict.values())

async def delete_class_from_db(conn: asyncpg.Connection, class_id: int):
    """Deletes a class from db given class_id."""

    await conn.execute("DELETE FROM classes WHERE class_id= $1;", class_id)


async def get_students_from_classes_table(conn: asyncpg.Connection, class_id:int):

    return await conn.fetch("SELECT * FROM students WHERE class_id = $1;", class_id)