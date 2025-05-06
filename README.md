# SSTool - Release

Welcome to the official release repository. This repository contains the executable versions of the tool, ready for download.

## About SSTool

This is a tool primarily designed for performing SS (screenshots) on users of your Minecraft server. Simply download it, run it, and use the options you need.

The tool is currently in **Beta**. More functionalities will be added in future versions.

## Features

- Scan recent `.exe` files
- Check resource packs and mods
- Monitor recording applications
- Verify recently connected USB devices
- Monitor active Windows processes
- Detect mouse macro software

## How to download and use

1. Download the `.exe` file from the [Releases](https://github.com/7Str1kes/SSTool-release/releases/tag/1.0.0-BETA) section.
2. Run the file on the user's PC.
3. Select the option you want.

## Important Notes

- **This is a Beta version**: The tool is still under development, and some features may be subject to changes. We appreciate your suggestions and bug reports.
- More features will be added in future versions. Stay tuned for updates!
- Be sure to run the tool with sufficient privileges to access certain system processes.

## License

This repository and its contents are licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Comments and Support

If you encounter any issues or have suggestions for improvements, feel free to open an issue.

Stay tuned for future versions!


# SSTool - Source Code

## How to Compile

1. Make sure you have Python installed (version 3.8 or higher).
2. Install PyInstaller if you don't have it already:

    ```bash
    pip install pyinstaller
    ```

3. Compile the tool by running the following command from the project root:

    ```bash
    pyinstaller ss_tool.py --noconfirm --onefile --icon=logo.ico --name=SSTool-1.0.0-BETA
    ```

    This will generate the `.exe` file.