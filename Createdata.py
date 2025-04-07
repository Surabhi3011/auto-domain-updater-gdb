import arcpy
import os

# 1. Create File GDB
gdb_folder = r"<GDB_Folder_Path"
gdb_name = "RoadNetwork.gdb"
gdb_path = os.path.join(gdb_folder, gdb_name)

if not arcpy.Exists(gdb_path):
    arcpy.management.CreateFileGDB(gdb_folder, gdb_name)
    print(f"Created GDB: {gdb_path}")
else:
    print(f"GDB already exists: {gdb_path}")

arcpy.env.workspace = gdb_path
spatial_ref = arcpy.SpatialReference(4326)  # WGS 84

# 2. Create 'roads' feature class
roads_fc = "roads"
if not arcpy.Exists(os.path.join(gdb_path, roads_fc)):
    arcpy.management.CreateFeatureclass(gdb_path, roads_fc, "POLYLINE", spatial_reference=spatial_ref)
    arcpy.management.AddField(roads_fc, "roadtype", "TEXT", field_length=50)
    arcpy.management.AddField(roads_fc, "name", "TEXT", field_length=100)
    print("Created 'roads' feature class.")

# Sample data for 'roads' with dummy line geometries
roads_data = [
    ("Arterial", "Main St", [(0, 0), (1, 1)]),
    ("Collector", "River Rd", [(1, 1), (2, 2)]),
    ("Local", "Maple Ave", [(2, 2), (3, 3)]),
    ("Highway", "I-80", [(3, 3), (4, 4)]),
    ("Alley", "3rd Alley", [(4, 4), (5, 5)]),
]

with arcpy.da.InsertCursor(roads_fc, ["roadtype", "name", "SHAPE@"]) as cursor:
    for rt, name, coords in roads_data:
        array = arcpy.Array([arcpy.Point(x, y) for x, y in coords])
        polyline = arcpy.Polyline(array, spatial_ref)
        cursor.insertRow((rt, name, polyline))
print("Inserted sample data into 'roads'.")

# 3. Create 'roadnetwork' feature class
roadnet_fc = "roadnetwork"
if not arcpy.Exists(os.path.join(gdb_path, roadnet_fc)):
    arcpy.management.CreateFeatureclass(gdb_path, roadnet_fc, "POLYLINE", spatial_reference=spatial_ref)
    arcpy.management.AddField(roadnet_fc, "roadtype", "TEXT", field_length=50)
    arcpy.management.AddField(roadnet_fc, "segment_id", "TEXT", field_length=20)
    print("Created 'roadnetwork' feature class.")

roadnet_data = [
    ("SEG001", "Local", [(10, 0), (11, 1)]),
    ("SEG002", "Arterial", [(11, 1), (12, 2)]),
    ("SEG003", None, [(12, 2), (13, 3)]),
    ("SEG004", "Collector", [(13, 3), (14, 4)]),
]

with arcpy.da.InsertCursor(roadnet_fc, ["segment_id", "roadtype", "SHAPE@"]) as cursor:
    for sid, rt, coords in roadnet_data:
        array = arcpy.Array([arcpy.Point(x, y) for x, y in coords])
        polyline = arcpy.Polyline(array, spatial_ref)
        cursor.insertRow((sid, rt, polyline))
print("Inserted sample data into 'roadnetwork'.")

# 4. Create domain and assign to roadnetwork.roadtype
domain_name = "RoadNameDomain"
field_type = "TEXT"

# Delete if it already exists
if domain_name in [d.name for d in arcpy.da.ListDomains(gdb_path)]:
    arcpy.management.DeleteDomain(gdb_path, domain_name)
    print(f"Existing domain '{domain_name}' deleted.")

arcpy.management.CreateDomain(
    gdb_path,
    domain_name,
    "Valid Road Types",
    field_type,
    "CODED"
)
print(f"Created domain: {domain_name}")

# Add initial values
initial_codes = [("Arterial", "Arterial"), ("Local", "Local")]
for code, desc in initial_codes:
    arcpy.management.AddCodedValueToDomain(gdb_path, domain_name, code, desc)
print("Added initial domain values.")

# Assign domain to roadnetwork.roadtype
arcpy.management.AssignDomainToField(roadnet_fc, "roadtype", domain_name)
print(f"Domain '{domain_name}' assigned to 'roadnetwork.roadtype'.")

print("\nTest environment setup complete.")