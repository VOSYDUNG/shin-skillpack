# Load into Grok, Gemini, Copilot, or any model behind an API

None of these have a skill loader. They all have one of: a custom-instructions field, a
system prompt, or an attachable file. That is enough.

## Grok (x.ai)

- **Custom instructions** — paste `portable/ROUTER-ONLY.md`. The field is not large; the
  router fits, a full bundle usually does not.
- **Per-conversation** — paste the relevant `portable/<domain>.bundle.md` as the first message
  of the chat, prefixed with: *"These are the procedures you follow for this conversation."*
  Then state your actual request. Grok holds it for the rest of the thread.
- **Files** — where Grok accepts an attachment, attach the bundle instead of pasting.

## Gemini (Gems)

Create a Gem, paste one `*.bundle.md` into the Gem's instructions, attach the others as
knowledge files. Same shape as a ChatGPT Custom GPT — see [`chatgpt.md`](chatgpt.md).

## Microsoft Copilot

Paste the bundle at the top of the conversation. Copilot's persistent-instruction surfaces vary
by tenant and license; the per-conversation paste always works.

## Any model via API (Claude API, OpenAI API, local Llama / Qwen / DeepSeek)

Read the bundle as the system prompt:

```python
from pathlib import Path
import anthropic

system = Path("portable/operations.bundle.md").read_text(encoding="utf-8")

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    system=system,                       # cache this — it is large and constant
    messages=[{"role": "user", "content": "/status-report weekly, kênh OTC"}],
)
print(msg.content[0].text)
```

Two notes for API use:

- **Cache the system prompt.** A bundle is 6k–30k tokens and never changes between turns. On
  the Claude API, mark it with `cache_control` and you pay for it once per cache window instead
  of once per turn.
- **Pick the bundle, not the all-in-one.** `SHIN-ALL-IN-ONE.bundle.md` is ~184 KB — it fits in
  a large context window, but routing accuracy drops and cost rises. Load the one domain the
  endpoint serves.

## Local models (Ollama, LM Studio)

Put a bundle in a Modelfile:

```
FROM qwen3:32b
SYSTEM """
<paste portable/operations.bundle.md here>
"""
```

Smaller models (under ~14B) follow the routing table but drift from the output templates.
If the deliverable's format matters — and for `/status-report`, `/write-spec`,
`/change-request` it does — load one skill's section rather than a whole bundle.

## The honest limits

| | |
|---|---|
| **Ports cleanly** | Every procedure, framework, checklist and output template. This is most of the pack. |
| **Needs pasted data** | Anything behind a `~~` placeholder — the skills assume connected systems. Paste the ticket list, metrics, or notes instead. |
| **Needs a filesystem** | `productivity` writes `TASKS.md`, `CLAUDE.md`, `memory/`. In a chat-only tool, keep those as documents you maintain. |
| **Claude-only** | `artifact-capabilities` — the `window.claude` runtime exists only in claude.ai Artifacts. Reference, not runnable. |
| **Lost** | Progressive disclosure. Claude Code loads one skill when needed; everywhere else the whole bundle sits in context, costing tokens on every turn. That is the price of portability. |
