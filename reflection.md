# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design utilizes a composition-based object-oriented hierarchy. It maps out a clear, linear ownership flow where Owner objects contain Pet objects, and Pet objects contain their specific Task objects, while a centralized manager handles the system's core logic.

What classes did you include, and what responsibilities did you assign to each?

- Owner: Acts as the top-level user entity. It stores the owner's ID and name, and manages a list of Pet objects (handling adding and removing pets).

Pet: Represents the animal, storing demographic details (species, age) and maintaining a specific list of Task objects assigned to that pet.

Task: A data structure representing an event. It tracks scheduling specifics like start_time, end_time, priority, and whether the task is_recurring or is_completed.

ScheduleManager: The algorithmic brain of the app. It reads tasks from the pets to build a master_schedule, detects time overlaps, and sorts tasks into a daily agenda.

**b. Design changes**

- Did your design change during implementation?
  Yes — the relationship and statefulness of the scheduling logic evolved.
- If yes, describe at least one change and why you made it.
  I consciously shifted the ScheduleManager to be as stateless and algorithmic as possible, rather than having the Pet class handle scheduling validation. The manager now ingests tasks, performs conflict detection, sorts, and expands recurring occurrences. This simplifies testing and keeps UI concerns separate.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - Time windows (start_time / end_time / duration)
  - Priority (Priority enum used as tie-breaker)
  - Recurrence (daily/weekly simple expansion)
  - Completion status (is_completed) for agenda filtering

- How did you decide which constraints mattered most?
  I prioritized constraints that directly prevent double-booking (time windows) and help the owner make decisions quickly (priority and completed/pending state). Recurrence and unscheduled backlog help keep the daily agenda actionable without over-complicating input.

**b. Tradeoffs**

- **Describe one tradeoff your scheduler makes.**
  The scheduler strictly checks for exact time overlaps between task durations but does not account for transition or "buffer" time between different activities.
- **Why is that tradeoff reasonable for this scenario?**
  Adding buffer/transfer times would increase input complexity for users and require extra preferences (per-task or per-owner buffers). For a CLI/initial app, exact overlap prevention gives predictable behavior and keeps the UX simple.

---

## 3. AI Collaboration

**a. How you used AI**

- Copilot was used for: rapid code completion, generating docstrings and test scaffolding, suggesting small refactors (e.g., using list comprehensions), and proposing algorithms (recurrence expansion, lightweight conflict checks).
- Most effective Copilot features:
  - Inline completion for method bodies and clear docstring templates.
  - Test generation suggestions that speed up creating pytest cases.
  - Short code snippets showing idiomatic Python (lambda keys, sorted usage).

**b. Judgment and verification**

- One AI suggestion rejected or modified:
  Copilot suggested embedding scheduling checks inside `Pet.assign_task` (making Pets responsible for conflict detection). I rejected that to keep a single, testable scheduling authority (`ScheduleManager`) and avoid duplicating logic across Pets. This keeps ownership/concerns separated and simplifies testing.

- How I evaluated/verified suggestions:
  I wrote small pytest cases that asserted sorting, recurrence expansion, and conflict behavior immediately after accepting or modifying suggestions.

**c. Workflow / chat organization**

- Using separate chat sessions / focused prompts for design, implementation, and testing helped keep context small and made it easier to iterate: design chat for UML and API, implementation chat for code edits, testing chat for pytest scaffolding. Each phase produced concise artifacts (UML notes, code changes, tests) that I could verify independently.

**d. Lead architect takeaways**

- AI is a powerful collaborator but must be guided: accept high-value idiomatic snippets, reject or adapt suggestions that break architectural boundaries, and always add tests to verify behavior. Being the lead architect means deciding tradeoffs, keeping ownership clear, and using AI to speed implementation while retaining control over design choices.

---

## 4. Testing and Verification

**a. What you tested**

- Unit tests validate: Task behavior (completion, duration), Pet task assignment, sorting (time + priority), recurring expansion for daily agendas, and conflict detection + add/reject vs force-add.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  Reasonably confident for the covered behaviors (sorting, recurrence expansion, basic conflict detection). Edge cases remain (very large schedules, buffered transitions, complex recurrence rules).
- What edge cases would you test next if you had more time?
  - Multi-day recurring patterns and DST/daylight boundary behavior
  - Performance on large schedules (interval tree or bisect optimization)
  - Buffer/transition time handling and auto-rescheduling strategies

---

## 5. Reflection

**a. What went well**

- Rapid iteration using Copilot: generating tests and docstrings saved time; moving scheduling logic into a small manager made the code easy to reason about and test.

**b. What you would improve**

- Add interval-indexing for faster conflict queries and implement a simple auto-rescheduler that suggests the nearest free slot.

**c. Key takeaway**

- The best use of AI in software design is as an assistant to implement and prototype ideas quickly while keeping a human in the loop to enforce architecture, tradeoffs, and correctness with tests.
