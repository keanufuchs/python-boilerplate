# Tablebuster

## Overview

This project processes CSV files, applies a series of transformations, and combines the results into a single Excel file. Each CSV file is added as a sheet in the Excel workbook, with the sheet name corresponding to the CSV filename.

### Requirements

* Python 3.10+
* Microsoft Excel source data as .xlsx
* Poetry or Pip for dependency installation.

Tested with:
* Python 3.10.12

### Setup

Clone the repository and change to directory.

   ```bash
   git clone git@gitlab.com:bechtle-cisco-devnet/datacenter/tablebuster.git
   cd tablebuster
   ```

(Recommended) Use a Python virtual environment. Pyenv example:

  ```bash
  pyenv virtualenv 3.10.12 tablebuster
  pyenv local tablebuster
  pyenv activate tablebuster
  ```

#### Poetry

Install dependencies via Poetry.

   ```bash
   poetry install
   ```

#### Pip

Install dependencies via Pip.

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

#### Tablebuster Configuration

All tool related configurations are handled through the `app/config/config.yml` file. This file defines:

- The paths for input/output data.
- CSV processing options (delimiter, encoding).
- The order in which operations are executed.

Additionally, the following option has been added:

- **verbose**: When set to `True`, all `DEBUG` logs will be sent to the console. If set to `False`, only `INFO` and higher levels will be shown.

```yaml
verbose: True # Set to False for higher log levels (INFO and above)
```

#### Sheet conversion/generation

All configuration related to the conversion and generation of the target data is drawn from one or more configuration files under `app/config/sheets`.
You can create your own nested directory structure to organize these files. All `.yml` files in this
directory structure will be merged into a single python dictionary.

See _Column Mapping_ for detailed instructions.

#### Logging Configuration

All configuration related to logging is set in `app/config/logging.json`. Refer to [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#custom-handling-of-levels) for more information.

### Execution

The project provides two primary command sections: `generate` and `confluence`. Below are the detailed instructions for each.

#### 1. **Export Confluence Tables**

Exports tables from Confluence local CSV files in the input folder. Each Confluence page has it's tables stored to a seperate
file.

```bash
python main.py confluence export-tables
```

**Description:**

- **Command**: `confluence`
- **Subcommands**: `export-tables`
- **Functionality**: Extracts tables from Confluence and exports them as CSV files into the input directory specified in `config.yml`.

#### 2. **Process CSV Files**

Processes CSV files by applying a series of transformations based on the configuration.

```bash
python main.py generate csv-to-excel [OPTIONS]
```

**Options:**

- `--filename "filename.csv"`: Process a specific CSV file or list of CSV files, seperated by comma. Defaults to None
- `--merge` or `-a`: Run the script for all CSV files in the input directory instead of a single file. Defaults to True.
- `--extend` or `-e`: Run additional sheet generation rules from the `CONFIG.sheets` section. Requires `--merge` to be set. Defaults to True.

**Examples:**

1. **Process a Single CSV File:**

   ```bash
   python main.py generate csv-to-excel "filename.csv"
   ```

2. **Export All Files with Deletion and Save to Output Folder:**

   ```bash
   python main.py generate csv-to-excel
   ```

#### **Execution Flow:**

1. **Export Confluence Tables:**
   - Run `python main.py confluence export-tables` to export tables from Confluence to the input folder.

2. **Process CSV Files:**
   - Depending on the options provided (`--filename`), the script will process the specified CSV files, apply sanity checks, remove duplicates, clean headers, and perform other transformations as defined in `config.yml`.

### Input & Output

- **Input Files**: The input directory is specified in the `config.yml` file under `input_path`.
- **Output Files**: All output will be stored as a single Excel file in the path specified under `output_path` and `output_file_name`. When using the `--deletefile` option, the processed CSV will be saved in the output folder with the provided filename.

### Logs

Logs are automatically generated and stored in `logs/app.log`. Verbose logging can be controlled with the `verbose` flag in the `config.yml`.

### CSV Processing Options

The way imported CSVs are processed can be modified through the operations defined in `config.yml`:

```yaml
execution_order:
  - remove_empty_rows
  - remove_duplicate_rows
  - extend_rows
  # - cleanup_headers
  # - line_filter
```

- **remove_empty_rows**: Removes empty rows from the data. (Default: `False`)
- **remove_duplicate_rows**: Removes duplicate rows from the data. (Default: `False`)
- **extend_rows**: Expands rows based on a delimiter found in specified columns.
- **cleanup_headers**: Cleans up headers in the CSV (Default: `False`).

### CSV Settings

```yaml
csv_delimiter: "," # CSV delimiter used for processing
csv_encoding: "utf-8" # CSV file encoding
header_row_count: 1 # Number of header Rows. Re-Occurring headers will be filtered from the result
```

### Row Operations

Here are the row processing operations explained:

- **remove_empty_rows**: Removes rows where all columns are empty.
- **remove_duplicate_rows**: Removes rows with duplicate content across all columns.
- **extend_rows**: Expands rows based on a delimiter found in certain columns.

**Example configuration for `extend_rows`:**

```yaml
extend_rows:
  - column: "Destination Group Name"
    delimiter: ";"
    extend: True
  - column: "Source Group Name"
    delimiter: ";"
    extend: True
```

### Line Filters

Specific rows can be filtered based on conditions defined in the `config.yml`. Rows that match these conditions will be removed.

**Example filter configuration:**

```yaml
line_filter:
  - column: "Source Group Name"
    condition: "contains"
    value: "?"
  - column: "Source Group Name"
    condition: "equals"
    value: ""
  - column: "Number"
    condition: "isempty"
    value: true
  - column: "Source Group Name"
    condition: "equals"
    value: "Posit Namespaces:"
```

### Column Mapping

The **Column Mapping** section defines how individual columns are processed, transformed, and combined during the CSV-to-Excel operation. You can apply various operations to either retrieve data from other sheets, manipulate values, or perform complex transformations such as conditionals, lookups, or regex replacements.

Here's a deeper explanation of the supported operations and elements involved:

#### Supported Operations:

1. **concat**: Concatenates multiple values together using a delimiter.
   - Combines values from columns or static values into a single string.
   - **Required fields**:
     - `delimiter`: The character used to separate values.
     - `elements`: The values to concatenate, defined as individual `value` operations.
2. **lookup**: Looks up a value from another sheet and replaces it based on a matching column.
   - Used for cross-referencing data between sheets.
   - **Required fields**:
     - `lookup_source`: Defines the column where the lookup value is found.
     - `lookup_target`: Defines the column where the corresponding value is retrieved.
3. **replace_pattern**: Uses a regular expression (regex) to find and replace parts of a string.
   - **Required fields**:
     - `search_pattern`: The regex pattern to search for.
     - `replace_pattern`: The string that will replace the matched pattern.
4. **condition**: Applies conditional logic to the values, performing operations based on whether a condition is met.
   - **Required fields**:
     - `values`: Defines the values to compare.
     - `operator`: Specifies the comparison operator (e.g., `==`, `!=`, `contains`).
     - `if_true`: Operation to perform if the condition is true.
     - `if_false`: Operation to perform if the condition is false.

#### Elements

There are two types of elements you can work with: **column** and **static**. These elements define where values come from and how they are used in operations.

1. **Column**:

   - Refers to a value from a specific column in a given sheet.
   - **Attributes**:
     - `type`: Always `"column"` for column references.
     - `name`: The name of the column to reference.
     - `sheet`: The sheet from which the column is sourced.
   - **Example**:
     ```yaml
     element:
       type: "column"
       name: "Source Zone"
       sheet: "Confluence_Export"
     ```

2. **Static**:

   - A fixed, constant value used in transformations.
   - **Attributes**:
     - `type`: Always `"static"` for static values.
     - `value`: The specific static value to use.
   - **Example**:
     ```yaml
     element:
       type: "static"
       value: "-"
     ```

#### Example of Column Mapping

In the following example, we are performing several operations, including concatenating values from columns, applying conditional logic, and using lookup and regex operations.

```yaml
Contracts:
  Name:
    operation: "concat"
    delimiter: "_"
    elements:
      - operation: "value"
        element:
          type: "column"
          name: "Source Zone"
          sheet: "Confluence_Export"
      - operation: "condition"
        values:
          - operation: "value"
            element:
              type: "column"
              name: "Source Namespace"
              sheet: "Confluence_Export"
          - operation: "value"
            element:
              type: "static"
              value: "-"
        operator: "!="
        if_true:
          operation: "concat"
          delimiter: "_"
          elements:
            - operation: "value"
              element:
                type: "column"
                name: "Source VRF"
                sheet: "Confluence_Export"
      - operation: "lookup"
        lookup_source:
          operation: "value"
          element:
            type: "column"
            name: "Source Group Name"
            sheet: "Confluence_Export"
        lookup_target:
          operation: "value"
          element:
            type: "column"
            name: "Group Name"
            sheet: "EPGs-Groups"
        if_true:
          operation: "condition"
          values:
            - operation: "value"
              element:
                type: "column"
                name: "EPG Name"
                sheet: "EPGs-Groups"
            - operation: "value"
              element:
                type: "static"
                value: "aci-containers-nodes"
          operator: "=="
          if_true:
            operation: "value"
            element:
              type: "column"
              name: "Source Group Name"
              sheet: "Confluence_Export"
          if_false:
            operation: "value"
            element:
              type: "column"
              name: "EPG Name"
              sheet: "EPGs-Groups"
              search_pattern: "((_mEPG)|(_EPG))"
              replace_pattern: ""
        if_false:
          operation: "value"
          element:
            type: "static"
            value: "EPG-not-found"
```

#### Detailed Operation Breakdown:

1. **Concatenation** (`concat`):
   - Combines values from multiple columns like `Source Zone`, `Source Namespace`, and `Source VRF` using an underscore (`_`) as a delimiter.
2. **Condition** (`condition`):
   - Checks if the `Source Namespace` is not equal to `"-"`. If true, it concatenates additional elements (e.g., `Source VRF`). If false, it applies a lookup operation.
3. **Lookup** (`lookup`):
   - If the `Source Group Name` from the `Confluence_Export` sheet matches a value in the `Group Name` column of the `EPGs-Groups` sheet, it retrieves the corresponding `EPG Name`. If no match is found, it uses a static value `"EPG-not-found"`.
4. **Regex Replacement** (`replace_pattern`):
   - For certain `EPG Name` values, it removes specific patterns like `"_mEPG"` or `"_EPG"` using regex.

### Final Notes

- Ensure that `CONFIG` and other dependent variables are correctly set up before using this class.
- The `csv_content` variable is critical throughout the class and must always be properly initialized.
- Make sure to handle any edge cases, such as empty CSV files or missing columns, to prevent runtime errors.
- Regularly update your `config.yml` to reflect any changes in processing requirements or new transformations.

---

## Additional Improvements and Best Practices

While the documentation has been updated to reflect your new command structures, here are some additional recommendations to enhance your project's functionality and maintainability:

### 1. **Argument Parsing Enhancements**

Ensure that your `main.py` effectively parses the new command-line arguments (`--deletefile`, `-d`, `--all`, `-a`). Using libraries like `argparse` or `click` can simplify this process and provide better user feedback.

**Example using `argparse`:**

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="CSV to Excel Processing Tool")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for 'confluence' command
    confluence_parser = subparsers.add_parser('confluence', help='Confluence related commands')
    confluence_subparsers = confluence_parser.add_subparsers(dest='subcommand')
    export_parser = confluence_subparsers.add_parser('export-tables', help='Export Confluence tables to CSV')

    # Subparser for 'run' command
    run_parser = subparsers.add_parser('run', help='Process CSV files')
    run_parser.add_argument('--filename', type=str, help='Name of the CSV file to process')
    run_parser.add_argument('--deletefile', '-d', type=str, help='Filename for exporting processed CSV')
    run_parser.add_argument('--all', '-a', action='store_true', help='Process all CSV files in the input directory')

    args = parser.parse_args()

    if args.command == 'confluence':
        if args.subcommand == 'export-tables':
            # Call the method to export tables
            export_confluence_tables()
    elif args.command == 'run':
        if args.all:
            # Process all CSV files
            process_all_csv_files(deletefile=args.deletefile)
        elif args.filename:
            # Process a specific CSV file
            process_single_csv_file(filename=args.filename, deletefile=args.deletefile)
        else:
            parser.error("Please specify either --filename or --all")

if __name__ == "__main__":
    main()
```

### 2. **Error Handling and Logging**

Ensure robust error handling throughout your script to manage unexpected scenarios gracefully. Enhance logging to provide more insightful information during execution.

**Example:**

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_csv_input(self) -> None:
    """Process a CSV file and apply a series of transformations based on the configuration."""
    try:
        # Existing processing logic
        ...
    except Exception as e:
        logger.error(f"An error occurred while processing the CSV file: {e}")
        raise
```

### 3. **Unit Testing**

Implement unit tests to ensure each component of your CSV processing pipeline works as expected. This will help in maintaining code quality and catching bugs early.

**Example using `unittest`:**

```python
import unittest
from app.csv_handler import CSVHandler

class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        self.handler = CSVHandler('test.csv')
        self.handler.csv_content = [
            ['Header1', 'Header2'],
            ['Data1', 'Data2'],
            ['Data3', 'Data4']
        ]

    def test_remove_empty_rows(self):
        # Add a row with empty data
        self.handler.csv_content.append(['', ''])
        self.handler.remove_empty_rows()
        self.assertEqual(len(self.handler.csv_content), 3)  # Header + 2 data rows

    def test_remove_duplicate_rows(self):
        # Add a duplicate row
        self.handler.csv_content.append(['Data1', 'Data2'])
        self.handler.remove_duplicate_rows()
        self.assertEqual(len(self.handler.csv_content), 3)  # Header + 2 unique data rows

if __name__ == '__main__':
    unittest.main()
```

### 4. **Documentation Enhancements**

Consider adding more detailed examples, especially for complex configurations like `Column Mapping`. Providing sample `config.yml` files and example CSV files can help users understand how to utilize the tool effectively.

### 5. **Configuration Validation**

Implement validation for your `config.yml` to ensure that all required fields are present and correctly formatted. This can prevent runtime errors due to misconfigurations.

**Example using `PyYAML` and `schema`:**

```python
import yaml
from schema import Schema, And, Or, Use, SchemaError

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    schema = Schema({
        'input_path': str,
        'output_path': str,
        'output_file_name': str,
        'csv_delimiter': str,
        'csv_encoding': str,
        'execution_order': [str],
        'sanity_checks': [{
            'column': str,
            'condition': Or('contains', 'equals', 'notempty'),
            'value': Or(str, None)
        }],
        'extend_rows': [{
            'column': str,
            'delimiter': str,
            'extend': bool
        }],
        'line_filter': [{
            'column': str,
            'condition': Or('contains', 'equals', 'isempty'),
            'value': Or(str, bool)
        }],
        'verbose': bool
    })

    try:
        validated_config = schema.validate(config)
        return validated_config
    except SchemaError as e:
        logger.error(f"Configuration validation error: {e}")
        raise

# Usage
CONFIG = load_config('app/config/config.yml')
```