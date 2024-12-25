import cmd
from argparse import ArgumentParser
import json
import datetime


class Expense:
    def __init__(self, id, description, amount, necessary):
        self.id = id
        self.desctiption = description
        self.amount = amount
        self.necessary = necessary
        self.createdAt = datetime.datetime.now().isoformat()
        self.updatedAt = self.createdAt

    def to_dict(self) -> dict:
        """converts the expense object to dict"""
        return {
            "id": self.id,
            "description": self.desctiption,
            "amount": self.amount,
            "necessary": self.necessary,
        }


class ExpenseTrackerCLI(cmd.Cmd):
    prompt = "expense_tracker>>"
    intro = "Welcome to ExpenseTrackerCLI. type 'help' to see all available commans"

    def write_to_json_file(self, data):
        try:
            with open("expenses.json", mode="w", encoding="utf-8") as write_file:
                json.dump(data, write_file)
        except json.JSONDecodeError:
            print("Error Writing to expenses, the expense.json file is corrupted")
        except FileNotFoundError:
            print("the expenses.json file does not exist")

    def get_all_expenses(self) -> list:
        """retrieves all expenses from expenses.json"""
        try:
            with open("expenses.json", mode="r", encoding="utf-8") as read_file:
                expenses = json.load(read_file)
        except FileNotFoundError:
            with open("expenses.json", mode="w", encoding="utf-8") as write_file:
                json.dump([], write_file)
            return []
        except json.JSONDecodeError:
            print("Error reading expenses, the expenses.json file is corrupted")
            return []
        return expenses if expenses else []

    def get_next_id(self, expenses):
        return max((expense["id"] for expense in expenses), default=0) + 1

    def do_add(self, args):
        """adds a new expense"""
        parser = ArgumentParser(description="Add an expense to the tracker.")
        parser.add_argument(
            "--description", "-d", required=True, help="Description of the expense"
        )
        parser.add_argument(
            "--amount", "-a", required=True, help="Amount of the expense"
        )
        parser.add_argument(
            "--necessary",
            "-n",
            action="store_true",
            help="Mark the expense as ncessary",
        )

        try:
            parsed_args = parser.parse_args(args.split())
            description = parsed_args.description.strip().strip('"').strip("'")
            amount = parsed_args.amount
            necessary = parsed_args.necessary

            expenses = self.get_all_expenses()

            id = self.get_next_id(expenses)
            expense = Expense(id, description, amount, necessary).to_dict()
            expenses.append(expense)
            self.write_to_json_file(expenses)
            print(f"Expense {description} added sucessfully")
        except SystemExit:
            pass  # prevent argparse from exiting the program

    def do_exit(self, line):
        """command to exit the cli"""
        print("Goodbye")
        return True


if __name__ == "__main__":
    ExpenseTrackerCLI().cmdloop()
