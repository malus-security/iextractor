# VFDecrypt

[VFDecrypt](https://www.theiphonewiki.com/wiki/VFDecrypt) is used to decrypt Apple iOS root filesystem images. Root filesystem images inside IPSW files are encrypted for iOS >= 9. Since iOS 10, root filesystem images are not encrypted and VFDecrypt is no longer required.

Decrypting root filesystem images requires the decryption key. This is provided for most root filesystem images version by the community at [The iPhone Wiki](https://www.theiphonewiki.com/wiki/Firmware_Keys).

There are several VFDecrypt builds available on the Internet. We've used and updated the implementation [here](https://github.com/trailofbits/iverify-oss/tree/master/vendor/vfdecrypt). We've updated `vfdecrypt.c` to support OpenSSL >= 1.1.0 and the `Makefile` to be OS-dependent.

You can build and run `lzssdec` on macOS and on Linux.

You build `vfdecrypt` using

```
make
```

You runn `vfdecrypt` by passing it the root filesystem key, the root filesystem image and the output (decrypted) file:

```
./vfdecrypt -i ~/Projects/store/out/iPhone5,1_9.3_13E237/058-25512-331.dmg -k 2a66fd6377af8f60d5e300ac3aa8d9c44a1c0dee94579ad3f8a26515debbf381bb971ae8 -o decrypted.dmg
```

iExtractor runs `vfdecrypt` as part of the `bin/decrypt_fs` and `scripts/decrypt_fs` scripts.
