import cmd


class ExpenseTrackerCLI(cmd.Cmd):
    prompt = "expense_tracker>>"
    intro = "Welcome to ExpenseTrackerCLI. type 'help' to see all available commans"

    def do_exit(self, line):
        """command to exit the cli"""
        print("Goodbye")
        return True


if __name__ == "__main__":
    ExpenseTrackerCLI().cmdloop()
