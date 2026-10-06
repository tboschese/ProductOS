# ProductOS terminal

**Release:** 0.3.0-alpha.6 — local runtime preview

Use the terminal to create a product decision, supply context and evidence, connect your own
assistant, preserve its answer, and record your chosen decision. Generated answers stay distinct
from reviewed decisions and approved canonical knowledge.

## Install and start

From the ProductOS clone:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[terminal]'
productos
```

Python 3.9 or newer is required. The terminal dependency is optional; noninteractive commands
work with the base installation. A ProductOS repository supplies instructions and schemas.
Outside the clone, select it explicitly:

```bash
productos --repository /path/to/ProductOS --workspace /path/to/personal-workspace
```

By default, personal data goes to `~/.productos`, outside canonical knowledge. Use a terminal
of at least 80 columns and 24 rows; larger screens make evidence and answer reading easier.
Forms and panels support scrolling. The current interface is Portuguese; each decision's
analysis language can be Portuguese, English, or Spanish.

## First decision

1. Choose **Nova decisão**, enter a title and question, and select the analysis language.
2. Supply context, constraints, and unknowns in **Contexto**.
3. Add evidence with its source, locator, epistemic status, and limitations in **Evidências**.
   An attached UTF-8 text file is copied as evidence content; later changes to that original
   file do not alter an already frozen analysis input. Links are recorded, not fetched.
4. Select **Conexão de IA**. Saving configuration does not execute a model.
5. In **Análises**, request analysis or export context for manual exchange. Select a previous
   analysis to inspect its original response and the revision of the input it used.
6. Review the evidence and write your actual choice and next step in **Decisão**.

Shortcuts: `F2` new decision, `F6` save, `F5` analyze, `F4` connection,
`F8` cancel inference, `F10` save and exit, `Esc` close a form. `Ctrl+N`, `Ctrl+S`, `Ctrl+R`,
and `Ctrl+Q` are also available where the focused editor does not consume them. If inference is active,
exit first cancels it; exit again after cancellation. Text editors retain their own editing keys.

## Connections

### Manual: any assistant you can exchange text with

The initial connection is **Copiar e colar**. **Exportar contexto** freezes a packet, displays
its text and saved path, and creates an analysis awaiting a manual response. Send the packet to
your assistant, then use **Importar resposta** to paste its answer or select a UTF-8 response
file. The copy button uses the terminal's clipboard support, which varies by terminal; the
saved text packet is always available.

ProductOS records the requested model when declared. It does not independently verify which
model generated an imported answer. There is no automatic integration implied by owning a
browser chat subscription.

### Installed Codex

Select **Codex instalado**, choose a model if desired, and supply the CLI path when it is not
on `PATH`. Authentication stays with the CLI; authenticate using its own documented flow.
The adapter uses `codex exec` in a fresh, ephemeral, read-only workspace with a supplied
instruction bundle. It ignores unrelated user configuration and rejects observed tool events.
The [official OpenAI documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
describes non-interactive operation and existing CLI authentication.

```bash
productos connect --kind codex --model YOUR_AVAILABLE_MODEL
productos doctor
```

`doctor` checks executable availability and local paths without executing a model or verifying
authentication. The requested model is recorded; a reported model remains unknown when the
transport does not expose it. Context length, account access, and cost depend on the assistant.

### Custom command: another CLI or your own API bridge

Configure **Comando personalizado** with a JSON array of executable and arguments. The program
must accept one UTF-8 prompt on stdin, emit only its final answer on stdout, and exit zero on
success. An argument equal to `{model}` is replaced with the selected model. ProductOS does
not use a shell or interpolate prompt text into command arguments.

Example connection file, with a placeholder executable to replace with your own integration:

```json
{
  "schema_version": "0.1.0",
  "kind": "command",
  "model": "YOUR_AVAILABLE_MODEL",
  "command": ["/absolute/path/to/your-assistant-bridge", "--model", "{model}"],
  "timeout_seconds": 240
}
```

```bash
productos connect --file connection.json
```

Use the assistant's own authentication or environment-based credential handling; do not put
credential contents into command arguments or decision records. Generic commands run in a fresh
temporary directory. ProductOS cannot independently verify their internal tool use or model
identity. Native OpenAI, Anthropic, Gemini, or local-model API adapters are not bundled in this
release; manual exchange and a compatible command bridge provide the current portability.

## Noninteractive workflow

```bash
productos new --title 'Retention decline' --question 'Investigate or change onboarding?' --locale en
productos list
productos context DECISION_ID --file context.txt
productos evidence DECISION_ID --statement 'Reported decline' --source 'User report' \
  --locator 'Product meeting' --limitations 'No cohort data attached'
productos export DECISION_ID
productos import ANALYSIS_ID --file answer.txt
productos decide DECISION_ID --decision 'Validate measurement first' --next-action 'Compare cohorts'
productos show DECISION_ID
```

Replace `DECISION_ID` and `ANALYSIS_ID` with the generated identifiers. `productos analyze
DECISION_ID` invokes the configured assistant; in manual mode it creates a packet instead.
Global `--repository` and `--workspace` options go before the command.

`analyze` and `export` also accept `--structured` to request a JSON decision record. Valid JSON
is checked against the existing schema. Malformed or schema-invalid responses remain original
answers, accompanied by validation errors. Structural validity does not establish source
accuracy, reference completeness, or human approval. The terminal's normal flow uses Markdown.

## History, integrity, and recovery

- `decisions/`: schema-validated personal records with revisions, context, evidence, and the
  user's choice. Updates check for a stale revision.
- `analyses/ANALYSIS_ID/`: frozen `prompt.txt`, `instructions.txt`, and `decision.json`, plus
  `analysis.json` and the original `response.txt` after completion. SHA-256 checks detect changed
  snapshot or answer files. These are integrity checks, not cryptographic signatures.
- `connection.json`: local adapter configuration, with no credential fields.
- One writer owns a workspace lock. Abruptly interrupted inference is marked failed on the
  next opening; saved inputs remain available. Timeout, cancellation, and transport failure are
  distinct from completion. Existing completed answers are not overwritten by imports.

User decisions and responses are not copied into `knowledge/`. Save a separate workspace for
personal material. The current preview supports local use, not collaborative editing or a
portable standalone distribution with embedded knowledge.

## Qualification

Offline tests cover real subprocess transport using fake assistants, timeout/cancellation,
provenance, malformed output, and the terminal workflow at 120×40 and 80×24. A real Codex smoke
run verifies the runtime transport on an illustrative retention question. It is not a calibrated
behavioral baseline. The earlier [21-case pilot](../evals/baselines/seed-pilot-2026-10-05/README.md)
remains uncalibrated and fails its multilingual gate; arbitrary connected models are not
automatically qualified by that pilot.
