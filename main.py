"""Contains Developer, QAEngineer and PM implementation.
class Developer
class Assignment
class Project
class QAEngineer
class ProjectManager
"""

from __future__ import annotations
import itertools
from datetime import datetime
from typing import List, Dict


class Developer:
    """Developer representation.
    Attributes:
        _id (int): Developers ID, is incremented for each instance.
        full_name (str): First + last names.
        address (str): Registration address.
        email (str): Personal company e-mail.
        phone_number (str) : Person's working phone number.
        position (str): Persons company position (e.g., 'Junior').
        salary (str): Salary amount (can be re-calculated).
        projects (List[Projects]): List of assigned projects
                            (many-to-many with Project instance).
        assignments (List[Assignment]): List of assigned tasks in
                                    Assignment container.
    """

    id_iter = itertools.count()

    def __init__(self, full_name: str, address: str, email: str,
                 phone_number: str, position: str, salary: str) -> None:
        """Developer's initializer.
        """
        self._id = next(self.id_iter)
        self.full_name: str = full_name
        self.address: str = address
        self.email: str = email
        self.phone_number: str = phone_number
        self.position: str = position
        self.salary: str = salary
        self.projects: List[Project] = []
        self.assignments: List[Assignment] = []

    def get_assigned_projects(self) -> List[str]:
        """Returns all project titles assigned to developer.
         Arguments:
            None.
        Returns:
            List[str], list of project titles
        """
        return [project.title for project in self.projects]

    def assign(self, project: Project) -> None:
        """Assigns current developer to project instance.
        Args:
            project (Project): Project instance to be assigned to developer.
        Returns:
            None.
        """
        if project in self.projects:
            raise ValueError(f"Project {project.title} already exists")
        self.projects.append(project)
        print(f"Project {project.title} has been added to developer "
              f"{self.full_name}")

    def cancel_appointment(self, project: Project) -> None:
        """Assigns current developer to project instance.
        Arguments:
            project (Project): Project instance to be removed from developer.
        Returns:
            None.
        """
        if project in self.projects:
            self.projects.remove(project)
            print(f"Project {project.title} has been removed from developer {self.full_name}")

    def __str__(self):
        """String representation of the Developer"""
        return f"Developer {self.full_name}"


class Assignment:
    """Assignment as the container for tasks.
    Related to Developer, QAEngineer and ProjectManager classes.
    Attributes:
        received_tasks (Dict): dictionary in form of
                        {date1: task1, date2: task2,...}.
                        Here date1, date2, ... are strings from datetime.
                        E.g., d = datetime.now(); d = d.utctime("%m/%d/%Y")
        is_done (bool): True, if all tasks are completed.
        description (str): General assignment description.
        status (str): Percent of completed tasks.
    """

    def __init__(self, description: str) -> None:
        """Assignment initializer."""
        self.description: str = description
        self.received_tasks: Dict = {}
        self.status: str = ""
        self.is_done = False

    def get_tasks_to_date(self, date: str) -> List:
        """Returns all tasks before date in arguments.
        Arguments:
            date (str): should be in format of '09/30/2022'!.
        Returns:
            List of tasks.
        """
        date_to_compare = datetime.strptime(date, "%m/%d/%Y")
        # List comprehension
        return [v for k, v in self.received_tasks.items()
                if datetime.strptime(k, "%m/%d/%Y") < date_to_compare]

    def calculate_status(self) -> None:
        """Calculates percentage of implemented tasks.
        Arguments:
            None.
        """
        tasks = [task for _, task in self.received_tasks.items()
                 if task["is_done"]]
        if tasks:
            self.status = str(100 * len(tasks) / len(self.received_tasks)) + "%"
        else:
            self.status = str("0%")


class Project:
    """Project representation.
    Attributes:
        title (str): Project's name.
        start_date (str): Start date.
        tasks_list (List): list of all tasks related to project.
        developers (List[Developer]): List of assigned developers.
        limit (int): specifies maximum number of workers.
    """

    def __init__(self, title: str, limit: int) -> None:
        """Project initializer."""
        self.title: str = title
        self.start_date: str = datetime.now().strftime("%m/%d/%Y")
        self.tasks_list: List[Dict] = []
        self.developers: List[Developer] = []
        self.limit: int = limit

    def add_developer(self, developer: Developer) -> None:
        """Assigns developer to project instance.
        Args:
            developer (Developer): Concrete developer to be assigned.
        Returns:
            None.
        """
        try:
            developer.assign(project=self)
        except ValueError:
            print(f"Developer {developer.full_name} exists")
        self.developers.append(developer)

    def remove_developer(self, developer: Developer) -> None:
        """Removes developer from project instance.
        Args:
            developer (Developer): Concrete developer to be removed.
        Returns:
            None.
        """
        developer.cancel_appointment(project=self)
        self.developers.remove(developer)


class QAEngineer:
    """QA engineer representation.
    Attributes:
        _id (int): QAEngineer ID, is incremented for each instance.
        full_name (str): First + last names.
        address (str): Registration address.
        email (str): Personal company e-mail.
        phone_number (str) : Person's working phone number.
        position (str): Persons company position (e.g., 'Junior').
        salary (str): Salary amount (can be re-calculated).
        projects (List[Projects]): List of assigned projects
                        (many-to-many with Project instance).
    """

    id_iter = itertools.count()

    def __init__(self, full_name: str, address: str, email: str,
                 phone_number: str, position: str, salary: str) -> None:
        """QAEngineer's initializer.
        """
        self._id = next(self.id_iter)
        self.full_name: str = full_name
        self.address: str = address
        self.email: str = email
        self.phone_number: str = phone_number
        self.position: str = position
        self.salary: str = salary
        self.projects: List[Project] = []

    def test_feature(self, assignment: Assignment) -> str:
        """Simply the stub method, will be implemented in future.
        Arguments:
            assignment (Assignment): assignment obtained from the developer.
        Returns:
            String contains dummy info about testing:).
        """
        return f"Assignment {assignment.description} has been tested " \
               f"by {self.full_name}"


class ProjectManager:
    """Project manager representation.
    Attributes:
        _id (int): PM's ID, is incremented for each instance.
        full_name (str): First + last names.
        address (str): Registration address.
        email (str): Personal company e-mail
        phone_number (str) : Person's working phone number.
        position (str): Persons company position (e.g., 'Junior').
        salary (str): Salary amount (can be re-calculated).
        project (Projects): Assume PM -> Project relation.
    """

    id_iter = itertools.count()

    def __init__(self, full_name: str, address: str, email: str,
                 phone_number: str, position: str, salary: str,
                 project: Project) -> None:
        """ProjectManager initializer.
        """
        self._id = next(self.id_iter)
        self.full_name: str = full_name
        self.address: str = address
        self.email: str = email
        self.phone_number: str = phone_number
        self.position: str = position
        self.salary: str = salary
        self.project: project = project

    def discuss_progress(self, developer: Developer) -> str:
        """Simply the stub method, will be implemented in future.
        Arguments:
            developer (Developer): Processing the developer's progress.
        Returns:
            String contains dummy discussion:).
        """

        # Let's obtain each assignment description.
        descriptions = [assignment.description for assignment in developer.assignments]
        # concat list of strings (descriptions) into one string
        descriptions = " ".join(descriptions)
        return f"Task's progress of {descriptions} has been tested " \
               f"by {self.full_name}"
