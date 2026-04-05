# PawPal+ Project Reflection

## 1. System Design
Core Actions:

Be able to track pet care taks i.e allow user to add/edit tasks
Be able to create a daily plan based on the user constraints 
Lastly be able to display plan clearly 

Objects - Owner, Pet, Task, Scheduler

Owner - attributes: have a unique identifer,time constraints & priorties, methods: add/edit pets,
Pet - attributes: have a unique identifer, link up to owner, link up to tasks.
Task - attributes: link up to pet for specific task, method: add/edit tasks
Scheduler - attributes: get the time time constraints & priorties from the user, get the tasks for specific pets. method: create a daily plan, display the daily plan and explain the reasoning

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

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
