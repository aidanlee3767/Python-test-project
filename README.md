# My First Git Project
# Python-test-project

## Project setup
```bash
uv sync

source .venv/bin/activate
```
## Project Structure
```
  src/
  ├── ai_model/          # AI model implementations
  ├── project/           # Project-specific modules
  └── simple_agent/      # Main chatbot application
      ├── agents/        # Specialized agents
      ├── utils/         # Utility modules
      └── workflow/      # Workflow orchestration
```

## Running the Application

### Command Line Interface
```bash
python -m src.simple_agent.main
```

### Streamlit Web Interface
```bash
streamlit run app.py
```
또는
```bash
python -m src.simple_agent.run_streamlit
```

웹 브라우저에서 `http://localhost:8501`로 접속하여 사용할 수 있습니다.
