# auto-domain-updater-gdb
Auto-update coded value domains in ArcGIS File Geodatabases using Python. Reads unique values from a feature class and updates an existing domain with only new entries. Designed for ArcGIS Pro 3.3+.
# Auto Domain Updater for File Geodatabases

This repository provides a simple, reusable workflow to **automatically update a coded value domain** in a File Geodatabase, based on values from another feature class. It solves a common problem faced by GIS professionals: ensuring consistency of attribute values like road names, sign codes, etc., across multiple layers—without repetitive manual domain updates.

---

## 🔧 What This Tool Does

✔ Reads a list of unique values from a source feature class  
✔ Adds only **new** values to an existing domain (no duplication or deletion)  
✔ Supports use cases like syncing road names or MUTCD codes  
✔ Logs changes for easy traceability  

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `createdata.py` | Creates a sample file geodatabase, schema, and dummy data for testing |
| `updatedomain.py` | Core script that updates a domain based on unique field values from a source feature class |
| `filegdbsample.zip` | Zipped sample File GDB with feature classes and domain applied (generated using `createdata.py`) |

---
## 🛠️ Requirements

- **ArcGIS Pro 3.3+**
- Python environment with `arcpy` (default with ArcGIS Pro)
- Windows OS (File GDB compatibility)

---

## 📝 How to Use

1. Unzip `filegdbsample.zip` to get the `.gdb`
2. Run `updatedomain.py` after updating the following parameters in the script:
   - `gdb_path` → path to your `.gdb`
   - `source_fc`, `source_field`
   - `target_domain_name`

The script will:
- Extract unique values from the source feature class
- Compare them against current domain values
- Add only the new ones
- Log everything in a file called `domain_update_log.txt`

---

## 🔍 Why This Matters

ArcGIS tools like attribute rules and domains are powerful—but maintaining them manually is tedious. This script offers a lightweight automation to keep domains clean, updated, and in sync with evolving datasets. Especially useful for municipalities, utilities, and asset management workflows.

---

## 🧠 Future Improvements (Ideas Welcome!)

- GUI with parameter selection  
- Integration with task scheduler  
- Option to delete obsolete domain values  
- Support for Enterprise Geodatabases  

---

## 🙌 Author
Surabhi Gupta
[GeoCloud Insights](https://geocloudinsights.substack.com)
