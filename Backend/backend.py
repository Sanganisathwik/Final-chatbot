from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input models
class SymptomsModel(BaseModel):
    symptoms: list[str]

class HealthQueryModel(BaseModel):
    query: str

class OutputModel(BaseModel):
    output: str

class GenerateResponseModel(BaseModel):
    input: str

# Disease and medication mapping
disease_data = {
    "flu": {"symptoms": ["fever", "cough", "body aches"], "medication": "Paracetamol, Cough Syrup, Rest"},
    "diabetes": {"symptoms": ["excessive thirst", "frequent urination", "fatigue"], "medication": "Metformin, Insulin"},
    "hypertension": {"symptoms": ["headache", "dizziness", "blurred vision"], "medication": "Amlodipine, Losartan"},
    "covid-19": {"symptoms": ["fever", "dry cough", "loss of taste/smell"], "medication": "Supportive care, Paracetamol, Hydration"}
}

@app.post("/detect-disease", response_model=OutputModel)
async def detect_disease(symptoms_data: SymptomsModel):
    user_symptoms = set(symptom.lower() for symptom in symptoms_data.symptoms)
    for disease, data in disease_data.items():
        if any(symptom in user_symptoms for symptom in data["symptoms"]):
            return OutputModel(output=f"Possible condition: {disease}. Recommended medication: {data['medication']}")
    return OutputModel(output="No matching disease found. Consult a doctor.")

@app.post("/health-tips", response_model=OutputModel)
async def health_tips(query_data: HealthQueryModel):
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(f"Provide health tips for: {query_data.query}")
    return OutputModel(output=f"Health Tip: {response.text.strip().split('.')[0]}")

@app.post("/generate-response", response_model=OutputModel)
async def generate_response(request_data: GenerateResponseModel):
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(f"Answer this health-related question: {request_data.input}")
    return OutputModel(output=response.text.strip())

@app.post("/generate-sample-queries")
async def generate_sample_queries():
    return [
        "What are the symptoms of flu?",
        "How to manage diabetes?",
        "Tips for better sleep",
        "How to reduce stress?",
        "What are the symptoms of COVID-19?"
    ]

@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Chatbot! Use available endpoints for assistance."}
