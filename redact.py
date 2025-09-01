# import json
# import re

# # Read identified entities
# with open('identified.json', 'r', encoding='utf-8') as file:
#     identified_entities = json.load(file)

# # Read original text
# with open('test.txt', 'r', encoding='utf-8') as file:
#     text = file.read()

# # Read dummy values
# with open('dummy_values.json', 'r', encoding='utf-8') as file:
#     dummy_values = json.load(file)

# # Create replacement mapping
# replacement_map = {}
# for label, entities in identified_entities.items():
#     if label in dummy_values:
#         dummy_value = dummy_values[label]
#         for entity in entities:
#             replacement_map[entity] = dummy_value

# # Sort entities by length (longest first) to avoid partial replacements
# sorted_entities = sorted(replacement_map.keys(), key=len, reverse=True)

# # Replace entities in text
# redacted_text = text
# for entity in sorted_entities:
#     # Use case-insensitive replacement and handle special characters properly
#     # Escape the entity for regex but don't use word boundaries for complex entities
#     escaped_entity = re.escape(entity)
    
#     # Use case-insensitive flag and replace all occurrences
#     redacted_text = re.sub(escaped_entity, replacement_map[entity], redacted_text, flags=re.IGNORECASE)

# # Save redacted text
# with open('redacted.txt', 'w', encoding='utf-8') as file:
#     file.write(redacted_text)

# print(f"Text redacted successfully. {len(replacement_map)} entities replaced.")
# print("Replacement mapping:")
# for original, dummy in replacement_map.items():
#     print(f"  '{original}' -> '{dummy}'")

# # Save replacement mapping to JSON
# with open('replacement_mapping.json', 'w', encoding='utf-8') as file:
#     json.dump(replacement_map, file, ensure_ascii=False, indent=4)



import json
import re
import random

# Read identified entities
with open('identified.json', 'r', encoding='utf-8') as file:
    identified_entities = json.load(file)

# Read original text
with open('test.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Read dummy values
with open('dummy_values.json', 'r', encoding='utf-8') as file:
    dummy_values = json.load(file)

# Create replacement mapping
replacement_map = {}
for label, entities in identified_entities.items():
    if label in dummy_values:
        dummy_data = dummy_values[label]
        
        # Check if dummy_data is a list or a single value
        if isinstance(dummy_data, list):
            # If we have multiple entities, ensure they get different dummy values
            # Create a shuffled copy to avoid repetition
            shuffled_dummies = dummy_data.copy()
            random.shuffle(shuffled_dummies)
            
            for i, entity in enumerate(entities):
                # Use modulo to cycle through dummy values if more entities than dummies
                dummy_value = shuffled_dummies[i % len(shuffled_dummies)]
                replacement_map[entity] = dummy_value
        else:
            # Single value, use it for all entities of this label
            for entity in entities:
                replacement_map[entity] = dummy_data

# Sort entities by length (longest first) to avoid partial replacements
sorted_entities = sorted(replacement_map.keys(), key=len, reverse=True)

# Replace entities in text
redacted_text = text
for entity in sorted_entities:
    # Use case-insensitive replacement and handle special characters properly
    escaped_entity = re.escape(entity)
    
    # Use case-insensitive flag and replace all occurrences
    redacted_text = re.sub(escaped_entity, replacement_map[entity], redacted_text, flags=re.IGNORECASE)

# Save redacted text
with open('redacted.txt', 'w', encoding='utf-8') as file:
    file.write(redacted_text)

print(f"Text redacted successfully. {len(replacement_map)} entities replaced.")
print("Replacement mapping:")
for original, dummy in replacement_map.items():
    print(f"  '{original}' -> '{dummy}'")

# Save replacement mapping to JSON for reference
with open('replacement_mapping.json', 'w', encoding='utf-8') as file:
    json.dump(replacement_map, file, ensure_ascii=False, indent=4)