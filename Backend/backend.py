from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables and configure Gemini
load_dotenv()
api_key = "AIzaSyBsOChWdEgk7ResbVkk9WcLor2w127NO4U"
genai.configure(api_key=api_key)

# Initialize the Gemini API with specific configuration
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Test healthcare response")
    print("Successfully connected to Gemini API and tested model access")
except Exception as e:
    print(f"Error testing Gemini API access: {str(e)}")

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
    message: str

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
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Provide health tips for: {query_data.query}")
        if not response or not response.text:
            return OutputModel(output="I apologize, but I couldn't generate health tips. Please try again.")
        return OutputModel(output=f"Health Tip: {response.text.strip().split('.')[0]}")
    except Exception as e:
        print(f"Error generating health tips: {str(e)}")
        return OutputModel(output=f"I apologize, but there was an error: {str(e)}")

@app.post("/generate-response", response_model=OutputModel)
async def generate_response(request_data: GenerateResponseModel):
    try:
        print(f"Received message: {request_data.message}")
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = """You are a professional healthcare assistant chatbot. Provide accurate, helpful medical information while:
        1. Using clear, simple language that patients can understand
        2. Including relevant medical facts and evidence-based recommendations
        3. Adding appropriate medical disclaimers when needed
        4. Maintaining a professional but compassionate tone
        5. Focusing only on healthcare-related topics
        6. Encouraging users to seek professional medical help when appropriate

        User's health question: {message}
        
        Please provide a helpful medical response."""
        
        try:
            response = model.generate_content(
                prompt.format(message=request_data.message),
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            if not response or not response.text:
                return OutputModel(output="I apologize, but I couldn't generate a medical response. Please try again.")
                
            return OutputModel(output=response.text.strip())
            
        except Exception as model_error:
            print(f"Error generating content: {str(model_error)}")
            return OutputModel(output=f"I apologize, but there was an error with the AI model: {str(model_error)}")
            
    except Exception as e:
        print(f"Error in generate_response: {str(e)}")
        return OutputModel(output="I apologize, but there was an unexpected error. Please try again later.")

@app.post("/generate-sample-queries")
async def generate_sample_queries():
    return [
        "What are common symptoms of diabetes?",
        "How can I manage high blood pressure naturally?",
        "What are the early warning signs of a heart attack?",
        "How can I improve my immune system?",
        "What are effective ways to manage stress-related health issues?"
    ]

@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Assistant API! Use the available endpoints for medical information and assistance."}
