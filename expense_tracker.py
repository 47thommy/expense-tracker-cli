import cmd
from argparse import ArgumentParser
import json
import datetime
import shlex
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
import os


class Expense:
    def __init__(self, id: int, description: str, amount: int, necessary: bool):
        self.id = id
        self.description = description
        self.amount = amount
        self.necessary = necessary
        self.createdAt = datetime.datetime.now().isoformat()

    def to_dict(self) -> dict:
        """converts the expense object to dict"""
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "necessary": self.necessary,
            "createdAt": self.createdAt,
        }


class ExpenseTrackerCLI(cmd.Cmd):
    prompt = "expense_tracker>>"
    intro = "Welcome to ExpenseTrackerCLI. type 'help' to see all available commans"

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.ai_summary = True
        try:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o-mini")
        except Exception as e:
            print(f"Error connecting to openai: {e}")
            print("All summaries will only summarize amount spent ")
            self.ai_summary = False
            pass
        self.current_year = datetime.datetime.now().year

    def summarizer(self, expenses):
        """summarizes expenses"""
        if self.ai_summary:
            print("summarizing expenses...")
            message = f"summerize the following expense data: {expenses}. your response should be in a readable format which will be displayed on a terminal"
            response = self.llm.invoke(message)
            return response.content
        else:
            total = sum((int(expense["amount"]) for expense in expenses))
            return f"Total expenses: {total}"

    def write_to_json_file(self, data):
        try:
            with open("expenses.json", mode="w", encoding="utf-8") as write_file:
                json.dump(data, write_file)
        except json.JSONDecodeError:
            print("Error Writing to expenses, the expense.json file is corrupted")
            return
        except FileNotFoundError:
            print("the expenses.json file does not exist")
            return

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

    def format_expenses(self, expenses: list) -> None:
        """Formats a list of expenses into a table and prints the table"""
        if not expenses:
            return "No expenses found."

        # Header for the table
        table = f"{'ID':<5}{'Date':<12}{'Description':<40}{'Amount':<10}\n"
        table += "-" * 77 + "\n"

        # Format each expense
        for expense in expenses:
            expense_date = datetime.datetime.fromisoformat(
                expense["createdAt"]
            ).strftime("%Y-%m-%d")
            table += f"{expense['id']:<5}{str(expense_date):<12}{expense['description']:<40}${expense['amount']:<10}\n"

        print(table)

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
            parsed_args = parser.parse_args(shlex.split(args))
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

    def do_list(self, line):
        """lists all expenses"""
        expenses = self.get_all_expenses()
        self.format_expenses(expenses)

    def do_summary(self, args):
        """summarizes all expenses"""
        parser = ArgumentParser(description="Summarize an expense for a specific month")
        parser.add_argument(
            "--month", "-m", help="Month of the current year to do summarization"
        )
        try:
            parsed_args = parser.parse_args(shlex.split(args))
            month = parsed_args.month
            expenses = self.get_all_expenses()
            if month:
                month = int(month)
                expenses = [
                    expense
                    for expense in expenses
                    if int(
                        datetime.datetime.fromisoformat(expense["createdAt"]).strftime(
                            "%m"
                        )
                    )
                    == month
                    and datetime.datetime.fromisoformat(expense["createdAt"]).year
                    == self.current_year
                ]
                if not expenses:
                    print(
                        f"you have no expenses at the specified month of year {self.current_year}"
                    )
                    return
            if not expenses:
                print("you have no expenses to summarize")

            summary = self.summarizer(expenses)
            print(summary)
        except SystemExit:
            pass  # prevent argparse from exiting the cli

    def do_delete(self, args):
        """deletes an expense"""

        parser = ArgumentParser(description="remove an expense from the tracker")
        parser.add_argument(
            "--id",
            "-i",
            required=True,
            help="Deletes an expense from the expense tracker",
        )

        try:
            parsed_args = parser.parse_args(shlex.split(args))
            id = int(parsed_args.id)
            confirmation = input(
                f"Are you sure you want to delete expense ID {id}? (y/n):"
            )
            if confirmation.lower() != "y":
                print("Deletion Cancelled")
                return
            expenses = self.get_all_expenses()
            initial_count = len(expenses)

            expenses = [expense for expense in expenses if expense["id"] != id]
            if initial_count == len(expenses):
                print(f"No expense with id {id} found")
                return
            self.write_to_json_file(expenses)
            print(f"expense with {id} id deleted succesfully")
        except SystemExit:
            pass  # prevent argparse from exiting the cli

    def do_export_csv(self, line):
        """exports expenses as a csv"""
        expenses = self.get_all_expenses()
        if not expenses:
            print("No expenses to export.")
            return
        try:
            df = pd.DataFrame(expenses)
            df.to_csv("report.csv", index=False)
            print(f"Expenses exported to csv:report.csv")
        except Exception as e:
            print(f"Error:{e}")

    def do_exit(self, line):
        """command to exit the cli"""
        print("Goodbye")
        return True


if __name__ == "__main__":
    ExpenseTrackerCLI().cmdloop()
