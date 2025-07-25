**1. Create a New Poetry Project:**

  * **Command:**
    ```bash
    poetry new my_new_project
    ```
  * **Instruction:** This creates a folder `my_new_project` with basic Poetry files.

-----

**2. Navigate into Your Project Directory:**

  * **Command:**
    ```bash
    cd my_new_project
    ```
  * **Instruction:** You *must* be inside your project folder to run most Poetry commands.

-----

**3. Install Project Dependencies & Create Virtual Environment:**

  * **Command:**
    ```bash
    poetry install
    ```
  * **Instruction:** This reads `pyproject.toml`, creates a virtual environment, and installs dependencies.

-----

**4. Run a Command within the Poetry Environment:**

  * **Command:**
    ```bash
    poetry run python --version
    # Or to run your main script (e.g., if you have main.py)
    # poetry run python my_new_project/main.py
    ```
  * **Instruction:** Executes the specified command using the Python interpreter from the project's virtual environment.

-----

**5. List Poetry Environments for the Current Project:**

  * **Command:**
    ```bash
    poetry env list
    ```
  * **Instruction:** Shows details of the virtual environment linked to your current project.

-----

**6. Add a New Dependency:**

  * **Command:**
    ```bash
    poetry add requests
    ```
  * **Instruction:** Installs the `requests` package and adds it to `pyproject.toml` and `poetry.lock`.

-----

**7. Activate the Virtual Environment (for direct use):**

  * **Command:**
    ```bash
    poetry shell
    ```
  * **Instruction:** Activates the project's virtual environment in your current terminal session. You can then run `python` directly without `poetry run`.
      * To exit: `exit`

-----