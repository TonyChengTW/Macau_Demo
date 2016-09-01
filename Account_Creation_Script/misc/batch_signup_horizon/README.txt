usage:

1. git clone git@172.16.100.91:samlo/misc.git; cd misc/batch_signup_horizon;

2. edit config.py to fit your needs

3. run "python gen_list.py" to generate list.json as account menifest

4. check the content of list.json

5. run "python create_accounts.py" to create accounts

6. verify the result by horizon/openstack cli

7. run "python delete_accounts.py" to clean what you have done

p.s. Do not modify list.json before clean up action, delete_accounts.py needs this list to work

