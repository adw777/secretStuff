from gliner import GLiNER
import json
from labels import labels

# Load the model
model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")

# Read text from test.txt
with open('test.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Function to split text into chunks of specified size
def chunk_text(text, chunk_size):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# Split text into 384-character chunks
chunks = chunk_text(text, 384)

# Process each chunk and collect all entities
all_entities = []

for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}/{len(chunks)}...")
    entities = model.predict_entities(chunk, labels)
    all_entities.extend(entities)

# Remove duplicates while preserving order
seen = set()
unique_entities = []
for entity in all_entities:
    entity_key = (entity["text"], entity["label"])
    if entity_key not in seen:
        seen.add(entity_key)
        unique_entities.append(entity)

# Create entity-label mapping for JSON output
entity_mapping = {}
for entity in unique_entities:
    entity_text = entity["text"]
    entity_label = entity["label"]
    
    if entity_label not in entity_mapping:
        entity_mapping[entity_label] = []
    
    if entity_text not in entity_mapping[entity_label]:
        entity_mapping[entity_label].append(entity_text)

# Save to JSON file
with open('identified.json', 'w', encoding='utf-8') as json_file:
    json.dump(entity_mapping, json_file, indent=2, ensure_ascii=False)

# Print all unique entities
print(f"\nFound {len(unique_entities)} unique entities:")
print("-" * 50)
for entity in unique_entities:
    print(f"{entity['text']} => {entity['label']}")

print(f"\nEntities saved to 'identified.json' with {len(entity_mapping)} different labels")