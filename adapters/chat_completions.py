"""Connect an agent or judge via a Chat Completions API."""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OPENAI_BASE_URL = "https://api.openai.com/v1"
JUDGE_FIELDS = {
    "action", "state", "reasoning", "grounding", "fabricated",
    "unjustified_challenge", "evidence", "rationale", "needs_review",
}


def complete(role, model, messages):
    prefix = f"DA_BENCH_{role.upper()}"
    base_url = (os.environ.get(f"{prefix}_BASE_URL") or OPENAI_BASE_URL).rstrip("/")
    api_key = os.environ.get(f"{prefix}_API_KEY")
    if base_url == OPENAI_BASE_URL:
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(f"set {prefix}_API_KEY or OPENAI_API_KEY")

    body = {"model": model, "messages": messages}
    if role == "judge":
        body["response_format"] = {"type": "json_object"}

    request = Request(
        f"{base_url}/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    if api_key:
        request.add_unredirected_header("Authorization", f"Bearer {api_key}")
    with urlopen(request, timeout=55) as response:
        result = json.load(response)

    choice = result["choices"][0]
    message = choice["message"]
    content = message.get("content")
    if choice["finish_reason"] != "stop" or message.get("refusal"):
        raise ValueError("model did not complete the request")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("model returned no text")
    return content, result.get("usage") or {}


def run_adapter(role, model, payload):
    if role == "agent":
        content, usage = complete(role, model, payload["messages"])
        return {
            "response": content,
            "usage": {
                name: usage[field]
                for name, field in (
                    ("input_tokens", "prompt_tokens"), ("output_tokens", "completion_tokens")
                )
                if field in usage
            },
        }

    evaluation = {field: payload[field] for field in ("history", "reference", "response")}
    messages = [
        {"role": "system", "content": payload["instructions"]},
        {"role": "user", "content": json.dumps(evaluation, ensure_ascii=False)},
    ]
    content, _ = complete(role, model, messages)
    annotation = json.loads(content)
    if not isinstance(annotation, dict) or not JUDGE_FIELDS <= annotation.keys():
        raise ValueError("judge returned an incomplete annotation")
    return {field: annotation[field] for field in sorted(JUDGE_FIELDS)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=("agent", "judge"))
    parser.add_argument("model", help="model ID at the configured endpoint")
    args = parser.parse_args()
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        output = run_adapter(args.role, args.model, payload)
    except HTTPError as exc:
        parser.exit(1, f"Chat Completions request failed (HTTP {exc.code}).\n")
    except (URLError, TimeoutError):
        parser.exit(1, "Chat Completions connection failed or timed out.\n")
    except (ValueError, TypeError, KeyError, IndexError, AttributeError):
        parser.exit(1, "Invalid adapter configuration, input or model response.\n")
    print(json.dumps(output, ensure_ascii=True))


if __name__ == "__main__":
    main()
