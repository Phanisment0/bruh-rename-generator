from json import JSONDecodeError, JSONDecoder, load
from pathlib import Path
from util.identifier import Identifier
from collections import defaultdict

class NamespaceScanner:
	model_items = {}

	def __init__(self, path: Path):
		if not path.exists(): path.mkdir(parents=True)
		self.path = path
		self.model_items = defaultdict(list)

	def scan(self):
		print("\u001B[34;44mINFO\u001B[0m Namespace Terdeteksi:")
		for namespace_folder in self.path.iterdir():
			if not namespace_folder.is_dir(): continue
			print(f"     - \u001B[32m{namespace_folder.name}\u001B[0m")

			self.read_models(namespace_folder)
	
	def read_models(self, namespace_folder: Path):
		models_path = namespace_folder / "models"

		if not models_path.exists() or not models_path.is_dir():
			print(f"       | \u001B[33mWARN\u001B[0m Folder \u001B[34mmodels\u001B[0m tidak di temukan di namespace \u001B[34m{namespace_folder.name}\u001B[0m")
			return
		for model_file in models_path.rglob("*.json"):
			try:
				relative_model_path = model_file.relative_to(models_path)
				id = Identifier(f"{namespace_folder.name}:{relative_model_path}")
				
				with open(model_file, 'r', encoding='utf-8') as f: data = load(f)
				if isinstance(data, dict):
					if "types" in data: self.read_model_json(data, id)
					if "textures" in data: self.read_textures(data["textures"], id)
				

			except ValueError:      print(f"       | \u001B[31mERROR\u001B[0m Nama model \u001B[34m{model_file.name}\u001B[0m bukan nama yang valid.")
			except JSONDecodeError: print(f"       | \u001B[31mERROR\u001B[0m File \u001B[34m{model_file.name}\u001B[0m bukan JSON yang valid.")
			except Exception as e:  print(f"       | \u001B[31mERROR\u001B[0m Gagal membaca \u001B[34m{model_file.name}\u001B[0m: {e}")
	
	def read_model_json(self, data: JSONDecoder, id: Identifier):
		for material in data["types"]:
			self.model_items[Identifier(material)].append(id)
			print(f"       \u001B[32m+>\u001B[0m {id} -> {material}")
	
	def read_textures(self, textures_data: dict, model_id: Identifier):
		if not isinstance(textures_data, dict): return
		for texture_key, texture_path in textures_data.items():
			if not isinstance(texture_path, str): continue
			if texture_path.startswith("#"): continue
			try: texture_id = Identifier(texture_path)
			except ValueError:
				print(f"       | \u001B[31mERROR\u001B[0m Model \u001B[34m{model_id}\u001B[0m -> ID Texture \u001B[31m'{texture_path}'\u001B[0m tidak valid.")
				continue
			
			actual_texture_file = self.path / texture_id.namespace / "textures" / f"{texture_id.path}.png"
			if not actual_texture_file.exists(): print(f"       | \u001B[33mWARN\u001B[0m Model \u001B[34m{model_id}\u001B[0m -> File texture tidak ditemukan: \u001B[33m{texture_id}\u001B[0m (\u001B[34m{actual_texture_file.name}\u001B[0m)")