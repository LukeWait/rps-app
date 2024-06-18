# Rock Paper Scissors LAN App

## Description
The Rock Paper Scissors LAN App is an interactive GUI tool that allows users to connect over a local area network (LAN) to play Rock Paper Scissors and communicate via text messages.

<p align="center">
  <img src="https://github.com/LukeWait/rps-app/raw/main/assets/screenshots/rps-app-login.png" alt="App Screenshot" width="600">
</p>

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Source Code](#source-code)
- [Dependencies](#dependencies)

## Installation

### Executable
#### Windows
1. Download the `rps_app_win_v2_1_0.zip` from the [releases page](https://github.com/LukeWait/rps-app/releases).
2. Extract the contents to a desired location.
3. Run the `RPSApp.exe` file.

#### Linux
1. Download the `rps_app_linux_v2_1_0.zip` from the [releases page](https://github.com/LukeWait/rps-app/releases).
2. Extract the contents to a desired location.
3. Make the RPSApp file executable by running the following command in the terminal:
    ```sh
    chmod +x RPSApp
    ```
4. Run the RPSApp file by navigating to the directory in the terminal and executing:
    ```sh
    ./RPSApp
    ```

### From Source
To install and run the application from source:

1. Clone the repository:
    ```sh
    git clone https://github.com/LukeWait/rps-app.git
    cd rps-app
    ```

2. (Optional) Create and activate a virtual environment:
    - **Windows**:
      ```sh
      python -m venv rps_app_venv
      rps_app_venv\Scripts\activate
      ```
    - **Linux**:
      ```sh
      python3 -m venv rps_app_venv
      source rps_app_venv/bin/activate
      ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    - **Windows**:
      ```sh
      python src\rps_app.py
      ```
    - **Linux**:
      ```sh
      python src/rps_app.py
      ```

## Usage
After running the application, you can log in with your username and password or create a new account. Once connected to the network, you can challenge other users to a game of Rock Paper Scissors and chat with them using the built-in messaging system.

## Development
### Building Executables with PyInstaller
To build executables for Windows, macOS, and Linux, you can use PyInstaller. I recommend using PyInstaller version 6.1.0 as it is stable and does not flag the executable as a virus. First, ensure you have PyInstaller installed:
```sh
pip install pyinstaller==6.1.0
```
Then, run the following command to create an executable:
```sh
pyinstaller --onefile --add-data "assets/images:assets/images" --add-data "assets/fonts:assets/fonts" --add-data "assets/audio:assets/audio" --add-data "data:data" --noconsole src/rps_app.py
```
This will generate the executable in the `dist` directory. It will also create a `build` directory and `.spec` file. These are used in the build process and can be safely removed.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Icons used in the app are designed by Freepik - [www.freepik.com](https://www.freepik.com).

Fonts used in the app are open source Google Fonts.

## Source Code
The source code for this project can be found in the GitHub repository: [https://github.com/LukeWait/rps-app](https://www.github.com/LukeWait/rps-app).

## Dependencies
For those building from source, the dependencies listed in `requirements.txt` are:
- packaging==23.2
- customtkinter==5.2.1
- CTkMessagebox==2.5
- CTkListbox==0.10
- CTkToolTip==0.8
- Pillow==10.1.0
- gTTS==2.4.0
- playsound==1.2.2
