#!/usr/bin/env bash
set -euo pipefail

DRIVER_BUNDLE='cn.wch.CH34xVCPDriver'
DRIVER_URL='https://raw.githubusercontent.com/WCHSoftGroup/ch34xser_macos/main/CH34xVCPDriver.pkg'

ok() { printf 'OK: %s\n' "$1"; }
warn() { printf 'WARN: %s\n' "$1"; }
err() { printf 'ERROR: %s\n' "$1"; }

driver_info() {
  systemextensionsctl list 2>/dev/null || true
}

driver_installed() {
  driver_info | grep -q "$DRIVER_BUNDLE"
}

driver_enabled() {
  driver_info | grep -Eq 'activated[[:space:]]+enabled'
}

serial_ports() {
  ls /dev 2>/dev/null | grep -Ei '^(cu|tty)\.(usb|wch|SLAB|serial)' || true
}

usb_ch34x_connected() {
  ioreg -p IOUSB -l 2>/dev/null | grep -Eqi 'USB Serial|1A86|7523'
}

open_driver_settings() {
  open 'x-apple.systempreferences:com.apple.ExtensionsPreferences' >/dev/null 2>&1 || true
  open 'x-apple.systempreferences:com.apple.LoginItems-Settings.extension' >/dev/null 2>&1 || true
}

install_driver() {
  tmp_dir="$(mktemp -d)"
  pkg_file="$tmp_dir/CH34xVCPDriver.pkg"

  echo 'Downloading official CH34x driver...'
  curl -fL "$DRIVER_URL" -o "$pkg_file"

  echo 'Installing CH34x driver...'
  sudo installer -pkg "$pkg_file" -target /

  rm -rf "$tmp_dir"
  ok 'Driver package installed.'
}

echo '=== CH34x macOS driver setup ==='

if [ "$(uname)" != 'Darwin' ]; then
  err 'This script is only for macOS.'
  exit 1
fi

echo '[1/5] Checking driver package...'

if driver_installed; then
  ok 'CH34x driver is installed.'
else
  warn 'CH34x driver is not installed.'
  install_driver
fi

echo '[2/5] Checking driver approval...'

if driver_enabled; then
  ok 'CH34x Driver Extension is enabled.'
else
  warn 'Driver is installed but not approved/enabled yet.'
  echo 'Opening Driver Extensions settings...'
  open_driver_settings
  echo
  echo 'Enable this driver extension:'
  echo "$DRIVER_BUNDLE"
  echo
  echo 'Path: System Settings -> General -> Login Items & Extensions -> Driver Extensions'
  echo
  read -r -p 'Press Enter after enabling the driver, or press Enter to check later... '

  if driver_enabled; then
    ok 'Driver approved and active.'
  else
    warn 'Driver is still not active. You can approve it later and re-run this script.'
  fi
fi

echo '[3/5] Checking connected USB device...'

if usb_ch34x_connected; then
  ok 'CH34x USB device detected.'
else
  warn 'CH34x USB device is not connected or not detected.'
  echo 'This is OK for pre-install. Connect the device later and re-run this script to verify.'
fi

echo '[4/5] Checking serial port...'

ports="$(serial_ports)"

if [ -n "$ports" ]; then
  ok 'Serial port available:'
  printf '%s\n' "$ports" | sed 's#^#/dev/#'
else
  warn 'No serial port found yet.'
  echo 'This is expected if the device is not connected.'
fi

echo '[5/5] Status'

if driver_enabled; then
  if [ -n "$ports" ]; then
    ok 'READY: driver is active and serial device is available.'
  else
    ok 'PREPARED: driver is active. Connect the USB device later.'
  fi
else
  warn 'NOT READY: driver is installed but still needs macOS approval.'
fi
