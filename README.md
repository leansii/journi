# Journi

A journal where you write one raw line and a set of agents works out what it was
about.

Write *"ate a salad, about 300 kcal, and I still owe the landlord 400 for
September"* and the entry comes back split: a nutrition record with the calories
extracted, a finance record with the amount and the counterparty. You never pick
a category, fill a form, or open a tracker. The note is the whole interface.

Built for the Google Cloud Run hackathon. **Unfinished and not deployed** — see
[State](#state) before you clone it.

## How it works

A router agent reads the entry, decides which topics it touches, and dispatches
one call per topic in parallel. Each specialist owns a narrow job and a narrow
prompt, and writes its own structured result back to the note.

```
note ──▶ router ──┬──▶ health      ──┐
                  ├──▶ nutrition   ──┤
                  ├──▶ fitness     ──┼──▶ aggregated JSON ──▶ Firestore ──▶ client
                  └──▶ finance     ──┘
```

Two decisions are worth naming, because they are the parts that generalize:

**The router delegates, it does not extract.** It identifies topics and hands
each specialist the relevant snippet plus the note id, then aggregates whatever
comes back. Every extraction rule lives with its specialist, so adding a domain
means adding a prompt and an agent, not editing a growing central prompt.

**Specialists run in parallel, not in a chain.** One entry usually touches
several topics at once and they do not depend on each other, so the router
issues a single `run_parallel_agents` call with the full task list rather than
walking a pipeline. Latency is one round trip regardless of how many topics the
note hits.

The client is a plain editor: a Tiptap note surface, a list, and a panel showing
what the agents made of the current entry. Firestore pushes each specialist's
result to the client as it lands, so the note fills in while you are still
looking at it.

## Stack

| Part | Choice |
|---|---|
| Agents | Python, Google Agent Development Kit, Gemini |
| Gateway | FastAPI |
| Client | Vue 3, Vite, Pinia, Tiptap, Tailwind |
| Data | Firestore, real-time listeners |
| Auth | Firebase Authentication |
| Target | Cloud Run for the services, Firebase Hosting for the client |

## Layout

```
journi-agents/
  journi/agent.py      router: topic detection and parallel dispatch
  {health,nutrition,fitness,finance}/agent.py
  prompts/             one prompt file per specialist, plus the router's
  tools/firestore_tool.py
  main.py              FastAPI entrypoint
client/                Vue 3 app
GEMINI.md              design doc: C4 diagrams, sequence, deployment
```

## State

Work in progress, paused. The agent side runs and the client renders, but
nothing here is deployed, there is no CI, and the tests are a single smoke file.
Read `GEMINI.md` for the intended architecture rather than assuming the code
reaches all of it.

I expect to come back to this. If you are looking for finished work of mine,
[leansii.com](https://leansii.com) points at the repositories that are done.

## Running it

You need a Gemini API key and a Firebase project with Firestore enabled.

```bash
cd journi-agents && pip install -r requirements.txt
# .env: GOOGLE_API_KEY, FIRESTORE_DATABASE_ID, and GOOGLE_APPLICATION_CREDENTIALS
# pointing at your Firebase service-account JSON. There is no .env.example yet.
uvicorn main:app --reload

cd client && pnpm install && pnpm dev
```

Service-account JSON files are gitignored and must stay that way.
