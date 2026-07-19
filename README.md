# AI Compiler Pipeline

A Streamlit-based application that converts natural language software requirements into a structured, self-healed application blueprint. It uses the Gemini API to generate database schemas, API endpoints, UI pages, and business rules from a simple prompt.

## 🚀 Live Demo

Open the deployed app here:

https://ai-compiler-pipeline-niranjanrp.streamlit.app/

## ✨ Features

- Converts user prompts into structured app architecture blueprints
- Generates database schema definitions
- Creates API endpoint mappings
- Defines UI page structure
- Includes basic self-healing validation for missing or inconsistent schema data
- Provides a simple and interactive Streamlit UI

## 🛠️ Tech Stack

- Python
- Streamlit
- Pydantic
- Google Gemini API

## 📁 Project Structure

- app.py - Streamlit web interface
- compiler.py - Core pipeline logic for blueprint generation
- models.py - Pydantic models for schema validation
- requirements.txt - Python dependencies

## 📸 Screenshots

### Main Interface
![Compiler Interface](docs/screenshots/interface.png)
*Input panel for API key and application requirements*

### Generated Output
![Generated Blueprint](docs/screenshots/output.png)
*JSON configuration output showing the compiled system blueprint*

### Pipeline Metrics
![Metrics Dashboard](docs/screenshots/metrics.png)
*System analysis metrics and automated repair operations logs*

## ▶️ Run Locally

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Enter your Gemini API key in the app and provide a prompt to generate the blueprint.

## 🔧 Notes

- This app requires a valid Gemini API key to generate outputs.
- The generated blueprint is displayed as structured JSON in the UI.

## 📌 Purpose

This project demonstrates how AI can be used to turn plain English requirements into a structured software architecture plan with schema-level validation.
