# PawPal+ Project Reflection

## 1. System Design
    - a user should get a daily plan
    - add a pet
    -keep track of tasks

**a. Initial design**

- Briefly describe your initial UML design.
The UML has four classes. Owner: time budget, start time, and preferences. Pet: animal and owns the task list. Task: priority, duration, recurrence, and a scheduled_time slot which starts empty. Scheduler takes an Owner and a Pet, sorts and filters their tasks, fits them into the time budget, and produces the final plan with an explanation.

- What classes did you include, and what responsibilities did you assign to each?
Owner and Pet are both passive data holders, Task for priority, and Scheduler for the planning logic.


**b. Design changes**

- Did your design change during implementation?
Yes

- If yes, describe at least one change and why you made it.
 Owner/Pet not linkek, now checks if owner.pets and pet not in owner.pets and raises a ValueError immediately, so a mismatched pair fails at construction time instead of silently producing a wrong plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler considers three main factors: available time, task priority, and recurrence. Priority is the most important because essential tasks like feeding or medication should always be handled first. Available time is the next constraint since it limits how many tasks can be completed in a day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The scheduler uses a greedy approach, meaning it schedules higher-priority tasks first and skips tasks that no longer fit within the remaining time. This can sometimes leave out smaller tasks that could have fit together, but it keeps the scheduling process simple, predictable, and easy to understand. For a small daily pet-care schedule, this approach is practical and matches how most people naturally plan their day.

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
