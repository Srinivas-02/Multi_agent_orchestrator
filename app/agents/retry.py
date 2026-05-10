from app.agents.constants import MAX_VALIDATION_RETRIES


def should_retry(retry_count: int, max_retries: int = MAX_VALIDATION_RETRIES) -> bool:
    return retry_count < max_retries


def build_retry_message(error: str) -> str:
    return (
        "Your previous response was invalid.\n"
        f"Error: {error}\n"
        "Please return either a valid tool call or a non-empty final answer."
    )
