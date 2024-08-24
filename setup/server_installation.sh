#!/bin/bash

# Ensure the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Prompt for the domain name
read -p "Enter the domain name (e.g., subdomain.domain.example): " DOMAIN_NAME

# Check if SSL certificate already exists
if [ ! -f "/etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem" ]; then
    is_ssl_certificate_required=true
else
    is_ssl_certificate_required=false
    echo "SSL certificate already exists for $DOMAIN_NAME. Skipping certificate request."
fi

if [ "$is_ssl_certificate_required" = true ]; then
    # Prompt for the email address for Certbot (optional)
    read -p "Enter your email address for Certbot (this is used for warnings about expiry, deprecation, etc. Leave blank to not provide an email address): " CERTBOT_EMAIL
fi

# Generate SSH Key if it doesn't exist
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
fi

# Prompt to add SSH key to GitHub
cat ~/.ssh/id_rsa.pub
echo "Add the above SSH key to your GitHub account."
echo "Press [Enter] key after adding the SSH key to GitHub..."
read -p ""

# List of GitHub SSH key fingerprints
GITHUB_KEYS=(
    "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl"
    "github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg="
    "github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVlOhGeYrnZaMgRK6+PKCUXaDbC7qtbW8gIkhL7aGCsOr/C56SJMy/BCZfxd1nWzAOxSDPgVsmerOBYfNqltV9/hWCqBywINIR+5dIg6JTJ72pcEpEjcYgXkE2YEFXV1JHnsKgbLWNlhScqb2UmyRkQyytRLtL+38TGxkxCflmO+5Z8CSSNY7GidjMIZ7Q4zMjA2n1nGrlTDkzwDCsw+wqFPGQA179cnfGWOWRVruj16z6XyvxvjJwbz0wQZ75XK5tKSb7FNyeIEs4TT4jk+S4dhPeAUC5y+bDYirYgM4GC7uEnztnZyaVWQ7B381AK4Qdrwt51ZqExKbQpTUNn+EjqoTwvqNj4kqx5QUCI0ThS/YkOxJCXmPUWZbhjpCg56i+2aB6CmK2JGhn57K5mj0MNdBXA4/WnwH6XoPWJzK5Nyu2zB3nAZp+S5hpQs+p1vN1/wsjk="
)

# Add GitHub's SSH key fingerprints to known hosts if not already present
for KEY in "${GITHUB_KEYS[@]}"; do
    if ! grep -q "$KEY" ~/.ssh/known_hosts; then
        echo "$KEY" >> ~/.ssh/known_hosts
    fi
done

# Generate a secure MySQL root password excluding specific characters
MYSQL_ROOT_PASSWORD=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#%^&*()_+-=') for _ in range(31)))")

# Update package lists and upgrade all packages
apt update && apt upgrade -y

# Install Python, pip, git, MySQL server, Nginx, and Certbot
apt install python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx expect -y

# Add Swap Space if it doesn't exist
if [ ! -f /swapfile ]; then
    fallocate -l 4G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
fi

# Increase Swapiness
echo vm.swappiness=60 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Install MySQL Server
apt install mysql-server -y

# Create a Minimal MySQL Configuration
echo "
[mysqld]
innodb_buffer_pool_size=64M
innodb_log_file_size=32M
max_connections=50
table_open_cache=400
performance_schema=OFF
" >> /etc/mysql/mysql.conf.d/mysqld.cnf

# Start MySQL Service
systemctl start mysql

# Secure MySQL installation
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -e "DROP USER IF EXISTS ''@'localhost';"
mysql -e "DROP USER IF EXISTS ''@'$(hostname)';"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "FLUSH PRIVILEGES;"

# Log in to MySQL and set root password
mysql -u root <<MYSQL_SCRIPT
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY '$MYSQL_ROOT_PASSWORD';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

# Obtain an SSL certificate if required
if [ "$is_ssl_certificate_required" = true ]; then
    if [ -z "$CERTBOT_EMAIL" ]; then
        certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --register-unsafely-without-email
    else
        certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos -m $CERTBOT_EMAIL
    fi
fi

# Clone the Repository or pull the latest changes
if [ -d "/root/ginrummy-engine" ]; then
    cd /root/ginrummy-engine && git pull
else
    git clone git@github.com:SimonMayer/ginrummy-engine.git /root/ginrummy-engine && cd /root/ginrummy-engine
fi

# Create a Virtual Environment
python3 -m venv venv

# Activate the Virtual Environment
source venv/bin/activate

# Install Dependencies
pip install flask_cors flask_jwt_extended mysql-connector-python bcrypt gevent

# Install Gunicorn
pip install gunicorn

# Install and Set Up the Database
python3 -m setup.install_database --host=localhost --user=root --database=GinRummy --password="$MYSQL_ROOT_PASSWORD"

# Prompt for user creation details in a loop
while true; do
    read -p "Do you want to create a new user? (yes/no): " CREATE_USER
    case "${CREATE_USER,,}" in
        yes | y )
            read -p "Enter the username for the new user: " APP_USERNAME
            while true; do
                read -s -p "Enter the password for the new user: " APP_PASSWORD
                echo
                read -s -p "Confirm the password for the new user: " APP_PASSWORD_CONFIRM
                echo
                if [ "$APP_PASSWORD" == "$APP_PASSWORD_CONFIRM" ]; then
                    break
                else
                    echo "Passwords do not match. Please try again."
                fi
            done
            python3 -m app.create_user $APP_USERNAME $APP_PASSWORD
            ;;
        no | n )
            break
            ;;
        * )
            echo "Please answer yes/y or no/n."
            ;;
    esac
done

# Set Up systemd Service
echo "
[Unit]
Description=Gunicorn instance to serve ginrummy-engine
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/ginrummy-engine
Environment=\"PATH=/root/ginrummy-engine/venv/bin\"
ExecStart=/root/ginrummy-engine/venv/bin/gunicorn --timeout 3600 --workers 3 --worker-class gevent --bind 127.0.0.1:8000 --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log wsgi:app

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ginrummy-engine.service

mkdir -p /var/log/gunicorn
chown www-data:www-data /var/log/gunicorn

# Reload systemd and Start Gunicorn Service
systemctl daemon-reload
systemctl start ginrummy-engine
systemctl enable ginrummy-engine

# Set Up Nginx as a Reverse Proxy with SSL
echo "
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name $DOMAIN_NAME;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        rewrite ^/?(.*)$ /\$1 break;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_buffering off;
    }
}
" > /etc/nginx/sites-available/ginrummy-engine

# Enable the custom Nginx configuration
if [ ! -f /etc/nginx/sites-enabled/ginrummy-engine ]; then
    ln -s /etc/nginx/sites-available/ginrummy-engine /etc/nginx/sites-enabled/
fi

# Remove the default Nginx configuration if it exists
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

# Restart Nginx
systemctl restart nginx
