from secretstuff import SecretStuffPipeline

pipeline = SecretStuffPipeline()

# Process complete files
# redact_result = pipeline.process_text_file(
#     input_file="outs/test.txt",
#     output_redacted="outs/redacted.txt",
#     output_identified="outs/entities.json",
#     output_mapping="outs/mapping.json"
# )
# print(redact_result)
# # Reverse from files
# reverse_result = pipeline.reverse_from_files("outs/updated_afterCloudcall.txt", "outs/mapping.json", "outs/final.txt")
# print(reverse_result)

text = """
text_to_be_redacted
"""

# Step 1: Just identify PII
entities = pipeline.identify_pii(text)
print(entities)

# Step 2: Redact when ready
redacted_text = pipeline.redact_pii(text)
print(redacted_text)


processed_text= """
processed_text_after_cloud_llm_call
"""
# Step 3: Reverse after processing
restored_text, _, _ = pipeline.reverse_redaction(processed_text)
print(restored_text)