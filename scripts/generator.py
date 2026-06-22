import json
from json import load
from dataclasses import asdict
from pathlib import Path
from items import MinecraftRootModel, SelectModel, CaseItem, InnerModel

class Generator:
	def __init__(self, path: Path, model_items: dict):
		self.path = path
		self.model_items = model_items

	def format_item_name(self, model_path: str) -> str:
		pure_name = model_path.split("/")[-1]
		return pure_name.replace('_', ' ').replace(".json", '').title()

	def generate_item_files(self):
		print("\n\u001B[34;44mINFO\u001B[0m \u001B[32mMemulai Generate Rename Item\u001B[0m\n")

		for material_id, model_list in self.model_items.items():
			item_file_target =  Path(f"pack/assets/minecraft/items/{material_id.path}.json")
			item_file_target.parent.mkdir(parents=True, exist_ok=True)

			root_model = MinecraftRootModel(model=SelectModel())
			root_model.model.fallback.model = f"minecraft:item/{material_id.path}"
			if item_file_target.exists():
				try:
					with open(item_file_target, 'r', encoding='utf-8') as f: existing_data = load(f)
					if "model" in existing_data and "cases" in existing_data["model"]:
						for case in existing_data["model"]["cases"]: root_model.model.cases.append(CaseItem(when=case["when"],model=InnerModel(type=case["model"]["type"], model=case["model"]["model"])))
				except Exception as e: print(f"   | \u001B[31mERROR\u001B[0m Gagal memuat file target lama {item_file_target.name}: {e}")

			existing_names = {c.when for c in root_model.model.cases}
			existing_paths = {c.model.model for c in root_model.model.cases}

			added_count = 0
			for model_id in model_list:
				model_str_path = str(model_id).replace(".json", '')
				display_name = self.format_item_name(model_id.path)

				if display_name in existing_names or model_str_path in existing_paths: continue
				root_model.model.cases.append(CaseItem(when=display_name, model=InnerModel(model=model_str_path)))
				added_count += 1
				print(f"   \033[92m+>\033[0m '{display_name}' -> {model_str_path} ke {item_file_target.name}")
			if added_count > 0:
				try:
					with open(item_file_target, 'w', encoding='utf-8') as f: json.dump(asdict(root_model), f, indent=2, ensure_ascii=False)
				except Exception as e: print(f"   | \u001B[31mERROR\u001B[0m Gagal menyimpan file {item_file_target.name}: {e}")