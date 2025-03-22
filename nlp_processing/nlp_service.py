from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_trf") # Replace with your model
    print("SpaCy model loaded successfully")
except OSError:
    print("Downloading SpaCy model...")
    import spacy.cli
    spacy.cli.download("en_core_web_trf")
    nlp = spacy.load("en_core_web_trf")


class TextInput(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_text(text_input: TextInput):
    try:
        doc = nlp(text_input.text)
        # Extract entities, keywords, etc.
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return {"entities": entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000)) #Get port from environment variable
    uvicorn.run(app, host="0.0.0.0", port=port)
