from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from langchain_core.load.dump import dumps
from langsmith import Client

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    prompt_ref: str = "leonanluppi/bug_to_user_story_v1"
    out_path: Path = Path("prompts/raw_prompts.yml")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s - %(message)s",
    )


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def serialize_prompt(pulled: Any) -> tuple[Dict[str, Any], str]:
    """
    Serializa o objeto retornado pelo LangSmith em um dict JSON-safe.
    Primeiro tenta `langchain_core.load.dump.dumps` (mais estruturado).
    Se falhar, cai para string.
    """
    try:
        prompt_data = json.loads(dumps(pulled))
        return prompt_data, "langchain_core.load.dump.dumps"
    except Exception as exc:  # pragmático: pode variar por versão/objeto
        LOG.exception("Falha ao serializar com dumps(); usando fallback.")
        return {"raw": str(pulled), "warning": f"Falhou ao usar dumps(): {exc!r}"}, "fallback str(pulled)"


def write_yaml(path: Path, payload: Dict[str, Any]) -> None:
    ensure_parent_dir(path)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            payload,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def pull_prompt(client: Client, prompt_ref: str) -> Any:
    try:
        return client.pull_prompt(prompt_ref)
    except Exception as exc:
        raise RuntimeError(f"Falha ao fazer pull do prompt '{prompt_ref}'. Verifique credenciais/ENV.") from exc


def main() -> int:
    setup_logging()
    load_dotenv()

    settings = Settings()
    client = Client()

    pulled = pull_prompt(client, settings.prompt_ref)
    prompt_data, serializer_used = serialize_prompt(pulled)

    payload: Dict[str, Any] = {
        "prompt_ref": settings.prompt_ref,
        "serializer_used": serializer_used,
        "prompt": prompt_data,
    }

    write_yaml(settings.out_path, payload)

    LOG.info("OK: prompt salvo em %s (serializer: %s)", settings.out_path, serializer_used)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
