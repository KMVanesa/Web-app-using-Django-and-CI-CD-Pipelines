#! /bin/bash
cd /home/ubuntu/
DIR=/home/ubuntu/DjangoApp1
if [ -d "$DIR" ]; then
    sudo rm -rf DjangoApp1/
    sudo systemctl daemon-reload
    sudo systemctl restart gunicorn
    sudo nginx -t && sudo systemctl restart nginx
else 
    echo "$DIR does not exist."
fi
