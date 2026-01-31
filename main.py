from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import argostranslate.translate as translate
import uvicorn
from language_install import install_languages

app = FastAPI(title="Argos Translation API")

@app.on_event("startup")
def startup():
    install_languages([("en", "ar")])

class TranslateRequest(BaseModel):
    pageText: List[str]
    targetLang: Optional[str] = "ar"
    sourceLang: Optional[str] = "en"

@app.post("/translate")
def translate_text(data: TranslateRequest):

    # Validate languages
    installed_langs = translate.get_installed_languages()
    installed_codes = [lang.code for lang in installed_langs]

    if data.sourceLang not in installed_codes or data.targetLang not in installed_codes:
        raise HTTPException(
            status_code=400,
            detail=f"Language not installed. Available: {installed_codes}"
        )

    results = []

    for text in data.pageText:
        if text.strip():
            results.append(
                translate.translate(
                    text,
                    data.sourceLang,
                    data.targetLang
                )
            )
        else:
            results.append(text)

    return {
        "translated": results
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
