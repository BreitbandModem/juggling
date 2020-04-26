diskutil eraseDisk ExFat raspi /dev/disk3
diskutil unmountDisk /dev/disk3
sudo dd bs=1m if=2020-02-13-raspbian-buster-lite.img of=/dev/rdisk3 conv=sync
diskutil mountDisk /dev/disk3
touch /Volumes/boot/ssh
cp wpa_supplicant /Volumes/boot/wpa_supplicant.conf
