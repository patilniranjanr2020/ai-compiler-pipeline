from pydantic import BaseModel, Field
from typing import List, Dict

class DBSchema(BaseModel):
    table_name: str = Field(description="Database table name (e.g., users, contacts).")
    # Force the model to explain types so columns never map to empty dictionaries
    columns: Dict[str, str] = Field(description="Detailed mapping of column names to database field types, e.g., {'id': 'SERIAL PRIMARY KEY', 'email': 'VARCHAR(255) UNIQUE', 'role': 'VARCHAR(50)'}")

class APIEndpoint(BaseModel):
    path: str = Field(description="The URL endpoint path, e.g., /api/contacts")
    method: str = Field(description="HTTP method, e.g., GET, POST, DELETE")
    mapped_db_table: str = Field(description="The exact database table matching this route data transaction")
    validation_required_fields: List[str] = Field(description="Payload key field attributes mandatory for validation, e.g., ['email', 'password']")

class UIPage(BaseModel):
    page_name: str = Field(description="Name of the presentation interface layout.")
    components: List[str] = Field(description="UI rendering blocks present inside this layout context, e.g., ['LoginForm', 'ContactTableData']")

class AppBlueprint(BaseModel):
    """The strict architecture execution target definition."""
    app_name: str
    target_roles: List[str] = Field(description="Plain list string array containing access roles, e.g., ['Admin', 'User', 'Anonymous']")
    database_schema: List[DBSchema]
    api_schema: List[APIEndpoint]
    ui_schema: List[UIPage]
    business_logic_rules: List[str] = Field(description="Rules for data gating constraints.")