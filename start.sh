#! /bin/bash
cd /home/ubuntu/
pwd
ls -al
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r DjangoApp1/requirements.txt
sudo chown ubuntu:www-data -R /home/ubuntu/DjangoApp1/
sudo chmod 775 -R /home/ubuntu/DjangoApp1/
source env.sh
python3 DjangoApp1/manage.py migrate
source env.sh
python3 DjangoApp1/manage.py collectstatic -y
sudo cp DjangoApp1/deploy/gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo cp DjangoApp1/deploy/DjangoApp1 /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/DjangoApp1 /etc/nginx/sites-enabled
sudo nginx -t && sudo systemctl restart nginx