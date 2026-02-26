from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

feedbackstorage = []

class Feedback(BaseModel):
    name : str
    message: str

def FeedbackAnswer(name: str):
    return f"Feedback received. Thank you, {name}"

@app.post("/feedback")
def root(feedback: Feedback):
    feedbackstorage.append(feedback)
    return {
        "status": "success",
        "message": FeedbackAnswer(feedback.name)
    }

@app.get("/test")
def test():
    return feedbackstorage