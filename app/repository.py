from .decorators import monitor_db_operation


@monitor_db_operation(operation="insert_device")
async def repo_create_device(conn, query, *args):
    """
    Function to execute a database insert query and return the result row.
    """
    row = await conn.fetchrow(query, *args)
    return row


@monitor_db_operation(operation="select_device")
async def select_create_device(conn, query, *args):
    """
    Function to execute a database insert query and return the result row.
    """
    row = await conn.fetch(query, *args)
    return row
