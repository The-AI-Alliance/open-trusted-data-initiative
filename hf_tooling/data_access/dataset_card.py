from huggingface_hub import DatasetCard

card_data = DatasetCard.load('HuggingFaceFW/fineweb-2').data

print(f"name {card_data.pretty_name}")
print(f"license {card_data.license}")
print(f"configs {card_data.configs}")
print(f"languages {card_data.language}")
print(f"size categories {card_data.size_categories}")
print(f"task categories {card_data.task_categories}")
