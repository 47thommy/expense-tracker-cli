# Expense Tracker CLI

## Project Description

The **Expense Tracker CLI** is a command-line interface application designed to help users track their expenses efficiently. Users can add, list, summarize, and delete expenses, as well as export them to a CSV file. The application integrates with OpenAI's GPT-based summarization for providing insightful summaries of expenses when an API key is provided. If the API is unavailable, the application falls back to summarizing the total expenses based on the amount.

## Features

- Add new expenses with a description, amount, and optional necessity flag.
- View all recorded expenses in a formatted table.
- Summarize expenses with or without OpenAI integration.
  - OpenAI-based summarization for detailed insights.
  - Fallback summarization for total expense amount.
- Summarize expenses optionally for a specific month.
- Delete specific expenses with confirmation.
- Export all expenses to a CSV file.

---

## How to Run the Application

### Prerequisites

2. **Environment Variables**:
   - Create a `.env` file in the project root and include your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
     - If no API key is provided, the summarization feature will fall back to calculating the total expenses.
3. **Required Libraries**: Install the dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/47thommy/expense-tracker-cli.git
   ```
2. Navigate to the project directory:
   ```bash
   cd expense-tracker-cli
   ```
3. Start the CLI application:
   ```bash
   python expense_tracker.py
   ```

---

## Available Commands

### 1. **Add an Expense**

Add a new expense to the tracker.

```
add -d <description> -a <amount> [-n]
```

- `-d`, `--description`: Description of the expense (required).
- `-a`, `--amount`: Amount of the expense (required).
- `-n`, `--necessary`: Mark the expense as necessary (optional).

**Example**:

```
add -d "Grocery Shopping" -a 50 -n
```

### 2. **List Expenses**

List all recorded expenses in a tabular format.

```
list
```

### 3. **Summarize Expenses**

Summarize all expenses, optionally for a specific month.

```
summary [-m <month>]
```

- `-m`, `--month`: Specify a month (e.g., `1` for January).

**Example**:

```
summary -m 12
```

- If OpenAI integration is enabled, detailed insights will be generated.
- If OpenAI integration is unavailable, the fallback will calculate the total amount spent.

### 4. **Delete an Expense**

Delete a specific expense by its ID with a confirmation prompt.

```
delete -i <id>
```

- `-i`, `--id`: ID of the expense to delete (required).

**Example**:

```
delete -i 3
```

### 5. **Export Expenses to CSV**

Export all recorded expenses to a CSV file.

```
export_csv
```

The CSV file will be saved as `report.csv` in the current directory.

### 6. **Exit the CLI**

Exit the application.

```
exit
```

---

### Notes

- Data is stored in a local JSON file (`expenses.json`). Ensure the file exists or will be created in the current directory.
- Summarization requires a valid OpenAI API key for GPT-based summaries; otherwise, the fallback summarization will be used.

---

### Project URL

```
https://roadmap.sh/projects/expense-tracker
```
