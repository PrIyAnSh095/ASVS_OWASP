import zipfile
import os

print("Generating Test Archives for ASVS 5.2.3...")

# 1. Normal Zip
with zipfile.ZipFile("normal.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("test1.txt", "Hello World")
    zf.writestr("test2.txt", "Secure coding is fun.")
print("Created normal.zip (Passes both)")

# 2. Too Many Files Zip (Inode Exhaustion simulation)
with zipfile.ZipFile("many-files.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for i in range(15): # Secure app limits to 10
        zf.writestr(f"file_{i}.txt", "tiny")
print("Created many-files.zip (Fails secure, Passes vulnerable)")

# 3. Simulated Zip Bomb (Large uncompressed size)
# Generates 15MB of zeroes, which compresses down to a few kilobytes.
# Secure app limits to 5MB uncompressed.
massive_data = b"0" * (15 * 1024 * 1024) 
with zipfile.ZipFile("simulated-zip-bomb.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("bomb.txt", massive_data)
print("Created simulated-zip-bomb.zip (Fails secure, Extracts 15MB blindly in vulnerable)")

print("Done!")
