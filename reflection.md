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
es, the relationship and statefulness of the scheduling logic evolved.
- If yes, describe at least one change and why you made it.
I consciously shifted the ScheduleManager to be as stateless and algorithmic as possible, rather than having it permanently store duplicate state. Instead of the Pet class handling its own scheduling validation, the ScheduleManager acts independently—it accepts tasks, cross-references them to detect start/end overlaps, uses priority as a tie-breaker, and returns clean schedules. I made this change because keeping the manager stateless drastically simplifies automated testing and makes it much easier to integrate with the Streamlit UI later. Additionally, I ensured strict composition relationships (Owner -> Pet, Pet -> Task) so that deleting a parent object safely cascades and removes the associated child objects.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
