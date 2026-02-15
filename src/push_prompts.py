"""
Push de prompts otimizados para o LangSmith Prompt Hub.

- Lê prompts/bug_to_user_story_v2.yml
- Normaliza (se vier aninhado e com system_prompt/user_prompt)
- Valida (system/user, few-shot, 2+ techniques)
- Faz push para o LangSmith como: {LANGSMITH_USERNAME}/bug_to_user_story_v2
"""

import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any

from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

from utils import load_yaml, check_env_vars, print_section_header

# garante carregar o .env da raiz do projeto mesmo rodando de qualquer pasta
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env", override=True)

PROMPT_FILE = PROJECT_ROOT / "prompts/bug_to_user_story_v2.yml"
PROMPT_SLUG = "bug_to_user_story_v2"


def normalize_prompt_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza seu YAML para {system, user, metadata{description,tags,techniques}}."""
    data = dict(raw) if isinstance(raw, dict) else {}

    # formato: bug_to_user_story_v2: {...}
    if "bug_to_user_story_v2" in data and isinstance(data["bug_to_user_story_v2"], dict):
        data = data["bug_to_user_story_v2"]
    elif len(data) == 1:
        only_key = next(iter(data.keys()))
        if isinstance(data.get(only_key), dict):
            data = data[only_key]

    system = (data.get("system") or data.get("system_prompt") or "").strip()
    user = (data.get("user") or data.get("user_prompt") or "").strip()

    description = (data.get("description") or "").strip()
    tags = data.get("tags") or []
    techniques = data.get("techniques") or []

    if not isinstance(tags, list):
        tags = [str(tags)]
    if not isinstance(techniques, list):
        techniques = [str(techniques)]

    return {
        "system": system,
        "user": user,
        "metadata": {"description": description, "tags": tags, "techniques": techniques},
    }


def validate_prompt(prompt_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    system = (prompt_data.get("system") or "").strip()
    user = (prompt_data.get("user") or "").strip()
    metadata = prompt_data.get("metadata") or {}

    if not system:
        errors.append("Campo obrigatório ausente ou vazio: system (ou system_prompt no YAML).")
    if not user:
        errors.append("Campo obrigatório ausente ou vazio: user (ou user_prompt no YAML).")

    combined = f"{system}\n{user}".lower()
    fewshot_markers = ["few-shot", "exemplo", "entrada", "saída", "saida", "input", "output"]
    if not any(m in combined for m in fewshot_markers):
        errors.append("Não detectei Few-shot (inclua exemplos de entrada/saída).")

    techniques = metadata.get("techniques") or []
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("metadata.techniques deve conter pelo menos 2 técnicas.")

    if "todo" in combined:
        errors.append("Encontrado 'TODO' no prompt.")

    return (len(errors) == 0), errors


def build_prompt(prompt_data: Dict[str, Any]) -> ChatPromptTemplate:
    system = prompt_data["system"].strip()
    user = prompt_data["user"].strip()

    # garante variável do desafio
    if "{bug_report}" not in (system + "\n" + user):
        user = f"{user}\n\nRelato de bug:\n{{bug_report}}"

    return ChatPromptTemplate.from_messages([("system", system), ("user", user)])

def push_prompt_to_langsmith(prompt_identifier: str, prompt_data: Dict[str, Any]) -> str:
    """
    Push usando langsmith 0.7.x com autenticação via env vars.
    Não força tenant/org manualmente.
    """
    client = Client()

    prompt_obj = build_prompt(prompt_data)

    meta = prompt_data.get("metadata") or {}
    description = meta.get("description") or None
    tags = meta.get("tags") or None

    return client.push_prompt(
        prompt_identifier,
        object=prompt_obj,
        description=description,
        tags=tags,
    )

def main() -> int:
    print_section_header("PUSH DE PROMPTS OTIMIZADOS (LangSmith Hub)")

    check_env_vars(["LANGSMITH_API_KEY"])
    if not PROMPT_FILE.exists():
        print(f"ERRO: Arquivo não encontrado: {PROMPT_FILE}")
        return 1

    prompt_identifier = PROMPT_SLUG  # sem owner para evitar "another tenant"

    raw = load_yaml(str(PROMPT_FILE))
    prompt_data = normalize_prompt_data(raw)

    ok, errors = validate_prompt(prompt_data)
    if not ok:
        print("Prompt inválido. Corrija antes do push:")
        for e in errors:
            print(f" - {e}")
        return 1

    print(f"Fazendo push do prompt: {prompt_identifier}")
    try:
        url = push_prompt_to_langsmith(prompt_identifier, prompt_data)
        print(f"Push OK: {prompt_identifier}")
        print(f"{url}")
        print("Próximo passo: python src/evaluate.py")
        return 0
    except Exception as e:
        print(f"Erro ao fazer push: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())