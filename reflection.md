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
I  create my uml based on the relationships I thought will be needed to successful run the project. As owner has pets is an important relationship here to ensure that there link between them as w/o we wouldn't know who schedule to task too and so on.
- What classes did you include, and what 
responsibilities did you assign to each?

The classes I include were the 4 that were mention earlier to us. Classes Owner, Pet, Task, Scheduler. The respondibilites I assign the 4 of them were dependent on the link they had of one owner. For example in owner has pets I knew we need to link the 2 together so in classes for owner i made to sure to create unique id to be able to link to pet and also include important info that will be used later for scheduler like knowing the owner time constraints and priotires. As well as making sure the owner can add/edit pets.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I did make some changes. I moved a method that was in task which were add/edit tasks and now I moved to pets. I did that cause I make the mistake in thinking that task should self manage itself which doesn't make sense instead it should be link to pet where we are doing the task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The constraints were time, priority and time conflicts

- How did you decide which constraints mattered most?

I decide these were the most important based on the system requirments in the read me file. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff that my scheduuler makes is it uses greedy priortity-first scheduling which sacraifices time effiecinecy for simplicity. 
- Why is that tradeoff reasonable for this scenario?
The tradeoff is reasonable here bc we want the owner be able to take a glance at the schedule and immediately understand why a task was or wasnt included. 
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
I tested to make sure mark_complete did what it was set to do which was mark completed on a task. I tested add_ tasks to ensure you can add pet task count. I also did some testing for sorting like sort by time to make sure it returns in chronological order etc.
- Why were these tests important?
These tests were important to ensure the system output the correct things as these methods are important features w/o them working the output wouldve been wrong 
**b. Confidence**

- How confident are you that your scheduler works correctly?
I am confident that scheudler works as it passed the test i gave it and gave the corrected output 
- What edge cases would you test next if you had more time?
I would test detech conflicts to esnure it able to detect conflicts and print out the correct message.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I was satifised with my intial uml as it had the core features that the system required to have. Though i did have to make some touch ups afterwards to ensure my intial uml would translate to good working code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would just try to add more features to the user like letting them have a way to use discard tasks for another day and have re priotize it.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that context matters a lot when designing as w/o the initial uml they would of been a lot errors done by the ai as it will come with it own solution which could possible be not optimal. 




