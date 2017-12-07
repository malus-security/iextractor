# Joker

[Joker](http://newosxbook.com/tools/joker.html) is a kernelcache inspecting tool created by [Jonathan Levin](http://newosxbook.com/index.php). We use it to extract the sandbox kernel extension (`com.apple.security.sandbox`).

Download it from [http://newosxbook.com/tools/joker.tar](http://newosxbook.com/tools/joker.tar).

Last downloaded: December 2, 2017
Executable file timestamps: September 10, 2017

## Joker and Kernel Extensions

Joker can be used to list all kernel extensions in a kernel cache file, with a command such as:

```
./joker.universal -k ../../store/tmp/iPhone_4.0_64bit_10.3_14E277/iPhone_4.0_64bit_10.3_14E277.kernelcache.mach.arm
```

In order to extract the sandbox extension, use a command such as:

```
./joker.universal -K com.apple.security.sandbox ../../store/tmp/iPhone_4.0_64bit_10.3_14E277/iPhone_4.0_64bit_10.3_14E277.kernelcache.mach.arm
```

The sandbox extension file will be placed in `/tmp/com.apple.security.sandbox.kext`.
