# Burn Raspbian Image
## Format SD Card
```
diskutil eraseDisk ExFat raspi /dev/disk3
diskutil unmountDisk /dev/disk3
```
## Burn Raspbian Image
```
sudo dd bs=1m if=2020-02-13-raspbian-buster-lite.img of=/dev/rdisk3 conv=sync
```
## Enable SSH and Configure WIFI
```
diskutil mountDisk /dev/disk3
touch /Volumes/boot/ssh
cp wpa_supplicant /Volumes/boot/wpa_supplicant.conf
```

# Setup Raspbian
## Change Hostname
```bash
sudo hostname raspicam
```

## Update Packages
```bash
sudo apt update
sudo apt upgrade
```

# Install Git
```bash
sudo apt install git
```

# Install Docker

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo shutdown -r now
```

## Create SSH Keys
```bash
ssh-keygen
cat .ssh/id_rsa.pub 
```
Add public key to GitHub Account:
https://github.com/settings/keys

# Setup Juggling Project
## Clone Repo
```bash
mkdir ~/github
cd ~/github
git clone git@github.com:BreitbandModem/juggling.git
```

## Build and Run Docker Image
Manually build and run image
```bash
cd ~/github/juggling
docker build -t juggling:0.1 .
docker images
docker run -d -p 80:5000 -v /home/pi/github/juggling/app/webapp.py:/app.py juggling:0.1
```

Use automatic deploy script
```bash
ssh picam 'cd github/juggling/ && git pull origin master && ./deploy.sh'
```