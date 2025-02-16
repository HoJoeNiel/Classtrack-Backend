
# This file contains various resuable sql query functions for Class entity.

import asyncpg


async def get_classes_from_db(conn: asyncpg.Connection):
    """Returns a list of classes from the database."""

    # Query from the database
    classes = conn.fetch("SELECT * FROM class")