#Cypher

Cypher is a proof of concept ransomware which implements the PyCrpto module and uses gmail(Currently) as a simple command and control server.
It is a work in progress as of yet and i will be releasing updates periodically depending on the amount of time i have to work on the project.

#Operation

Cypher operates by generating a unique client ID for each box that has been infected. The client ID and encryption key will be sent via email
to a gmail adress by leveraging python's SMTP lib. After Cypher has enumerated the files we wish to encrypt
the multiprocessing and PyCrypto libs are employed to do the actual encrypting.
I opted to use the multiprocessing lib to speed up the encryption process.

Finally Cypher will write out a README note and the client ID which would have to be relayed to the operator
in order to retrieve the proper decrypting binary and key respectively.

#Update

The lastest version of the encryption module adds bootlocker functionality by attempting to override the MBR with a custom bootloader.
Shoutout to NO-OP for his contribution in this regard. I've added the source code together with boot.bin for illustrative purposes.  

#To do

* Extensive and multi-platform testing.

* ~~Write decrypting module.~~

* Functionality to restore MBR

* Designing and developing a more secure C&C mechanism.
1. Possibly HTTP in favor of SMTP and;
2. Web App to dynamically provide encryption keys in favor of local generation

#Want to contribute?

I'd be more than willing to collaborate on this and if you wish to contribute feel free to open an issue or a pull request and we may discuss the details and/or ideas we could work on and you might want to suggest.



![alt tag](https://pbs.twimg.com/media/CfJsdtPWsAEc-Gs.jpg)
 

