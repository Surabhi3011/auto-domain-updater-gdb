import arcpy
import os
import datetime

# === User Configuration ===
gdb_path = r"<GDBPath>/RoadNetwork.gdb"
source_fc = "roads"
source_field = "roadtype"

target_domain = "RoadNameDomain"
log_folder = r"<LogPath>\logs"
os.makedirs(log_folder, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_folder, f"domain_update_log_{timestamp}.txt")

# === Step 1: Get current domain values ===
existing_values = set()
for domain in arcpy.da.ListDomains(gdb_path):
    if domain.name == target_domain and domain.domainType == 'CodedValue':
        existing_values = set(domain.codedValues.keys())
        break

# === Step 2: Read unique road types from roads ===
new_values = set()
with arcpy.da.SearchCursor(os.path.join(gdb_path, source_fc), [source_field]) as cursor:
    for row in cursor:
        val = row[0]
        if val and val not in existing_values:
            new_values.add(val)

# === Step 3: Add new values to domain ===
if new_values:
    with open(log_file, "w") as log:
        log.write(f"Domain Update Log: {target_domain}\n")
        log.write(f"Timestamp: {timestamp}\n")
        log.write(f"Source: {source_fc}.{source_field}\n")
        log.write("New Values Added:\n")

        for val in sorted(new_values):
            arcpy.management.AddCodedValueToDomain(gdb_path, target_domain, val, val)
            log.write(f"- {val}\n")

    print(f"{len(new_values)} new values added to domain '{target_domain}'.")
    print(f"Log saved to: {log_file}")
else:
    print("No new domain values to add. Domain is already up to date.")