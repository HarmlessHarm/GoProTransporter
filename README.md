# GoProTransporter

### Installation

#### Requirements
- **OS:** Windows (not tested on other distros)
- **Python:** 3.10 tested (should work with other versions)
- **Env:** Conda (or another virtual environment)

#### Install dependencies
Create a conda environment from `environment.yml`
```sh
conda env create -f environment.yml
```

### Usage
*Using python*
```sh
python GoProTransporter.py
```

1. Opens UI in with two directory selection buttons
2. Select directory with GoPro files (Example: `D:\DCIM\100GOPRO`)
3. Select the target directory in which you want to copy the files. (Example: `E:\2024_Q1_Skitrip`)
	- This script will create proxy files based on the `.LRV` files on the GoPro.
4. Press **Copy**
5. Wait until complete! (Or cancel)
	- Already copied files will be skipped


#### Proxy files
Proxy files will be generated in a format that Davinci Resolve expects.   
The `.LRV` files on the GoPro will be renamed from `GLxxxxxx.LRV` to `GXxxxxxx.mov` and they will be stored in a `proxies` that will be created inside the target directory.


### Building executable
The executable is generated using `pyinstaller` which is already included in the conda environment, using the folling command:
```sh
pyinstaller --onefile --windowed --additional-hooks-dir=./hooks GoProTransporter.py 
```
Alternatively you can use the `bundle.sh` shell script to do this for you
```sh
./bundle.sh
```
Then you can run script using the `GoProTransporter.exe` executable which is generated in `dist/`. You can place it anywhere and open the UI.


### TODO's
1. Other editing programs proxy setup.
2. No proxy option
3. Better styling of UI