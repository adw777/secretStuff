import json
import re

# Read the redacted text
with open('updated_afterCloudcall.txt', 'r', encoding='utf-8') as file:
    redacted_text = file.read()

# Read replacement mapping
with open('replacement_mapping.json', 'r', encoding='utf-8') as file:
    replacement_mapping = json.load(file)

# Create reverse mapping (dummy value -> original value)
reverse_mapping = {}
for original, dummy in replacement_mapping.items():
    reverse_mapping[dummy] = original

# Sort dummy values by length (longest first) to avoid partial replacements
sorted_dummies = sorted(reverse_mapping.keys(), key=len, reverse=True)

# Replace dummy values back to original values
final_text = redacted_text
replaced_count = 0

for dummy_value in sorted_dummies:
    original_value = reverse_mapping[dummy_value]
    
    # Escape special regex characters in the dummy value
    escaped_dummy = re.escape(dummy_value)
    
    # Count occurrences before replacement
    occurrences = len(re.findall(escaped_dummy, final_text, flags=re.IGNORECASE))
    
    if occurrences > 0:
        # Replace with case-insensitive matching
        final_text = re.sub(escaped_dummy, original_value, final_text, flags=re.IGNORECASE)
        replaced_count += occurrences
        print(f"Replaced '{dummy_value}' -> '{original_value}' ({occurrences} times)")

# Save final text
with open('final.txt', 'w', encoding='utf-8') as file:
    file.write(final_text)

print(f"\nReversal completed successfully. {replaced_count} total replacements made.")
print("Final text saved to 'final.txt'")