from pydantic import BaseModel, Field
from typing import List, Dict

class DBSchema(BaseModel):
    table_name: str = Field(description="Name of the database table (e.g., users, contacts)")
    columns: Dict[str, str] = Field(description="Column names and their data types (e.g., {'id': 'INTEGER', 'email': 'VARCHAR'})")

class APIEndpoint(BaseModel):
    path: str = Field(description="The URL endpoint route (e.g., /api/login, /api/contacts)")
    method: str = Field(description="HTTP Method like GET, POST, PUT, DELETE")
    mapped_db_table: str = Field(description="The exact database table name this endpoint interacts with")

class UIPage(BaseModel):
    page_name: str = Field(description="Name of the UI view (e.g., Login, Dashboard)")
    components: List[str] = Field(description="UI elements present (e.g., text_input, data_table, line_chart)")

class AppBlueprint(BaseModel):
    """The absolute structural contract for the generated application."""
    app_name: str
    target_roles: List[str] = Field(description="User roles like Admin, PremiumUser, Anonymous")
    database_schema: List[DBSchema]
    api_schema: List[APIEndpoint]
    ui_schema: List[UIPage]
    business_logic_rules: List[str] = Field(description="Operational rules like 'Only PremiumUser can access payments'")