# Rename Item Generator

Repository ini berisi script generator otomatis untuk membantu pendaftaran rename item ke dalam file json item Minecraft. Script ini berguna jika kamu sering menambahkan item kustom berbasis perubahan nama (seperti senjata, kustom tekstur, atau equipment mod) ke resource pack dan malas mendaftarkannya satu per satu secara manual.

Dengan script ini, kamu cukup menaruh file model json di folder namespace masing-masing, lalu biarkan sistem yang melakukan pemindaian dan penyusunan file item secara otomatis berdasarkan nama file yang digunakan.

## Fitur Utama

- Pemindaian folder namespace secara dinamis untuk mencari file model json baru yang mendukung rename item.
- Validasi ketat nama file dan path tekstur agar selalu menggunakan huruf kecil dan karakter standar Minecraft untuk mencegah error saat di Minecraft
- Deteksi otomatis file tekstur (.png) di folder komputer untuk memastikan tidak ada tekstur yang hilang atau salah path.
- Penggabungan data baru dengan data lama tanpa menimpa isi file json item yang sudah didaftarkan sebelumnya.
- Otomatis melakukan kompresi seluruh isi folder menjadi sebuah file ZIP di folder build yang siap dipakai.

## Persyaratan Sistem

Proyek ini dibuat sepenuhnya menggunakan pustaka bawaan Python (Standard Library). Kamu tidak perlu menginstal paket tambahan apa pun lewat pip. Cukup pastikan Python versi 3.7 atau yang lebih baru sudah terpasang di komputermu.

## Cara Menggunakan

1. Taruh seluruh file model json kustom milikmu di dalam folder namespace masing-masing (misalnya di folder pack/assets/terraria/models/item/). Nama file json ini akan otomatis menjadi nama item yang harus diketikkan di anvil (Contoh: `murasama.json` berarti item harus di-rename menjadi `Murasama` di dalam game).
2. Taruh juga file gambar tekstur pendukungnya di folder textures yang sesuai.
3. Jalankan file build.bat dengan cara klik dua kali dari file explorer Windows.
4. Periksa log yang muncul di layar terminal CMD untuk melihat apakah ada error nama file, tekstur yang hilang, atau untuk melihat item apa saja yang berhasil ditambahkan.
5. Jika proses selesai, ambil file zip hasil build di dalam folder build/resource_pack.zip untuk langsung dimasukkan ke folder resourcepacks milik Minecraft.

# Dokumentasi

## Aturan Khusus File Model JSON

Agar script generator ini tahu ke mana harus mendaftarkan sistem rename item milikmu, kamu wajib menambahkan sebuah properti khusus bernama "types" di tingkat paling atas (root) pada setiap file model JSON yang kamu buat.

Properti "types" ini berbentuk sebuah list (array) string yang berisi ID material Minecraft. Isi dari list inilah yang menentukan item vanilla apa saja yang bentuknya akan berubah ketika diganti namanya menggunakan anvil di dalam game.

### Contoh Format File Model JSON

Misalkan kamu memiliki file model senjata bernama `murasama.json` (yang nantinya akan memicu perubahan visual saat item diubah namanya menjadi `Murasama`), isi bagian atas filenya harus diatur seperti ini:

```json
{
  "types": [
    "minecraft:diamond_sword",
    "minecraft:netherite_sword"
  ],
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "terraria:item/sword/murasama"
  }
}
```

### Cara Kerja Pemetaan Item:

1. Jika kamu mengisi "types" dengan "minecraft:diamond_sword", maka ketika script dijalankan, sistem rename untuk model tersebut akan otomatis didaftarkan ke dalam file `pack/assets/minecraft/items/diamond_sword.json`.
2. Kamu bisa memasukkan lebih dari satu material di dalam satu file model JSON (seperti contoh di atas). Efeknya, fitur rename item tersebut akan otomatis berlaku untuk dua jenis senjata sekaligus (`diamond_sword` dan `netherite_sword`).
3. File model JSON standar bawaan Minecraft atau file lama yang tidak memiliki properti "types" di dalamnya akan dilewati otomatis oleh script scanner untuk menghindari penumpukan data yang tidak diinginkan.