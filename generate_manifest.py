import os
import json
from urllib.parse import quote
from pyaxmlparser import APK

def create_manifest_for_category(category_name, base_url, output_path):
    # ... (כל תוכן המתודה נשאר זהה לחלוטין)
    """Scans a directory for APKs and generates a manifest file."""
    app_list = []
    print(f"\nScanning category: '{category_name}'...")

    if not os.path.isdir(category_name):
        print(f"Directory '{category_name}' not found. Skipping.")
        return

    # Create the icons directory if it doesn't exist
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Created '{icons_dir}' directory.")

    for filename in sorted(os.listdir(category_name)):
        if filename.lower().endswith(".apk"):
            filepath = os.path.join(category_name, filename)
            try:
                apk = APK(filepath)
                
                if not all([apk.package, apk.application, apk.version_name, apk.version_code]):
                    print(f"  [!] Skipping {filename}: Missing essential info (package, name, or version).")
                    continue

                print(f"  [+] Processing: {apk.application} (v{apk.version_name})")
                
                # Encode the icon package name for the URL
                encoded_icon_filename = quote(f"{apk.package}.png")
                icon_url_for_json = f"{base_url}/icons/{encoded_icon_filename}"
                extract_icon(apk, "icons")

                encoded_apk_filename = quote(filename)

                app_info = {
                    "appName": apk.application,
                    "packageName": apk.package,
                    "size": os.path.getsize(filepath),
                    "iconUrl": icon_url_for_json,
                    "apkUrl": f"{base_url}/{category_name}/{encoded_apk_filename}",
                    "versionName": apk.version_name, 
                    "versionCode": int(apk.version_code)
                }
                app_list.append(app_info)

            except Exception as e:
                print(f"  [!] CRITICAL ERROR processing {filename}: {e}")
                
    manifest_file_path = os.path.join(output_path, f"{category_name}.json")
    with open(manifest_file_path, 'w', encoding='utf-8') as f:
        json.dump(app_list, f, indent=2, ensure_ascii=False)
        
    print(f"\nManifest for '{category_name}' created successfully at {manifest_file_path}")

def extract_icon(apk, output_dir):
    # ... (כל תוכן המתודה נשאר זהה לחלוטין)
    """Extracts the APK's icon and saves it as a PNG."""
    try:
        icon_path_in_apk = apk.get_app_icon()
        if not icon_path_in_apk:
            print(f"    - WARNING: Icon not found for {apk.package}")
            return
        
        output_icon_path = os.path.join(output_dir, f"{apk.package}.png")
        icon_data = apk.get_file(icon_path_in_apk)
        with open(output_icon_path, 'wb') as f:
            f.write(icon_data)
    except Exception as e:
        print(f"    - WARNING: Could not extract icon for {apk.package}: {e}")


if __name__ == '__main__':
    # These details must match your GitHub repository
    GITHUB_USERNAME = "ASDFG0537701349"
    GITHUB_REPOSITORY = "770kosher-app-apks"
    BRANCH = "main"
    
    # *** התיקון הקריטי כאן: שינוי הדומיין ***
    MEDIA_BASE_URL = f"https://media.githubusercontent.com/media/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/{BRANCH}"
    
    OUTPUT_DIR = "listings"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process both categories using the new base URL
    create_manifest_for_category("apps", MEDIA_BASE_URL, OUTPUT_DIR)
    create_manifest_for_category("games", MEDIA_BASE_URL, OUTPUT_DIR)
    
    print("\n----------------------------------------------------")
    print("All done! Now, commit and push your changes.")
    print("----------------------------------------------------")