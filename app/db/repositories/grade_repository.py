import asyncpg
from fastapi import Depends
import app.core.database as db
from app.db.models.grade_model import AssessmentModel


async def insert_assessment_to_db(conn: asyncpg.Connection, class_id: int, type_name: str, new_assessment:AssessmentModel):
    
    new_assessment_dict =  new_assessment.model_dump()
    values = ", ".join(new_assessment_dict.keys())
    placeholder = ", ".join(f"${i + 1}" for i in range(len(new_assessment_dict)))
    
    query = f"""
        INSERT INTO assessments ({values}) VALUES ({placeholder})    
    """

    return await conn.execute(query, *new_assessment_dict.values())



async def score_trigger(conn: asyncpg.Connection = Depends(db.get_connection)):
    
    function_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_proc WHERE proname = 'insert_default_scores'
        );
    """)
    if not function_exists:
        await conn.execute("""
                CREATE OR REPLACE FUNCTION insert_default_scores()
                RETURNS TRIGGER AS $$
                BEGIN
                    INSERT INTO scores (student_number, grade_id, score)
                    SELECT s.student_number, NEW.grade_id, 0
                    FROM students s
                    WHERE s.class_id = NEW.class_id;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                        
        """)

    trigger_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = 'auto_insert_scores'                                 
        );
    """)


    if not trigger_exists:
        await conn.execute("""
            CREATE TRIGGER auto_insert_scores
            AFTER INSERT ON assessments
            FOR EACH ROW EXECUTE FUNCTION insert_default_scores();
        """)
    await conn.close()
    