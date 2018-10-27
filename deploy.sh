#!/bin/bash
args=("$@")

if [ $# -eq 0 ]
	 then
		echo "Too few arguments. Usage: deploy.sh /path/to/django/root "
else
	cd ${args[0]}
	curl -s -o eventsignup.tar https://example.com
	tar -xf eventsignup.tar

fi

