```Bash
cat /etc/services | grep -i "^ldap" | sort --reverse > ~/foundit.txt && cat ~/foundit.txt
```
````Bash
ldaps           636/udp
ldaps           636/tcp                         # LDAP over SSL
ldap            389/udp
ldap            389/tcp                 # Lightweight Directory Access Protocol
```
