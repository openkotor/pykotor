# Patches (CI / fork note)

`holocron-indoor-builder-3d-preview.patch` is a unified diff against the checked-in HolocronToolset submodule ref (`f7a656b38…`) for Indoor Map Builder’s OpenGL tile preview. Apply when the HolocronToolset remote is unreachable:

```bash
cd Tools/HolocronToolset && git apply ../../patches/holocron-indoor-builder-3d-preview.patch
```

Then commit inside `Tools/HolocronToolset` and update the submodule gitlink in the PyKotor root.

The patch matches **`AreaEntity` / `AreaExporter`** mesh categories (floors, walls, doorframes from last hook, inner/outer corners, room objects) and wires **`OpenGLSceneRenderer`** (`QOpenGLWidget`) with map refresh after load/new/module extract. Separate Avalonia apps (**Kit Editor**, interaction **modes**) are not duplicated in PyKotor—only data + preview/export parity.
