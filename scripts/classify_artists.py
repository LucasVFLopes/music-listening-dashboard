import os
import json
import time
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

# ========================
# CONFIGURAÇÕES
# ========================
INPUT_FILE = "artist_frequency.csv"
OUTPUT_FILE = "artist_classification.csv"
TOP_N = 1000

MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0
MAX_RETRIES = 3
SLEEP_BETWEEN_CALLS = 0.3

# ========================
# CLIENTE OPENAI
# ========================
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente.")

client = OpenAI(api_key=api_key)

# ========================
# PROMPTS
# ========================
SYSTEM_PROMPT = """
You are a music classification system.
Your task is to classify musical artists based on their overall musical style.
You must strictly follow the provided schema and allowed values.
Do not add explanations or extra text.
Always return valid JSON.
""".strip()

USER_PROMPT_TEMPLATE = """
Classify the following musical artist according to the schema below.

Artist name: "{artist_name}"

Schema:
{{
  "macro_genre": "rock | electronic | hip_hop | pop | reggae | metal | other",
  "sub_genre": "string (max 3 words)",
  "energy_level": "low | medium | high | very_high",
  "mood": ["calm | happy | aggressive | melancholic | psychedelic | energetic"]
}}

Rules:
- Choose ONE macro_genre.
- Choose ONE energy_level.
- Choose 1 to 3 moods.
- Do not include explanations.
- Do not include any text outside the JSON.
""".strip()

# ========================
# FUNÇÃO DE CLASSIFICAÇÃO
# ========================
def classify_artist(artist_name: str) -> dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": USER_PROMPT_TEMPLATE.format(
                            artist_name=artist_name
                        ),
                    },
                ],
            )

            content = response.choices[0].message.content.strip()
            parsed = json.loads(content)

            required_keys = {"macro_genre", "sub_genre", "energy_level", "mood"}
            if not required_keys.issubset(parsed.keys()):
                raise ValueError("JSON retornado incompleto.")

            return parsed

        except Exception as e:
            if attempt == MAX_RETRIES:
                print(f"❌ Falha ao classificar '{artist_name}': {e}")
                return {
                    "macro_genre": "other",
                    "sub_genre": "unknown",
                    "energy_level": "medium",
                    "mood": []
                }

            time.sleep(1.5 * attempt)

# ========================
# PIPELINE PRINCIPAL
# ========================
def main():
    df = pd.read_csv(INPUT_FILE)

    top_artists = df.head(TOP_N)["artist_clean"].tolist()
    print(f"Classificando Top {TOP_N} artistas...")

    results = []

    for artist in tqdm(top_artists):
        classification = classify_artist(artist)

        results.append({
            "artist_clean": artist,
            "macro_genre": classification["macro_genre"],
            "sub_genre": classification["sub_genre"],
            "energy_level": classification["energy_level"],
            "mood": ", ".join(classification["mood"]),
        })

        time.sleep(SLEEP_BETWEEN_CALLS)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("\n✅ Classificação concluída.")
    print(f"Arquivo gerado: {OUTPUT_FILE}")
    print(f"Total de artistas classificados: {len(out_df)}")

# ========================
# EXECUÇÃO
# ========================
if __name__ == "__main__":
    main()
