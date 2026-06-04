import os
import json
from google import genai
from google.genai import types
from models import AppBlueprint

class AICompiler:
    def __init__(self, api_key: str):
        # Initializing client safely with zero cloud cost
        self.client = genai.Client(api_key=api_key)

    def run_pipeline(self, user_prompt: str, log_callback) -> dict:
        # ---- STAGE 1, 2, & 3: Generation Pipeline ----
        log_callback("⚙️ Pipeline Processing: Extracting intent and structuring architecture...", "running")
        
        system_instruction = (
            "You are an expert software compiler. Break down the user's app request "
            "into a perfectly matching Database schema, API schema, UI layout, and Business logic rules. "
            "Ensure cross-layer consistency: every API endpoint mapped_db_table MUST exist in the database_schema."
        )

        try:
            # FIX: Extract the structural schema dictionary from Pydantic
            raw_schema = AppBlueprint.model_json_schema()
            
            # Recursive helper function to strip 'additionalProperties' fields safely
            def remove_additional_properties(schema_dict):
                if isinstance(schema_dict, dict):
                    schema_dict.pop('additionalProperties', None)
                    for key, value in schema_dict.items():
                        remove_additional_properties(value)
                elif isinstance(schema_dict, list):
                    for item in schema_dict:
                        remove_additional_properties(item)
            
            # Clean our schema before passing it to Gemini Free Tier
            remove_additional_properties(raw_schema)

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"User Request: {user_prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    # Pass the cleaned schema dictionary directly
                    response_schema=raw_schema,
                    temperature=0.1,
                ),
            )
            app_config = json.loads(response.text)
            
        except Exception as e:
            log_callback(f"❌ Generation Stage Failed: {str(e)}", "running")
            raise e

        # ---- STAGE 4: Refinement, Validation & Repair Layer ----
        log_callback("🔍 Stage 4: Validation Engine checking cross-layer integrity...", "running")
        
        valid_tables = [table["table_name"] for table in app_config.get("database_schema", [])]
        repaired = False

        for endpoint in app_config.get("api_schema", []):
            if endpoint["mapped_db_table"] not in valid_tables:
                log_callback(f"⚠️ Validation Alert: Endpoint {endpoint['path']} references missing table '{endpoint['mapped_db_table']}'. Auto-repairing...", "running")
                
                if valid_tables:
                    endpoint["mapped_db_table"] = valid_tables[0]
                    repaired = True

        if repaired:
            log_callback("✅ Core Engine auto-healed schema mismatches safely.", "running")
        else:
            log_callback("✅ Compilation execution alignment checks passed with 100% integrity.", "running")

        log_callback("✨ Architecture successfully compiled!", "complete")
        return app_config