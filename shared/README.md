構築メモ

まずは、加瀬さんのwaseda-server-constructionのリポジトリを元に構築した。

Directory Serverの管理にはApache Directory Studioを用いる

instance.inf
self_sign_cert_valid_months = 360

/etc/openldap/ldap.con
TLS_REQCERT=never

cp /usr/share/dirsrv/schema/60sudo.ldif  /etc/dirsrv/slapd-ldap1/schema/

/etc/nssswitch.conf
sudoers: files sss
   を追加

systemctl restart ssd

Pam.d以下については、以下のサイトを参考にした。

https://wiki.archlinux.jp/index.php/LDAP_%E8%AA%8D%E8%A8%BC

pam.d以下をshared/etc 以下に格納。

/etc/pam.d/sudo

auth       sufficient      pam_sss.so
auth       required        pam_unix.so try_first_pass
auth       required        pam_nologin.so
account    include      system-auth
password   include      system-auth
session    include      system-auth


/etc/pam.d/passwd

#%PAM-1.0
# This tool only uses the password stack.
password        sufficient      pam_sss.so
#password       required        pam_cracklib.so difok=2 minlen=8 dcredit=2 ocredit=2 retry=3
#password       required        pam_unix.so sha512 shadow use_authtok
password        required        pam_unix.so sha512 shadow nullok


/etc/pam.d/su

#%PAM-1.0
auth            sufficient      pam_ldap.so
auth            required        pam_env.so
auth            sufficient      pam_rootok.so
# Uncomment the following line to implicitly trust users in the "wheel" group.
#auth           sufficient      pam_wheel.so trust use_uid
# Uncomment the following line to require a user to be in the "wheel" group.
#auth           required        pam_wheel.so use_uid
auth            substack        system-auth
auth            include         postlogin
auth            required        pam_unix.so use_first_pass
account         sufficient      pam_succeed_if.so uid = 0 use_uid quiet
account         include         system-auth
password        include         system-auth
session         include         system-auth
session         include         postlogin
session         optional        pam_xauth.so


/etc/pam.d/su-l

#%PAM-1.0
auth            sufficient      pam_ldap.so
auth            include         su
auth            required        pam_unix.so use_first_pass
account         include         su
password        include         su
session         optional        pam_keyinit.so force revoke
session         include         su



/etc/pam.d/passwd

