
def generate_insert_query(obj_dict: dict, table_name: str, returning: str = '*'):
    """
    Helper func to generate insert query dynamically

    Args:
        obj : the pydantic object to insert e.g. GradeType, ClassModel, etc.
        table_name (str): Table name to insert into. 
        returning (str, optional): Return value of insert query. Defaults to '*'.
    """
 
    values = ", ".join(obj_dict.keys())
    placeholders = ", ".join(f"${i + 1}" for i in range(len(obj_dict)))

    return f"INSERT INTO {table_name} ({values}) VALUES ({placeholders}) returning {returning};"