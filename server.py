import argparse
import os
import socket

Upload_Folder = 'Uploads'
def ls(conn, directory='.'):
    parser = argparse.ArgumentParser(description='List files in a directory')
    parser.add_argument('directory', type=str, nargs='?', default='.')
    args = parser.parse_args()

    files = os.listdir(args.directory)
    files_str = '\n'.join(files)
    conn.sendall(files_str.encode('utf-8'))

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        return "File {} telah dihapus.".format(filename)
    else:
        return "File {} tidak ada.".format(filename)

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

def get_file_size(filename):
    if os.path.exists(filename):
        size_bytes = os.path.getsize(filename)
        return str(size_bytes)
    else:
        return "File {} tidak ada.".format(filename)

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        command = data.split()
        if command[0] == 'ls':
            ls(conn, command[1] if len(command) > 1 else '.')
        elif command[0] == 'rm':
            if len(command) > 1:
                response = remove_file(command[1])
            else:
                response = "Usage: rm [filename]"
            conn.sendall(response.encode('utf-8'))    
        elif command[0] == 'upload':
            if len(command) > 1:
                filename = command[1]
                response = upload(conn, filename)
                conn.sendall(response.encode('utf-8'))
            else:
                response = "Usage: upload [filename]"
            conn.sendall(response.encode('utf-8'))
            if response == "ready":
             continue 
        elif command[0] == 'download':
            if len(command) > 1:
                filename = command[1]
                response = download(conn, filename)
            else:
                response = "Usage: download [filename]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'size':
            if len(command) > 1:
                filename = command[1]
                response = get_file_size(filename)
            else:
                response = "Usage: size [filename]"
            conn.sendall(response.encode('utf-8'))
        elif command[0] == 'byebye':
            response = "Goodbye!"
            conn.sendall(response.encode('utf-8'))
            conn.close()
            break
        elif command[0] == 'connme':
            response = "Connection established successfully."
            conn.sendall(response.encode('utf-8'))
            continue  
        else:
         response = "Invalid command."
         conn.sendall(response.encode('utf-8'))
def main():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Menunggu koneksi...", PORT)

        while True:
            conn, addr = server_socket.accept()
            print('Connected by', addr)
            handle_client(conn)
            handle_client(conn)

if __name__ == "__main__":
    main()
