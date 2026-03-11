from gen.messages_pb2 import PRDetails, PRSummary
from nodes.git_hub_pr_summarizer import git_hub_pr_summarizer


class _NoOpLogger:
    """Minimal AxiomLogger implementation for unit tests."""
    def debug(self, msg: str, **attrs) -> None: pass
    def info(self, msg: str, **attrs) -> None: pass
    def warn(self, msg: str, **attrs) -> None: pass
    def error(self, msg: str, **attrs) -> None: pass


class _NoOpSecrets:
    def get(self, name: str):
        return "", False


def test_git_hub_pr_summarizer_missing_secret():
    """Without a secret, the node should return an error summary."""
    log = _NoOpLogger()
    secrets = _NoOpSecrets()
    pr = PRDetails(pr_title="Add streaming", pr_body="Adds SSE support.", repo="axiom/axiom", author="alice")
    result = git_hub_pr_summarizer(log, secrets, pr)
    assert isinstance(result, PRSummary)
    assert result.repo == "axiom/axiom"
    assert result.pr_title == "Add streaming"
    assert "ANTHROPIC_API_KEY" in result.summary
