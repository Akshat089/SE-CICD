#!/usr/bin/env python3
"""
Unit tests for To-Do List CLI Application
"""

import unittest
import os
import json
import sys

# Add parent directory to path to import todo module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from todo import TodoList


class TestTodoList(unittest.TestCase):
    """Test cases for TodoList class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_filename = 'test_todos.json'
        self.todo_list = TodoList(filename=self.test_filename)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_add_task_success(self):
        """Test adding a valid task"""
        result = self.todo_list.add_task("Buy groceries")
        self.assertTrue(result)
        self.assertEqual(len(self.todo_list.todos), 1)
        self.assertEqual(self.todo_list.todos[0]['task'], "Buy groceries")
        self.assertFalse(self.todo_list.todos[0]['completed'])
    
    def test_add_empty_task(self):
        """Test adding an empty task should fail"""
        result = self.todo_list.add_task("")
        self.assertFalse(result)
        self.assertEqual(len(self.todo_list.todos), 0)
    
    def test_add_whitespace_task(self):
        """Test adding a whitespace-only task should fail"""
        result = self.todo_list.add_task("   ")
        self.assertFalse(result)
        self.assertEqual(len(self.todo_list.todos), 0)
    
    def test_add_multiple_tasks(self):
        """Test adding multiple tasks"""
        self.todo_list.add_task("Task 1")
        self.todo_list.add_task("Task 2")
        self.todo_list.add_task("Task 3")
        self.assertEqual(len(self.todo_list.todos), 3)
        self.assertEqual(self.todo_list.todos[0]['id'], 1)
        self.assertEqual(self.todo_list.todos[1]['id'], 2)
        self.assertEqual(self.todo_list.todos[2]['id'], 3)
    
    def test_list_tasks_empty(self):
        """Test listing tasks when list is empty"""
        result = self.todo_list.list_tasks()
        self.assertEqual(result, "No tasks found.")
    
    def test_list_tasks_with_items(self):
        """Test listing tasks with items"""
        self.todo_list.add_task("Task 1")
        self.todo_list.add_task("Task 2")
        result = self.todo_list.list_tasks()
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
    
    def test_complete_task_success(self):
        """Test marking a task as completed"""
        self.todo_list.add_task("Complete this task")
        result = self.todo_list.complete_task(1)
        self.assertTrue(result)
        self.assertTrue(self.todo_list.todos[0]['completed'])
    
    def test_complete_nonexistent_task(self):
        """Test completing a task that doesn't exist"""
        result = self.todo_list.complete_task(999)
        self.assertFalse(result)
    
    def test_delete_task_success(self):
        """Test deleting a task"""
        self.todo_list.add_task("Task to delete")
        self.assertEqual(len(self.todo_list.todos), 1)
        result = self.todo_list.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(self.todo_list.todos), 0)
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist"""
        result = self.todo_list.delete_task(999)
        self.assertFalse(result)
    
    def test_delete_task_reindexing(self):
        """Test that tasks are reindexed after deletion"""
        self.todo_list.add_task("Task 1")
        self.todo_list.add_task("Task 2")
        self.todo_list.add_task("Task 3")
        self.todo_list.delete_task(2)
        
        self.assertEqual(len(self.todo_list.todos), 2)
        self.assertEqual(self.todo_list.todos[0]['id'], 1)
        self.assertEqual(self.todo_list.todos[1]['id'], 2)
        self.assertEqual(self.todo_list.todos[1]['task'], "Task 3")
    
    def test_clear_all_tasks(self):
        """Test clearing all tasks"""
        self.todo_list.add_task("Task 1")
        self.todo_list.add_task("Task 2")
        self.todo_list.add_task("Task 3")
        result = self.todo_list.clear_all()
        self.assertTrue(result)
        self.assertEqual(len(self.todo_list.todos), 0)
    
    def test_persistence(self):
        """Test that todos are saved and loaded correctly"""
        self.todo_list.add_task("Persistent task")
        
        # Create a new TodoList instance with the same file
        new_todo_list = TodoList(filename=self.test_filename)
        self.assertEqual(len(new_todo_list.todos), 1)
        self.assertEqual(new_todo_list.todos[0]['task'], "Persistent task")
    
    def test_task_properties(self):
        """Test that tasks have all required properties"""
        self.todo_list.add_task("Test task")
        task = self.todo_list.todos[0]
        
        self.assertIn('id', task)
        self.assertIn('task', task)
        self.assertIn('completed', task)
        self.assertIn('created_at', task)
        
        self.assertIsInstance(task['id'], int)
        self.assertIsInstance(task['task'], str)
        self.assertIsInstance(task['completed'], bool)
        self.assertIsInstance(task['created_at'], str)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
