linux: 
	gcc -o vfdecrypt vfdecrypt.c -lcrypto
mac:
	gcc -I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib/ -o vfdecrypt vfdecrypt.c -lcrypto -DMAC_OSX
install: 
	cp ./vfdecrypt /usr/local/bin
	ldconfig
uninstall:
	rm -rf /usr/local/bin/vfdecrypt
clean:
	rm -rf ./vfdecrypt
