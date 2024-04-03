# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create directories if they don't exist
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "<html>\n<head>\n</head>\n<body>\nHolberton School\n</body>\n</html>\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {\n\tlisten 80 default_server;\n\tlisten [::]:80 default_server;\n\troot /var/www/html;\n\tindex index.html index.htm index.nginx-debian.html;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n}",
  owner   => 'root',
  group   => 'root',
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
