#!/bin/bash

# cleans up the appdir directory
rm -rf appdir

# initializes the appdir directory for flatpak usage
flatpak build-init appdir com.rhtraining.demoapp com.redhat.Platform com.redhat.Sdk el9
# creates a sandboxed bin directory in the appdir directory
flatpak build appdir mkdir /app/bin
# makes the hello-world.sh script executable
flatpak build appdir chmod +x hello-world.sh
# installs the hello-world.sh script in the bin directory
flatpak build appdir install -Dm755 hello-world.sh /app/bin/hello-world.sh
# installs the .desktop file in the applications directory
flatpak build appdir install -Dm644 com.rhtraining.demoapp.desktop /app/share/applications/com.rhtraining.demoapp.desktop
# installs the icon in the icons directory
flatpak build appdir install -Dm644 com.rhtraining.demoapp.png /app/share/icons/hicolor/128x128/apps/com.rhtraining.demoapp.png
# installs the metainfo file in the metainfo directory
flatpak build appdir install -Dm644 com.rhtraining.demoapp.metainfo.xml /app/share/metainfo/com.rhtraining.demoapp.metainfo.xml
# Finish the build with the appropiate permissions
flatpak build-finish --command="hello-world.sh" --share=ipc --socket=fallback-x11 --socket=wayland appdir
# Deletes the repo directory
rm -rf ~/repo
# Creates the repo directory
flatpak build-export ~/repo appdir stable
# Deploys the flatpak repository file
cp rhtraining.flatpakrepo ~/repo
cp icon.png ~/repo
cp rhtraining.gpg ~/repo
# Signs the repository
flatpak build-sign ~/repo --gpg-sign=9DC24AE7C186B84CAD9A381CD176CF204974AA22 --gpg-homedir=gpg
# Signs the summary file
flatpak build-update-repo  ~/repo --gpg-sign=9DC24AE7C186B84CAD9A381CD176CF204974AA22 --gpg-homedir=gpg