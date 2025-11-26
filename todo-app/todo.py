#!/usr/bin/env python3
"""
To-Do List CLI Application
A simple command-line interface for managing your to-do tasks.
"""

import json
import os
import sys
from datetime import datetime


class TodoList:
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def add_task(self, task):
        """Add a new task to the todo list"""
        if not task or task.strip() == '':
            return False
        
        todo_item = {
            'id': len(self.todos) + 1,
            'task': task.strip(),
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.todos.append(todo_item)
        self.save_todos()
        return True

    def list_tasks(self):
        """List all tasks"""
        if not self.todos:
            return "No tasks found."
        
        output = []
        output.append("\n" + "="*60)
        output.append("YOUR TO-DO LIST")
        output.append("="*60)
        
        for todo in self.todos:
            status = "✓" if todo['completed'] else "✗"
            output.append(f"{todo['id']}. [{status}] {todo['task']}")
            output.append(f"   Created: {todo['created_at']}")
        
        output.append("="*60 + "\n")
        return "\n".join(output)

    def complete_task(self, task_id):
        """Mark a task as completed"""
        for todo in self.todos:
            if todo['id'] == task_id:
                todo['completed'] = True
                self.save_todos()
                return True
        return False

    def delete_task(self, task_id):
        """Delete a task by ID"""
        initial_length = len(self.todos)
        self.todos = [todo for todo in self.todos if todo['id'] != task_id]
        
        if len(self.todos) < initial_length:
            # Reindex the remaining tasks
            for i, todo in enumerate(self.todos):
                todo['id'] = i + 1
            self.save_todos()
            return True
        return False

    def clear_all(self):
        """Clear all tasks"""
        self.todos = []
        self.save_todos()
        return True


def print_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("TO-DO LIST CLI APPLICATION")
    print("="*60)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Clear All Tasks")
    print("6. Exit")
    print("="*60)


def main():
    """Main function to run the To-Do List application"""
    todo_list = TodoList()
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            task = input("Enter task description: ").strip()
            if todo_list.add_task(task):
                print("✓ Task added successfully!")
            else:
                print("✗ Failed to add task. Task cannot be empty.")
        
        elif choice == '2':
            print(todo_list.list_tasks())
        
        elif choice == '3':
            try:
                task_id = int(input("Enter task ID to complete: "))
                if todo_list.complete_task(task_id):
                    print(f"✓ Task {task_id} marked as completed!")
                else:
                    print(f"✗ Task {task_id} not found.")
            except ValueError:
                print("✗ Invalid input. Please enter a number.")
        
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to delete: "))
                if todo_list.delete_task(task_id):
                    print(f"✓ Task {task_id} deleted successfully!")
                else:
                    print(f"✗ Task {task_id} not found.")
            except ValueError:
                print("✗ Invalid input. Please enter a number.")
        
        elif choice == '5':
            confirm = input("Are you sure you want to clear all tasks? (yes/no): ").lower()
            if confirm == 'yes':
                todo_list.clear_all()
                print("✓ All tasks cleared!")
            else:
                print("Operation cancelled.")
        
        elif choice == '6':
            print("\nThank you for using To-Do List CLI!")
            sys.exit(0)
        
        else:
            print("✗ Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
