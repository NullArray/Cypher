# Cypher

Cypher is a proof of concept ransomware which implements the PyCrypto module and uses gmail(Currently) as a simple command and control server.
It is a work in progress as of yet and i will be releasing updates periodically depending on a couple of factors

# Operation

Cypher operates by generating a unique client ID for each box that has been infected. The client ID and encryption key will be sent via email to a gmail adress by leveraging python's SMTP lib. The new version of Cypher will give the operator the choice to pick between gmail and the C&C infrastructure that comes with the finished project, namely a web application to generate and store key pairs together with client IDs. If the operator chooses to employ the Cypher web app the ransomware will contact via HTTP by leveraging the Mechanize lib.

After Cypher has enumerated the files we wish to encrypt the multiprocessing and PyCrypto libs are employed to do the actual encrypting. I opted to use the multiprocessing lib to speed up the encryption process.

Finally Cypher will write out a README note and the client ID which would have to be relayed to the operator
in order to retrieve the proper decrypting binary and key respectively.

# Update

I have added some logic to have the ransomware log in to the web app with the Mechanize lib. As of yet functionality to retrieve a key from the web app and to post the client ID have not been implemented. SMTP is still available and in the near future optional depending on the preference of the operator.

I am setting up a web application as an alternative C&C mechanism, in keeping with the Python theme of this project i am employing the Django framework for the web app. Commits will be pushed to the repo in due time.

The latest version of the encryption module adds bootlocker functionality by attempting to overwrite the MBR with a custom bootloader.
Shoutout to NO-OP for his contribution in this regard. I've added the source code together with boot.bin for illustrative purposes.  

# To do

* Extensive and multi-platform testing.

* ~~Write decrypting module.~~

* Functionality to restore MBR

* Designing and developing a more secure C&C mechanism.
  * ~~Possibly HTTP in favor of SMTP~~ and;
  * Web App to dynamically provide encryption keys in favor of local generation

# Want to contribute?

I'd be more than willing to collaborate on this and if you wish to contribute feel free to open an issue or a pull request and we may discuss the details and/or ideas we could work on and you might want to suggest.



![alt tag](https://pbs.twimg.com/media/CfJsdtPWsAEc-Gs.jpg)
 
### Note 

Development of C&C web application has been postponed for the time being. If you want to get creative i would recommend [this fork](https://github.com/NullArray/Ransom) or [this original](https://github.com/filtration/Ransom) web application written in PHP with Laravel by my friend [Filtration](https://github.com/filtration). It is compatible with Cypher with a little tinkering.

Furthermore, someone seems to have uploaded the stub for the main Cypher file to Virus Total. You can check it out by clicking [here](https://www.virustotal.com/en/file/93fbdc903478e94596c083099c0adc1bb929f39894cc3782e19ff501339d0746/analysis/). For testing purposes i'd be interested to see detection rates for the Windows variant once it's encoded with someting like [peCloakCapstone](https://github.com/v-p-b/peCloakCapstone) or [PeCloak](https://www.securitysift.com/pecloak-py-an-experiment-in-av-evasion/). That is of course after the main Python file has been compiled to exe with Py2Exe or Pyinstaller.

Also, if you have any pull requests to submit please feel free to do so. Open Source collaboration on this Ransomware remains to be of import to me.

Thanks.
