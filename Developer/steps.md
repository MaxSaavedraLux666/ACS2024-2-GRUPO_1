```markdown
# Guide to Creating and Managing a Python Virtual Environment

This guide explains how to create a Python virtual environment, activate it, and manage dependencies using a `requirements.txt` file. All steps are based on the following folder structure:

```

Developer/
├── backend/
├── simulation/
│     ├── venv/
│     └── requirements.txt

```

## 1. **Create a Virtual Environment**

### On Linux
1. Navigate to the `simulation` folder:
   ```bash
   cd Developer/simulation
```

2. Create the virtual environment in the `venv` folder:
   ```bash
   python3 -m venv venv
   ```

### On Windows

1. Navigate to the `simulation` folder:
   ```cmd
   cd Developer\simulation
   ```
2. Create the virtual environment in the `venv` folder:
   ```cmd
   python -m venv venv
   ```

---

## 2. **Activate the Virtual Environment**

### On Linux

Activate the virtual environment:

```bash
source venv/bin/activate
```

### On Windows

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

> Once activated, the virtual environment's name (e.g., `venv`) will appear at the beginning of your terminal prompt.

---

## 3. **Install Dependencies from `requirements.txt`**

1. Ensure the virtual environment is activated.
2. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. **Update Dependencies in `requirements.txt`**

If you need to save the current dependencies of the project to `requirements.txt`:

1. Ensure the virtual environment is activated.
2. Generate or update the file:
   ```bash
   pip freeze > requirements.txt
   ```

---

## Important Notes

* **Project Structure:** Always ensure you're in the correct directory (`Developer/simulation`) before working with the virtual environment or the `requirements.txt` file.
* **Deactivate the Virtual Environment:** When you're done, you can deactivate it using:
  * On Linux:
    ```bash
    deactivate
    ```
  * On Windows:
    ```cmd
    deactivate
    ```
* **Common Issues:** If you have multiple Python versions installed, ensure you're using the correct version with `python3` on Linux or by specifying the path explicitly on Windows.
