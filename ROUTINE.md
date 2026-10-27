# Rutinitas otomatis AIVOOMA (sumber utama, selalu diperbarui)

Dokumen ini dibaca setiap kali rutinitas jalan. **Setiap run wajib memperbarui file ini dan `learnings.md`** kalau menemukan
cara kerja yang lebih baik, kesalahan baru, atau pelajaran dari data. Skill `aivooma-weekly` hanya menunjuk ke sini,
jadi perbaikan di sini langsung berlaku tanpa perlu mengubah skill.

## Keputusan user yang terkunci
- Channel YouTube AIVOOMA, penonton luar negeri (AS). Bahasa video, judul, deskripsi: Inggris.
- Karakter utama saat ini: **Nugget**, kucing oranye 2D orisinal. TIDAK terkunci (permintaan user 27 Okt: "jangan terpaku
  sama kucing nugget, harus update jika ada yang baru"). Ikuti aturan evolusi README.md no. 11–14: tiap batch minimal
  2 dari 7 video eksperimen baru (format/karakter/gaya/tren baru dari riset terbaru); data yang menentukan porsi.
  Semua desain orisinal, jangan meniru karakter channel lain.
- Tanpa dialog/narasi. Musik orisinal + efek suara + teks pendek.
- Video tidak boleh berulang (aturan inauthentic content YouTube). Aturan anti-ulang di README.md wajib.
- Semua otomatis. Buffer paket gratis (tidak upgrade).
- Jam tayang: 07:00 WIB (malam hari di AS), 1 video per hari.
- Konten untuk remaja/dewasa (meme, relatable), **madeForKids: false**.
- Kalau user memberi masukan baru, catat di file ini + learnings.md + dokumen project `claude/aivooma-riset-format.md`.

## ID penting
- Buffer org 6acfacf801a85ecc6480964d. Channel YouTube AIVOOMA: 6ae078d92f1f5ed648e86690.
- Metadata YouTube per posting: title (≤60 karakter), categoryId "23" (Comedy), privacy public, madeForKids false,
  isAiGenerated false (kartun 2D, bukan realistis), notifySubscribers true. `text` = deskripsi.
- Repo: michael241291/ai-vooma (publik). Video: https://raw.githubusercontent.com/michael241291/ai-vooma/main/episodes/<id>/<id>-v<ver>.mp4
- Dokumen project: claude/aivooma-riset-format.md.

## Batas Buffer (khusus AIVOOMA)
- Rutinitas ini hanya mengurus channel AIVOOMA (6ae078d92f1f5ed648e86690). Selalu filter `channelIds` ke channel ini;
  jangan membaca, menghitung, mengubah, atau menghapus posting channel lain di org.
- AIVOOMA maksimal **3** posting scheduled (3 hari ke depan). Sisanya disimpan sebagai draf. Draf tidak dihitung Buffer.
- Paket gratis membatasi jumlah posting scheduled per org. Kalau penjadwalan ditolak karena batas, biarkan sebagai draf,
  jangan coba lagi hari itu, dan laporkan.

## BAGIAN 1 — Harian
1. `list_posts` org dengan `channelIds` = [AIVOOMA], status scheduled + draft + error.
2. Hitung scheduled AIVOOMA (A). Slot = 3 − A.
3. Ambil draf AIVOOMA urut dueAt. Jadwalkan (`edit_post` mode customScheduled, dueAt 07:00+07:00) sebanyak slot,
   1 video per hari, hari kosong terdekat mulai besok. Kalau dueAt draf sudah lewat, geser ke hari kosong berikutnya.
4. Posting AIVOOMA berstatus error: laporkan alasannya.
5. Kalau hari ini Minggu (WIB) **atau** draf AIVOOMA tersisa < 3: jalankan BAGIAN 2.
6. Laporan singkat (SendUserMessage): yang dijadwalkan, antrean draf, error.

## BAGIAN 2 — Mingguan (batch 7 video)
### Persiapan
- add_repo michael241291/ai-vooma (access push), clone ke /home/claude/ai-vooma. Baca README.md, engine/README.md,
  learnings.md, log.json, ideas.json.
- Pasang pycairo/numpy/pillow + font Luckiest Guy sesuai engine/README.md.

### 1. Evaluasi
- Buffer `list_posts` channel AIVOOMA dengan includeMetrics (views, likes, comments) untuk video yang sudah tayang.
- Apify `streamers/youtube-scraper` startUrls https://www.youtube.com/@aivooma/shorts untuk angka terbaru.
- Isi `results` di log.json. Bandingkan per format, jenis twist, durasi, mood musik. Format dengan median views
  tertinggi dapat porsi lebih besar (tetap ≥3 format per minggu). Tulis pelajaran di learnings.md (paling baru di atas).

### 2. Riset tren (Apify)
- `streamers/youtube-scraper` searchQueries mis. "cat animation funny", "cute cat cartoon animation", "interactive animation cat",
  "relatable cat animation", "2d animation shorts", plus tema yang sedang ramai (musim/hari besar AS). maxResultsShorts 12,
  sortingOrder views, dateFilter month. Kalau hasil kosong, ulangi tanpa sortingOrder.
- Untuk 3–5 pemenang baru: aiVideoDescription true (murah) untuk membedah struktur per detik.
- Catat pola baru ke learnings.md dan tambah ide baru ke ideas.json (ubah ancaman/latar/twist, jangan menyalin persis).
- Riset juga di luar kucing: cari format/karakter/niche Shorts animasi yang sedang naik (bulan ini) dan belum dipakai channel.
  Hasilnya jadi minimal 2 video eksperimen per batch (aturan README no. 11). Kalau perlu karakter/gaya baru, buat di engine.

### 3. Rencana 7 video
- Pilih dari ideas.json. Aturan anti-ulang: situasi/ancaman/twist tidak pernah dipakai lagi; ≥3 format per 7 video,
  maksimal 3 per format; dua video berurutan beda format.
- Aturan anti-monoton (README.md no. 5–10, wajib dicek terhadap 7 video terakhir di log.json): dua video berurutan tidak
  boleh sama latar, mood musik pembuka, atau pola judul; satu latar/pola judul maksimal 2x per 7 video; hook, durasi,
  dan warna bervariasi; tiap batch minimal 1 hal baru di engine (latar/prop/efek/karakter sampingan/mood musik).
- Setiap video: hook di detik 0 (teks + situasi langsung terlihat), satu kejadian lucu, twist di akhir, ending yang bisa di-loop.
  Durasi 12–18 detik.

### 4. Produksi
- Tulis episodes/<id>/episode.json (spesifikasi di engine/README.md). Boleh menambah prop/efek/latar baru di engine
  kalau cerita butuh, lalu catat di engine/README.md.
- `--frames` dulu, LIHAT sheet.png: subjek terbaca, tidak terpotong, teks tidak menutupi aksi, urutan gambar benar.
- Render penuh, cek durasi dan level audio (tidak ada bagian sunyi > 1 detik kecuali disengaja).
- Efek suara baru hanya kalau benar-benar perlu (ElevenLabs sfx ±17 kredit/biji, generations_count 1); simpan ke assets/sfx
  dan daftar di engine/README.md. Jangan regenerate yang sudah ada.

### 5. Publish ke Buffer
- Update log.json (id, format, situation, twist, title, made, status) dan tandai ide terpakai di ideas.json.
- Hapus kf_*.png/sheet.png sebelum commit (sudah di .gitignore). git add, commit, push. Cek URL raw video → 200.
- Buffer `create_post` per video: channel AIVOOMA, schedulingType automatic, saveToDraft true, dueAt 07:00 WIB hari tayangnya,
  assets video URL raw, metadata youtube seperti di atas, text = deskripsi. BAGIAN 1 yang menjadwalkan.

### 6. Belajar
- Perbarui learnings.md, file ini (kalau prosedur berubah), dan claude/aivooma-riset-format.md (project).
- Laporan (SendUserMessage): 7 judul + tanggal tayang, hasil minggu lalu, pelajaran utama, kredit ElevenLabs terpakai, kendala.
