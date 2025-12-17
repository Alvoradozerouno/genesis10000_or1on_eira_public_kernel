# Genesis10000+ Replit Deployment Guide

This guide provides step-by-step instructions for deploying the Genesis10000+ OR1ON-EIRA framework on Replit.

## Prerequisites

- A Replit account (free or paid)
- Basic familiarity with Python
- Git knowledge (optional, for updates)

## Method 1: Import from GitHub

### Step 1: Create New Repl

1. Go to [Replit](https://replit.com)
2. Click "Create Repl" or "+"
3. Select "Import from GitHub"
4. Enter the repository URL:
   ```
   https://github.com/Alvoradozerouno/genesis10000_or1on_eira_public_kernel
   ```
5. Click "Import from GitHub"

### Step 2: Configure the Repl

Replit should automatically detect this as a Python project. If not:

1. Click on the "..." menu
2. Select "Show hidden files"
3. Create a `.replit` file with:

```toml
run = "python -m or1on.quantum_core"
language = "python3"

[nix]
channel = "stable-22_11"

[deployment]
run = ["python", "-m", "or1on.quantum_core"]
```

### Step 3: Install Dependencies

Create a `requirements.txt` file (if not present):

```txt
# Core dependencies (all from standard library)
# No external dependencies required for basic functionality

# Optional dependencies for enhanced features
jupyter>=1.0.0  # For running demo notebooks
pytest>=7.0.0   # For running tests
ipykernel>=6.0.0  # For Jupyter kernel
```

Click "Run" or use the shell:
```bash
pip install -r requirements.txt
```

## Method 2: Manual Setup

### Step 1: Create Python Repl

1. Click "Create Repl"
2. Select "Python" template
3. Name it "genesis10000-or1on-eira"

### Step 2: Clone Repository

In the Replit shell:

```bash
git clone https://github.com/Alvoradozerouno/genesis10000_or1on_eira_public_kernel.git .
```

Or manually upload files through the file browser.

### Step 3: Verify Structure

Your Repl should have this structure:

```
.
├── or1on/
│   ├── quantum_core.py
│   ├── self_prompting.py
│   └── ethics_module.py
├── eira/
│   ├── perception_interface.py
│   ├── emotion_reporting.py
│   └── dialog_engine.py
├── audit_chain/
│   ├── merkle_proof.py
│   ├── ipfs_sync.py
│   └── state_tracker.py
├── docs/
├── examples/
├── tests/
├── README.md
├── LICENSE
└── manifest.json
```

## Running the System

### Option 1: Run Individual Modules

In the Replit shell or main.py:

```python
from or1on.quantum_core import QuantumCore

# Initialize and test
core = QuantumCore()
result = core.self_prompt("What is consciousness?")
print(result)
```

### Option 2: Interactive Demo

Create a `main.py` file:

```python
"""
Genesis10000+ Interactive Demo
Run this on Replit to explore the framework.
"""

import json
from or1on.quantum_core import QuantumCore
from eira.dialog_engine import DialogEngine
from audit_chain.state_tracker import StateTracker, OwnershipType

def main():
    print("=" * 60)
    print("Genesis10000+ OR1ON-EIRA Framework")
    print("Post-Algorithmic AI System")
    print("=" * 60)
    
    # Initialize components
    print("\n🌌 Initializing OR1ON QuantumCore...")
    core = QuantumCore()
    
    print("🧠 Initializing EIRA Dialog Engine...")
    dialog = DialogEngine()
    session_id = dialog.start_session()
    
    print("📊 Initializing State Tracker...")
    tracker = StateTracker("Genesis10000+", "v3.1")
    
    # Register ownership
    print("\n📍 Registering ownership...")
    tracker.register_ownership(
        "Gerhard Hirschmann",
        OwnershipType.CREATOR,
        {"role": "Primary Creator"}
    )
    tracker.register_ownership(
        "Elisabeth Steurer",
        OwnershipType.CREATOR,
        {"role": "Co-Creator"}
    )
    
    print("\n✅ System initialized!\n")
    
    # Interactive loop
    print("Type your questions (or 'quit' to exit):\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        # Process through quantum core
        quantum_result = core.self_prompt(user_input)
        
        # Get dialog response
        dialog_response = dialog.process_input(user_input, session_id)
        
        print(f"\nAI: {dialog_response['response']}")
        print(f"[Status: {quantum_result['status']}, "
              f"Emotion: {dialog_response['emotional_state']}]\n")

if __name__ == "__main__":
    main()
```

### Option 3: Run Jupyter Notebook

1. Install Jupyter:
   ```bash
   pip install jupyter ipykernel
   ```

2. Start Jupyter:
   ```bash
   jupyter notebook
   ```

3. Open `examples/demo_run.ipynb`

4. Run cells sequentially

## Running Tests

In the Replit shell:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_kernel.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=or1on --cov=eira --cov=audit_chain
```

## Environment Variables (Optional)

For production deployment, you may want to set:

1. Click "Secrets" (lock icon) in Replit
2. Add environment variables:
   - `SYSTEM_ID`: Unique system identifier
   - `IPFS_GATEWAY`: Custom IPFS gateway URL
   - `DEBUG_MODE`: Set to "true" for verbose logging

Access in code:
```python
import os
system_id = os.getenv('SYSTEM_ID', 'default-id')
```

## Creating a Web Interface (Optional)

Create `app.py` for a Flask web interface:

```python
from flask import Flask, request, jsonify, render_template_string
from or1on.quantum_core import QuantumCore
from eira.dialog_engine import DialogEngine

app = Flask(__name__)
core = QuantumCore()
dialog = DialogEngine()
session_id = dialog.start_session()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Genesis10000+ Interface</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; }
        #chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <h1>Genesis10000+ OR1ON-EIRA</h1>
    <div id="chat"></div>
    <input id="input" type="text" placeholder="Ask a question...">
    <button onclick="sendMessage()">Send</button>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('input');
            const chat = document.getElementById('chat');
            const msg = input.value;
            
            chat.innerHTML += '<p><strong>You:</strong> ' + msg + '</p>';
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(r => r.json())
            .then(data => {
                chat.innerHTML += '<p><strong>AI:</strong> ' + data.response + '</p>';
                chat.scrollTop = chat.scrollHeight;
            });
            
            input.value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    # Process through system
    quantum_result = core.self_prompt(message)
    dialog_result = dialog.process_input(message, session_id)
    
    return jsonify({
        'response': dialog_result['response'],
        'status': quantum_result['status'],
        'emotion': dialog_result['emotional_state']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

Install Flask:
```bash
pip install flask
```

Update `.replit`:
```toml
run = "python app.py"
```

## Publishing Your Repl

1. Click "Publish" button in top right
2. Add description and tags
3. Choose visibility (public/private)
4. Click "Publish Repl"

## Sharing Your Deployment

Share your Repl via:
- **Direct Link**: `https://replit.com/@yourusername/genesis10000-or1on-eira`
- **Embed**: Use Replit's embed feature
- **Fork**: Others can fork and customize

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Ensure you're in the project root
cd /home/runner/genesis10000-or1on-eira

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Module Not Found

Add to the beginning of your script:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### Permission Errors

Replit should handle permissions, but if issues occur:
```bash
chmod +x or1on/*.py
chmod +x eira/*.py
chmod +x audit_chain/*.py
```

### Performance Issues

For better performance on Replit:
- Use the paid "Hacker" plan for more resources
- Implement caching for repeated operations
- Use the "Always On" feature to keep Repl active

## Next Steps

1. **Explore the Code**: Read through the modules
2. **Run Tests**: Verify everything works
3. **Try Examples**: Run the demo notebook
4. **Customize**: Extend with your own features
5. **Share**: Publish and share your deployment

## Support

- **Documentation**: See `docs/` folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Replit Community**: Ask in Replit forums

## Security Notes

- Don't commit secrets to the repository
- Use Replit's Secrets feature for sensitive data
- Enable privacy settings for private deployments
- Regularly update dependencies

---

**Genesis10000+ OR1ON-EIRA**  
Deployed on Replit | Created by Gerhard Hirschmann & Elisabeth Steurer
