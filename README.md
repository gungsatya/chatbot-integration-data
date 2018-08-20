# chatbot-integration-data
Chatbot pertukaran data dengan aplikasi Group Me

### File  Bot2User.py

1. 	Fungsi getLastIdMessageIn
	Fungsi yang digunakan untuk mengambil id message yang masuk dan di simpan di tabel msg_in. Ini biar program engga ngambil message yang sudah diambil sebelumnya dan tidak memberatkan database.

2.	Fungsi insertMessageIN 
	Fungsi untuk memasukan pesan yang diterima saat long polling kedalam tabel msg_in

3.	Fungsi search
	Fungsi untuk mencari paket2 pulsa yang ada dalam tabel pulse sesaui dengan nama pulsa/operator yang dimasukan pengguna.

4.	Fungsi buy
	Fungsi untuk memasukan data ke dalam tabel trx(transaksi)

5.	Fungsi sendMessage
	Fungsi untuk mengirim pesan ke group.

6.	Fungsi receiveMessages (Fungsi paling penting)
	Fungsi yang berguna untuk menerima pesan, mengatur hasil balasan yang diperlukan sesuai dengan pesan yang dikirim pengguna.


### File Bot2Bot.py

File ini jadi akan menjadi library di Bot2bot_in.py Bot2bot_out.py. Kenapa dipisah ? ini supaya kerja dari masing-masing fungsi berjalan optimal. karena kerja dari menerima, dan mengirim pesan sangat berat.

1. 	Fungsi getLastIdMessageIn
	Fungsi yang digunakan untuk mengambil id message yang masuk dan di simpan di tabel msg_in. Ini biar program engga ngambil message yang sudah diambil sebelumnya dan tidak memberatkan database.

2.	Fungsi insertMessageIN 
	Fungsi untuk memasukan pesan yang diterima saat long polling kedalam tabel msg_in

3.	Fungsi sendMessage
	Fungsi untuk mengirim pesan ke group.

4.	Fungsi isExistData
	Fungsi untuk mengecek apakah data yang dicari ada di tabel dan kolom yang sudah ditentukan. type 0 untuk melihat di Database MySQL, type 1 untuk mencari di database temporary SQLite.

5.	Fungsi do
	Fungsi untuk menjalankan query yang dikirimkan oleh bot lain.

6.	Fungsi importDb
	Fungsi untuk membuat 2 database SQlite, database temporary.db adalah database temporary yang digunakan untuk menampung data awal dari database MySQL, mirror.db adalah database yang dipakai oleh Client.

7.	Fungsi pulseChecker
	Fungsi untuk mengecek perubahan data yang terjadi di dalam tabel pulse dengan cara membandingkan data yang ada di dalam mysql dengan data yang ada di dalam sqlite temporary

8.	Fungsi trxChecker
	Sama seperti pulseChecker, cuma dia ngecek tabel trx

9.	Fungsi getMyName
	Fungsi untuk mengambil data nama bot yang kita gunakan, supaya kita ga mengambil pesan dari diri kita sendiri.

10.	Fungsi receiveMessages (Fungsi paling penting)
	Fungsi yang berguna untuk menerima pesan, mengatur hasil balasan yang diperlukan sesuai dengan pesan yang dikirim pengguna.

### File ClientListenner.py

Fungsinya cuma satu, cuma untuk menerima masukan dari client PHP dan mengirim datanya ke tabel trx yang ada di MySQL

	
