# Data Processing & CSV (`std.csv`)

Sikhar includes a built-in CSV parsing and generation module (`std.csv`) designed for tabular data manipulation, data science preprocessing, and system reports.

---

## Importing

```sk
aayaat std.csv
```

Both English functions (`read`, `write`, `parse`, `stringify`) and Nepali equivalents (`padh`, `lekh`) are provided.

---

## Parsing In-Memory CSV Text

Parse raw CSV text into a list of row dictionaries (with headers) or a list of row string lists:

```sk
aayaat std.csv

rakha raw_csv = "id,name,role,salary\n1,Aayush,Engineer,85000\n2,Pooja,Architect,95000"

# Parse with headers (returns list of maps)
rakha rows = csv.parse(raw_csv, sacho)

ko_lagi row ma rows {
    dekha row["name"] + " works as " + row["role"] + " with salary " + row["salary"]
}
```

### Without Headers
```sk
rakha raw_table = "apple,10\nbanana,20\norange,15"
rakha records = csv.parse(raw_table, jutho)

# records is [["apple", "10"], ["banana", "20"], ["orange", "15"]]
dekha records[0][0] # apple
```

---

## Stringifying Tabular Data

Convert list data into formatted CSV strings:

```sk
rakha employees = [
    {"name": "Ram", "department": "Core Engine"},
    {"name": "Sita", "department": "Bytecode VM"}
]

# Convert to standard comma-separated text
rakha csv_text = csv.stringify(employees)
dekha csv_text

# Custom delimiter (e.g. semicolon or tab)
rakha tsv_text = csv.stringify(employees, ";")
```

---

## Reading and Writing CSV Files

Read directly from and write directly to disk files with automatic directory creation:

```sk
aayaat std.csv

rakha products = [
    {"sku": "SK-001", "name": "Mechanical Keyboard", "price": "120"},
    {"sku": "SK-002", "name": "Ultra-wide Monitor", "price": "450"}
]

# Write to file (English or Nepali: csv.lekh)
csv.write("data/products.csv", products)

# Read from file (English or Nepali: csv.padh)
rakha loaded_products = csv.read("data/products.csv", sacho)

dekha "Total products loaded: " + lamba(loaded_products)
dekha "First item: " + loaded_products[0]["name"]
```

---

## Function Summary

| Function | Nepali Alias | Parameters | Return Type | Description |
|---|---|---|---|---|
| `csv.parse(text, [has_headers=true], [delimiter=','])` | — | `text: str, ...` | `list` | Parses CSV string into maps or lists |
| `csv.stringify(rows, [headers_or_delimiter], [delimiter=','])` | — | `rows: list, ...` | `str` | Converts row list into CSV string |
| `csv.read(file_path, [has_headers=true], [delimiter=','])` | `csv.padh` | `path: str, ...` | `list` | Reads CSV file from disk |
| `csv.write(file_path, rows, [headers_or_delimiter], [delimiter=','])` | `csv.lekh` | `path: str, ...` | `bool` | Writes tabular rows to disk |
