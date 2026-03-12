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
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Employment Predictor</title>

<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>

*{box-sizing:border-box;margin:0;padding:0;}

:root{
--ink:#121212;
--paper:#f7f4ee;
--cream:#f1ece3;
--accent:#d1452f;
--accent2:#2a5fc8;
--muted:#7b756c;
--border:#d8d1c5;
--card:#faf7f2;
}

html,body{
height:auto;
-webkit-overflow-scrolling:touch;
}

body{
font-family:'Sora',sans-serif;
background:var(--paper);
min-height:100vh;
display:flex;
align-items:flex-start;
justify-content:center;
padding:40px 20px;
overflow-y:auto;
}

body::before{
content:'';
position:fixed;
inset:0;
background-image:
linear-gradient(var(--border) 1px, transparent 1px),
linear-gradient(90deg,var(--border) 1px, transparent 1px);
background-size:50px 50px;
opacity:.35;
pointer-events:none;
}

.wrapper{
display:grid;
grid-template-columns:230px 1fr;
background:var(--card);
border:1px solid var(--border);
max-width:760px;
width:100%;
box-shadow:
8px 8px 0 var(--border),
20px 20px 35px rgba(0,0,0,.05);
animation:fade .6s ease;
}

@keyframes fade{
from{opacity:0;transform:translateY(20px);}
to{opacity:1;}
}

.sidebar{
background:var(--ink);
color:var(--paper);
padding:42px 28px;
display:flex;
flex-direction:column;
gap:30px;
}

.sidebar-label{
font-family:'DM Mono',monospace;
font-size:10px;
letter-spacing:.25em;
text-transform:uppercase;
color:#9d968c;
}

.sidebar-title{
font-family:'DM Serif Display',serif;
font-size:30px;
line-height:1.2;
}

.sidebar-title em{
color:#f0b89a;
}

.sidebar-divider{
width:36px;
height:2px;
background:var(--accent);
margin-top:14px;
}

.sidebar-desc{
font-size:13px;
color:#a79f95;
line-height:1.7;
}

.sidebar-stat{
margin-top:auto;
}

.stat-num{
font-family:'DM Serif Display',serif;
font-size:44px;
opacity:.15;
}

.stat-label{
font-family:'DM Mono',monospace;
font-size:9px;
letter-spacing:.2em;
color:#8e887f;
}

.main{
padding:42px 36px;
display:flex;
flex-direction:column;
gap:28px;
}

.main-header{
display:flex;
justify-content:space-between;
align-items:center;
border-bottom:1px solid var(--border);
padding-bottom:18px;
}

.main-header-title{
font-family:'DM Mono',monospace;
font-size:10px;
letter-spacing:.25em;
text-transform:uppercase;
color:var(--muted);
}

.badge{
font-family:'DM Mono',monospace;
font-size:9px;
letter-spacing:.15em;
border:1px solid var(--accent);
padding:4px 8px;
color:var(--accent);
}

.form-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:18px;
}

.field{
display:flex;
flex-direction:column;
gap:6px;
}

.field.full{
grid-column:1/-1;
}

label{
font-family:'DM Mono',monospace;
font-size:9px;
letter-spacing:.2em;
text-transform:uppercase;
color:var(--muted);
}

input,select{
width:100%;
padding:11px 12px;
font-size:13px;
font-family:'Sora',sans-serif;
background:var(--cream);
border:1px solid var(--border);
outline:none;
transition:.2s;
}

input:focus,select:focus{
background:#fff;
border-color:var(--ink);
}

.select-wrap{
position:relative;
}

.select-wrap::after{
content:'▾';
position:absolute;
right:10px;
top:50%;
transform:translateY(-50%);
font-size:12px;
color:var(--muted);
pointer-events:none;
}

.submit-row{
border-top:1px solid var(--border);
padding-top:14px;
}

button{
width:100%;
padding:14px;
font-family:'DM Mono',monospace;
font-size:11px;
letter-spacing:.2em;
text-transform:uppercase;
background:var(--ink);
color:white;
border:1px solid var(--ink);
cursor:pointer;
position:relative;
overflow:hidden;
}

button::after{
content:'';
position:absolute;
inset:0;
background:var(--accent);
transform:scaleX(0);
transform-origin:left;
transition:.35s ease;
}

button:hover::after{
transform:scaleX(1);
}

button span{
position:relative;
z-index:1;
}

.result-panel{
display:none;
background:var(--cream);
border:1px solid var(--border);
padding:18px 20px;
}

.result-panel.visible{
display:block;
animation:slide .4s ease;
}

@keyframes slide{
from{opacity:0;transform:translateY(8px);}
to{opacity:1;}
}

.result-label{
font-family:'DM Mono',monospace;
font-size:9px;
letter-spacing:.2em;
text-transform:uppercase;
color:var(--muted);
margin-bottom:6px;
}

.result-value{
font-family:'DM Serif Display',serif;
font-size:24px;
}

.result-value.positive{color:var(--accent2);}
.result-value.negative{color:var(--accent);}

@media(max-width:600px){

body{
align-items:flex-start;
padding-top:30px;
}

.wrapper{
grid-template-columns:1fr;
}

.sidebar{
flex-direction:row;
flex-wrap:wrap;
gap:15px;
padding:28px;
}

.sidebar-stat{
display:none;
}

.main{
padding:28px;
}

.form-grid{
grid-template-columns:1fr;
}

}

</style>
</head>

<body>

<div class="wrapper">

<aside class="sidebar">

<div class="sidebar-label">v1.0 · ML Model</div>

<div>
<div class="sidebar-title">Employment <em>Predictor</em></div>
<div class="sidebar-divider"></div>
</div>

<div class="sidebar-desc">
Enter candidate details to generate employment likelihood using our trained model.
</div>

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
<label>Age</label>
<input type="number" id="age" placeholder="24">
</div>

<div class="field">
<label>College Tier</label>
<input type="number" id="tier" placeholder="1-3">
</div>

<div class="field">
<label>Gender</label>
<div class="select-wrap">
<select id="gender">
<option value="">Select</option>
<option value="M">Male</option>
<option value="F">Female</option>
</select>
</div>
</div>

<div class="field">
<label>Skilled</label>
<div class="select-wrap">
<select id="skilled">
<option value="">Select</option>
<option value="Yes">Yes</option>
<option value="No">No</option>
</select>
</div>
</div>

<div class="field full">
<label>School</label>
<div class="select-wrap">
<select id="school">
<option value="">Select</option>
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
<div class="result-label">Prediction</div>
<div id="resultValue" class="result-value">—</div>
</div>

<div class="submit-row">
<button onclick="predict()" id="predictBtn">
<span id="btnText">Run Prediction</span>
</button>
</div>

</main>

</div>

<script>

async function predict(){

const btn=document.getElementById("predictBtn")
const txt=document.getElementById("btnText")

txt.textContent="Analysing..."
btn.disabled=true

try{

const response=await fetch("/predict",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
age:parseInt(document.getElementById("age").value),
collage_tier:parseInt(document.getElementById("tier").value),
gender:document.getElementById("gender").value,
skilled:document.getElementById("skilled").value,
school:document.getElementById("school").value
})
})

const data=await response.json()

const panel=document.getElementById("resultPanel")
const val=document.getElementById("resultValue")

panel.classList.add("visible")

val.textContent=data.result
val.className="result-value"

const r=(data.result||"").toLowerCase()

if(r.includes("yes")||r.includes("employ")) val.classList.add("positive")
else if(r.includes("no")||r.includes("not")) val.classList.add("negative")

}

catch{

const val=document.getElementById("resultValue")
document.getElementById("resultPanel").classList.add("visible")
val.textContent="Error — check API"
val.className="result-value negative"

}

txt.textContent="Run Prediction"
btn.disabled=false

}

</script>

</body>
</html>
"""