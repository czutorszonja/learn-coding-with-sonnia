# Mini Project 1: Study Task Tracker 📚

**Build a practical tool to track your study tasks!**

---

## What You'll Build

A program that helps you:
- ✅ Add study tasks to a list
- ✅ View all your tasks
- ✅ Mark tasks as complete
- ✅ See a summary of your progress

**Why this project?**
- Uses everything you've learned (functions, lists, loops, conditionals)
- Actually useful for exam preparation!
- No new concepts — just practice with what you know

---

## Step 1: Plan Your Program

Before coding, think about what you need:

**Data to store:**
- A list of tasks (strings)
- A way to track which tasks are complete

**Functions you'll need:**
- `add_task(tasks)` — Add a new task
- `view_tasks(tasks)` — Show all tasks
- `complete_task(tasks)` — Mark a task as complete
- `show_summary(tasks)` — Show completed vs pending

**Main program:**
- A while loop that shows a menu
- Get user input
- Call the right function based on input

---

## Step 2: Set Up Your Program

Start with this structure:

```python
# Study Task Tracker
# Your name here!

def add_task(tasks):
    # TODO: Add your code here
    pass

def view_tasks(tasks):
    # TODO: Add your code here
    pass

def complete_task(tasks):
    # TODO: Add your code here
    pass

def show_summary(tasks):
    # TODO: Add your code here
    pass

# Main program
def main():
    tasks = []  # Empty list to start
    
    while True:
        print("\n=== Study Task Tracker ===")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as complete")
        print("4. Show summary")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            show_summary(tasks)
        elif choice == "5":
            print("Good luck with your studies! 📚")
            break
        else:
            print("Invalid option. Try again!")

# Run the program
main()
```

---

## Step 3: Implement Each Function

### Function 1: `add_task(tasks)`

**What it should do:**
1. Ask the user what task they want to add
2. Add it to the tasks list
3. Confirm it was added

**Hint:** Use `input()` and `append()`!

---

### Function 2: `view_tasks(tasks)`

**What it should do:**
1. Check if there are any tasks
2. If empty, say "No tasks yet!"
3. If not empty, print each task with a number

**Hint:** Use `enumerate()` to number the tasks!

---

### Function 3: `complete_task(tasks)`

**What it should do:**
1. Show all tasks
2. Ask which task number to mark complete
3. Mark it as complete (you could add a ✓ symbol)

**Hint:** Lists are mutable — you can change items!

---

### Function 4: `show_summary(tasks)`

**What it should do:**
1. Count total tasks
2. Count completed tasks
3. Print a summary

**Hint:** You might need to track completed tasks separately!

---

## Step 4: Test Your Program

Run your program and try:
1. Add 3-4 tasks
2. View all tasks
3. Mark one as complete
4. Show summary
5. Exit

---

## Example Output

```
=== Study Task Tracker ===
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Show summary
5. Exit
Choose an option (1-5): 1

What task do you want to add? Study Python functions
Task added!

=== Study Task Tracker ===
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Show summary
5. Exit
Choose an option (1-5): 2

Your tasks:
1. Study Python functions
2. Review Lesson 7
3. Practice coding

=== Study Task Tracker ===
1. Add a task
2. View all tasks
3. Mark a task as complete
4. Show summary
5. Exit
Choose an option (1-5): 4

Summary:
Total tasks: 3
Completed: 0
Pending: 3
```

---

## Challenges (Optional)

Want to make it better? Try these:

### Challenge 1: Track Completed Tasks
Instead of just marking tasks, actually track which ones are done:
```python
# Use two lists
tasks = []
completed = []
```

### Challenge 2: Add Priority Levels
Let users mark tasks as high/medium/low priority:
```python
# Store tasks as tuples or lists
tasks = [
    ["Study Python", "high"],
    ["Review Lesson 7", "medium"]
]
```

### Challenge 3: Save to File
Research how to save tasks to a text file (so they persist after closing!)

---

## Tips

- **Start simple** — Get the basic version working first
- **Test as you go** — Test each function before moving to the next
- **Don't peek** — Try to solve it yourself before looking at the solution!
- **It's okay to struggle** — That's how you learn!

---

## Need Help?

If you get stuck:
1. Re-read the function description
2. Think about what tools you have (lists, loops, functions)
3. Try a simpler version first
4. Ask for help if you're really stuck!

---

## When You're Done

Celebrate! 🎉 You've built something real and useful!

Then you can:
- Use it to track your actual study tasks
- Add more features
- Share it with friends
- Move on to Lesson 8 (Dictionaries)!

---

**Good luck! You've got this! 💛**
