
# This file contains various resuable sql query functions for Class entity.

import asyncpg

from app.db.models.class_model import ClassModel, Students


async def get_classes_from_db(conn: asyncpg.Connection, prof_id: str):

    """Returns a list of classes from the database."""

    # Query from the database
    return await conn.fetch("SELECT * FROM classes WHERE prof_id = $1;", prof_id)

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
    """ Get class according to the given class_id """

    return await conn.fetch("SELECT * FROM students WHERE class_id = $1;", class_id)

async def insert_student_to_db(model: Students, conn: asyncpg.Connection, class_id:int):
    """ Insert Students to class according to class_id"""

    #Converts the pydantics model to dictionary
    new_student_dict = model.model_dump()

    #Makes each column comma seperated
    values = ", ".join(new_student_dict.keys())

    #iterates the placeholder to make it ($1, $2),
    placeholders = ", ".join(f"${i + 1}" for i in range(len(new_student_dict)))

    
    query = f"""
            INSERT INTO students ({values}) VALUES ({placeholders});
            """

    return await conn.execute(query, *new_student_dict.values())

async def delete_student_to_db(conn: asyncpg.Connection, class_id: int, student_number: int):
    return await conn.execute("DELETE FROM students WHERE student_number = $1 AND class_id: $2;",student_number, class_id)
