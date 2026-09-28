"""Load InteRecAgent runtime configuration from the project .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"


def load_project_env() -> Path:
    """Load .env defaults without overriding variables supplied by the OS."""
    env_file = Path(os.environ.get("INTERECAGENT_ENV_FILE", DEFAULT_ENV_FILE))
    load_dotenv(dotenv_path=env_file, override=False)

    # A local Codex server exposes an OpenAI-compatible chat-completions API.
    # Select it with LLM_PROVIDER=codex while preserving the original OpenAI/
    # Azure configuration in the .env file for easy switching.
    if os.environ.get("LLM_PROVIDER", "open_ai").strip().lower() == "codex":
        codex_url = os.environ.get(
            "CODEX_AS_API_URL", "http://127.0.0.1:18080/v1/chat/completions"
        ).strip()
        suffix = "/chat/completions"
        if codex_url.rstrip("/").endswith(suffix):
            codex_url = codex_url.rstrip("/")[:-len(suffix)]

        os.environ["OPENAI_API_BASE"] = codex_url
        os.environ["OPENAI_API_KEY"] = os.environ.get("CODEX_API_KEY", "EMPTY")
        # Keep the provider identity available to the direct client. Callers
        # backed by legacy LangChain normalize this to its `open_ai` spelling.
        os.environ["OPENAI_API_TYPE"] = os.environ.get("CODEX_API_TYPE", "codex")
        os.environ["AGENT_ENGINE"] = os.environ.get("CODEX_MODEL", "gpt-5.6-sol")
        os.environ["OPENAI_ENGINE"] = os.environ["AGENT_ENGINE"]
        os.environ["OPENAI_ENGINE_TYPE"] = "chat"

    # Both names occur in the original evaluation scripts. Keep them synchronized.
    agent_engine = os.environ.get("AGENT_ENGINE") or os.environ.get("OPENAI_ENGINE")
    if agent_engine:
        os.environ.setdefault("AGENT_ENGINE", agent_engine)
        os.environ.setdefault("OPENAI_ENGINE", agent_engine)

    # A separate simulator account is optional; default it to the agent account.
    fallbacks = {
        "SIMULATOR_API_KEY": "OPENAI_API_KEY",
        "SIMULATOR_API_BASE": "OPENAI_API_BASE",
        "SIMULATOR_API_TYPE": "OPENAI_API_TYPE",
        "SIMULATOR_API_VERSION": "OPENAI_API_VERSION",
        "SIMULATOR_ENGINE": "OPENAI_ENGINE",
    }
    for target, source in fallbacks.items():
        if not os.environ.get(target) and os.environ.get(source):
            os.environ[target] = os.environ[source]

    return env_file


ENV_FILE = load_project_env()


__all__ = ["PROJECT_ROOT", "DEFAULT_ENV_FILE", "ENV_FILE", "load_project_env"]
