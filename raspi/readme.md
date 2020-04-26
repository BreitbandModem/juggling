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

# Install Docker

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
```