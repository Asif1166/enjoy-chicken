import json
import shortuuid
from datetime import datetime

INPUT_FILE = "food_items.json"
OUTPUT_FILE = "food_items_fixture.json"
CATEGORIES_FILE = "categories_fixture.json"  # Your existing categories fixture

print("Loading input file...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = json.load(f)

data = raw[2]["data"]

# Load existing category IDs from your categories fixture
print("Loading existing categories...")
existing_category_ids = set()
try:
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        categories = json.load(f)
        for cat in categories:
            if cat.get("model") == "shop.category":
                existing_category_ids.add(cat.get("pk"))
    print(f"Found {len(existing_category_ids)} existing categories")
except FileNotFoundError:
    print(f"⚠️  Warning: {CATEGORIES_FILE} not found. Processing all items...")
    # If no categories file, we'll assume all category IDs are valid
    existing_category_ids = set(int(row["menu_id"]) for row in data)

fixtures = []
skipped_count = 0
added_count = 0

for row in data:
    category_id = int(row["menu_id"])

    if existing_category_ids and category_id not in existing_category_ids:
        skipped_count += 1
        print(f"⚠️  Skipping item '{row.get('name')}' - Category ID {category_id} does not exist")
        continue

    pid = shortuuid.ShortUUID(alphabet="abcdefgh12345").random(length=10)
    sku = "sku" + shortuuid.ShortUUID(alphabet="abcdefgh12345").random(length=10)

    # Handle price and discount calculations
    price = row.get("price")
    discount = int(row.get("discount", 0))
    old_price = None
    
    if price:
        price = float(price)
        if discount > 0:
            old_price = price
            price = price * (1 - discount / 100)

    # Parse dates properly
    created_at = row.get("created_at")
    updated_at = row.get("updated_at")
    
    if created_at:
        try:
            # Convert MySQL datetime to ISO format
            created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").isoformat()
        except:
            created_at = datetime.now().isoformat()
    else:
        created_at = datetime.now().isoformat()
    
    if updated_at:
        try:
            updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S").isoformat()
        except:
            updated_at = None
    
    fixtures.append({
        "model": "shop.product",
        "pk": int(row["id"]),
        "fields": {
            "pid": pid,
            "category": category_id,
            "title": row.get("name", ""),
            "eng_title": row.get("name", ""),
            "description": row.get("description", ""),
            "eng_description": row.get("description", ""),
            "offer_price": None,
            "price": f"{price:.2f}" if price else None,
            "old_price": f"{old_price:.2f}" if old_price else None,
            "specifications": None,
            "product_status": "published" if row.get("published") == "1" else "draft",
            "status": row.get("published") == "1",
            "in_stock": True,
            "featured": True,
            "digital": False,
            "sku": sku,
            "quantity": 100,
            "percentage": discount,
            "type": "Organic",
            "offer_countdown": None,
            "date": created_at,
            "updated": updated_at,
            "tax_applied": False,
            "offer_applied": discount > 0
        }
    })
    added_count += 1

print(f"\n✅ Successfully processed {added_count} items")
print(f"⚠️  Skipped {skipped_count} items (category not found)")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=2)

print(f"\n📁 Saved {len(fixtures)} items to {OUTPUT_FILE}")
print(f"\n📝 Next steps:")
print(f"1. Review the generated file: {OUTPUT_FILE}")
print(f"2. Load into database: python manage.py loaddata {OUTPUT_FILE}")