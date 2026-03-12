@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employment Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
            --ink: #0d0d0d; --paper: #f5f0e8; --cream: #ede8dc;
            --accent: #c8402a; --accent2: #2a5fc8; --muted: #7a7468;
            --border: #d0c9bc; --card: #faf8f4;
        }
        body {
            font-family: 'Sora', sans-serif; background: var(--paper);
            min-height: 100vh; display: flex; align-items: center;
            justify-content: center; padding: 24px; position: relative; overflow: hidden;
        }
        body::before {
            content: ''; position: fixed; inset: 0;
            background-image: linear-gradient(var(--border) 1px, transparent 1px),
                              linear-gradient(90deg, var(--border) 1px, transparent 1px);
            background-size: 48px 48px; opacity: 0.35; pointer-events: none;
        }
        body::after {
            content: ''; position: fixed; top: 32px; left: 32px;
            width: 60px; height: 60px;
            border-top: 2px solid var(--accent); border-left: 2px solid var(--accent); opacity: 0.6;
        }
        .corner-br {
            position: fixed; bottom: 32px; right: 32px; width: 60px; height: 60px;
            border-bottom: 2px solid var(--accent2); border-right: 2px solid var(--accent2); opacity: 0.6;
        }
        .wrapper {
            position: relative; z-index: 1; display: grid;
            grid-template-columns: 220px 1fr; background: var(--card);
            border: 1px solid var(--border);
            box-shadow: 8px 8px 0 var(--border), 16px 16px 0 rgba(0,0,0,0.04);
            max-width: 740px; width: 100%;
            animation: reveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
        }
        @keyframes reveal {
            from { opacity: 0; transform: translateY(24px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .sidebar {
            background: var(--ink); color: var(--paper);
            padding: 40px 28px; display: flex; flex-direction: column; gap: 32px;
        }
        .sidebar-label { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); }
        .sidebar-title { font-family: 'DM Serif Display', serif; font-size: 28px; line-height: 1.15; color: var(--paper); }
        .sidebar-title em { font-style: italic; color: #f0b89a; }
        .sidebar-divider { width: 32px; height: 2px; background: var(--accent); }
        .sidebar-desc { font-size: 12px; color: #a09890; line-height: 1.7; font-weight: 300; }
        .sidebar-stat { margin-top: auto; }
        .stat-num { font-family: 'DM Serif Display', serif; font-size: 42px; color: var(--paper); opacity: 0.15; line-height: 1; }
        .stat-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.18em; color: var(--muted); text-transform: uppercase; margin-top: 4px; }
        .main { padding: 40px 36px; display: flex; flex-direction: column; gap: 28px; }
        .main-header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
        .main-header-title { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); }
        .badge { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); border: 1px solid var(--accent); padding: 3px 8px; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .field { display: flex; flex-direction: column; gap: 6px; }
        .field.full { grid-column: 1 / -1; }
        label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); }
        input, select {
            width: 100%; padding: 10px 12px; font-family: 'Sora', sans-serif;
            font-size: 13px; color: var(--ink); background: var(--cream);
            border: 1px solid var(--border); border-radius: 0; outline: none;
            transition: border-color 0.2s, background 0.2s;
            -webkit-appearance: none; appearance: none;
        }
        input:focus, select:focus { border-color: var(--ink); background: #fff; }
        .select-wrap { position: relative; }
        .select-wrap::after {
            content: '↓'; position: absolute; right: 12px; top: 50%;
            transform: translateY(-50%); font-size: 11px; color: var(--muted); pointer-events: none;
        }
        .submit-row { display: flex; align-items: center; gap: 16px; padding-top: 8px; border-top: 1px solid var(--border); }
        button {
            flex: 1; padding: 13px 24px; font-family: 'DM Mono', monospace;
            font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase;
            color: var(--paper); background: var(--ink); border: 1px solid var(--ink);
            cursor: pointer; transition: transform 0.1s; position: relative; overflow: hidden;
        }
        button::after {
            content: ''; position: absolute; inset: 0; background: var(--accent);
            transform: scaleX(0); transform-origin: left;
            transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        }
        button:hover::after { transform: scaleX(1); }
        button span { position: relative; z-index: 1; }
        button:active { transform: scale(0.98); }
        .result-panel { display: none; background: var(--cream); border: 1px solid var(--border); padding: 16px 20px; animation: slideIn 0.4s cubic-bezier(0.22, 1, 0.36, 1); }
        .result-panel.visible { display: block; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        .result-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
        .result-value { font-family: 'DM Serif Display', serif; font-size: 22px; color: var(--ink); }
        .result-value.positive { color: var(--accent2); }
        .result-value.negative { color: var(--accent); }
        @media (max-width: 580px) {
            .wrapper { grid-template-columns: 1fr; }
            .sidebar { padding: 28px 24px; flex-direction: row; flex-wrap: wrap; gap: 16px; }
            .sidebar-stat { display: none; }
            .main { padding: 28px 24px; }
            .form-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="corner-br"></div>
    <div class="wrapper">
        <aside class="sidebar">
            <div><div class="sidebar-label">v1.0 · ML Model</div></div>
            <div>
                <div class="sidebar-title">Employment <em>Predictor</em></div>
                <div class="sidebar-divider" style="margin-top:16px"></div>
            </div>
            <div class="sidebar-desc">Enter candidate details to generate an employment likelihood assessment using our trained model.</div>
            <div class="sidebar-stat">
                <div class="stat-num">ML</div>
                <div class="stat-label">Powered</div>
            </div>
        </aside>
        <main class="main">
            <div class="main-header">
                <div class="main-header-title">Candidate Profile</div>
                <div class="badge">Predictor</div>
            </div>
            <div class="form-grid">
                <div class="field">
                    <label for="age">Age</label>
                    <input type="number" id="age" placeholder="e.g. 24" min="16" max="65">
                </div>
                <div class="field">
                    <label for="tier">College Tier</label>
                    <input type="number" id="tier" placeholder="e.g. 1, 2, 3" min="1" max="5">
                </div>
                <div class="field">
                    <label for="gender">Gender</label>
                    <div class="select-wrap">
                        <select id="gender">
                            <option value="">Select</option>
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                        </select>
                    </div>
                </div>
                <div class="field">
                    <label for="skilled">Skilled</label>
                    <div class="select-wrap">
                        <select id="skilled">
                            <option value="">Select</option>
                            <option value="Yes">Yes</option>
                            <option value="No">No</option>
                        </select>
                    </div>
                </div>
                <div class="field full">
                    <label for="school">School</label>
                    <div class="select-wrap">
                        <select id="school">
                            <option value="">Select school</option>
                            <option value="GVHS">GVHS</option>
                            <option value="HCCS">HCCS</option>
                            <option value="BBI">BBI</option>
                            <option value="Girls School">Girls School</option>
                            <option value="KV">KV</option>
                            <option value="Chandrapur School">Chandrapur School</option>
                            <option value="Fail">Fail</option>
                        </select>
                    </div>
                </div>
            </div>
            <div id="resultPanel" class="result-panel">
                <div class="result-label">Prediction Result</div>
                <div class="result-value" id="resultValue">—</div>
            </div>
            <div class="submit-row">
                <button id="predictBtn" onclick="predict()">
                    <span id="btnText">Run Prediction</span>
                </button>
            </div>
        </main>
    </div>
    <script>
        async function predict() {
            const age = document.getElementById("age").value;
            const tier = document.getElementById("tier").value;
            const gender = document.getElementById("gender").value;
            const skilled = document.getElementById("skilled").value;
            const school = document.getElementById("school").value;
            const btn = document.getElementById("predictBtn");
            const btnText = document.getElementById("btnText");
            btnText.textContent = "Analysing...";
            btn.disabled = true;
            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ age: parseInt(age), collage_tier: parseInt(tier), gender, skilled, school })
                });
                const data = await response.json();
                const panel = document.getElementById("resultPanel");
                const val = document.getElementById("resultValue");
                panel.classList.add("visible");
                val.textContent = data.result;
                const r = (data.result || "").toLowerCase();
                val.className = "result-value";
                if (r.includes("employ") || r.includes("hired") || r.includes("yes")) val.classList.add("positive");
                else if (r.includes("not") || r.includes("no") || r.includes("unemploy")) val.classList.add("negative");
            } catch (err) {
                document.getElementById("resultPanel").classList.add("visible");
                const val = document.getElementById("resultValue");
                val.textContent = "Error — check connection";
                val.className = "result-value negative";
            } finally {
                btnText.textContent = "Run Prediction";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
    """