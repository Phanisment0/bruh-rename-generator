from pathlib import Path
from namespace_scannner import NamespaceScanner
from generator import Generator
import shutil

pack_path = Path("pack")
namespace_path = Path("pack/assets")
items_path = namespace_path / "minecraft" / "items"

build_path = Path("C:\\Users\\user\\AppData\\Roaming\\PrismLauncher\\instances\\1.21.11 - Opt\\minecraft\\resourcepacks")

if __name__ == "__main__":
	if not pack_path.exists():
		items_path.mkdir(parents=True, exist_ok=True)
		print("\u001B[34;44mINFO\u001B[0m Folder `pack` tidak di temukan. Struktur folder `pack` telah dibuat otomatis.")
  
	print("\u001B[34;44mINFO\u001B[0m Membaca Folder Namespace")
  
	scanner = NamespaceScanner(namespace_path)
	scanner.scan()

	generator = Generator(namespace_path, scanner.model_items)
	generator.generate_item_files()
  
	print("\n\u001B[34;44mINFO\u001B[0m \u001B[32mMengompres Resource Pack menjadi ZIP...\u001B[0m")
	build_path.mkdir(exist_ok=True)
	
	shutil.make_archive(str(build_path / "resource_pack"), 'zip', pack_path)
	print("\u001B[34;44mINFO\u001B[0m \u001B[32mProses Selesai! File ZIP tersimpan di folder `build/`.\u001B[0m")