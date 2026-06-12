import os
import json

FOLDER_SUMBER_MODEL = "assets/minecraft/models/item/terraria" 
FILE_TARGET_ITEM = "assets/minecraft/items/diamond_sword.json"

def format_item_name(filename):
    name_without_ext = os.path.splitext(filename)[0]
    return name_without_ext.replace('_', ' ').title()

def generate_minecraft_path(full_file_path):
    clean_path = full_file_path.replace("\\", "/")
    path_without_ext = os.path.splitext(clean_path)[0]
    marker = "assets/minecraft/models/"
    if marker in path_without_ext:
        _, relative_minecraft_path = path_without_ext.split(marker, 1)
        return f"minecraft:{relative_minecraft_path}"
    else:
        file_name = os.path.basename(path_without_ext)
        return f"minecraft:item/{file_name}"

def auto_register_models():
    if not os.path.exists(FOLDER_SUMBER_MODEL):
        print(f"[ERROR] Folder sumber '{FOLDER_SUMBER_MODEL}' tidak ditemukan!")
        return
    if not os.path.exists(FILE_TARGET_ITEM):
        print(f"[ERROR] File target '{FILE_TARGET_ITEM}' tidak ditemukan!")
        return

    try:
        with open(FILE_TARGET_ITEM, 'r', encoding='utf-8') as f:
            target_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Gagal membaca file target: {e}")
        return

    if "model" not in target_data or "cases" not in target_data["model"]:
        print("[ERROR] Struktur JSON target tidak valid (tidak ada 'model' -> 'cases').")
        return

    cases_list = target_data["model"]["cases"]
    
    existing_names = set()
    existing_models = set()
    for case in cases_list:
        if "when" in case:
            existing_names.add(case["when"])
        if "model" in case and "model" in case["model"]:
            existing_models.add(case["model"]["model"])

    added_count = 0
    print(f"Memindai seluruh folder model di: {FOLDER_SUMBER_MODEL}...\n")

    for root, dirs, files in os.walk(FOLDER_SUMBER_MODEL):
        for file in files:
            if file.endswith('.json'):
                full_file_path = os.path.join(root, file)
                model_path = generate_minecraft_path(full_file_path)
                item_name = format_item_name(file)
                if item_name in existing_names:
                    print(f"[SKIPPED] Nama '{item_name}' sudah terdaftar.")
                    continue
                if model_path in existing_models:
                    print(f"[SKIPPED] Path model '{model_path}' sudah digunakan.")
                    continue
                new_case = {
                    "when": item_name,
                    "model": {
                        "type": "minecraft:model",
                        "model": model_path
                    }
                }
                cases_list.append(new_case)
                existing_names.add(item_name)
                existing_models.add(model_path)
                
                added_count += 1
                print(f"\033[92m[ADDED]\033[0m '{item_name}' -> {model_path}")
    if added_count > 0:
        try:
            with open(FILE_TARGET_ITEM, 'w', encoding='utf-8') as f:
                json.dump(target_data, f, indent=2, ensure_ascii=False)
            print(f"\n[SUKSES] Berhasil mendaftarkan {added_count} model baru ke {FILE_TARGET_ITEM}")
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan perubahan: {e}")
    else:
        print("\n[INFO] Semua model sudah terdaftar. Tidak ada perubahan dilakukan.")

if __name__ == "__main__":
    auto_register_models()