# CExoResMan Resource Manager

This page documents the core resource manager used by both KotOR I and II.  All functions listed below were reverse-engineered from the game executables.

## Overview
The `CExoResMan` class provides a unified interface for locating and loading game resources (textures, models, scripts, etc.) from a variety of storage formats. The order in which it checks those sources matches the game's [resource resolution order](KEY-File-Format#key-file-purpose): override directory, then loaded MOD/SAV, then KEY/BIF.

* **Directories** on disk (e.g. override)
* **Encapsulated containers** (BIF/ERF)
* **Image resources** (raw binary blobs)
* **Resource files** (ERF modules)

Every lookup path follows the same basic structure:

1. Check the `CRes` structure for flags or already-cached data.
2. Compute a hash or index key using helper calls (`0x005e9b60`/`0x005e9b90`).
3. Iterate the relevant table until a match is found.
4. Call into the resource-specific loader via virtual methods.
5. Update the `CRes` object and optionally fire callbacks.

## Key methods

- `GetResOfType` – returns a `CExoStringList` of resource names by type.
- `AddResourceDirectory`/`AddResourceImageFile` – register search paths.
- `ServiceFromDirectory`/`ServiceFromEncapsulated`/`ServiceFromImage`/`ServiceFromResFile` – core lookup routines for each storage type.
- `CancelRequest`/`Demand` – control reference counting and cancellation.
- `Exists` – quick existence test that fills a timestamp pointer.
- `Update` – periodic maintenance, may refresh internal caches.
- `ReadRaw` – fetch raw bytes; dispatches to the appropriate service method.
- `WipeDirectory` – internal utility used when a directory is removed.

All routines are documented with their decompiled pseudocode in the source code comment above.

## Notes for contributors
- When adding new resource types, mimic the existing hash/lookup pattern.
- Ensure that resource tables are updated on both K1 and TSL; the engines are nearly identical.
- See the [2DA-File-Format](2DA-File-Format) page for how key tables are structured.

(Additional research pending: cross-reference with actual BIF/ERF parsing functions in the codebase.)

### See also

- [KEY-File-Format](KEY-File-Format) -- Resource resolution order and BIF/KEY layout
- [BIF-File-Format](BIF-File-Format), [ERF-File-Format](ERF-File-Format) -- Container formats
- [2DA-File-Format](2DA-File-Format) -- Key table structure; [reverse_engineering_findings](reverse_engineering_findings) -- Engine analysis