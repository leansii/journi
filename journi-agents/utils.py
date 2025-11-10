import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
GEMINI_2_5_FLASH = "gemini-2.5-flash"

def load_prompt(prompt_filename: str) -> str:
    """Loads a prompt from the root 'prompts' directory."""
    prompt_path = os.path.join(PROMPTS_DIR, prompt_filename)
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error(f"Prompt file not found at: {prompt_path}")
        # Возвращаем заглушку, чтобы агент не падал совсем, но было видно ошибку
        return f"ERROR: Prompt {prompt_filename} not found."