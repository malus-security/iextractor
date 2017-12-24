# LZSS Decompress

[LZSS (Lempel–Ziv–Storer–Szymanski)](https://en.wikipedia.org/wiki/Lempel–Ziv–Storer–Szymanski) is a compression algorithm used to compress the Apple iOS kernelcache. Apples provides their LZSS decompression implementation as [open source code](https://opensource.apple.com/source/BootX/BootX-59/bootx.tproj/sl.subproj/lzss.c).

`lzzdec` is a tool created by Willem Hengeveld used to decompress LZSS-packed files. Originally downloaded from [here](http://nah6.com/~itsme/cvs-xdadevtools/iphone/tools/lzssdec.cpp) (there are other links available in the Internet), it's referred by [NowSecure's guide to reversing the iOS kernel](https://www.nowsecure.com/blog/2014/04/14/ios-kernel-reversing-step-by-step/).

A raw kernelcache file inside an IPSW file (such as `kernelcache.release.n41`) is encrypted for iOS <= 9 and compressed with LZSS for all iOS versions. A (decrypted) kernelcache dump consists of a header and the actual LZSS-compressed kernelcache. In order to use `lzssdec` you need to find the offset of the LZSS-compressed part in the kernelcache dump. We created a custom Python script for that in `../../bin/get_lzss_section_offset.py`, by taking into account that the compressed part starts with the Mach-O magic header word `0xfeedface` or `0xfeedfacf`.

You can build and run `lzssdec` on macOS and on Linux.

You build `lzssdec` using

```
make
```

You run `lzssdec` by passing it the offset to the LZSS-compressed part, as provided by the `../../bin/get_lzss_section_offset.py` script and the (decrypted) kernelcache dump as standard input. For example:

```
$ ../../bin/get_lzss_section_offset.py ~/Projects/store/out/iPhone5,1_9.3_13E237/kernelcache.decrypted
448
$ ./lzssdec -o 448 < ~/Projects/store/out/iPhone5,1_9.3_13E237/kernelcache.decrypted > kernelcache.mach.arm
$ file kernelcache.mach.arm
kernelcache.mach.arm: Mach-O armv7s executable, flags:<NOUNDEFS|PIE>
```

iExtractor runs `lzssdec` as part of the `bin/decrypt_kernel` and `scripts/decrypt_kernel` scripts.

[Joker](http://newosxbook.com/tools/joker.html) is also able to decompress kernelcache dumps but only for 64bit kernels.
