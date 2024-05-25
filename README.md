# RobotsHTML

Some of the things being assumed here:

1. You have installed python3.8 or above.
2. You have created a virtual environment (recommended but not mandatory).
3. You have used pip to install from the requirements.txt file.
   ```bash
    python3 -m pip install -r requirements.txt
    ```

<br>

## Usage

From the base directory run:

```bash
python3 main.py
```

OR

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --loop uvloop --http h11
```

<br>
