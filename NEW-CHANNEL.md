# Channel baru: Tiny Chaos (rencana 13 Nov 2026)

## Kenapa channel baru
- AIVOOMA: 12 Shorts berturut-turut hanya ditampilkan ke 0–4 orang dan 100% digeser, apa pun format/karakter/gaya
  pembukanya (dicek Buffer + Apify 13 Nov). Bukan made for kids, tidak ada pembatasan. Penyebab paling mungkin: riwayat
  channel (254 subscriber lama dari konten AI surreal yang tidak menonton kucing, video lama dihapus). Keputusan user
  13 Nov: jeda AIVOOMA, buat channel baru dengan target lebih jelas.
- Permintaan user 13 Nov: **jangan cuma kucing, videonya harus beragam.** Nama "Orange Cat Hours" dibatalkan.

## Target
- Penonton: anak muda/dewasa di AS, usia 18–34, paham meme. BUKAN anak-anak.
- Janji channel (satu, supaya algoritma tetap paham): **"life's little chaos, animated"** — momen sehari-hari yang
  relatable dan bikin orang tag temannya. Topiknya beragam, rasanya konsisten: kartun pendek, lucu, tanpa dialog, Inggris.

## Pilar konten (rotasi tiap minggu, 7 video)
1. Pets (Nugget si kucing, nanti anjing dan hewan lain): maks 2 per minggu.
2. Kehidupan dewasa sehari-hari (alarm Senin, kerja/WFH, gym, belanja, baterai HP, paket datang, "one more episode"): 2.
3. Makanan + musiman (Thanksgiving, Black Friday, Natal, Tahun Baru, Super Bowl, dst.): 1.
4. Otak/interaktif (cari perbedaan, pilih 1/2/3, ilusi, satisfying loop): 1.
5. Wildcard tren minggu itu dari riset: 1.
- Aturan: tidak ada pilar >2 per minggu; tokoh utama tidak sama dua hari berturut-turut; minimal 3 tokoh utama berbeda
  per minggu; tetap semua aturan anti-ulang, anti-monoton, Creative v2 dan evolusi di README.
- Format "taruh jarimu / tap layar" bukan format utama (terasa tontonan anak).

## Pemeran (orisinal, bertambah terus)
- Nugget (kucing oranye) — sudah ada. Gravy (kalkun cemas) — sudah ada.
- Perlu dibuat di engine sebelum batch pertama: **manusia** sederhana (orang dewasa muda, beberapa variasi rambut/baju)
  dan **anjing**. Tambah tokoh baru kalau riset menunjukkan perlu.

## Identitas
- Nama: **Tiny Chaos**. Handle usulan: @tinychaostoons (cadangan @tinychaos.toons, @dailytinychaos).
  Nama cadangan: "Daily Chaos", "Lowkey Toons".
- Avatar (logo teks) + banner (Nugget + Gravy): `assets/brand-v3/`. Deskripsi: `assets/brand-v3/channel-description.txt`.

## Checklist user saat membuat channel
1. Buat sebagai **Brand Account baru** (bukan ganti nama AIVOOMA).
2. Upload avatar, banner, deskripsi. Negara: United States. Bahasa: English.
3. Settings → Channel → Advanced: "No, set this channel as not made for kids".
4. Settings → Upload defaults: kategori Comedy; kalau ada pilihan AI/altered content, set "No".
5. Buffer: lepas channel AIVOOMA, sambungkan channel baru (paket gratis maks 3 channel).
6. Kabari Claude → ID channel baru ditulis di ROUTINE.md, status jeda dicabut, batch pertama dibuat.

## Penilaian
- Setelah 3 video: kalau ditampilkan ke ratusan orang (views ratusan+), hambatan memang di channel lama.
  Kalau tetap 0–4 views, masalahnya di isi/gaya video → pindah ke visual Google Flow (Veo) 3D.
- Setelah 2 minggu: pilar yang di atas median dapat porsi lebih, yang di bawah dikurangi.

## Riset validasi (Apify, 13 Nov 2026)
- **BlobbyClips** (2,89 jt subs): topik beragam tapi satu rasa — "The Wifi at 3am Be Like!" 10,2 jt, "When You Lose Your Job!"
  9,0 jt, "FaceTime with Different People!" 10,4 jt, "Gaming Memories in 50 Years!" 35 jt, "When Tape Sticks to Itself" 5,5 jt.
  Durasi 16–33 dtk. Pola judul konsisten: "X Be Like!" / "When X!" + 2 emoji kembar. Animasi dari animator (kredit di deskripsi).
  → Bukti: channel dengan topik beragam bisa sangat besar, asal janji dan pola judulnya konsisten.
- **equmi** (kucing saja, channel Okt 2024): naik 42 rb → 58,5 rb subs. Okt–Nov 135 rb–5,1 jt per Short, median ±330 rb.
  → Bukti: niche kucing tetap bisa, jadi beragam bukan syarat — tapi tidak merugikan.
- Kesamaan dua pemenang: animasi ekspresif (tokoh "berakting", gerak halus), satu punchline jelas, 11–33 dtk.
  **Risiko terbesar kita bukan topik, tapi kualitas animasi**: engine kode kita kaku dibanding mereka; video terbaik AIVOOMA
  hanya 1,3 rb. Channel baru menghapus beban channel lama, tapi tidak memperbaiki kualitas.
- Keputusan untuk mengurangi risiko: 6 video pertama channel baru = 3 dari engine (ditingkatkan: gerak lebih hidup, akting
  wajah, 15–25 dtk, pola judul "X Be Like!") + 3 dari Google Flow (Veo) yang klipnya diunduh user. Bandingkan "stayed to
  watch" dan views 48 jam; cara produksi yang menang dipakai seterusnya.

## 100% dibuat Claude? (user 13 Nov: "pengennya semua dibuat oleh Claude")
- Bukti format buatan kode bisa viral: simulasi bola "Will the ball escape?" — bouncyball 86 jt views (Jun 2025),
  Satisfying Shapes 36 jt + 26 jt (Mei 2024), satisfying.ba11s 38–67 jt (akhir 2023). Semua dibuat dari kode.
- Tapi November 2026 sudah jenuh: upload baru di format sama hanya 1–20 rb, banyak di bawah 4 rb (Apify 13 Nov).
  Meniru mentah = risiko gagal + risiko "konten repetitif" untuk monetisasi.
- Belum ketemu contoh kartun karakter yang 100% dibuat kode lalu viral; pemenang kartun (equmi, BlobbyClips) digambar animator.
- Arah usulan (semua tetap dibuat Claude, tanpa Flow): gabungkan kekuatan kode + humor relatable Tiny Chaos:
  1) simulasi fisika berlabel relatable ("My salary vs bills", "Me vs Monday", "Brain cells during an exam") — beda dari
     ball-escape generik; 2) puzzle/kuis visual (cari perbedaan, pilih jalur, ilusi) ; 3) skit kartun engine yang ditingkatkan.
  Data 2 minggu menentukan porsi.
