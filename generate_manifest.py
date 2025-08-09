import os
import json
from pyaxmlparser import APK

def create_manifest_for_category(category_name, base_url, output_path):
    """Scans a directory for APKs and generates a manifest.json file."""
    app_list = []
    print(f"\nScanning category: {category_name}...")

    if not os.path.isdir(category_name):
        print(f"Directory '{category_name}' not found. Skipping.")
        return

    # Create the icons directory if it doesn't exist
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"Created '{icons_dir}' directory.")

    for filename in sorted(os.listdir(category_name)):
        if filename.endswith(".apk"):
            filepath = os.path.join(category_name, filename)
            try:
                apk = APK(filepath)
                
                if not apk.package or not apk.package.strip():
                    print(f"  [!] Skipping {filename}: Invalid package name.")
                    continue
                
                print(f"  [+] Processing: {apk.application} ({apk.package})")
                
                # --- NEW AND IMPROVED ICON EXTRACTION ---
                try:
                    # Use the official method to get the icon path
                    icon_path_in_apk = apk.get_app_icon()

                    if icon_path_in_apk:
                        output_icon_path = os.path.join(icons_dir, f"{apk.package}.png")
                        icon_data = apk.get_file(icon_path_in_apk)
                        with open(output_icon_path, 'wb') as f:
                            f.write(icon_data)
                        print(f"    - Icon extracted successfully.")
                    else:
                        print(f"    - WARNING: Icon path not found inside the APK.")
                except Exception as icon_e:
                    print(f"    - WARNING: Could not extract icon. Reason: {icon_e}")

                # -------------------------------------------

                app_info = {
                    "appName": apk.application,
                    "packageName": apk.package,
                    "size": os.path.getsize(filepath),
                    "iconUrl": f"{base_url}/icons/{apk.package}.png",
                    "apkUrl": f"{base_url}/{category_name}/{filename}"
                }
                app_list.append(app_info)
                
            except Exception as e:
                print(f"  [!] CRITICAL ERROR processing {filename}: {e}")
                
    # Write the JSON manifest file
    manifest_file_path = os.path.join(output_path, f"{category_name}_manifest.json")
    with open(manifest_file_path, 'w', encoding='utf-8') as f:
        json.dump(app_list, f, indent=2, ensure_ascii=False)
        
    print(f"\nManifest for '{category_name}' created successfully at {manifest_file_path}")

if __name__ == '__main__':
    # !!! These details must match your GitHub repository !!!
    GITHUB_USERNAME = "ASDFG0537701349"
    GITHUB_REPOSITORY = "770kosher-app-apks"
    BRANCH = "main"

    RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/{BRANCH}"
    
    OUTPUT_DIR = "manifests"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process both categories
    create_manifest_for_category("apps", RAW_BASE_URL, OUTPUT_DIR)
    create_manifest_for_category("games", RAW_BASE_URL, OUTPUT_DIR)
    
    print("\n----------------------------------------------------")
    print("All done! Remember to commit and push the 'manifests' and 'icons' folders to your repository.")
    print("----------------------------------------------------")