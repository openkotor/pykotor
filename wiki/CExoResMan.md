# CExoResMan Resource Manager

This page documents the core resource manager used by both KotOR I and II.  All functions listed below were reverse-engineered from the game executables.

## Overview
The `CExoResMan` class provides a unified interface for locating and loading game resources (textures, models, scripts, etc.) from a variety of storage formats:

* **Directories** on disk
* **Encapsulated archives** (BIF/ERF)
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

## Address map (verified so far)

The following addresses were confirmed during this reverse-engineering session:

- `GetResOfType` @ (/K1/k1_win_gog_swkotor.exe @ 0x00407390, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `ServiceFromDirectory` @ (/K1/k1_win_gog_swkotor.exe @ 0x004078f0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `ServiceFromEncapsulated` @ (/K1/k1_win_gog_swkotor.exe @ 0x00407bd0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `ServiceFromImage` @ (/K1/k1_win_gog_swkotor.exe @ 0x00407d50, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `ServiceFromResFile` @ (/K1/k1_win_gog_swkotor.exe @ 0x00407e00, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `CancelRequest` @ (/K1/k1_win_gog_swkotor.exe @ 0x004088f0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `Demand` @ (/K1/k1_win_gog_swkotor.exe @ 0x004089f0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `Exists` @ (/K1/k1_win_gog_swkotor.exe @ 0x00408bc0, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `Update` @ (/K1/k1_win_gog_swkotor.exe @ 0x00408d40, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `ReadRaw` @ (/K1/k1_win_gog_swkotor.exe @ 0x00408e30, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)
- `WipeDirectory` @ (/K1/k1_win_gog_swkotor.exe @ 0x00408e90, /TSL/k2_win_gog_aspyr_swkotor2.exe @ TODO: Find this address)

## Behavior notes from decompilation

- `Demand` dispatches by storage kind using high bits of `CRes` metadata and forwards to one of the `ServiceFrom*` routines.
- `ReadRaw` is a thin dispatcher that routes to `ServiceFromDirectoryRaw`, `ServiceFromEncapsulatedRaw`, `ServiceFromImageRaw`, or `ServiceFromResFileRaw` based on source kind.
- `ServiceFromResFile` includes a resource-bucket index extraction step (`(res_id >> 0x14) & 0x3ff`) before virtual loader calls.
- `Update` maintains async/queued demand state (`+0x28`, `+0x2c`) and promotes resources into pending service when eligible.
- Add/remove helpers (`AddResourceDirectory`, `AddResourceImageFile`, `RemoveResourceDirectory`, `RemoveResourceImageFile`) are lightweight wrappers around key-table manager operations.

## Notes for contributors
- When adding new resource types, mimic the existing hash/lookup pattern.
- Ensure that resource tables are updated on both K1 and TSL; the engines are nearly identical.
- See the `2DA-File-Format.md` page for how key tables are structured.

(Additional research pending: cross-reference with actual BIF/ERF parsing functions in the codebase.)