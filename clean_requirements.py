# GP38a

# clean_requirements.py

WINDOWS_ONLY_PACKAGES = {
    'pywin32', 'pypiwin32', 'winshell', 'colorama', 'win32-setctime',
    'wmi', 'comtypes', 'pyreadline', 'pywinauto'
}

output_file = "requirements_clean.txt"

with open("requirements.txt", "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        pkg = line.strip().split("==")[0].lower()
        if pkg in WINDOWS_ONLY_PACKAGES:
            print(f"⚠️  Removing Windows-only package: {pkg}")
        else:
            outfile.write(line)

print(f"\n✅ Cleaned requirements saved to: {output_file}")


