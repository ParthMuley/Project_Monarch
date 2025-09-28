# Project Monarch  

An autonomous, multi-guild AI agent organization inspired by the anime *Solo Leveling*.

This project creates a system where a central "Monarch" agent manages an army of specialized AI agents (organized into guilds) to complete complex, multi-domain tasks. The system is designed to be modular, scalable, and capable of learning from its experience.

## ✨ Core Features
- **Multi-Guild Architecture:** Agents are organized into specialized guilds (Writers, Coders, Artists).
- **Dynamic Workflows:** The Monarch uses a configuration-driven workflow engine to manage multi-step projects.
- **Agent Career Paths:** Agents gain XP, rank up, and can be promoted to more advanced roles.
- **Tool Use:** High-rank agents can use external tools like a web search and a code interpreter.
- **Persistent Memory:** The organization learns from successfully completed jobs using a vector database.
- **Economic Strategy:** The Monarch makes cost-based decisions to efficiently manage a budget.
- **Professional CLI:** The project is packaged as a clean command-line tool.

## ⚙️ Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd project-monarch
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up API Keys:**
    Create a `.env` file in the root of the project and add your API keys:
    ```
    OPENAI_API_KEY=sk-YourKeyHere
    SERPAPI_API_KEY=YourKeyHere
    ```

5.  **Install the CLI:**
    Install the project in editable mode to create the `monarch` command.
    ```bash
    pip install -e .
    ```

## 🚀 Usage

You can now run the project from any directory in your terminal.

**Coder Guild Example:**
```bash
monarch "Create a python class for a snake game, including a plan, the code, and a final review."
