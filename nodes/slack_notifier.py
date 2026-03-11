from gen.messages_pb2 import SlackMessage, SlackResult
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def slack_notifier(log: AxiomLogger, secrets: AxiomSecrets, input: SlackMessage) -> SlackResult:
    """Posts a message to a Slack channel via an incoming webhook URL.

    Reads SLACK_WEBHOOK_URL from secrets. The webhook URL determines the default
    channel; input.channel is sent as an override only when non-empty. Returns
    SlackResult.ok=True on success or ok=False with an error description on failure.
    """
    import requests

    webhook_url, ok = secrets.get("SLACK_WEBHOOK_URL")
    if not ok:
        log.error("slack_notifier: SLACK_WEBHOOK_URL secret not found")
        return SlackResult(ok=False, error="SLACK_WEBHOOK_URL secret not registered.")

    payload: dict = {"text": input.text}
    if input.channel:
        payload["channel"] = input.channel

    log.info("slack_notifier: posting to Slack", text_len=len(input.text))
    response = requests.post(webhook_url, json=payload, timeout=10)

    if response.status_code == 200 and response.text == "ok":
        log.info("slack_notifier: message delivered")
        return SlackResult(ok=True, error="")

    log.error("slack_notifier: delivery failed", status=response.status_code, body=response.text)
    return SlackResult(ok=False, error=f"HTTP {response.status_code}: {response.text}")
