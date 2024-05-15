# Pemrograman Jaringan Tugas-2

Philipus Pelea H. Bani 
IF-02-01 / 1203220159
--------------------------------

## Soal
Buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut :
a. Is : ketika client menginputkan command tersebut, maka server akan memberikan daftar file dan folder 
b. rm {nama file} : ketika client menginputkan command tersebut, maka server akan menghapus file dengan acuan nama file yang diberikan pada parameter pertama
c. download {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan file dengan acuan nama file yang diberikan pada parameter pertama
d. upload {nama file} : ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file dengan acuan nama file yang diberikan pada parameter pertama
e. size {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) dengan acuan nama file yang diberikan pada parameter pertama
f. byebye : ketika client menginputkan command tersebut, maka hubungan socket client akan diputus
g. connme : ketika client menginputkan command tersebut, maka hubungan socket client akan terhubung. 

- buat readme.md dengan memberikan Nama dan nim serta penjelasan dan cara menggunakan setiap command yang tersedia penilaian 50% : program 50% : readme
- Upload di github dan kumpulkan url repositorinya

## Hasil

**1. Command Ls**

```
def ls(conn, directory='.'):
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()

    files = os.listdir(args.directory)
    files_str = '\n'.join(files)
    conn.sendall(files_str.encode('utf-8'))
```    

Fungsi tersebut memiliki tujuan untuk mengirim daftar file dan folder dalam sebuah direktori kepada koneksi socket yang diberikan. Berikut adalah penjelasanmya :

`def ls(conn, directory='.'):`
   - Fungsi `ls` menerima dua argumen. Argumen pertama adalah `conn`. Argumen kedua adalah `directory`, yang merupakan direktori yang akan di-list. Argumen ini bersifat opsional, dengan nilai default `'.'`, yang artinya direktori saat ini.
`parser = argparse.ArgumentParser(description='List files in a directory')`
   - Membuat objek parser untuk mengurai argumen baris perintah. Ini adalah bagian dari modul `argparse` yang digunakan untuk memproses argumen baris perintah secara sistematis.
`parser.add_argument('directory', type=str, nargs='?', default='.')`
   - Menambahkan argumen `directory` ke parser. Argumen ini adalah argumen opsional yang mengizinkan kita untuk menentukan direktori yang akan di-list. `type=str` menunjukkan bahwa argumen ini harus berupa string. `nargs='?'` menunjukkan bahwa argumen ini adalah opsional. `default='.'` menunjukkan bahwa jika argumen ini tidak disediakan, nilai defaultnya adalah direktori saat ini (`'.'`).
`args = parser.parse_args()`
   - Mengurai argumen baris perintah yang diberikan kepada fungsi `ls` dan menyimpan hasilnya dalam objek `args`. Objek ini akan berisi nilai-nilai yang diberikan untuk setiap argumen yang didefinisikan sebelumnya pada objek parser.
`files = os.listdir(args.directory)`
   - Mengambil daftar file dan folder dalam direktori yang ditentukan oleh argumen `directory`. Nilai `args.directory` adalah nilai yang diberikan oleh pengguna atau nilai default `'.'` jika tidak ada nilai yang diberikan.
`files_str = '\n'.join(files)`
   - Menggabungkan daftar file dan folder menjadi satu string dengan pemisah baris baru (`'\n'`).
`conn.sendall(files_str.encode('utf-8'))`
   - Mengirim string yang berisi daftar file dan folder ke koneksi socket yang diberikan. Sebelum mengirim, string dikodekan ke format byte menggunakan UTF-8 agar dapat dikirim melalui koneksi socket. Metode `sendall` digunakan untuk memastikan bahwa semua data dikirimkan.

   - Output yang di dapat :

**2. Command rm**

```
def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return "File {} telah dihapus.".format(filename)
    else:
        return "File {} tidak ada.".format(filename)
```        

Fungsi `remove_file` digunakan untuk menghapus file dengan nama yang diberikan. 
Pada awalnya, fungsi memeriksa apakah file tersebut ada dalam sistem file dengan menggunakan `os.path.exists()`. 
Jika file tersebut ada, maka fungsi `os.remove()` akan digunakan untuk menghapusnya, diikuti dengan mengembalikan pesan yang menyatakan bahwa file telah dihapus. 
Jika file tidak ditemukan, fungsi akan mengembalikan pesan yang menyatakan bahwa file tersebut tidak ada dalam sistem file.

Outputnya:

**3. Command Upload**

```
def upload(conn, filename, upload_dir='.'):

     with open(filename, 'wb') as f:
         data = conn.recv(1024)
         while True:
             data = conn.recv(1024)
             if not data:
                 break
             f.write(data)
     print("File {} telah di upload.".format(filename)) 
```     

Fungsi `upload` bertanggung jawab untuk menerima dan menyimpan file yang dikirimkan melalui koneksi socket ke dalam sistem file. Pertama, fungsi membuka file dengan mode write-binary (`'wb'`) menggunakan perintah `open`. Selanjutnya, data diterima dari koneksi socket menggunakan `conn.recv(1024)`, yang berarti menerima data dalam potongan sebesar 1024 byte. Proses penerimaan data dilakukan dalam loop `while` untuk memastikan semua data file diterima dengan lengkap. Setelah data diterima, data tersebut ditulis ke file yang dibuka menggunakan `f.write(data)`. Loop akan berakhir ketika tidak ada data yang diterima lagi. Terakhir, fungsi akan mencetak pesan yang menyatakan bahwa file telah berhasil diunggah ke sistem file.

Outputnya :

**4. Command Download**

```
def download(conn, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)
        return "File {} berhasil di download.".format(filename)
    else:
        return "File {} tidak ada.".format(filename)
```

Fungsi `download` bertugas untuk mengirim file kepada klien melalui koneksi socket jika file dengan nama yang diberikan ada dalam sistem file. Pertama, fungsi memeriksa apakah file tersebut ada dalam sistem file menggunakan `os.path.exists()`. Jika file tersebut ada, maka file akan dibuka dengan mode read-binary (`'rb'`) menggunakan perintah `open`. Selanjutnya, data dari file dibaca dalam potongan sebesar 1024 byte menggunakan `f.read(1024)`, dan kemudian dikirimkan melalui koneksi socket ke klien menggunakan `conn.sendall(data)`. Proses ini dilakukan dalam loop `while` untuk memastikan semua data file terkirim. Setelah semua data terkirim, fungsi akan mengembalikan pesan yang menyatakan bahwa file berhasil diunduh. Jika file tidak ditemukan, fungsi akan mengembalikan pesan yang menyatakan bahwa file tidak ada dalam sistem file.

Output : 

**5. Command Size**

```
def get_file_size(filename):
    if os.path.exists(filename):
        size_bytes = os.path.getsize(filename)
        return str(size_bytes)
    else:
        return "File {} tidak ada.".format(filename)
```

Fungsi `get_file_size` bertujuan untuk mendapatkan ukuran file dengan nama yang diberikan. Pertama, fungsi memeriksa apakah file tersebut ada dalam sistem file menggunakan `os.path.exists()`. Jika file tersebut ada, ukuran file dalam byte diambil menggunakan `os.path.getsize(filename)`. Ukuran file tersebut kemudian dikonversi menjadi string dan dikembalikan. Jika file tidak ditemukan, fungsi akan mengembalikan pesan yang menyatakan bahwa file tidak ada dalam sistem file.

Output :

**6. Command Byebye**

```
elif command[0] == 'byebye':
            response = "Goodbye!"
            conn.sendall(response.encode('utf-8'))
            conn.close()
            break
```

Jika perintah yang diterima dari klien adalah 'byebye', maka server akan mengirimkan pesan "Goodbye!" kepada klien menggunakan conn.sendall(response.encode('utf-8')). Setelah itu, koneksi socket (conn) akan ditutup menggunakan conn.close(), yang mengakhiri hubungan antara server dan klien. Dengan kata lain, jika klien mengirimkan perintah 'byebye', server akan mengirimkan pesan perpisahan kepada klien dan kemudian menutup koneksi.

Output :

**7. Command Connme**

```
elif command[0] == 'connme':
            response = "Connection established successfully."
            conn.sendall(response.encode('utf-8'))
            continue  
        else:
         response = "Invalid command."
         conn.sendall(response.encode('utf-8'))
```

Jika perintah yang diterima adalah 'connme', server akan mengirimkan pesan "Connection established successfully." kepada klien menggunakan conn.sendall(response.encode('utf-8')), menandakan bahwa koneksi berhasil dibuat. Setelah itu, perulangan akan dilanjutkan ke iterasi selanjutnya menggunakan continue, sehingga server dapat terus menerima perintah-perintah berikutnya dari klien. Jika perintah yang diterima tidak valid (tidak cocok dengan perintah yang didefinisikan), server akan mengirimkan pesan "Invalid command." kepada klien menggunakan conn.sendall(response.encode('utf-8')).

Output :

## Soal Tambahan
1. Modifikasi agar file yang diterima dimasukkan pada folder tertentu
2. Modifikasi program agar memberikan feedback nama file dan filesize yang diterima
3. Apa yang terjadi jika pengirim mengirimkan file dengan nama yang sama dengan file yang telah dikirim sebelumnya? Dapat menyebabkan masalahkan? Lalu bagaimana solusinya? Implementasikan ke dalam program, solusi yang Anda berikan

----
#### Bagian yang diubah ada di bagian 'Def Upload'

```
def upload(conn, filename, upload_dir='.'):

    # with open(filename, 'wb') as f:
    #     data = conn.recv(1024)
    #     while True:
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         f.write(data)
    # print("File {} telah di upload.".format(filename)) 

    try:
        upload_dir = os.path.abspath(upload_dir)
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_destination = os.path.join(upload_dir, filename) #Menentukan lokasi Tujuan File yg akn diup
        if os.path.exists(file_destination):
            user_input = input("File {} sudah tersedia di {}. Apakah Anda ingin menggantinya? (y/n): ".format(filename, upload_dir))
            if user_input.lower() != 'y':
                return "Upload dibatalkan. File {} tidak diunggah.".format(filename)
        with open(file_destination, 'wb') as f:
            file_location = os.path.join(upload_dir, filename)
        return "File {} telah berhasil diunggah ke {}.".format(filename, file_location)
    except Exception as e:
        # Mengembalikan pesan error jika terjadi kesalahan
        error_message = "Terjadi kesalahan pada saat mengunggah file {}: {}".format(filename, str(e))
        print(error_message)
        return error_message
```

1. Pertama, kode akan mengambil alamat absolut dari direktori yang diberikan dan memeriksa apakah direktori tersebut ada. Jika tidak, maka kode akan membuatnya.
2. Kemudian, kode akan menentukan lokasi tujuan untuk file yang akan diunggah dengan menggabungkan direktori upload dengan nama file.
3. Jika file tersebut sudah ada di lokasi tujuan, kode akan meminta konfirmasi dari pengguna untuk menggantinya atau tidak.
4. Selanjutnya, kode akan membuka file yang akan diunggah dalam mode binary (wb) dan menetapkan lokasi file yang diunggah.
5. Akhirnya, jika tidak ada kesalahan yang terjadi dalam proses pengunggahan, kode akan mengembalikan pesan sukses yang menyatakan bahwa file telah berhasil diunggah ke lokasi yang ditentukan. 
Namun, jika terjadi kesalahan saat mengunggah file, pesan error akan ditampilkan dan kode akan mengembalikan pesan error tersebut.

#### File Berhasi diUpload


#### Filenya
