import asyncpg
from fastapi import Depends, HTTPException
import app.core.database as db
from app.db.models.grade_model import AssessmentModel, ScoreList


async def insert_assessment_to_db(conn: asyncpg.Connection, class_id: int, type_name: str, new_assessment:AssessmentModel):
    
    new_assessment_dict =  new_assessment.model_dump()

    grade_type_id_record = await conn.fetchrow("SELECT grade_type_id FROM grade_types WHERE type_name = $1", type_name )

    grade_type_id = grade_type_id_record["grade_type_id"] if grade_type_id_record else None 
    
    query = f""" 
        INSERT INTO assessments (class_id, grade_type_id, assessment_name)
        VALUES ($1, $2, $3)
    """    
    print(new_assessment_dict['assessment_name'])

    return await conn.execute(query, class_id, grade_type_id, new_assessment_dict['assessment_name'])



async def score_trigger(conn: asyncpg.Connection = Depends(db.get_connection)):
    """ this trigger the score of each student to default(0) every time professors create new assessment."""
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
                    INSERT INTO scores (student_number, assessment_id, score)
                    SELECT s.student_number, NEW.assessment_id, 0
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
    # await conn.close()

async def student_score_trigger(conn: asyncpg.Connection = Depends(db.get_connection)):
    
    function_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_proc WHERE proname = 'add_default_scores'                          
        );
    """)
                                        
    
    if not function_exists:
        await conn.execute(
            """
                CREATE OR REPLACE FUNCTION add_default_scores()
                RETURNS TRIGGER
                LANGUAGE plpgsql
                AS $$   
                BEGIN 
                    INSERT INTO scores (student_number, assessment_id, score)
                    SELECT NEW.student_number, a.assessment_id, 0
                    FROM assessments a
                    WHERE a.class_id = NEW.class_id;
                    RETURN NEW;
                END;
                $$;
            """
        )


    trigger_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = 'auto_add_scores'                          
        ); 
    """)

    if not trigger_exists:
        await conn.execute("""
                DROP TRIGGER IF EXISTS auto_add_scores ON students CASCADE;           
                
                CREATE TRIGGER auto_add_scores
                AFTER INSERT ON students
                FOR EACH ROW EXECUTE FUNCTION add_default_scores()
            """)
    

    
async def delete_assessment_to_db(class_id: int, grade_type_id: int, assessment_id, conn: asyncpg.Connection):

    query = """
        DELETE FROM assessments WHERE class_id = $1 AND grade_type_id = $2 AND assessment_id = $3 RETURNING assessment_id 
    """

    return await conn.fetchval(query, class_id, grade_type_id, assessment_id)

async def get_scores_from_db(class_id: int, grade_type_id: int, conn: asyncpg.Connection):

    assessment_id_record = await conn.fetch("SELECT assessment_id FROM assessments WHERE class_id = $1 AND grade_type_id = $2", class_id, grade_type_id)

    # assessment_id = [for assessment_id_record["assessment_id"] if assessment_id_record else None]
    assessment_id =  [record["assessment_id"] for record in assessment_id_record]
    query = """
        SELECT * FROM scores WHERE assessment_id = ANY($1)
        """
    # print(assessment_id)
    # return assessment_id
    return await conn.fetch(query, assessment_id)

async def update_scores_to_db(class_id: int, model:ScoreList, conn: asyncpg.Connection):
    query = """
        UPDATE scores
        SET score = $1
        WHERE student_number = $2 
        AND assessment_id = $3
        AND assessment_id IN (SELECT assessment_id FROM assessments WHERE class_id = $4)
    """


    try:
        async with conn.transaction():
            for score in model.scores:
                await conn.execute(query, score.score, score.student_number, score.assessment_id, class_id)

        return {'message': 'Scores successfully updated.'}
    except Exception as e:
        raise HTTPException(500, str(e))