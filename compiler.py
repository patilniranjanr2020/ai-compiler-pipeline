import os
import json
import time
from google import genai
from google.genai import types
from models import AppBlueprint

class AICompiler:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def run_pipeline(self, user_prompt: str, log_callback) -> tuple:
        start_time = time.time()
        metrics = {"latency_stages": {}, "retries": 0, "healed_issues": []}
        
        # ---- STAGE 1, 2, & 3: Compilation and Formatting Generation ----
        stage_start = time.time()
        log_callback("⚙️ Pipeline Status: Initializing Intent Extraction and Structural System Architecture design...", "running")
        
        # Explicit instructions to stop JSON array numerical key string corruption
        system_instruction = (
            "You are a production-grade software compiler tool. Convert user prompts into an explicit system blueprint.\n"
            "CRITICAL REQUIREMENT 1: You must thoroughly populate the 'columns' dictionary properties inside database tables. "
            "Never leave columns empty. Include fundamental fields like id, timestamp, and core descriptive properties.\n"
            "CRITICAL REQUIREMENT 2: All lists/arrays must be standard valid JSON configurations. "
            "Example: 'target_roles': ['Admin', 'User']. Never include indices like '0: Admin' inside array blocks."
        )

        try:
            raw_schema = AppBlueprint.model_json_schema()
            
            def remove_additional_properties(schema_dict):
                if isinstance(schema_dict, dict):
                    schema_dict.pop('additionalProperties', None)
                    for key, value in schema_dict.items():
                        remove_additional_properties(value)
                elif isinstance(schema_dict, list):
                    for item in schema_dict:
                        remove_additional_properties(item)
            
            remove_additional_properties(raw_schema)

            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"User Request: {user_prompt}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=raw_schema,
                    temperature=0.1,
                ),
            )
            app_config = json.loads(response.text)
            metrics["latency_stages"]["generation_layers"] = round(time.time() - stage_start, 2)
            
        except Exception as e:
            log_callback(f"❌ Generation Pipeline Crash: {str(e)}", "running")
            raise e

        # ---- STAGE 4: Self-Healing Validation & Automated Repair Engine ----
        stage_start = time.time()
        log_callback("🔍 Pipeline Status: Initiating Execution Awareness Cross-Layer Structural Integrity scans...", "running")
        time.sleep(0.5)
        
        valid_tables = [table["table_name"] for table in app_config.get("database_schema", [])]
        
        # 1. Structural Repair: Missing Columns Fallback Healing Loop
        for table in app_config.get("database_schema", []):
            if not table.get("columns"):
                metrics["retries"] += 1
                metrics["healed_issues"].append(f"Empty columns dict detected inside table '{table['table_name']}'.")
                log_callback(f"⚠️ Repair Engine Action: Table '{table['table_name']}' has empty schemas. Auto-injecting functional default keys...", "running")
                table["columns"] = {
                    "id": "SERIAL PRIMARY KEY",
                    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    "status_state": "VARCHAR(50)"
                }

        # 2. Cross-Layer Consistency Alignment validation check
        for endpoint in app_config.get("api_schema", []):
            if endpoint["mapped_db_table"] not in valid_tables:
                metrics["retries"] += 1
                metrics["healed_issues"].append(f"API endpoint path route {endpoint['path']} references non-existent table assignment mapping context.")
                log_callback(f"⚠️ Repair Engine Action: Endpoint {endpoint['path']} mapped to missing entity context. Re-routing safely...", "running")
                
                if valid_tables:
                    endpoint["mapped_db_table"] = valid_tables[0]

        metrics["latency_stages"]["validation_repair"] = round(time.time() - stage_start, 2)
        metrics["total_latency"] = round(time.time() - start_time, 2)
        
        log_callback("✨ Application blueprint successfully compiled and verified by validation engine.", "complete")
        return app_config, metrics