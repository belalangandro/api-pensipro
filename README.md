

# 📦 Modul PensiPro – Dokumentasi Detail

```
  source .venvaas/bin/activate
  uvicorn app.main:app --reload --port 8008  
```

## 1. **Member Management**

**Tujuan:** Mengelola data pensiunan sebagai anggota koperasi.
**Tabel terkait:**

* `members`, `member_contacts`, `member_bank_accounts`, `member_documents`

**Fungsi utama:**

* Registrasi anggota baru (data pribadi + pensiun).
* Verifikasi & simpan dokumen (KTP, SK pensiun, KK, foto, dll).
* Simpan kontak & rekening bank untuk pencairan.
* Status anggota (aktif, nonaktif, meninggal).

**Business rules:**

* NIK & No Pensiun harus unik.
* Dokumen wajib diverifikasi sebelum pengajuan pinjaman bisa jalan.
* Rekening default dipakai untuk pencairan kredit.

---

## 2. **Sales Management**

**Tujuan:** Mengelola aktivitas sales yang mencari & melayani calon anggota.
**Tabel terkait:**

* `sales_branches`, `sales`, `sales_visits`, `sales_commissions`, `sales_targets`

**Fungsi utama:**

* Master data cabang & sales.
* Pencatatan kunjungan sales ke calon pensiunan.
* Hitung & catat komisi otomatis setelah pinjaman cair.
* Monitor target vs realisasi per sales/cabang.

**Business rules:**

* Komisi dihitung % dari pinjaman cair.
* Target dicatat per bulan (`periode` YYYY-MM).
* Satu sales bisa punya banyak visit, satu visit bisa terkait calon anggota.

---

## 3. **Loan Origination System (LOS)**

**Tujuan:** Mengatur alur pengajuan kredit dari awal sampai komite.
**Tabel terkait:**

* `applications`, `application_docs`, `analysis`, `committee_decisions`

**Fungsi utama:**

* Input pengajuan kredit (plafon, tenor, bunga, biaya).
* Upload dokumen pengajuan (scan kontrak, slip pensiun, dll).
* Analisa kelayakan (DSR, skor risiko, rekomendasi analis).
* Keputusan komite (approve, reject, conditional).

**Business rules:**

* Status aplikasi: draft → submitted → analyzing → committee → approved/rejected → disbursed.
* Satu aplikasi hanya bisa masuk komite jika analisa sudah lengkap.
* Komite minimal terdiri dari 2 level (misalnya SPV + Manager).

---

## 4. **Loan Management System (LMS)**

**Tujuan:** Mengelola pinjaman setelah cair sampai lunas.
**Tabel terkait:**

* `loans`, `loan_schedules`, `loan_payments`, `loan_disbursements`, `loan_restructures`, `loan_settlements`

**Fungsi utama:**

* Master data pinjaman aktif (link ke aplikasi & anggota).
* Generate jadwal angsuran (flat/anuitas).
* Catat pembayaran (via potong pensiun/transfer/tunai).
* Catat pencairan dana & rekening penerima.
* Restrukturisasi (perpanjangan, penurunan bunga, penundaan).
* Pelunasan dipercepat + denda penalti.

**Business rules:**

* Status loan: active, closed, default.
* Restrukturisasi butuh persetujuan level manajemen.
* Pelunasan harus update seluruh jadwal & outstanding.

---

## 5. **Loan Product & Pricing**

**Tujuan:** Mengatur produk kredit pensiun & skema biaya.
**Tabel terkait:**

* `loan_products`, `loan_fees`, `penalty_rules`

**Fungsi utama:**

* Master produk pinjaman (tenor, plafon, bunga).
* Atur biaya (admin, provisi, asuransi) per produk.
* Atur aturan denda keterlambatan.

**Business rules:**

* Plafon maksimal ≤ 95% manfaat pensiun tersisa dalam tenor.
* DSR ≤ batas (`dsr_limit`).
* Usia + tenor ≤ `umur_maksimal`.

---

## 6. **Funder & Fronting Management**

**Tujuan:** Mengelola kerja sama koperasi dengan bank/mitra (fronting).
**Tabel terkait:**

* `funders`, `funder_allocations`, `funder_contracts`, `funder_settlements`

**Fungsi utama:**

* Master data funder (bank/koperasi lain).
* Alokasi pinjaman ke funder (participation/assignment).
* Simpan kontrak kerja sama.
* Hitung & catat settlement fee/bagi hasil dengan funder.

**Business rules:**

* Satu pinjaman bisa dibiayai funder penuh/parsial.
* Settlement periodik (misalnya bulanan).
* Sharing margin dihitung berdasarkan konfigurasi fee_originator & fee_servicing.

---

## 7. **Billing & Reconciliation**

**Tujuan:** Integrasi dengan Taspen/Asabri untuk potong pensiun.
**Tabel terkait:**

* `pension_cut_exports`, `pension_cut_export_lines`, `pension_cut_imports`, `pension_cut_import_lines`

**Fungsi utama:**

* Generate file instruksi potongan pensiun (CSV).
* Upload file realisasi potongan dari bank/Taspen.
* Matching otomatis antara jadwal angsuran & realisasi.
* Tandai mismatch/unmatched untuk investigasi.

**Business rules:**

* Export file per periode (YYYY-MM).
* Toleransi mismatch nominal harus dicatat.
* Jika unmatched → masuk ke `exception_logs`.

---

## 8. **Monitoring & Logging**

**Tujuan:** Audit, tracking, dan laporan performa pinjaman.
**Tabel terkait:**

* `aging_reports`, `exception_logs`, `audit_trails`

**Fungsi utama:**

* Laporan aging DPD (0–30, 31–60, 61–90, >90).
* Catat error teknis/proses (exception).
* Catat semua aksi penting (audit trail).

**Business rules:**

* Aging di-generate bulanan.
* Semua approval/reject harus tercatat di audit_trails.
* Exception harus bisa ditarik untuk debugging & audit regulator.

---

# 📊 Ringkasan

Dengan DB ini, kita punya **8 modul utama** yang saling terhubung:

1. Member Management
2. Sales Management
3. Loan Origination (LOS)
4. Loan Management (LMS)
5. Product & Pricing
6. Funder & Fronting
7. Billing & Reconciliation
8. Monitoring & Logging

---

# 📡 API Struktur – PensiPro (Extended)

## 1. **Member Management**

🔹 Tabel: `members`, `member_contacts`, `member_bank_accounts`, `member_documents`

**Endpoint utama:**

* `POST /members` → tambah anggota baru
* `GET /members` → list anggota (+ filter NIK/no_pensiun/status)
* `GET /members/{id}` → detail anggota
* `PUT /members/{id}` → update data anggota
* `DELETE /members/{id}` → hapus anggota
* `GET /members/{id}/loans` → histori pinjaman anggota
* `GET /members/{id}/applications` → histori pengajuan

**Sub-resource:**

* `POST /members/{id}/contacts`
* `POST /members/{id}/bank-accounts`
* `POST /members/{id}/documents`
* `PUT /members/{id}/documents/{doc_id}/verify` → verifikasi dokumen

---

## 2. **Sales Management**

🔹 Tabel: `sales_branches`, `sales`, `sales_visits`, `sales_commissions`, `sales_targets`

**Endpoint utama:**

* `POST /sales-branches` → tambah cabang
* `GET /sales-branches` → list cabang
* `POST /sales` → tambah sales (assign cabang)
* `GET /sales` → daftar sales
* `GET /sales/{id}` → detail sales
* `PUT /sales/{id}` → update sales
* `GET /sales/{id}/visits` → histori kunjungan
* `POST /sales/{id}/visits` → catat kunjungan
* `GET /sales/{id}/commissions?status=unpaid` → daftar komisi
* `POST /sales/{id}/commissions` → catat komisi
* `GET /sales/{id}/targets?periode=YYYY-MM` → target vs realisasi
* `POST /sales/{id}/targets` → set target bulanan
* `GET /sales/{id}/performance?periode=YYYY-MM` → rekap KPI sales

---

## 3. **Loan Origination (LOS)**

🔹 Tabel: `applications`, `application_docs`, `analysis`, `committee_decisions`

**Endpoint utama:**

* `POST /applications` → ajukan pinjaman
* `GET /applications` → list aplikasi (filter status)
* `GET /applications/{id}` → detail aplikasi
* `PUT /applications/{id}` → update draft
* `POST /applications/{id}/submit` → submit draft → analyzing
* `POST /applications/{id}/cancel` → batalkan aplikasi
* `POST /applications/{id}/documents` → upload dokumen
* `POST /applications/{id}/analyze` → input analisa kredit
* `POST /applications/{id}/decide` → input keputusan komite
* `PUT /applications/{id}/status` → update status workflow

---

## 4. **Loan Management (LMS)**

🔹 Tabel: `loans`, `loan_schedules`, `loan_payments`, `loan_disbursements`, `loan_restructures`, `loan_settlements`

**Endpoint utama:**

* `GET /loans` → daftar pinjaman
* `GET /loans/{id}` → detail pinjaman
* `PUT /loans/{id}/status` → close/default
* `GET /loans/{id}/schedules` → jadwal angsuran
* `GET /loans/{id}/outstanding` → sisa pokok, bunga, denda
* `POST /loans/{id}/payments` → catat pembayaran
* `POST /loans/{id}/disbursements` → catat pencairan
* `POST /loans/{id}/restructures` → ajukan restrukturisasi
* `POST /loans/{id}/settlements` → catat pelunasan dipercepat
* `POST /loans/{id}/penalties` → catat denda manual

---

## 5. **Product & Pricing**

🔹 Tabel: `loan_products`, `loan_fees`, `penalty_rules`

**Endpoint utama:**

* `POST /loan-products` → tambah produk
* `GET /loan-products` → list produk
* `GET /loan-products/{id}` → detail produk
* `PUT /loan-products/{id}` → update produk
* `POST /loan-products/{id}/fees` → atur biaya admin/provisi/asuransi
* `POST /loan-products/{id}/penalty-rules` → atur aturan denda
* `GET /loan-products/{id}/simulation?plafon=…&tenor=…` → simulasi cicilan

---

## 6. **Funder & Fronting**

🔹 Tabel: `funders`, `funder_allocations`, `funder_contracts`, `funder_settlements`

**Endpoint utama:**

* `POST /funders` → tambah mitra bank/funder
* `GET /funders` → daftar funder
* `GET /funders/{id}` → detail funder
* `PUT /funders/{id}` → update funder
* `POST /loans/{id}/allocate-funder` → alokasi pinjaman ke funder
* `POST /funders/{id}/contracts` → upload kontrak kerjasama
* `GET /funders/{id}/portfolio` → daftar pinjaman aktif di funder
* `POST /funders/{id}/settlements` → generate settlement bulanan
* `GET /funders/{id}/settlements?periode=YYYY-MM` → detail settlement

---

## 7. **Billing & Reconciliation**

🔹 Tabel: `pension_cut_exports`, `pension_cut_export_lines`, `pension_cut_imports`, `pension_cut_import_lines`

**Endpoint utama:**

* `POST /billing/export` → generate file potongan pensiun (CSV)
* `GET /billing/export/{id}` → detail export
* `POST /billing/import` → upload realisasi potongan (CSV)
* `GET /billing/import/{id}` → hasil matching & unmatched list
* `GET /billing/unmatched?periode=YYYY-MM` → unmatched list
* `POST /billing/reconcile/{id}` → manual matching
* `GET /billing/member/{member_id}` → histori potongan anggota

---

## 8. **Monitoring & Logging**

🔹 Tabel: `aging_reports`, `exception_logs`, `audit_trails`

**Endpoint utama:**

* `GET /reports/aging?periode=YYYY-MM` → laporan aging
* `GET /reports/loan-quality?periode=YYYY-MM` → laporan NPL/DPD
* `GET /reports/funder-margin?periode=YYYY-MM` → margin funder vs koperasi
* `GET /logs/exceptions` → list error proses
* `GET /logs/audit-trails?ref_table=…&ref_id=…` → histori aksi

---

# 📊 Ringkasan Endpoint

Dengan DB ini, total **70+ endpoint** terbagi ke 8 modul:

* Member Management → ±10 endpoint
* Sales Management → ±12 endpoint
* Loan Origination (LOS) → ±10 endpoint
* Loan Management (LMS) → ±10 endpoint
* Product & Pricing → ±7 endpoint
* Funder/Fronting → ±9 endpoint
* Billing & Reconciliation → ±7 endpoint
* Monitoring & Logging → ±5 endpoint

---
---

# 🔄 Flow per Modul – PensiPro (Revisi Lengkap)

## 1. **Member Management**

**Flow:**

1. Admin / Sales input data pensiunan → `POST /members`.
2. Upload dokumen wajib (KTP, KK, SK pensiun) → `POST /members/{id}/documents`.
3. Verifikasi dokumen → `PUT /members/{id}/documents/{doc_id}/verify`.
4. Tambah rekening bank untuk pencairan → `POST /members/{id}/bank-accounts`.
5. Sistem lakukan **dedup check** (NIK/no_pensiun unik).
6. Jika status anggota berubah (nonaktif/meninggal) → otomatis update semua loan terkait (pelunasan via ahli waris / mark default).
7. Member siap digunakan untuk **LOS** (Loan Origination).

---

## 2. **Sales Management**

**Flow:**

1. Buat cabang → `POST /sales-branches`.
2. Tambah sales ke cabang → `POST /sales`.
3. Sales kunjungi calon pensiunan → `POST /sales/{id}/visits`.
4. Jika pensiunan setuju → sales input aplikasi di **LOS**.
5. Setelah loan cair → sistem hitung komisi otomatis → `POST /sales/{id}/commissions`.
6. Komisi masuk ke payroll, status `paid/unpaid` bisa dimonitor.
7. Set target bulanan → `POST /sales/{id}/targets`.
8. Supervisor approve target → update status target.
9. KPI per sales/cabang bisa dipantau → `GET /sales/{id}/performance`.

---

## 3. **Loan Origination (LOS)**

**Flow:**

1. Sales/Admin ajukan pinjaman → `POST /applications`.
2. Upload dokumen aplikasi → `POST /applications/{id}/documents`.
3. Submit aplikasi → `POST /applications/{id}/submit`.
4. Sistem jalankan **pre-check otomatis** (DSR, umur+tenor, double financing).
5. Analis melakukan analisa manual → `POST /applications/{id}/analyze`.
6. Komite multi-level approve (SPV → Manager → Direksi) → `POST /applications/{id}/decide`.
7. Jika approved → sistem buat record `loans` (masuk ke **LMS**).
8. Jika reject atau withdraw → aplikasi close, sales & member dapat notifikasi.

---

## 4. **Loan Management (LMS)**

**Flow:**

1. Loan aktif terbentuk dari aplikasi → `loans`.
2. Sistem generate jadwal angsuran → `GET /loans/{id}/schedules`.
3. Lakukan pencairan ke rekening anggota → `POST /loans/{id}/disbursements`.
4. Cicilan tiap bulan tercatat otomatis dari billing → `POST /loans/{id}/payments`.
5. Jika telat → sistem hitung denda via `penalty_rules` → `POST /loans/{id}/penalties`.
6. Admin bisa koreksi pembayaran salah input (reverse transaction).
7. Jika anggota ajukan restrukturisasi → `POST /loans/{id}/restructures` (bisa lebih dari sekali, histori tersimpan).
8. Jika lunas lebih cepat → `POST /loans/{id}/settlements`.
9. Jika DPD > 90 hari → sistem auto-flag status `default`.
10. Status loan update: `active` → `closed` (lunas) / `default` (gagal bayar).

---

## 5. **Product & Pricing**

**Flow:**

1. Admin buat produk → `POST /loan-products`.
2. Tambahkan biaya admin/provisi/asuransi → `POST /loan-products/{id}/fees`.
3. Tambahkan aturan denda → `POST /loan-products/{id}/penalty-rules`.
4. Produk bisa di-lock hanya untuk funder tertentu.
5. Sales/Member bisa lakukan simulasi cicilan → `GET /loan-products/{id}/simulation?plafon=…&tenor=…`.
6. Produk aktif digunakan saat input aplikasi di LOS.

---

## 6. **Funder & Fronting**

**Flow:**

1. Tambah funder → `POST /funders`.
2. Upload kontrak kerja sama → `POST /funders/{id}/contracts`.
3. Loan tertentu dialokasikan ke funder → `POST /loans/{id}/allocate-funder`.
4. Funder bisa lihat portofolio → `GET /funders/{id}/portfolio`.
5. Loan bisa **di-assign penuh** ke funder (piutang dialihkan).
6. Akhir bulan → generate settlement → `POST /funders/{id}/settlements`.
7. Jika ada mismatch, admin bisa koreksi settlement.
8. Koperasi dan funder bagi hasil sesuai konfigurasi fee originator/servicing.

---

## 7. **Billing & Reconciliation**

**Flow:**

1. Akhir bulan → sistem generate file potong pensiun → `POST /billing/export`.
2. File dikirim ke Taspen/Asabri.
3. Bank/Taspen kirim balik file realisasi → upload ke sistem → `POST /billing/import`.
4. Sistem matching → `GET /billing/import/{id}`.

   * Jika match → update `loan_payments`.
   * Jika unmatched → masuk `GET /billing/unmatched?periode=…`.
5. Admin bisa reconcile manual → `POST /billing/reconcile/{id}`.
6. Jika ada potongan berlebih → sistem buat refund request.
7. Sistem bisa retry unmatched di periode berikutnya.
8. Histori potongan bisa dicek per anggota → `GET /billing/member/{member_id}`.

---

## 8. **Monitoring & Logging**

**Flow:**

1. Sistem generate aging report bulanan → `GET /reports/aging?periode=…`.
2. Cek kualitas portofolio (NPL/DPD) → `GET /reports/loan-quality?periode=…`.
3. Hitung margin funder → `GET /reports/funder-margin?periode=…`.
4. Semua exception dicatat (dengan severity) → `GET /logs/exceptions`.
5. Audit trail simpan detail lengkap (user, timestamp, old_value, new_value) → `GET /logs/audit-trails`.
6. Semua approval, pencairan, settlement harus bisa diaudit kembali.

---

# 📌 **Use Case dari Modul PensiPro**

## 1. **Member Management**

* Registrasi anggota pensiunan koperasi.
* Verifikasi dokumen (KTP, KK, SK pensiun).
* Update status anggota (aktif, nonaktif, meninggal).
* Cek histori pinjaman & potongan pensiun per anggota.

---

## 2. **Sales Management**

* Monitoring aktivitas sales (kunjungan, pipeline).
* Hitung otomatis komisi setelah loan cair.
* Penetapan target bulanan per sales/cabang.
* Evaluasi KPI & kinerja cabang.

---

## 3. **Loan Origination (LOS)**

* Input aplikasi kredit pensiun (plafon, tenor, bunga).
* Pre-check otomatis (DSR, usia, double financing).
* Analisa kredit oleh analis.
* Approval komite multi-level (SPV → Manager → Direksi).
* Notifikasi status ke sales & anggota.

---

## 4. **Loan Management (LMS)**

* Generate jadwal angsuran (flat/anuitas).
* Pencairan dana ke rekening anggota.
* Catat pembayaran via potong pensiun/bank.
* Restrukturisasi pinjaman.
* Pelunasan dipercepat + denda penalti.

---

## 5. **Product & Pricing**

* Definisi produk kredit pensiun (plafon, tenor, bunga).
* Simulasi cicilan untuk sales/anggota.
* Atur biaya admin/provisi/asuransi.
* Atur aturan denda keterlambatan.

---

## 6. **Funder & Fronting**

* Kerja sama dengan **bank/koperasi lain/multifinance** untuk pendanaan.
* Alokasi loan ke funder (penuh/parsial).
* Simpan kontrak kerja sama funder.
* Generate settlement bulanan (bagi hasil margin).
* Laporan portofolio per funder.

👉 **Inilah titik strategis buat kerjasama dengan bank/funder**.

* Koperasi jadi **originator** (punya akses ke pensiunan).
* Bank jadi **funder/fronting** (kasih modal).
* Revenue sharing → fee originator & fee servicing sesuai kontrak.

---

## 7. **Billing & Reconciliation**

* Generate file potongan pensiun → kirim ke Taspen/Asabri.
* Import file realisasi dari bank/Taspen.
* Matching otomatis vs jadwal angsuran.
* Handle unmatched → masuk investigasi.
* Histori potongan per anggota.

---

## 8. **Monitoring & Logging**

* Aging report bulanan (DPD 0–30, 31–60, dst).
* NPL/loan quality report.
* Margin funder vs koperasi.
* Exception log untuk error sistem.
* Audit trail (approval, settlement, pencairan).

---

# 🤝 **Kerja Sama dengan Bank (Funding Use Case)**

Dengan modul **Funder & Fronting**, kamu bisa posisikan sistem PensiPro sebagai **Loan Originator Platform**.
Flow kerja samanya bisa seperti ini:

1. **Koperasi** (pakai PensiPro) → punya akses ke **pasar pensiunan** (anggota).

2. **Bank** → butuh channel kredit pensiun tapi tidak punya akses langsung.

3. **Skema Kerja Sama**:

   * **Fronting** → kredit atas nama bank, koperasi hanya originator (sales & pengelola).
   * **Channeling/Partnership** → koperasi kasih akses ke pipeline, bank sediakan dana.
   * **Participating Loan** → 1 loan bisa didanai koperasi + bank (sharing porsi).

4. **Revenue Sharing**:

   * Bank dapat bunga (principal + interest).
   * Koperasi dapat **fee originator** + **fee servicing** (administrasi & collection).
   * Semua tercatat di `funder_settlements`.

---

# 🎯 Ringkasan Value Proposition buat Bank

* **Bank dapat akses** ke pasar pensiunan yang biasanya koperasi lebih dekat.
* **Risiko lebih rendah** karena potong pensiun (gaji tetap, DP default kecil).
* **Sistem sudah siap** → API, workflow, monitoring, billing, settlement.

---


# 🔄 **Skema Kerja Sama Koperasi – Bank via PensiPro**

## 1. **Originasi & Input Aplikasi (di Koperasi)**

* Sales koperasi daftar **anggota pensiunan** → `POST /members`.
* Upload dokumen (KTP, KK, SK pensiun) → `POST /members/{id}/documents`.
* Ajukan pinjaman → `POST /applications`.
* Sistem PensiPro jalanin **pre-check otomatis** (DSR, umur, tenor).

---

## 2. **Analisa & Approval**

* Analis koperasi input analisa kredit → `POST /applications/{id}/analyze`.
* Komite koperasi approve/reject → `POST /applications/{id}/decide`.
* Jika **approved**, sistem otomatis generate loan di `loans`.

---

## 3. **Alokasi Funder (Bank)**

* Loan yang sudah approved dialokasikan ke **bank partner** → `POST /loans/{id}/allocate-funder`.
* Koperasi tetap jadi **originator** & **servicer** (collect angsuran).
* Bank jadi **funder/fronting** → taruh modal → masuk ke `funders` & `funder_allocations`.

---

## 4. **Pencairan Dana**

* Dana cair ke rekening pensiunan → `POST /loans/{id}/disbursements`.
* Sumber dana bisa full dari bank atau mix (bank + koperasi).

---

## 5. **Pembayaran via Potong Pensiun**

* Setiap bulan, sistem generate file instruksi potongan pensiun → `POST /billing/export`.
* File dikirim ke Taspen/Asabri.
* Hasil realisasi dari bank masuk lagi → `POST /billing/import`.
* Sistem matching otomatis → update ke `loan_payments`.

---

## 6. **Settlement Koperasi–Bank**

* Akhir bulan → sistem hitung bagi hasil → `POST /funders/{id}/settlements`.
* Formula → pakai `fee_originator_pct` & `fee_servicing_pct` dari kontrak.
* Hasil settlement:

  * **Bank** → bunga & pokok sesuai porsi.
  * **Koperasi** → originator fee + servicing fee.
* Laporan bisa ditarik → `GET /funders/{id}/settlements?periode=YYYY-MM`.

---

## 7. **Monitoring & Audit**

* Bank bisa akses portofolio → `GET /funders/{id}/portfolio`.
* Koperasi bisa monitor aging & DPD → `GET /reports/aging?periode=…`.
* Semua transaksi (approval, pencairan, settlement) tercatat di `audit_trails`.

---

# 🎯 Value Tambahan

* **Koperasi**: tetap pegang hubungan dengan anggota, dapat fee.
* **Bank**: dapat exposure ke pasar pensiunan yang stabil & low risk.
* **Regulator-ready**: semua ada audit trail, settlement jelas, billing sesuai Taspen/Asabri.
---

---

# 📦 Modul Baru: **Notification Management**

**Tujuan:** Mengelola pengiriman & tracking notifikasi ke user/anggota.

**Tabel terkait:**
`notifications`, `notification_templates`

**Fungsi utama:**

* Kirim notifikasi otomatis (loan approve/reject, pembayaran masuk, settlement).
* Kirim notifikasi manual (broadcast, custom).
* Simpan template (biar konsisten).
* Cek histori notifikasi per user/member.

**Business rules:**

* Notifikasi default dikirim minimal **in-app**.
* Bisa multi-channel (in-app + email/WA/SMS).
* Template reusable untuk event rutin (approve, reject, DPD, dsb).
* Semua notifikasi dicatat di DB untuk audit trail.

---

# 📡 API Struktur – Notification

### 🔹 Endpoint Utama

* `POST /notifications`
  → kirim notifikasi ke user/member.

* `GET /notifications?user_id=…&is_read=false`
  → list notifikasi per user (filter belum dibaca).

* `PUT /notifications/{id}/read`
  → tandai notifikasi sudah dibaca.

* `DELETE /notifications/{id}`
  → hapus notifikasi (opsional).

---

### 🔹 Endpoint Template

* `POST /notification-templates`
  → buat template baru.

* `GET /notification-templates`
  → list template aktif.

* `PUT /notification-templates/{id}`
  → update template.

* `DELETE /notification-templates/{id}`
  → hapus template.

---

# 📌 Contoh Use Case

1. **Aplikasi Loan Approved**

   * Sistem trigger → insert ke `notifications` (in-app).
   * Kalau setting channel WA/email → push ke API pihak ketiga.

2. **Pembayaran Masuk**

   * Setelah `loan_payments` tercatat, sistem auto kirim notifikasi:

     * “Pembayaran Rp1.500.000 sudah diterima untuk Loan #123.”

3. **Settlement Funder**

   * Akhir bulan → `funders/{id}/settlements` generate → auto kirim notifikasi ke finance koperasi & bank.

---

# 📦 **User Management – Fungsi & Use Case**

## 1. `sys_users`

**Fungsi:**

* Menyimpan data akun user (admin, sales, analis, komite, finance, dll).
* Jadi entitas utama login & authentication.

**Use Case:**

* Admin menambahkan user baru untuk staff koperasi.
* Sales login ke aplikasi untuk input pengajuan.
* Sistem update `last_login_at` setiap kali user berhasil login.

---

## 2. `sys_roles`

**Fungsi:**

* Master data role (misalnya: Admin, Sales, Analis, Komite, Finance, Auditor).
* Menjadi basis role-based access control (RBAC).

**Use Case:**

* Admin membuat role baru: "Compliance Officer".
* Role "Komite" hanya bisa approve/reject aplikasi pinjaman.
* Role "Sales" hanya bisa input member & aplikasi.

---

## 3. `sys_user_roles`

**Fungsi:**

* Relasi many-to-many user ↔ role.
* Memungkinkan satu user punya lebih dari satu role.

**Use Case:**

* User "Budi" punya role **Sales** dan **Branch Supervisor**.
* User "Andi" punya role **Analis** sekaligus **Komite**.

---

## 4. `sys_permissions`

**Fungsi:**

* Definisi granular hak akses (misalnya: `VIEW_MEMBER`, `EDIT_LOAN`, `APPROVE_APPLICATION`).
* Lebih detail daripada role.

**Use Case:**

* Permission `EXPORT_BILLING` hanya dimiliki role Finance.
* Permission `APPROVE_APPLICATION` hanya dimiliki role Komite.

---

## 5. `sys_role_permissions`

**Fungsi:**

* Relasi role ↔ permission.
* Mapping siapa boleh apa.

**Use Case:**

* Role "Admin" otomatis dapat semua permission.
* Role "Sales" hanya dapat `VIEW_MEMBER`, `CREATE_APPLICATION`.
* Role "Komite" hanya dapat `APPROVE_APPLICATION`.

---

## 6. `sys_modules`

**Fungsi:**

* Master modul yang ada di sistem (LOS, LMS, Sales, Member, Billing, Notification).
* Bisa dipakai untuk kontrol modul aktif/tidak.

**Use Case:**

* Modul `Billing` dimatikan sementara untuk maintenance.
* Modul `Funder` hanya aktif untuk koperasi tertentu.

---

## 7. `sys_user_sessions`

**Fungsi:**

* Tracking login session (token, IP, device, expired).
* Basis untuk Single Sign-On (SSO) atau multi-device login.

**Use Case:**

* User login dari HP → sistem simpan session dengan `device_info = Android`.
* Jika user logout → token dihapus dari tabel.
* Sistem force logout semua session user tertentu (misalnya saat password reset).

---

## 8. `sys_configurations`

**Fungsi:**

* Menyimpan konfigurasi global sistem (parameter & setting).
* Bisa diubah tanpa redeploy aplikasi.

**Use Case:**

* Simpan konfigurasi `MAX_LOGIN_ATTEMPTS = 5`.
* Simpan `DEFAULT_NOTIFICATION_CHANNEL = inapp`.
* Admin update `INTEREST_CAP = 12%`.

---

# 🎯 **Ringkasan Use Case User Management**

1. **Registrasi & Login User**

   * Admin buat user → user login → sistem cek password → buat session.

2. **Role & Permission Management**

   * Admin assign role ke user → role punya permission → sistem kontrol akses endpoint.

3. **Audit & Security**

   * Setiap login tercatat di `sys_user_sessions`.
   * Aktivitas penting (insert/update/approve) tercatat di `audit_trails` (sudah ada di db.txt).

4. **Configuration Management**

   * Sistem baca `sys_configurations` untuk parameter global (misalnya timeout, limit, dsr_default).

5. **Modular Control**

   * Sistem cek `sys_modules` untuk menentukan apakah modul tertentu aktif.

---

Dengan model **RBAC** yang kita bikin (user → role → permission → module), sistem ini bisa dipadukan dengan **JWT token** model mirip **Keycloak**. Jadi informasi akses user sudah *embed* di token, FE tinggal kasih token tiap request, BE tinggal validasi token tanpa harus query DB setiap kali.

---

# 📌 Konsep JWT mirip Keycloak

### 1. **Payload Token** (contoh format)

```json
{
  "sub": "123",                // user_id
  "preferred_username": "budi",
  "email": "budi@example.com",
  "full_name": "Budi Santoso",
  "roles": ["SALES", "SUPERVISOR"],
  "permissions": ["VIEW_MEMBER", "CREATE_APPLICATION"],
  "modules": ["LOS", "LMS", "MEMBER"],
  "iat": 1695709200,
  "exp": 1695716400,
  "iss": "pensiPro-auth"
}
```

👉 Jadi dari token ini saja, FE/BE sudah tahu:

* Siapa user-nya (`sub`, `username`, `email`).
* Role apa aja (`roles`).
* Hak akses granular (`permissions`).
* Modul apa saja yang aktif (`modules`).
* Berlaku sampai kapan (`exp`).

---

### 2. **Flow JWT**

1. User login → sistem validasi username/password → ambil data dari `sys_users`, `sys_user_roles`, `sys_role_permissions`.
2. Generate JWT dengan **secret key** atau **RSA keypair**.
3. FE simpan token di storage (biasanya `localStorage` atau `cookie`).
4. Setiap request FE → tambahkan header:

   ```
   Authorization: Bearer <jwt-token>
   ```
5. BE validasi signature + expiry token.
6. Kalau valid → cek claim role/permission → izinkan atau tolak akses endpoint.

---

### 3. **Keamanan**

* Token **signed** (HMAC256 / RSA256) → ga bisa diubah sembarangan.
* Bisa tambahin `aud` (audience), `iss` (issuer), `jti` (unique token id) buat lebih secure.
* Refresh token bisa dipakai untuk perpanjangan session (disimpan di `sys_user_sessions`).

---

### 4. **Kelebihan Model Ini**

✅ **Stateless** → BE tidak perlu query DB user setiap request.
✅ **Fast** → cukup validasi token + cek claim.
✅ **Scalable** → gampang di-deploy di banyak server (karena session ada di token).
✅ **Flexible** → claim di token bisa custom (misal: branch_id, funder_access).

---

# 🎯 Use Case JWT di PensiPro

1. **Sales Login** → token berisi role `SALES` + permission `CREATE_APPLICATION`.

   * FE bisa langsung hide menu yang ga punya permission.
   * BE auto tolak request kalau ga ada claim `CREATE_APPLICATION`.

2. **Komite Approval** → token berisi role `KOMITE` + permission `APPROVE_APPLICATION`.

   * Endpoint `POST /applications/{id}/decide` hanya bisa diakses kalau token punya permission itu.

3. **Finance Settlement** → token punya role `FINANCE`, module `Funder`.

   * Endpoint `POST /funders/{id}/settlements` cuma bisa diakses role FINANCE.

---

---


# 📡 **API – User Management PensiPro**

## 1. **Authentication & Session**

### 🔹 `POST /auth/login`

* **Fungsi:** Login user → validasi username/password → generate JWT token + simpan session di `sys_user_sessions`.
* **Tabel:** `sys_users`, `sys_user_sessions`.

### 🔹 `POST /auth/logout`

* **Fungsi:** Hapus/invalidasi session (blacklist token).
* **Tabel:** `sys_user_sessions`.

### 🔹 `POST /auth/refresh`

* **Fungsi:** Perpanjang session pakai refresh token.
* **Tabel:** `sys_user_sessions`.

---

## 2. **User Management**

### 🔹 `POST /users`

* **Fungsi:** Tambah user baru (admin, sales, analis, komite).
* **Tabel:** `sys_users`.

### 🔹 `GET /users`

* **Fungsi:** List semua user dengan filter (`is_active`, role).
* **Tabel:** `sys_users`, `sys_user_roles`.

### 🔹 `GET /users/{id}`

* **Fungsi:** Ambil detail user (roles, permissions, status).
* **Tabel:** `sys_users`, `sys_user_roles`, `sys_roles`.

### 🔹 `PUT /users/{id}`

* **Fungsi:** Update data user (email, phone, status).
* **Tabel:** `sys_users`.

### 🔹 `DELETE /users/{id}`

* **Fungsi:** Nonaktifkan user (soft delete `is_active=0`).
* **Tabel:** `sys_users`.

---

## 3. **Role Management**

### 🔹 `POST /roles`

* **Fungsi:** Tambah role baru (misalnya "Compliance Officer").
* **Tabel:** `sys_roles`.

### 🔹 `GET /roles`

* **Fungsi:** List role yang tersedia.
* **Tabel:** `sys_roles`.

### 🔹 `GET /roles/{id}`

* **Fungsi:** Detail role (permissions apa saja).
* **Tabel:** `sys_roles`, `sys_role_permissions`, `sys_permissions`.

### 🔹 `PUT /roles/{id}`

* **Fungsi:** Update role (ubah deskripsi/nama).
* **Tabel:** `sys_roles`.

### 🔹 `DELETE /roles/{id}`

* **Fungsi:** Nonaktifkan role (opsional soft delete).
* **Tabel:** `sys_roles`.

---

## 4. **User–Role Assignment**

### 🔹 `POST /users/{id}/roles`

* **Fungsi:** Assign role ke user.
* **Tabel:** `sys_user_roles`.

### 🔹 `DELETE /users/{id}/roles/{role_id}`

* **Fungsi:** Cabut role dari user.
* **Tabel:** `sys_user_roles`.

---

## 5. **Permission Management**

### 🔹 `POST /permissions`

* **Fungsi:** Tambah permission baru (misal `EXPORT_BILLING`).
* **Tabel:** `sys_permissions`.

### 🔹 `GET /permissions`

* **Fungsi:** List semua permission.
* **Tabel:** `sys_permissions`.

### 🔹 `POST /roles/{id}/permissions`

* **Fungsi:** Assign permission ke role.
* **Tabel:** `sys_role_permissions`.

### 🔹 `DELETE /roles/{id}/permissions/{perm_id}`

* **Fungsi:** Cabut permission dari role.
* **Tabel:** `sys_role_permissions`.

---

## 6. **Module Management**

### 🔹 `POST /modules`

* **Fungsi:** Tambah modul (LOS, LMS, Billing, Funder, Notification).
* **Tabel:** `sys_modules`.

### 🔹 `GET /modules`

* **Fungsi:** List modul yang tersedia & status aktif.
* **Tabel:** `sys_modules`.

### 🔹 `PUT /modules/{id}/status`

* **Fungsi:** Aktif/nonaktifkan modul.
* **Tabel:** `sys_modules`.

---

## 7. **Configuration Management**

### 🔹 `POST /configurations`

* **Fungsi:** Tambah konfigurasi global (misal `MAX_LOGIN_ATTEMPTS=5`).
* **Tabel:** `sys_configurations`.

### 🔹 `GET /configurations`

* **Fungsi:** List konfigurasi.
* **Tabel:** `sys_configurations`.

### 🔹 `PUT /configurations/{id}`

* **Fungsi:** Update konfigurasi (ubah nilai setting).
* **Tabel:** `sys_configurations`.

---

# 🎯 Ringkasan Fungsi API

* **Authentication:** login/logout/refresh session.
* **User:** CRUD user.
* **Role:** CRUD role.
* **User–Role:** assign & revoke role.
* **Permission:** definisi granular, assign ke role.
* **Modules:** kontrol modul aktif.
* **Configurations:** parameter global sistem.

---
 contoh **flow login + generate JWT** pakai struktur tabel `sys_users`, `sys_roles`, `sys_permissions`, dll yang udah kita set. Aku bikin dalam bentuk **pseudocode API** biar gampang diimplementasi ke stack manapun (Node.js, Go, Python, Java, dll).

---

# 🔑 **Login & JWT Generation Flow**

## 1. **Login Endpoint**

```http
POST /auth/login
Content-Type: application/json

{
  "username": "budi",
  "password": "rahasia123"
}
```

---

## 2. **Backend Logic (pseudocode)**

```python
def login(username, password):
    # 1. Cek user
    user = db.query("SELECT * FROM sys_users WHERE username = ?", [username])
    if not user:
        return {"error": "User not found"}, 401

    # 2. Verifikasi password
    if not verify_password(password, user.password_hash):
        return {"error": "Invalid credentials"}, 401

    # 3. Ambil role user
    roles = db.query("""
        SELECT r.role_name
        FROM sys_user_roles ur
        JOIN sys_roles r ON ur.role_id = r.role_id
        WHERE ur.user_id = ?
    """, [user.user_id])

    # 4. Ambil permission user
    permissions = db.query("""
        SELECT p.permission_code
        FROM sys_user_roles ur
        JOIN sys_roles r ON ur.role_id = r.role_id
        JOIN sys_role_permissions rp ON r.role_id = rp.role_id
        JOIN sys_permissions p ON rp.permission_id = p.permission_id
        WHERE ur.user_id = ?
    """, [user.user_id])

    # 5. Ambil module aktif
    modules = db.query("SELECT module_code FROM sys_modules WHERE is_active = 1")

    # 6. Generate JWT payload
    payload = {
        "sub": user.user_id,
        "preferred_username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "roles": [r.role_name for r in roles],
        "permissions": [p.permission_code for p in permissions],
        "modules": [m.module_code for m in modules],
        "iat": now(),
        "exp": now() + timedelta(hours=2),
        "iss": "pensiPro-auth"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # 7. Simpan session (opsional, untuk refresh token)
    db.insert("INSERT INTO sys_user_sessions (user_id, token, expired_at) VALUES (?, ?, ?)",
              [user.user_id, token, payload["exp"]])

    return {"access_token": token}
```

---

## 3. **Contoh JWT Payload**

```json
{
  "sub": 5,
  "preferred_username": "budi",
  "email": "budi@example.com",
  "full_name": "Budi Santoso",
  "roles": ["SALES", "SUPERVISOR"],
  "permissions": ["VIEW_MEMBER", "CREATE_APPLICATION"],
  "modules": ["LOS", "LMS", "MEMBER"],
  "iat": 1695709200,
  "exp": 1695716400,
  "iss": "pensiPro-auth"
}
```

---

## 4. **Validasi di Endpoint**

Contoh BE ketika ada request ke **buat aplikasi loan**:

```python
@requires_auth(permission="CREATE_APPLICATION")
def create_application(request):
    user = request.user  # hasil decode JWT
    # proses create aplikasi
    return {"status": "ok"}
```

👉 Middleware `requires_auth` akan:

1. Ambil token dari header `Authorization: Bearer <jwt>`.
2. Verifikasi signature + expiry.
3. Cek apakah `permission` ada di payload JWT.
4. Kalau tidak ada → return `403 Forbidden`.

---

# 🎯 Ringkasan

* JWT menyimpan info lengkap (user, role, permission, module).
* BE cukup validasi token → **stateless & scalable**.
* FE tinggal bawa token di tiap request → **secure**.


---


FE **bisa ekstrak** isi token JWT (khusus bagian **payload**) karena JWT itu sifatnya:

* **Header & Payload → base64 encoded (bisa dibaca siapa aja)**
* **Signature → encrypted (ga bisa dimanipulasi tanpa secret/private key)**

Contoh JWT bentuk string:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOjUsInJvbGVzIjpbIlNBT...
.DyOxlx7zFjZxW2I7E5U0bQG3k58JvD6Nn8
```

Kalau di **decode payload-nya** (misalnya pakai `atob` di JS atau jwt-decode lib), hasilnya jadi JSON:

```json
{
  "sub": 5,
  "preferred_username": "budi",
  "email": "budi@example.com",
  "roles": ["SALES", "SUPERVISOR"],
  "permissions": ["VIEW_MEMBER", "CREATE_APPLICATION"],
  "modules": ["LOS", "MEMBER"],
  "exp": 1695716400,
  "iss": "pensiPro-auth"
}
```

---

# ⚖️ Konsekuensi untuk FE

* **FE bisa baca payload JWT** → biasanya dipakai untuk:

  * Menentukan menu apa yang ditampilkan (hide button kalau user ga punya permission).
  * Menampilkan info profil user (nama, email).
* **FE tidak bisa memalsukan token** karena signature divalidasi di BE.

👉 Jadi walaupun FE bisa ekstrak, tetap **aman**, karena kalau FE coba ubah payload, signature jadi invalid → BE langsung tolak.

---

# 🔐 Praktik terbaik

1. Jangan taruh data sensitif (misal password hash) di payload JWT, karena bisa dibaca siapa saja.
2. Taruh hanya data identitas & hak akses (role, permission, module).
3. Validasi **selalu di BE**. FE hanya pakai payload untuk UX, bukan untuk keamanan utama.
