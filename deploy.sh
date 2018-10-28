#!/bin/bash
args=("$@")

if [ $# -ne 3 ]
	 then
		echo "Too few arguments. Usage: deploy.sh path user group"
		echo ""
		echo "Path: /path/to/django/root"
		echo "user: owner of files/folders in root"
		echo "group: usergroup of files/folders in root"
		echo ""
else
	cd ${args[0]}
	static_owner=""
	static_group=""
		if [ -d ./static ]
		then
			file_meta=($(ls -ld ./static))
			static_owner="${file_meta[2]}"
			static_group="${file_meta[3]}"
		else
			static_owner=${args[1]}
			static_group=${args[2]}
		fi
	curl -s -o eventsignup.tar https://example.com
	tar -xf eventsignup.tar
#eventsignup, omat, static, media
	chown -R ${args[1]} eventsignup/
	chown -R ${args[1]} omat/
	chgrp -R ${args[2]} omat/
	chgrp -R ${args[2]} eventsignup/

fi

