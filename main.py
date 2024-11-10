from encryption import *
from clipboard import *
from host import *
from client import *

from helper import get_internal_ip

if __name__ == "__main__":
    option = 0
    
    while (option != 4):
        print("1. Run as host")
        print("2. Run as client")
        print("3. Help")
        print("4. Exit")
        option = int(input("Enter option: "))
        
        if option == 1:
            public_key = input("Enter public key from client: ")
            encrypted_ip = encrypt_ip(get_internal_ip(), public_key)
            print(encrypted_ip)
            print("please share encrypted IP with client")
            run_host()
 

        elif option == 2:
            generate_keys()
            print("please share the above public key with the host and wait for the encrypted ip")
            host_ip = input("Enter the host encrypted IP")
            decrypted_ip = decrypt_ip(host_ip)
            print("here is the decrypted Ip: ", decrypted_ip)
            run_client(decrypted_ip)

        elif option == 3:
            print("""HI! Welcome to Clippy! We are here to help make your collaborative coding session easier than ever. Below is some info on how to use this executable!
                  
                  1. If you are the host select one from the option tree. You will then be prompted to ask your fellow collaborator for their public key so that we can 
                  securly create your session. 

                  2. If you are the client you will need to send your public key to the host. This will be created upoon you selecting option 2 from the start menu.
                  you will then need to wait for the host to send you the encrypted ip address and enter it so we can decode it ans start your session!

                  3. Once you have successfully initiated a connection the keybinds you must kow are below for each platform !

                    MacOS
                        - copy to local clipboard cmd+c
                        - send shared clipboard copy to shared clipboard cmd+;
                        - get from shared clipboard cmd+' and store in local clipboard
                        - Paste from local clipboard cmd+v

                    *please note that for your convienence we have seperated the shared and local clipboard so you can use your regular copy paste. If there is an item in shared clipboard you will ned to 
                    grab it or send it using the above commands*
                  
                    Microsoft
                        - copy to local clipboard ctrl+c
                        - send shared clipboard copy to shared clipboard ctrl+;
                        - get from shared clipboard ctrl+' and store in local clipboard
                        - Paste from local clipboard ctrl+v
                    *please note that for your convienence we have seperated the shared and local clipboard so you can use your regular copy paste. If there is an item in shared clipboard you will ned to 
                    grab it or send it using the above commands* 
                  """)
        elif option == 4:
            print("Goodbye!")

        else:
            print("Invalid option")
