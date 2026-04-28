# Patches (CI / fork note)

`holocron-indoor-builder-3d-preview.patch` is a `git format-patch` export of HolocronToolset changes for Indoor Map Builder’s OpenGL tile preview. Apply inside `Tools/HolocronToolset` when the submodule gitlink cannot be fetched:

```bash
cd Tools/HolocronToolset && git am ../../patches/holocron-indoor-builder-3d-preview.patch
```

Then commit the submodule in the PyKotor root as usual.
