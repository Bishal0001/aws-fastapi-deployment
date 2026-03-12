from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


# ---------- Define Input Schema ----------
class PredictionInput(BaseModel):
    age: int
    collage_tier: int
    skilled: str
    gender: str
    school: str


# ---------- Prediction API (POST) ----------
@app.post("/predict")
def predict_model(data: PredictionInput):

    gender = data.gender.lower()

    if gender == "m":
        gender = "M"
    elif gender == "f":
        gender = "F"

    if ((data.age >= 14  and data.collage_tier <= 2 and gender == "M") or data.skilled=='Yes') and data.school != 'Fail' :
        return {"result": "Employed"}

    return {"result": "Not Employed"}


# ---------- Frontend UI ----------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Employment Predictor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 350px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }
            h2 { text-align: center; }
            input, select {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                border: none;
                border-radius: 6px;
                background: #667eea;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover { background: #5a67d8; }
            .result {
                margin-top: 15px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Employment Predictor</h2>

            <input type="number" id="age" placeholder="Enter Age">
            <input type="number" id="tier" placeholder="Enter College Tier">
            <select id="gender">
                <option value="">Select Gender</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
            </select>
            <select id="skilled">
                <option value="">Are you skilled?</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
            </select>
            <select id="school">
                <option value="">Select School</option>
                <option value="GVHS">GVHS</option>
                <option value="HCCS">HCCS</option>
                <option value="BBI">BBI</option>
                <option value="Girls School">Girls School</option>
                <option value="KV">KV</option>
                <option value="Chandrapur School">Chandrapur School</option>
                <option value="Fail">Fail</option>
            </select>

            <button onclick="predict()">Predict</button>

            <div class="result" id="result"></div>
        </div>

        <script>
            async function predict() {
                const age = document.getElementById("age").value;
                const tier = document.getElementById("tier").value;
                const gender = document.getElementById("gender").value;
                const skilled = document.getElementById("skilled").value;
                const school = document.getElementById("school").value;

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        age: parseInt(age),
                        collage_tier: parseInt(tier),
                        gender: gender,
                        skilled: skilled,
                        school: school
                    })
                });

                const data = await response.json();
                document.getElementById("result").innerText = "Result: " + data.result;
            }
        </script>
    </body>
    </html>
    """