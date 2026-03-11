from gen.messages_pb2 import PRDetails, PRSummary
from gen.axiom_logger import AxiomLogger, AxiomSecrets


def git_hub_p_r_summarizer(log: AxiomLogger, secrets: AxiomSecrets, input: PRDetails) -> PRSummary:
    """Calls the Anthropic API to produce a one-paragraph plain-English summary of a pull request.

    Reads ANTHROPIC_API_KEY from secrets. Sends the PR title and body to
    claude-3-5-haiku-20241022 and returns a concise summary suitable for
    posting to a team channel.
    """
    import anthropic

    api_key, ok = secrets.get("ANTHROPIC_API_KEY")
    if not ok:
        log.error("git_hub_p_r_summarizer: ANTHROPIC_API_KEY secret not found")
        return PRSummary(summary="Error: ANTHROPIC_API_KEY secret not registered.", repo=input.repo, pr_title=input.pr_title)

    client = anthropic.Anthropic(api_key=api_key)

    prompt = (
        f"Summarise the following GitHub pull request in one concise paragraph "
        f"suitable for a team Slack channel. Focus on what changed and why.\n\n"
        f"Repository: {input.repo}\n"
        f"Author: {input.author}\n"
        f"Title: {input.pr_title}\n\n"
        f"Description:\n{input.pr_body}"
    )

    log.info("git_hub_p_r_summarizer: calling Anthropic", repo=input.repo, pr=input.pr_title)
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    summary = message.content[0].text.strip()
    log.info("git_hub_p_r_summarizer: done", summary_len=len(summary))
    return PRSummary(summary=summary, repo=input.repo, pr_title=input.pr_title)
