
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

from blog_writing_crew.crew import BlogWritingCrew

app = FastAPI(
    title="Ink & Enchantment API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BlogRequest(BaseModel):
    topic: str = Field(min_length=5, max_length=500)
    tone: str
    length: str
    words: int
    audience: str = "General readers"


@app.get("/")
def home():
    return {"message": "Ink & Enchantment API is running!"}


@app.post("/generate")
def generate_blog(request: BlogRequest):
    try:
        inputs = {
            "topic": request.topic,
            "tone": request.tone,
            "length": request.length,
            "words": request.words,
            "target_audience": request.audience,
            "current_year": str(datetime.now().year)
        }

        result = BlogWritingCrew().crew().kickoff(inputs=inputs)

        content = getattr(result, "raw", None) or str(result)
        content = content.strip()

        lines = content.splitlines()
        title = request.topic
        article = content

        for index, line in enumerate(lines):
            if line.strip():
                if line.strip().startswith("#"):
                    title = line.strip().lstrip("#").strip()
                    article = "\n".join(
                        lines[index + 1:]
                    ).strip()
                else:
                    title = line.strip()
                    article = "\n".join(
                        lines[index + 1:]
                    ).strip()
                break

        if not article:
            article = content

        return {
            "title": title,
            "article": article
        }

    except Exception as e:
        print(f"Blog generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Blog generation failed. Please try again."
        )
