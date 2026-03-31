# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial design focused on a strict object-oriented hierarchy to keep data modular and distinct. I mapped out a one-to-many relationship between Owners, Pets, and Tasks.

What classes did you include, and what responsibilities did you assign to each?

- Owner: Stores owner details and manages a list of Pet objects.

 Pet: Holds pet-specific data (name, species, age, medical needs) and maintains a personal schedule of tasks.

 Task: A data-heavy class representing an event (e.g., Feeding, Walk, Medication, Vet Appointment). It stores time, duration, priority level, and recurring status.

 ScheduleManager: The central "brain" or controller class. It takes tasks across all pets, handles sorting, detects scheduling conflicts, and processes recurring task generation.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
