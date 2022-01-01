# iExtractor: Automate Extraction from iOS Firmware Files

iExtractor is a collection of tools and scripts to automate data extraction from iOS firmware files (i.e. IPSW files). It runs on macOS and partially on Linux (certain tools and features only work on macOS).

IPSW (*iPhone Software*) files are provided publicly by Apple for OTA (over-the-air) updates for devices running iOS. [ipsw.me](https://ipsw.me/) provides links to IPSW files by device and iOS version. Similar information is on [The iPhone Wiki](https://www.theiphonewiki.com/wiki/Firmware_Keys).

IPSW files are ZIP files packing the filesystem, kernel image and other files. The filesystem image and kernel image files for iOS <= 9 are encrypted; the firmware keys for most of these files are provided by the community on [The iPhone Wiki](https://www.theiphonewiki.com/wiki/Firmware_Keys). In the command output below `058-25512-331.dmg` (the largest file) is the filesystem image file and `kernelcache.release.n41` is the kernel image file or the *kernelcache*.

```
$ unzip -l iPhone5,1_9.3_13E237_Restore.ipsw
  Length      Date    Time    Name
---------  ---------- -----   ----
  20660492  03-25-2016 08:55   058-25481-332.dmg
1623427584  03-25-2016 09:03   058-25512-331.dmg
  21491980  03-25-2016 08:55   058-25517-331.dmg
[...]
  10850444  03-25-2016 04:46   kernelcache.release.n41
[...]
```

iExtractor automates the unpacking, decryption and extraction of interesting data from IPSW files. Output data provided by iExtractor from IPSW files is:

  * an archive of the entire filesystem content
  * the kernelcache
  * system dynamic library files (`.dylib`) from the unpacked dynamic library shared cache (`dyld_shared_cache`)
  * reversed sandbox profiles

iExtractor is open source software released under the 3-clause BSD license.

## Installation

iExtractor uses external tools and glue scripts. You have to run iExtractor in the Bourne-again Shell (Bash).

After cloning the iExtractor repository, you have to clone some of the required tools as submodules:

```
git submodule update --init tools/sandblaster
git submodule update --init tools/xpwn
```

In order to install required packages use the commands below on Linux (Debian-based):

```
sudo apt-get update
sudo apt-get install coreutils grep sed tar wget unzip build-essential
sudo apt-get install libssl-dev python2.7 libz-dev libbz2-dev libusb-dev cmake libpng12-dev dmg2img
```

or the following commands on macOS using [MacPorts](https://www.macports.org/):

```
sudo port selfupdate
sudo port install coreutils grep wget unzip
sudo port install openssl python27 zlib bzip2 libpng cmake
sudo port install libusb
```

The `dmg2img` tool and package isn't required on macOS. The `libusb` installation isn't required and it's not detected by the `xpwn` installation.

There should be similar commands on macOS if you are using [Homebrew](https://brew.sh/).

Some external tools in the `tools/` subfolder need to be built. You need to build:

  * `vfdecrypt`

    ```
    cd tools/vfdecrypt/
    make
    ```

  * `lzssdec`

    ```
    cd tools/lzssdec/
    make
    ```

  * `dsc_extractor`

    ```
    cd tools/dyld/
    make
    ```

  * `xpwn`

    ```
    cd tools/xpwn/
    mkdir builddir
    cd builddir/
    cmake ..
    make
    ```

    Use `builddir/` for the folder name as it is hardcoded inside scripts.

  * `sandblaster` dependencies (only available on macOS):

    ```
    cd tools/sandblaster
    git submodule update --init tools/sandbox_toolkit
    # while in tools/sandblaster/
    cd tools/sandbox_toolkit/extract_sbops
    make
    # while in tools/sandblaster/
    cd tools/sandbox_toolkit/extract_sbprofiles
    make
    ```

## Setup

Before running iExtractor scripts you need to create a `config` file in the root of the repository. You can make a copy of the `config.sample` file and update that:

```
cp config.sample config
```

In the `config.sample` file downloaded and extracted data is stored in subfolders in the current directory (`STORE=.`). You can update the `STORE` variable to a different folder where you want the data stored.

You then need to create the storage subfolders. Assuming `STORE` points to the current directory (`.`), run the commands:

```
mkdir ipsw
mkdir out
```

The `ipsw/` folder stores downloaded IPSW files and the `out/` folder stores data extracted and processed by iExtractor. You will look in the `out/` folder for interesting data and copy data from/to the `out/` folder if you want to extract/process part of it on another system.

## Usage

In order to do all processing for a given firmware, use the `run_all` wrapper script. You need to pass it a firmware id, i.e. one of the file names in the `firmware-metadata/` subfolder:

```
./run_all iPhone5,1_9.3_13E237
```

If you want to do all steps except the lengthier (and more storage hungry) steps of packing the filesystem and extracting the system dynamic libraries files, you can use the `run_no_pack_fs_no_dyld` wrapper script:

```
./run_no_pack_fs_no_dyld iPhone5,1_9.3_13E237
```

Similarly, if you downloaded and unpacked IPSW files elsewhere (on another system), you copied the interesting extracted data and you want to work on that data without going into the download and unpack steps, you can use the `run_no_download_no_unpack` script:

```
./run_no_download_no_unpack iPhone5,1_9.3_13E237
```

You can run a single step by going to the `scripts/` subfolder and running a script there:

```
cd scripts/
./decrypt_kernel iPhone5,1_9.3_13E237
```

Or you can create your own custom script based on `run_all` or `run_no_pack_no_fs_no_dyld`. Read more below.

If you want to check all files and folders corresponding to a given firmware ID, use the `list_files` wrapper script. It gives you information about the existence and basic properties of those files (IPSW input file, kernelcache, reversed sandbox profiles etc.):

```
./list_files iPhone5,1_9.3_13E237
```

Similarly, if you want to remove all or some of the files and folders corresponding to a givn firmware ID, use the `clean.sample` script or create a script starting from that. The `clean.sample` script uses `rm -i` (i.e. interactive run) to prevent you from removing a file by mistake:

```
./clean.sample iPhone5,1_9.3_13E237
```

## Internals

External tools are located in the `tools/` subfolder. They are to be run through two layers of scripts: a lower-layer set of scripts located in the `bin/` subfolder and a higher-layer set of scripts in the `scripts/` subfolder. The scripts in the `scripts/` subfolder are the ones you will work with.

Each higher-layer script in the `scripts/` subfolder does a specific action: unpacking an IPSW file, extracting the dynamic library shared cache, extracting the sandbox extension etc.

Each script uses a firmware id as an argument; supported firmware ids are files in the `firmware-metadata/` subfolder; each file in the `firmware-metadata/` subfolder uses the firmware id as a name and stores in plain text firmware-related information required by scripts. You can add support for a new firmware, by creating a file in the `firmware-metadata/` subfolder named after the firmware id and filling it with the required information (download URL and decryption keys) similar to existing files.

You can run each script in the `scripts/` subfolder either by itself, or by tying scripts together in a wrapper script, such as `run_all`, `run_no_pack_fs`, `run_no_pack_fs_no_dyld`, `run_no_download_no_unpack` and `run_sandblaster`. For debugging purposes or if you want to work on the lower layers, use the scripts in the `bin/` subfolder.

When running a script, if previous output data exists it will prompt if you want to overwrite that. That is why, in a wrapper script, you would usually provide an `N` (for `no`) to the standard input of a script:

```
yes N | ./decrypt_kernel "$firmware_id"
```

You can start from existing scripts to create new ones and extend iExtractor to extract and process other interesting data from IPSW files.

## Documentation

Read in-depth information about iExtractor on [the wiki](https://github.com/malus-security/iExtractor/wiki).

## Community

Join us on [Discord](https://discord.gg/m3gjuyHYw9) for live discussions.
