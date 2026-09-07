from ultralytics import YOLO


print("=" * 60)
print("DOK-ANPR MODEL TEST")
print("=" * 60)


# Vehicle
print("\n[1] Loading vehicle model...")

vehicle_model = YOLO(
    "models/vehicle/vehicle_model.pt"
)

print("[OK] Vehicle model loaded")
print("[CLASSES]")
print(vehicle_model.names)


# Plate
print("\n[2] Loading plate model...")

plate_model = YOLO(
    "models/plate/plate_model.pt"
)

print("[OK] Plate model loaded")
print("[CLASSES]")
print(plate_model.names)


print("\n" + "=" * 60)
print("ALL MODELS LOADED SUCCESSFULLY")
print("=" * 60)