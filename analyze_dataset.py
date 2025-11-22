from datasets import load_dataset
import json

# Load the dataset
print("Loading dataset...")
ds = load_dataset("gauravshrm211/VC-startup-evaluation-for-investment")
print("Dataset loaded successfully!")

# Print dataset information
print("\n=== DATASET INFO ===")
print(ds)
print(f"Total examples: {len(ds['train'])}")

# Show first few examples
print("\n=== SAMPLE EXAMPLES ===")
for i in range(min(3, len(ds['train']))):
    print(f"\nExample {i+1}:")
    example = ds['train'][i]
    print(f"Prompt: {example['prompt']}")
    print(f"Completion: {example['completion']}")
    print(f"Reasoning: {example['reasoning']}")

# Analyze the data structure
print("\n=== DATA STRUCTURE ANALYSIS ===")
prompts = [example['prompt'] for example in ds['train']]
completions = [example['completion'] for example in ds['train']]

print(f"Average prompt length: {sum(len(p) for p in prompts) / len(prompts):.2f} characters")
print(f"Average completion length: {sum(len(c) for c in completions) / len(completions):.2f} characters")

# Show some statistics
prompt_lengths = [len(p) for p in prompts]
completion_lengths = [len(c) for c in completions]

print(f"Prompt length range: {min(prompt_lengths)} - {max(prompt_lengths)} characters")
print(f"Completion length range: {min(completion_lengths)} - {max(completion_lengths)} characters")

# Check for any missing values
missing_reasoning = sum(1 for example in ds['train'] if example['reasoning'] is None)
print(f"Examples with missing reasoning: {missing_reasoning}/{len(ds['train'])}")

print("\n=== POTENTIAL USES ===")
print("1. Fine-tuning LLMs for VC startup evaluation")
print("2. Training a classifier for investment decisions")
print("3. Creating a question-answering system for startup analysis")
print("4. Building a recommendation system for VCs")
print("5. Developing an automated startup evaluation tool")

# Save a sample to JSON for inspection
sample_data = []
for i in range(min(10, len(ds['train']))):
    sample_data.append({
        "id": i,
        "prompt": ds['train'][i]['prompt'],
        "completion": ds['train'][i]['completion'],
        "reasoning": ds['train'][i]['reasoning']
    })

with open("sample_data.json", "w", encoding="utf-8") as f:
    json.dump(sample_data, f, indent=2, ensure_ascii=False)

print(f"\nSaved first 10 examples to sample_data.json for detailed inspection")