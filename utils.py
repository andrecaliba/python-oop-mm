"""
Task Management Utilities Module

This module contains the TaskManager class which handles all task-related operations,
including creation, retrieval, updating, and deletion of tasks.
"""

from uuid import uuid4
import time
import datetime
from db import cursor, db
from models.task import Task

# Current timestamp for task creation tracking
ts = time.time()


class TaskManager():
    """
    TaskManager class for managing all task-related operations.
    
    This class provides methods to add, list, update, mark as completed,
    and delete tasks from the database.
    """
    def __init__(self):
        """
        Initialize the TaskManager.
        
        No parameters are required as the TaskManager uses the global
        database connection established in db.py
        """
        # Private attribute to track if manager is initialized
        self.__initialized = True
    
    # ==================== Property Getters ====================
    
    @property
    def is_initialized(self):
        """Check if the TaskManager is properly initialized."""
        return self.__initialized
    
    # ==================== Public Methods ====================
    
    def add_task(self):
        """Add a new task and return the Task object."""
        title = input("Enter the title: ")
        description = input("Enter a description: ")
        month = enter_month()
        day = enter_day(month)
        year = enter_year()
        priority = enter_priority()
        status = enter_status()
        
        # Generate unique task ID and format due date
        task_id = str(uuid4())
        due_date = f"{year}-{month}-{day}"
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create Task object with provided details
        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
            created_at=timestamp
        )
        
        # Save task to database and display confirmation
        if task.save():
            print("\nTask added successfully!")
            task.display()
            return task
        else:
            print("\nFailed to add task.")
            return None
    def list_tasks(self):
        """
        Display all tasks from the database with optional sorting.
        
        Allows users to sort tasks by:
        - Due date (ascending)
        - Priority (High to Low)
        - Status (Pending -> In Progress -> Completed)
        - No sorting (default database order)
        
        :return: List of Task objects displayed
        """
        print("\nHow would you like to sort the tasks?")
        print("1. Due Date")
        print("2. Priority (High to Low)")
        print("3. Status")
        print("4. No sorting (default)")
        
        sort_choice = input("Enter your choice (1-4): ")
        
        # Map user choice to sorting column
        sort_map = {
            "1": "due_date",
            "2": "priority",
            "3": "status",
            "4": None
        }
        
        # Retrieve tasks with the selected sorting method
        tasks = Task.get_all(sort_by=sort_map.get(sort_choice))
        
        if not tasks:
            print("\nNo tasks found.")
            return []
        
        # Display formatted table header
        print("\n" + "="*120)
        print(f"{'ID':<38} {'TITLE':<20} {'DESCRIPTION':<25} {'DUE DATE':<12} {'PRIORITY':<10} {'STATUS':<15} {'CREATED AT':<20}")
        print("="*120)
        
        # Display each task in a formatted table row
        for task in tasks:
            # Truncate long values for better display
            task_id = task.id[:8] + "..."  # Show first 8 characters of UUID
            title = task.title[:20] if len(task.title) > 20 else task.title
            description = task.description[:25] if len(task.description) > 25 else task.description
            due_date = str(task.due_date)
            priority = task.priority
            status = task.status
            created_at = str(task.created_at)
            
            print(f"{task_id:<38} {title:<20} {description:<25} {due_date:<12} {priority:<10} {status:<15} {created_at:<20}")
        
        # Display table footer with total count
        print("="*120)
        print(f"\nTotal tasks: {len(tasks)}\n")
        
        return tasks
    
    def update_task(self):
        """
        Update the details of an existing task.
        
        Allows users to modify task properties including:
        - Title
        - Description
        - Due Date
        - Priority
        - Status
        
        :return: Updated Task object if successful, None otherwise
        """
        # Display all tasks to help user find the task ID
        self.list_tasks()
        task_id = input("\nEnter the task ID (you can use the first 8 characters): ")
        
        # Retrieve the task from database
        task = Task.get(task_id)
        
        if not task:
            print("Task not found!")
            return None
        
        print("\nCurrent task details:")
        task.display()
        
        print("\nWhat would you like to update?")
        print("1. Title")
        print("2. Description")
        print("3. Due Date")
        print("4. Priority")
        print("5. Status")
        
        choice = input("Enter your choice (1-5): ")
        
        # Update selected field
        if choice == "1":
            new_title = input("Enter new title: ")
            if task.update_details(title=new_title):
                print("Title updated successfully!")
        elif choice == "2":
            new_description = input("Enter new description: ")
            if task.update_details(description=new_description):
                print("Description updated successfully!")
        elif choice == "3":
            month = enter_month()
            day = enter_day(month)
            year = enter_year()
            new_date = f"{year}-{month}-{day}"
            if task.update_details(due_date=new_date):
                print("Due date updated successfully!")
        elif choice == "4":
            new_priority = enter_priority()
            if task.update_details(priority=new_priority):
                print("Priority updated successfully!")
        elif choice == "5":
            new_status = enter_status()
            if task.update_status(new_status):
                print("Status updated successfully!")
        else:
            print("Invalid choice!")
            return None
        
        # Retrieve and display updated task
        updated_task = Task.get(task.id)
        if updated_task:
            print("\nUpdated task details:")
            updated_task.display()
            return updated_task
        
        return None
    
    def mark_completed(self):
        """
        Mark a task as completed in the database.
        
        Updates the task status to 'Completed' and displays the updated task.
        
        :return: Updated Task object if successful, None otherwise
        """
        # Display all tasks for user reference
        self.list_tasks()
        task_id = input("\nEnter the task ID to mark as completed (you can use the first 8 characters): ")
        
        # Retrieve the task from database
        task = Task.get(task_id)
        
        if not task:
            print("Task not found!")
            return None
        
        # Update task status to Completed and display result
        if task.update_status("Completed"):
            print(f"\nTask '{task.title}' marked as completed!")
            task.display()
            return task
        else:
            print("Failed to mark task as completed.")
            return None
    
    def delete_task(self):
        """
            Delete a task from the database with user confirmation.
            
            Displays the task details and asks for confirmation before deletion
            to prevent accidental data loss. Forces user to respond with 'yes' or 'no'.
            
            :return: True if deletion successful, False otherwise
        """
        # Display all tasks for user reference
        self.list_tasks()
        task_id = input("\nEnter the task ID to delete (you can use the first 8 characters): ")
        
        # Retrieve the task from database
        task = Task.get(task_id)
        
        if not task:
            print("Task not found!")
            return False
        
        # Display task details before deletion
        task.display()
        
        # Force user to answer 'yes' or 'no'
        while True:
            confirm = input(f"\nAre you sure you want to delete this task? (yes/no): ").lower().strip()
            
            if confirm == "yes":
                # Delete task if user confirms
                if task.delete():
                    print(f"\nTask '{task.title}' deleted successfully!")
                    return True
                else:
                    print("Failed to delete task.")
                    return False
            elif confirm == "no":
                print("Deletion cancelled.")
                return False
            else:
                print("Invalid input! Please enter 'yes' or 'no'.")


# ==================== Private Utility Functions ====================
# These functions are helper utilities for user input validation and formatting.
# While not strictly private (Python doesn't enforce it), they are intended
# for internal use by the TaskManager class.

def enter_month():
    """
    Prompt user to enter a month number and validate input.
    
    Displays a numbered list of months and ensures the user selects
    a valid month (1-12).
    
    :return: Month number as a string ("1" through "12")
    """
    # Valid month numbers
    numbered_dates = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    
    while True:
        print("Enter the month by its number")
        print("1 - January")
        print("2 - February")
        print("3 - March")
        print("4 - April")
        print("5 - May")
        print("6 - June")
        print("7 - July")
        print("8 - August")
        print("9 - September")
        print("10 - October")
        print("11 - November")
        print("12 - December")
        try:
            user = input()
            if user not in numbered_dates:
                raise ValueError("Invalid month number")
            else:
                return user
        except ValueError:
            print("Invalid input. Please try again.")


def enter_day(month):
    """
    Prompt user to enter a day number and validate based on the month.
    
    Ensures the user enters a valid day for the given month,
    accounting for the number of days in each month.
    
    :param month: Month number as a string ("1" through "12")
    :return: Day number as a string ("1" through max days in month)
    """
    # Days in each month (non-leap year)
    days_in_month = {
        "1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30,
        "7": 31, "8": 31, "9": 30, "10": 31, "11": 30, "12": 31
    }
    max_day = int(days_in_month[month])
    
    while True:
        user = input(f"Enter the day between 1-{max_day}: ")
        try:
            if int(user) < 1 or int(user) > max_day:
                raise ValueError(f"Day must be between 1-{max_day}")
            else:
                return user
        except ValueError:
            print("Invalid input. Please try again.")

def enter_year():
    """
    Prompt user to enter a year and validate it's 2026 or later.
    
    Ensures the entered year is at least 2026 (the current year).
    
    :return: Year as a string
    """
    while True:
        year = input("Enter a year: ")
        try:
            if int(year) < 2026:
                raise ValueError("Year must be 2026 onwards")
            return year
        except ValueError:
            print("Invalid input. Please enter a valid year (2026 or later).")

def enter_priority():
    """
    Prompt user to select a priority level for a task.
    
    Displays priority options (Low, Medium, High) and validates the selection.
    
    :return: Priority level as a string ("Low", "Medium", or "High")
    """
    # Define priority options
    priorities = ["1. Low", "2. Medium", "3. High"]
    priorities_num = ["1", "2", "3"]
    priorities_dict = {"1": "Low", "2": "Medium", "3": "High"}
    
    # Display priority options
    for priority in priorities:
        print(priority)
    
    while True:
        user = input("Enter the priority by its number: ")
        try:
            if user not in priorities_num:
                raise ValueError("Must be 1, 2, or 3")
            return priorities_dict[user]
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")

def enter_status():
    """
    Prompt user to select a status for a task.
    
    Displays status options (Pending, In Progress, Completed) and validates the selection.
    
    :return: Status as a string ("Pending", "In Progress", or "Completed")
    """
    # Define status options
    statuses = ["1. Pending", "2. In Progress", "3. Completed"]
    statuses_num = ["1", "2", "3"]
    status_dict = {"1": "Pending", "2": "In Progress", "3": "Completed"}
    
    # Display status options
    for status in statuses:
        print(status)
    
    while True:
        user = input("Enter the status by its number: ")
        try:
            if user not in statuses_num:
                raise ValueError("Must be 1, 2, or 3")
            return status_dict[user]
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")