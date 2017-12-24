# Dynamic Shared Cache Extractor

Apple dyld (*dynamic link editor*) loads and links the shared/dynamic libraries (`.dylib` files in Apple OSes: macOS, iOS). It is provided as open source software by Apple; you can [browse it](https://opensource.apple.com/source/dyld/) or you can download [dyld tarballs](https://opensource.apple.com/tarballs/dyld/). There is an [unofficial repository](https://github.com/opensource-apple/dyld) that's currently (December 2017) not updated to the latest dyld provided by Apple (`519.2.1`).

As told by [the iPhoneDevWiki](http://iphonedevwiki.net/index.php/Dyld_shared_cache) "all system (private and public) libraries have been combined into a big cache file to improve performance". This file is named `dyld_shared_cache_...` with a suffix denoting the architecture. Extraction of libraries from the dyld shared cache is not trivial since certain symbols are updated ("redacted").

Based on [ant4g0nist's blog post](http://ant4g0nist.blogspot.ro/2015/04/ios-shared-cache-extraction-to-solve.html), we downloaded the latest [dyld tarball](https://opensource.apple.com/tarballs/dyld/) (`dyld-519.2.1.tar.gz`), copied the contents of the `launch-cache/` subfolder in the repository and added a `Makefile` to build `dsc_extractor` (*dyld shared cache extractor*). `dsc_extractor` is used to extract the library files from the dyld shared cache. In the `dsc_extractor.cpp` source code file we enabled the `main` function to allow the building of the `dsc_exctractor` executable.

Building and running `dsc_extractor` requires macOS. To build the `dsc_extractor` executable run `make`:

```
make
```

To run `dsc_extractor` pass it two arguments: the path to the dyld shared cache file and the output folder that will store the extracted library files. The command below extracts the shared library files for an iOS 9 dyld shared cache in the current directory:

```
./dsc_extractor /mnt/ios/iPhone5,1_9.3_13E237/System/Library/Caches/com.apple.dyld/dyld_shared_cache_armv7s .
```
