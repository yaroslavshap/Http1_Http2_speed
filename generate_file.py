import subprocess

# Путь к файлу, который нужно создать
file_path = "large_file.bin"

# Размер файла в байтах (20 МБ)
file_size_mb = 2000
file_size_bytes = file_size_mb * 1024 * 1024

# Вызываем команду dd через subprocess для создания файла
subprocess.run(["dd", "if=/dev/zero", f"of={file_path}", f"bs={file_size_bytes}", "count=1"])
