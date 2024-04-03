#!/bin/bash

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a fake HTML file for testing
echo "<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>This is a test page for Nginx configuration</h1>
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Create symbolic link /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current to hbnb_static
sudo sed -i '/server_name _;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

exit 0
