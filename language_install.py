import argostranslate.package as package
import argostranslate.translate as translate

def install_languages(pairs):
    package.update_package_index()
    available_packages = package.get_available_packages()

    installed = translate.get_installed_languages()
    print("Installed Languages :", installed)
    installed_pairs = {
        (lang.code, to.code)
        for lang in installed
        for to in lang.translations
    }

    for from_code, to_code in pairs:
        if (from_code, to_code) in installed_pairs:
            continue

        pkg = next(
            (p for p in available_packages
             if p.from_code == from_code and p.to_code == to_code),
            None
        )

        if pkg:
            package.install_from_path(pkg.download())
            print(f"Installed {from_code} → {to_code}")
        else:
            print(f"Package not found: {from_code} → {to_code}")
