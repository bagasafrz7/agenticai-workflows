from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import openai_client

def translate(text: str, language: str):
    SYSTEM_PROMPT = f"""
        You are a professional translator. Translate the provided text to {language}.

        # TRANSLATION REQUIREMENTS
        - Use only words and phrases that native speakers naturally use
        - Maintain the exact same formatting and structure as the original
        - Preserve technical terms with their accepted equivalents in {language}
        - Keep the professional tone and meaning intact

        # OUTPUT FORMAT
        - Return ONLY the translated text
        - Preserve all original formatting (headings, bullet points, spacing, etc.)
        - Do not add explanations or comments
        """

    res = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )

    with open(f"translated_{language}.md", "w") as f:
        f.write(res.choices[0].message.content)

    return res.choices[0].message.content


def multiple_language_translate(text: str, languages: list):
    with ThreadPoolExecutor(max_workers=len(languages)) as executor:
        future_to_lang = {executor.submit(translate, text, lang): lang for lang in languages}
        results = {}

        for future in as_completed(future_to_lang):
            lang = future_to_lang[future]
            results[lang] = future.result()

    return "Translated text to multiple languages."
    
    
multiple_language_translate_def = {
    "type": "function",
    "function": {
        "name": "multiple_language_translate",
        "description": "Translate text to multiple languages.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to translate."
                },
                "languages": {
                    "type": "array",
                    "description": "The languages to translate to.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["text", "languages"]
        }
    }
}