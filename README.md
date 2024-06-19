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
1. Download the latest Windows release from the [releases page](https://github.com/LukeWait/rps-app/releases).
2. Extract the contents to a desired location.
3. Run the `RPSApp.exe` file.

#### Linux
1. Download the latest Linux release from the [releases page](https://github.com/LukeWait/rps-app/releases).
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
    - **Windows**:
      ```sh
      pip install -r requirements.txt
      ```
     - **Linux**:
       ```sh
       sudo apt-get install python3-gi
       sudo apt-get install python3-gi-cairo gir1.2-gtk-3.0
       sudo apt-get install libcairo2-dev
       sudo apt install libgirepository1.0-dev
       pip install pygobject==3.42.2
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

- **Add New User**: When playing for the first time you will need to create a profile. Click the `Add New User` button on the login page. Choose an avatar, username and password. Note: Password must contain at least 8 characters, 1 number, and 1 symbol. User information, including hashed passwords, is stored in a plain text file (user_data.txt) within the application directory.

<p align="center">
  <img src="https://github.com/LukeWait/rps-app/raw/main/assets/screenshots/rps-app-new-user.png" alt="New User Screenshot" width="600">
</p>

- **Hosting A Game**: From the `Host` tab you can choose to host a game that others can connect to. You can also select the number of rounds to be played.

<p align="center">
  <img src="https://github.com/LukeWait/rps-app/raw/main/assets/screenshots/rps-app-hosting.png" alt="Hosting Screenshot" width="600">
</p>

- **Joining A Game**: From the `Join` tab you can search for anyone waiting to host a session on the network.

<p align="center">
  <img src="https://github.com/LukeWait/rps-app/raw/main/assets/screenshots/rps-app-joining.png" alt="Joining Screenshot" width="600">
</p>

- **Playing A Game**: Once you're connected to another player, the connection status display will update. You can now freely use the text chat feature to communicate. Choose Rock, Paper, and Scissors from the buttons at the top of the output. Once the pre-determined rounds are completed, you will be disconnected.

<p align="center">
  <img src="https://github.com/LukeWait/rps-app/raw/main/assets/screenshots/rps-app-playing.png" alt="Playing Screenshot" width="600">
</p>

- **Disconnecting**: To stop a current network connection, click on the green network icon in the bottom right corner. Note: disconnecting mid-game will result in forfeiting the remaining rounds.

- **Changing User & Exiting**: To log out or exit the application, click on the profile icon in the top left corner. Note: disconnecting mid-game will result in forfeiting the remaining rounds.

- **Settings**: From the `Settings` tab you can choose to turn on/off audio options and select network ports.

## Development
### Building Executables with PyInstaller
#### Windows
Run the following command from the project main directory:
```sh
pyinstaller --onefile --add-data "assets/images:assets/images" --add-data "assets/fonts:assets/fonts" --add-data "assets/audio:assets/audio" --add-data "data:data" --noconsole src/rps_app.py
```
#### Linux
For Linux, you need to create a hook-PIL.py file to handle the PIL library correctly. Follow these steps:
1. Create a file named hook-PIL.py in the main directory of your project with the following content:
    ```sh
    from PyInstaller.utils.hooks import copy_metadata, collect_submodules

    datas = copy_metadata('Pillow')
    hiddenimports = collect_submodules('PIL')
    ```
2. Run the following command from the project main directory:
    ```sh
    pyinstaller --onefile --add-data "assets/images:assets/images" --add-data "assets/fonts:assets/fonts" --add-data "assets/audio:assets/audio" --add-data "data:data" --additional-hooks-dir=. --noconsole src/rps_app.py
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
- customtkinter==5.2.1
- CTkMessagebox==2.5
- CTkListbox==0.10
- CTkToolTip==0.8
- Pillow==10.1.0
- gTTS==2.4.0
- playsound==1.2.2
