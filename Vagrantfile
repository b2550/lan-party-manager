Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 5000, host: 5001
  config.vm.provision "shell", inline: <<-SHELL
    echo "--INSTALLING PYTHON--"
    apt-get update
    apt-get install -y python-pip python-dev build-essential
    export FLASK_APP=/vagrant/myonic/__init__.py
    export FLASK_DEBUG=1
    echo "--SETTING BASH PROFILE--"
    echo "export FLASK_APP=/vagrant/app/__init__.py" >> /etc/profile
    echo "export FLASK_DEBUG=1" >> /etc/profile
    echo "cd /vagrant/app" >> /etc/profile
    cat /etc/profile
    echo "--INSTALLING REQUIREMENTS--"
    pip install -r /vagrant/requirements.txt
  SHELL
end
