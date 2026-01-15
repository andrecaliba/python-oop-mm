"""
Task Model Module

This module defines the Task class which represents a task object in the application.
It provides methods for creating, retrieving, updating, and deleting tasks from the database.
"""

from db import db, cursor


class Task():
    """
    Task model class representing a task in the task management system.
    
    Attributes:
        id (str): Unique identifier (UUID) for the task
        title (str): Task title/name
        description (str): Detailed description of the task
        due_date (str): Due date in YYYY-MM-DD format
        priority (str): Priority level (Low, Medium, High)
        status (str): Current status (Pending, In Progress, Completed)
        created_at (str): Timestamp when the task was created
    """
    def __init__(self, id, title, description, due_date, priority, status, created_at):
        """
        Initialize a Task object with the provided parameters.
        
        :param id: Unique identifier (UUID) for the task
        :param title: Task title/name
        :param description: Detailed description of the task
        :param due_date: Due date in YYYY-MM-DD format
        :param priority: Priority level (Low, Medium, High)
        :param status: Current status (Pending, In Progress, Completed)
        :param created_at: Timestamp when the task was created
        """
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = created_at
    
    @staticmethod
    def get(task_id):
        """
        Retrieve a task from the database by ID.
        
        Uses LIKE matching to allow partial UUID matching (first 8 characters).
        This provides a more user-friendly way to specify tasks.
        
        :param task_id: The ID or partial ID of the task to retrieve
        :return: Task object if found, None otherwise
        :raises: Catches and logs any database errors
        """
        try:
            # Query using LIKE for partial UUID matching
            cursor.execute("SELECT * FROM tasks WHERE id LIKE %s", (task_id + '%',))
            result = cursor.fetchone()
            
            if result:
                # Construct and return Task object from database result
                return Task(
                    id=result[0],
                    title=result[1],
                    description=result[2],
                    due_date=result[3],
                    priority=result[4],
                    status=result[5],
                    created_at=result[6]
                )
            return None
        except Exception as e:
            print(f"Error retrieving task: {e}")
            return None
    
    @staticmethod
    def get_all(sort_by=None):
        """
        Retrieve all tasks from the database with optional sorting.
        
        Supports sorting by:
        - due_date: Ascending order (earliest first)
        - priority: High to Low (High > Medium > Low)
        - status: Pending to Completed (Pending > In Progress > Completed)
        - None: Default database order
        
        :param sort_by: Optional sorting criteria ('due_date', 'priority', 'status')
        :return: List of Task objects sorted according to criteria
        :raises: Catches and logs any database errors
        """
        try:
            # Execute query based on sort criteria
            if sort_by == "due_date":
                # Sort by due date in ascending order
                cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
            elif sort_by == "priority":
                # Sort by priority level (High > Medium > Low)
                cursor.execute("""
                    SELECT * FROM tasks 
                    ORDER BY CASE priority_level 
                        WHEN 'High' THEN 1 
                        WHEN 'Medium' THEN 2 
                        WHEN 'Low' THEN 3 
                        ELSE 4 
                    END
                """)
            elif sort_by == "status":
                # Sort by status (Pending > In Progress > Completed)
                cursor.execute("""
                    SELECT * FROM tasks 
                    ORDER BY CASE status 
                        WHEN 'Pending' THEN 1 
                        WHEN 'In Progress' THEN 2 
                        WHEN 'Completed' THEN 3 
                        ELSE 4 
                    END
                """)
            else:
                # Default: no sorting
                cursor.execute("SELECT * FROM tasks")
            
            # Fetch all results and convert to Task objects
            results = cursor.fetchall()
            tasks = []
            
            for result in results:
                tasks.append(Task(
                    id=result[0],
                    title=result[1],
                    description=result[2],
                    due_date=result[3],
                    priority=result[4],
                    status=result[5],
                    created_at=result[6]
                ))
            
            return tasks
        except Exception as e:
            print(f"Error retrieving tasks: {e}")
            return []
    
    def save(self):
        """
        Save the current task to the database (insert new task).
        
        Inserts all task attributes into the database and commits the transaction.
        
        :return: True if successful, False otherwise
        :raises: Catches and logs any database errors
        """
        try:
            # Insert task data into database
            cursor.execute(
                """INSERT INTO tasks VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                (self.id, self.title, self.description, self.due_date, 
                 self.priority, self.status, self.created_at)
            )
            # Commit the transaction to save changes
            db.commit()
            return True
        except Exception as e:
            print(f"Error saving task: {e}")
            return False
    
    def update_details(self, title=None, description=None, due_date=None, priority=None):
        """
        Update task details including title, description, due date, and priority.
        
        Only updates fields that are provided (not None). Updates both the instance
        attributes and the database record.
        
        :param title: New title for the task (optional)
        :param description: New description for the task (optional)
        :param due_date: New due date for the task in YYYY-MM-DD format (optional)
        :param priority: New priority level for the task (optional)
        :return: True if successful, False otherwise
        :raises: Catches and logs any database errors
        """
        try:
            # Update title if provided
            if title is not None:
                self.title = title
                cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (title, self.id))
            
            # Update description if provided
            if description is not None:
                self.description = description
                cursor.execute("UPDATE tasks SET description = %s WHERE id = %s", (description, self.id))
            
            # Update due date if provided
            if due_date is not None:
                self.due_date = due_date
                cursor.execute("UPDATE tasks SET due_date = %s WHERE id = %s", (due_date, self.id))
            
            # Update priority if provided
            if priority is not None:
                self.priority = priority
                cursor.execute("UPDATE tasks SET priority_level = %s WHERE id = %s", (priority, self.id))
            
            # Commit the transaction to save all changes
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def update_status(self, status):
        """
        Update the status of the task.
        
        Updates the task status in both the instance and the database.
        
        :param status: New status - must be one of: 'Pending', 'In Progress', 'Completed'
        :return: True if successful, False otherwise
        :raises: Catches and logs any database errors
        """
        try:
            # Update instance status
            self.status = status
            # Update database record
            cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, self.id))
            # Commit the transaction
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            return False
    
    def delete(self):
        """
        Delete the task from the database.
        
        Permanently removes this task from the database.
        
        :return: True if successful, False otherwise
        :raises: Catches and logs any database errors
        """
        try:
            # Delete the task record from the database
            cursor.execute("DELETE FROM tasks WHERE id = %s", (self.id,))
            # Commit the transaction to apply the deletion
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def __str__(self):
        """
        String representation of the task for printing.
        
        Returns a concise summary of the task showing ID, title, status, priority, and due date.
        
        :return: Formatted string representation of the task
        """
        return (f"Task(id={self.id[:8]}..., title='{self.title}', "
                f"status='{self.status}', priority='{self.priority}', "
                f"due_date='{self.due_date}')")
    
    def __repr__(self):
        """
        Detailed representation of the task for debugging.
        
        Returns the same as __str__ for consistency.
        
        :return: Formatted string representation of the task
        """
        return self.__str__()
    
    def display(self):
        """
        Display a formatted and readable view of all task details.
        
        Prints the task information in a nicely formatted table with clear labels
        for each field, making it easy for users to review task information.
        """
        print("\n" + "="*60)
        print(f"ID:          {self.id}")
        print(f"Title:       {self.title}")
        print(f"Description: {self.description}")
        print(f"Due Date:    {self.due_date}")
        print(f"Priority:    {self.priority}")
        print(f"Status:      {self.status}")
        print(f"Created At:  {self.created_at}")
        print("="*60)