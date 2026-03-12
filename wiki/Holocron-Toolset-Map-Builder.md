# Holocron Toolset: Map Builder (Indoor Map Builder)

*This page is merged from the toolset in-app help (Tools/HolocronToolset/src/toolset/help/tools/).*

The Map Builder (Indoor Map Builder) creates new areas with unique layouts from existing room models. Open it from the Main Window via **Tools** → **Indoor Map Builder**.

You select models and insert them into the map; models can be attached to each other (shown by a green line between connections). When the layout is ready, **File** → **Build** outputs a module file to the game's module folder, ready to warp into.

## Kits

Kits are collections of models from specific game areas. The toolset does not ship with kits; you must download them first (prompted when the window opens, or **File** → **Download Kits**).

## Controls

| Action                  | Keys                                |
|-------------------------|-------------------------------------|
| Move Camera             | Hold **CTRL** and drag **LMB**      |
| Zoom Camera             | Hold **CTRL** and **Scroll**        |
| Rotate Camera           | Hold **CTRL** and drag **MMB**      |
| Place Model at Cursor   | **RMB**                             |
| Rotate Model at Cursor  | **Scroll**                          |
| Flip Model at Cursor    | **MMB**                             |
| Select Model            | **LMB** on model                    |
| Multi-Select            | Hold **SHIFT** and **LMB**          |
| Move Model              | Drag **LMB**                        |
| Open Context Menu       | **RMB**                             |

### See also

- [Indoor Map Builder User Guide](Indoor-Map-Builder-User-Guide) -- Full guide: rooms, doors, walkmeshes, building
- [Indoor Map Builder Implementation Guide](Indoor-Map-Builder-Implementation-Guide) -- Technical details
- [Kit Structure Documentation](Kit-Structure-Documentation) -- Kit layout and generation
- [BWM-File-Format](BWM-File-Format) -- Walkmesh format used by built modules
