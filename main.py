"""
Main Application Entry Point

This module serves as the entry point for the Task Management Application.
"""

from models.task import Task
from utils import TaskManager


def main():
    """
    Main function that runs the task management application.
    
    Displays an interactive menu allowing users to:
    - Add new tasks
    - View all tasks with sorting options
    - Update existing tasks
    - Mark tasks as completed
    - Delete tasks
    - Exit the application
    """
    # Define valid menu choices
    MAIN_CHOICES = "123456"
    
    # Initialize the TaskManager for handling task operations
    tm = TaskManager()
    
    # Main application loop
    while True:
        # Display welcome banner
        print("================================================")
        print("=  Welcome to the Task Management Application  =")
        print("================================================")

        # Display menu options
        print("\nChoose from the following:")
        print("1. Add a new task")
        print("2. List all tasks with optional filtering.")
        print("3. Update a task's details.")
        print("4. Mark a task as completed.")
        print("5. Delete a task.")
        print("6. Exit")

        # Get user input
        user = input("\nEnter your choice: ")
        
        # Process user choice
        if user == "1":
            # Add a new task to the database
            tm.add_task()
        elif user == "2":
            # Display all tasks with sorting options
            tm.list_tasks()
        elif user == "3":
            # Update an existing task
            tm.update_task()
        elif user == "4":
            # Mark a task as completed
            tm.mark_completed()
        elif user == "5":
            # Delete a task from the database
            tm.delete_task()
        elif user == "6":
            # Exit the application
            print("Exiting application. Goodbye!")
            break


if __name__ == "__main__":
    main()