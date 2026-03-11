from gen.messages_pb2 import SlackMessage, SlackResult
from nodes.slack_notifier import slack_notifier


class _NoOpLogger:
    """Minimal AxiomLogger implementation for unit tests."""
    def debug(self, msg: str, **attrs) -> None: pass
    def info(self, msg: str, **attrs) -> None: pass
    def warn(self, msg: str, **attrs) -> None: pass
    def error(self, msg: str, **attrs) -> None: pass


class _NoOpSecrets:
    def get(self, name: str):
        return "", False


def test_slack_notifier_missing_secret():
    """Without a secret, the node should return ok=False with an error."""
    log = _NoOpLogger()
    secrets = _NoOpSecrets()
    msg = SlackMessage(text="Hello from Axiom!", channel="#axiom-demo")
    result = slack_notifier(log, secrets, msg)
    assert isinstance(result, SlackResult)
    assert result.ok is False
    assert "SLACK_WEBHOOK_URL" in result.error
