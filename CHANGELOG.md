# Changelog

All notable changes to this project will be documented in this file.
This project follows Semantic Versioning (MAJOR.MINOR.PATCH).

---

## [1.0.1] - 2026-01-03

### Added

- Human-readable WiFi status codes (no more magic numbers)
- Auto-reconnect strategy with retry handling

### Fixed

- Fix ESP32 reset (WDT) when client connects to AP mode
- Fix unstable AP activation sequence
- Fix blocking delays during WiFi operations

### Improved

- Improved AP configuration order (config before active)
- Better handling of power instability during AP startup
- Refactored internal state transitions for STA/AP modes

### Internal

- Code cleanup and better separation of responsibilities
- Reduced unnecessary blocking calls

---

## [1.0.0] - 2025-12-20

### Added

- Initial release of WiFiManager
- STA mode with stored networks
- AP fallback mode
- Network scan and auto-connect logic
