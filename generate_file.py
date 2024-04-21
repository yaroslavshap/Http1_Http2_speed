# import subprocess
#
# # Путь к файлу, который нужно создать
# file_path = "/Users/aroslavsapoval/myProjects/data/large_file.bin"
#
# # Размер файла в байтах (20 МБ)
# file_size_mb = 6.47
# file_size_bytes = file_size_mb * 1024 * 1024 * 1024
#
# # Вызываем команду dd через subprocess для создания файла
# subprocess.run(["dd", "if=/dev/zero", f"of={file_path}", f"bs={file_size_bytes}", "count=1"])


# верхним способом получается генерить файлы до двух гигабайт


file_path = "/Users/aroslavsapoval/myProjects/data/large_file.bin"
# Define the size of the file in bytes
file_size_gb = 6 / 2
file_size = file_size_gb * 1024 * 1024 * 1024  # 6.47 GB

# Define the size of the blocks in bytes
block_size = 1024 * 1024  # 1 MB

# Open the file in write mode
with open(file_path, 'wb') as f:
    # Write zeros to the file until it reaches the desired size
    for _ in range(int(file_size / block_size)):
        f.write(b'\\0' * block_size)

print(f"A file of size {file_size_gb} GB has been successfully created as large_file.bin")
