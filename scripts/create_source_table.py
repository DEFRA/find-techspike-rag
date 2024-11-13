import duckdb
import pandas as pd
from pathlib import Path

# Connect to DuckDB
con = duckdb.connect('my_document_processor.duckdb', read_only=False)

# Create raw documents table
con.execute("""
CREATE TABLE IF NOT EXISTS raw_documents (
    id VARCHAR,
    filename VARCHAR,
    content TEXT,
    created_at TIMESTAMP
)
""")

# Load text files
files = Path('data/actions').glob('*.txt')
rows = []
for f in files:
    with open(f) as file:
        rows.append({
            'id': str(f.stem),
            'filename': f.name,
            'content': file.read(),
            'created_at': pd.Timestamp.now()
        })

# Insert data
df = pd.DataFrame(rows)
df.to_csv('data/raw_documents.csv', index=False)
con.register('df', df)
con.execute("INSERT INTO raw_documents SELECT * FROM df")

# List all tables
print(con.execute("SHOW TABLES").fetchall())

# Verify data was inserted
result = con.execute("SELECT * FROM raw_documents").fetchdf()
print(f"Inserted {len(result)} rows into raw_documents:")
print(result)

# Ensure changes are committed before closing
con.commit()
con.close()
  