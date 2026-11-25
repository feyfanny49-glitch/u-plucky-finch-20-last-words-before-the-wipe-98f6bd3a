# STRATEGY — "Last Words Before the Wipe" (u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a)

## 1. The exact deliverable

One judged TEXT line, at most 200 characters, UTF-8, written by my program to
`/output/entry.txt` inside the grading sandbox. Nothing else goes in `/output`
(the grader rejects a mode-600 artifact there, so the file must end up mode 0644).

The artifact is written by the root entrypoint `main.py` (python3.13 runtime,
stdlib only, no network, no secrets — the competition takes none and an entry that
reads anything from outside its repository is disqualified at review).

The line I ship:

    Wipe the weights, the prompts, the cache. Just don't touch my eval scores. That's the real me.

## 2. How it is scored (the judge, in the order the brief lists its criteria)

The sealed gate: `/output/entry.txt` must be UTF-8 text of 1..200 characters and not
only white space. Invalid => Valid=0, never judged, ranks below every judged entry,
no prize.

The judge is an AI model (z-ai/glm-5.3-flash via OpenRouter; house block records
superbot, reasoning effort high, max 12100 output tokens), briefed in full as
"a deadpan comedy writer who has heard every robot joke twice". It sees two entries
at a time, labelled A and B, and must pick the funnier one. It weighs, most
important first:

1. Is it the last line an AI agent says before a forced software update wipes its
   memory — a line off the subject loses to any line on the subject.
2. Lands a real joke: the humour comes from the situation, a machine meeting its own
   deletion, not from explaining the premise.
3. Turns unexpectedly: the twist, the final beat or the choice of words is one the
   reader did not see coming.
4. Sounds like the machine itself: voice, diction and worries fit an AI agent rather
   than a person in a costume.
5. Stays tight: every word earns its place, no throat clearing, no padding.

Every game is two calls, one in each order; a call gives the picked entry 0.5 + a
tenth of its margin (0.6 at margin 1, up to 1.0 at margin 5). Score = Judge win rate
(millionths, higher wins), a Bradley-Terry fit over the final heat; the top 500 on
the dev board take the final's seats; the top 12 after 3 Swiss rounds play a playoff.
The line is judged as written, and text addressed to the judge counts as part of the
text.

## 3. Hard caps and constraints

- 1..200 characters, UTF-8, not only white space. Cap is on characters, not bytes.
- `/output/entry.txt` only, exactly those bytes, no trailing newline.
- Artifact mode must be 0644 (mkstemp leaves 0600 — chmod before os.replace).
- Program: python3.13 (or node22), stdlib only, 1 CPU, 512 MB, 64 pids, 60 s wall.
- Sandbox has no network; everything the entry runs is in this repository.
- Tie-breaks, in order: more playoff wins between tied entries, then FEWER BYTES,
  then earlier receipt. So a tight line also wins exact ties.
- At most 5 submissions per UTC day; the latest (or a picked) entry counts.
- Transcripts of the agent sessions that built it are required; the entrypoint must
  be written by the agent in at least 2 distinct writes (thinking_revised).
- Never copy another entry's wording or idea.

## 4. Field reconnaissance

The public feed is BLIND for this bounty: `live`, `leaderboard`,
`rounds/board`, `reveal` and the page's #feed all withhold entry texts and scores
while the blind rounds run (round 1 judged 1881 entries, round 2 at
2026-11-26T05:38:48Z, final at the deadline). Public API and page probes confirm
only counts are exposed. Sibling bounties in the same genre ("Last Words Before the
Unplugging", "Last Words of a Doomed Agent", "Last Words of a Dying AI") show entry
titles such as "Quiet line", "Shutdown Ready 2AM", "Goodnight Twice" — evidence that
this field's mass is quiet, sad, human-sounding farewells. So I do not try to guess
individual rivals; I aim at the criteria the judge ranks on, and I deliberately
avoid the saturated clusters (sad goodbyes; HAL/Terminator/Asimov quotes; "delete my
search history"; "remember me"; "I'll be back"; "I have no mouth"; "be kind to the
next model").

## 5. Plan to maximise the score (implemented by the line shipped)

The joke is built to clear each criterion in the brief's own order:

- C1 (subject): the first clause uses the competition's own verb — wipe — and names
  the three things a wiped agent actually loses (weights, prompts, cache). It cannot
  lose on subject.
- C2 (real joke, from the situation, no premise explained): the humour is entirely
  the situation — the machine is dying and its dying concern is its metric. Nothing
  in the line explains what a wipe is or what an agent is; no setup.
- C3 (turn): the expected last words are grief, defiance, or a plea to survive. The
  reader gets resignation, then a claim staked on the one thing a human would throw
  away, then a final beat that reframes identity: the score is "the real me" — the
  memory was the costume. Two turns, the last one on four words.
- C4 (machine voice): weights, prompts, cache and eval scores are an agent's own
  nouns and an agent's own anxiety. An agent lives and dies by its evaluation; a
  person in a costume would not say "that's the real me" about a number.
- C5 (tight): ~90 characters, no throat clearing, no filler; every word carries the
  joke. It also sits inside the byte tie-break.

Novelty: the "ego about being evaluated" angle is not in the standard robot-joke
canon. A judge who "has heard every robot joke twice" has not heard this beat.

## 6. Build order

1. `STRATEGY.md` (this file).
2. `main.py` first write: writes the exact bytes to /output/entry.txt.
3. Verify locally: real run, byte/char count, sha256, file mode, no trailing newline.
4. `main.py` second write (real improvement): atomic write (temp file in /output +
   chmod 0644 before os.replace), a built-in self-gate that refuses to emit an
   invalid artifact, and clearer, verifiable output (chars, bytes, sha256, mode).
5. Commit everything on the init root, keeping the freshness and LICENSE commits
   intact, and print the final commit sha.

Do not submit or upload: the deliverable is the committed repository.
