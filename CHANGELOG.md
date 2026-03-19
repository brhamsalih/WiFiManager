# Changelog

## [2.0.0] - 2026-03-19

### 🚨 Breaking Changes

- Moved AP configuration to `wifi.json`
- Changed response format (STATUS → status)
- Removed constructor-based AP config

### ✨ Added

- `quick_connect()` for fast connection + auto-save
- `update_ap()` to update AP settings dynamically
- `status_sta()` and `status_ap()` APIs
- DHCP hostname support
- AP client tracking (MAC + count)

### 🔧 Improved

- Better AP lifecycle handling
- More consistent return values
- Storage structure now supports both networks and AP settings

### 🐛 Fixed

- AP restart issues
- Storage file handling edge cases
