# Forge --> Toolset Merge Plan

Exhaustive file-by-file mapping of **Forge** (`vendor/KotOR.js/src/apps/forge/`) features to **Toolset** (`Tools/HolocronToolset/src/toolset/`) counterparts, with what to merge.

**📖 Companion Document**: [docs/LEVEL_EDITOR_CHECKLIST.md](docs/LEVEL_EDITOR_CHECKLIST.md) -- Comprehensive Unity/UE5-class feature roadmap for the unified Module Designer.

**🎯 Vision**: Transform the Module Designer into an **All-In-One level editor** where Indoor Builder room assembly, Forge-style walkmesh editing, and full GIT object placement happen in a single unified canvas with contextual modes -- comparable to Unity, Unreal Engine, Valve Hammer, and Bethesda Creation Kit.

---

## 1. Resource-Type Editors (Blueprint Editors)

Each Forge editor has a matching Toolset editor. Forge adds **inline 3D preview** and richer field layouts.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 1 | `components/tabs/tab-utc-editor/TabUTCEditor.tsx` | Creature blueprint editor -- appearance, stats, equipment slots, classes, scripts, **inline 3D model preview** | `gui/editors/utc.py` | Add 3D model preview panel, improve equipment slot UI |
| 2 | `components/tabs/tab-utd-editor/TabUTDEditor.tsx` | Door blueprint editor -- lock/trap settings, scripts, appearance, **inline 3D preview** | `gui/editors/utd.py` | Add 3D door model preview, improve lock/trap UI |
| 3 | `components/tabs/tab-ute-editor/TabUTEEditor.tsx` | Encounter blueprint editor -- creature lists, spawn options, difficulty, scripts | `gui/editors/ute.py` | Add encounter difficulty settings, improve creature list UI |
| 4 | `components/tabs/tab-uti-editor/TabUTIEditor.tsx` | Item blueprint editor -- base item, cost, properties, model variation, **inline 3D preview** | `gui/editors/uti.py` | Add 3D item model preview, better property editing |
| 5 | `components/tabs/tab-utm-editor/TabUTMEditor.tsx` | Store/merchant blueprint editor -- inventory list, buy/sell flags, markup, scripts | `gui/editors/utm.py` | Improve store inventory list with item thumbnails |
| 6 | `components/tabs/tab-utp-editor/TabUTPEditor.tsx` | Placeable blueprint editor -- appearance, locks, traps, scripts, inventory, **inline 3D preview** | `gui/editors/utp.py` | Add 3D placeable model preview |
| 7 | `components/tabs/tab-uts-editor/TabUTSEditor.tsx` | Sound blueprint editor -- sound list with **audio preview/selector**, distance, volume, looping, priority | `gui/editors/uts.py` | Add inline audio preview/playback for sound entries |
| 8 | `components/tabs/tab-utt-editor/TabUTTEditor.tsx` | Trigger blueprint editor -- trap settings, scripts, faction, cursor | `gui/editors/utt.py` | Improve trap/script UI layout |
| 9 | `components/tabs/tab-utw-editor/TabUTWEditor.tsx` | Waypoint blueprint editor -- name, map note, appearance, linked-to | `gui/editors/utw.py` | Minor UI improvements |

### Forge Blueprint Data Models (reference for field completeness)

These hold the full GFF field definitions for each blueprint type. Use these `pykotor` mappings to verify Toolset editors expose all fields.

| # | Forge File | Relevant PyKotor File(s) | What It Represents |
|---|-----------|--------------------------|-------------------|
| 10 | `module-editor/ForgeCreature.ts` | `resource/generics/utc.py` (+ helper: `tools/creature.py`) | All UTC fields -- appearance, stats, equipment, classes, scripts |
| 11 | `module-editor/ForgeDoor.ts` | `resource/generics/utd.py` (+ helper: `tools/door.py`) | All UTD fields -- lock, trap, scripts, appearance, walkmeshes |
| 12 | `module-editor/ForgePlaceable.ts` | `resource/generics/utp.py` (+ helper: `tools/placeable.py`) | All UTP fields -- appearance, lock, trap, scripts, inventory |
| 13 | `module-editor/ForgeSound.ts` | `resource/generics/uts.py` | All UTS fields -- sound resrefs, volume, distance, looping |
| 14 | `module-editor/ForgeTrigger.ts` | `resource/generics/utt.py` | All UTT fields + polygon vertices for area-of-effect |
| 15 | `module-editor/ForgeWaypoint.ts` | `resource/generics/utw.py` | All UTW fields -- map note, appearance, linked-to |
| 16 | `module-editor/ForgeEncounter.ts` | `resource/generics/ute.py` | All UTE fields + spawn-point list + region polygon |
| 17 | `module-editor/ForgeCamera.ts` | `resource/generics/git.py` (`class GITCamera`) | GIT camera fields -- FOV, pitch, position, orientation |

---

## 2. 3D Module Designer

The crown jewel. Forge's module editor is a full 3D scene editor with transform gizmos, object placement, scene graph, and camera controls.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 18 | `components/tabs/tab-module-editor/TabModuleEditor.tsx` | Full 3D module editor -- transform/rotate/add-object toolbar, context menus, sidebar, scene graph | `gui/windows/module_designer.py` | Port tool palette, transform gizmos, context menus, object-add workflow |
| 19 | `components/ModuleEditorSidebarComponent.tsx` | Module editor sidebar -- scene graph tree + GIT instance property editor for selected objects | `gui/windows/module_designer.py` | Port sidebar with scene graph + property panel for selected instances |
| 20 | `components/UI3DRendererView.tsx` | React canvas wrapper for 3D renderer with camera-view menu bar | `gui/widgets/renderer/module.py` | Port camera-view selector menu |
| 21 | `components/UI3DToolPalette.tsx` | Floating toolbar for 3D editors -- selectable/expandable tool buttons with icons | `gui/windows/designer_controls.py` | Port floating tool palette with select/translate/rotate/place modes |
| 22 | `components/UI3DOverlayComponent.tsx` | HUD overlay showing real-time camera position and rotation | `gui/widgets/renderer/module.py` | Add camera position/rotation HUD overlay |
| 23 | `components/SceneGraphTreeView.tsx` | Hierarchical tree-view of scene objects with expand/collapse and selection | `gui/windows/module_designer.py` | Port scene graph tree view into module designer sidebar |
| 24 | `UI3DRenderer.tsx` | Core Three.js 3D rendering engine -- scene, cameras (orbit/first-person), transform controls, raycasting, groups, render loop | `gui/widgets/renderer/module.py` | Port transform control modes (translate/rotate/scale gizmos), orbit camera, first-person camera, improved raycasting |
| 25 | `states/tabs/TabModuleEditorState.tsx` | Module editor state -- loads IFO/ARE/GIT, manages 3D scene, object selection, transform controls, add-object modes | `gui/windows/module_designer.py` + `data/me_controls.py` | Port formal control mode state machine (select/move/rotate/place) |
| 26 | `enum/EditorControlsTool.ts` | Enum: None, Select, Object Move/Rotate, Camera Move/Rotate, Placeable | `gui/windows/designer_controls.py` | Port explicit tool mode enum |
| 27 | `enum/EditorControlsCameraMode.ts` | Enum: Editor (free), Static, Animated camera modes | `data/me_controls.py` | Port camera mode switching |
| 28 | `enum/ModuleEditorTabMode.ts` | Enum: Edit vs Preview mode | `gui/windows/module_designer.py` | Port edit/preview mode toggle |

### Forge Module Data Models

| # | Forge File | What It Represents |
|---|-----------|-------------------|
| 29 | `module-editor/ForgeModule.ts` | Module data -- IFO fields (entry point, areas, scripts, time, description) |
| 30 | `module-editor/ForgeArea.ts` | Area data -- loads ARE/GIT/LYT/VIS, manages rooms and all GIT-listed game objects |
| 31 | `module-editor/ForgeRoom.ts` | Room data -- loads room model + walkmesh by name, manages VIS linked-room visibility |
| 32 | `module-editor/ForgePath.ts` | Path object (stub placeholder) |
| 33 | `module-editor/ForgeGameObject.ts` | Abstract base for all game objects -- position/rotation/scale, Object3D container, bounding box |
| 34 | `module-editor/ForgeMiniGame.ts` | Mini-game data model |
| 35 | `module-editor/ForgeMGEnemy.ts` | Mini-game enemy |
| 36 | `module-editor/ForgeMGPlayer.ts` | Mini-game player |
| 37 | `module-editor/ForgeMGTrack.ts` | Mini-game track |
| 38 | `module-editor/ForgeMGGunBank.ts` | Mini-game gun bank |
| 39 | `module-editor/ForgeMGGunBullet.ts` | Mini-game gun bullet |
| 40 | `module-editor/ForgeMGObstacle.ts` | Mini-game obstacle |
| 41 | `module-editor/ForgeItem.ts` | Item game object in module |
| 42 | `managers/SceneGraphTreeViewManager.ts` | Builds/maintains hierarchical scene-graph node tree (rooms, cameras, creatures, doors, etc.) | `gui/windows/module_designer.py` | Port scene graph hierarchy builder |

---

## 3. Walkmesh Editor

Forge has a dedicated walkmesh editor with face/vertex/edge selection and material painting. Toolset has a basic walkmesh renderer.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 43 | `components/tabs/tab-wok-editor/TabWOKEditor.tsx` | 3D walkmesh editor -- face/vertex/edge selection modes, material property sidebar | `gui/editors/bwm.py` | Port face/vertex/edge selection modes, material editing sidebar |
| 44 | `states/tabs/TabWOKEditorState.tsx` | WOK editor state -- loads walkmesh, manages selection modes, 3D visualization with helpers | `gui/widgets/renderer/walkmesh.py` + `gui/widgets/renderer/walkmesh_editor.py` | Port selection state machine, visualization helpers |

---

## 4. LIP Sync Editor

Forge's LIP editor has a 3D head preview that animates lip shapes in real-time synced to audio playback, plus a keyframe timeline. Toolset has a basic LIP editor with audio but no live 3D preview.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 45 | `components/tabs/tab-lip-editor/TabLIPEditor.tsx` | LIP editor -- **3D head preview with live lip animation**, keyframe timeline, waveform, shape controls | `gui/editors/lip/lip_editor.py` | Port 3D head preview with live lip-shape animation synced to audio |
| 46 | `components/tabs/tab-lip-editor/TabLIPEditorOptions.tsx` | LIP editor options sidebar -- scene graph/keyframe utility panel | `gui/editors/lip/lip_editor.py` | Port options sidebar |
| 47 | `states/tabs/tab-lip-editor/TabLIPEditorState.tsx` | LIP editor state -- audio playback, keyframe manipulation, head model management, 3D scene | `gui/editors/lip/lip_editor.py` | Port audio-synced playback state machine, keyframe editing logic |
| 48 | `states/tabs/tab-lip-editor/TabLIPEditorOptionsState.tsx` | LIP options sub-state | `gui/editors/lip/lip_editor.py` | Port options state |
| 49 | `data/LIPShapeLabels.ts` | LIP shape label data (phoneme --> shape name mapping) | `gui/editors/lip/lip_editor.py` | Port shape label definitions if missing |

---

## 5. Audio / Media Playback

Forge has a global audio player and individual audio playback within editors. Toolset has a media player widget.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 50 | `components/AudioPlayer.tsx` | Global audio player widget -- play/pause/stop/seek with waveform | `gui/widgets/media_player_widget.py` | Port waveform visualization, improve transport controls |
| 51 | `states/AudioPlayerState.ts` | Audio player state -- Web Audio API source/gain/analyser, playback control | `gui/widgets/media_player_widget.py` | Port audio analyser (for waveform/visualization) |
| 52 | `components/tabs/tab-audio-player/TabAudioPlayer.tsx` | Standalone audio player tab with waveform canvas and full transport controls | `gui/editors/wav.py` | Port waveform display, improve audio editor |
| 53 | `components/tabs/tab-bik-player/TabBIKPlayer.tsx` | BIK (Bink Video) player -- frame-by-frame WebGL YUV decoding with playback controls | No equivalent | Add BIK video playback support (new feature) |
| 54 | `components/tabs/tab-bik-player/yuvWebGL.ts` | WebGL YUV-to-RGB shader for BIK frame rendering | No equivalent | Reference for BIK rendering |

---

## 6. Model Viewer

Forge has a 3D model viewer with animation timeline and scene graph. Toolset has a basic model viewer.

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 55 | `components/tabs/tab-model-viewer/TabModelViewer.tsx` | 3D model viewer -- animation keyframe timeline, scene graph sidebar, camera overlay | `gui/editors/mdl.py` + `gui/widgets/renderer/model.py` | Port animation timeline, scene graph sidebar, camera controls |
| 56 | `components/ModelViewerSidebarComponent.tsx` | Model viewer sidebar -- animation selector, layout selector, camera speed, scene graph tree | `gui/editors/mdl.py` | Port animation selector sidebar, camera speed control |
| 57 | `components/KeyFrameTimelineComponent.tsx` | Reusable animation keyframe timeline -- animation list, seek bar, zoom, play/pause/loop | `gui/editors/mdl.py` + `gui/editors/lip/lip_editor.py` | Port as reusable timeline widget for both model viewer and LIP editor |
| 58 | `states/tabs/TabModelViewerState.tsx` | Model viewer state -- loads MDL/MDX, manages animations, timeline scrubbing, layout overlays | `gui/editors/mdl.py` | Port animation state management |

---

## 7. GFF Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 59 | `components/tabs/tab-gff-editor/TabGFFEditor.tsx` | GFF tree-view editor with field/struct property panels | `gui/editors/gff.py` | Compare field editing UX, port any improvements |
| 60 | `components/tabs/tab-erf-editor/ERFContextMenu.tsx` | Context menu for ERF entries (open, export) | `gui/editors/erf.py` | Port context menu actions |
| 61 | `components/tabs/tab-gff-editor/GFFContextMenu.tsx` | Context menu for GFF tree nodes (add/remove fields) | `gui/editors/gff.py` | Port context menu for field manipulation |

---

## 8. ERF/RIM Container Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 62 | `components/tabs/tab-erf-editor/TabERFEditor.tsx` | ERF/MOD/SAV/RIM container browser with resource list and context-menu actions | `gui/editors/erf.py` | Port resource list improvements, export actions |

---

## 9. 2DA Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 63 | `components/tabs/tab-twoda-editor/TabTwoDAEditor.tsx` | 2DA spreadsheet editor with editable cells and column headers | `gui/editors/twoda.py` | Port cell editing UX, column headers |
| 64 | `components/TwoDAEditorColumnHeader.tsx` | Column header component for 2DA editor | `gui/editors/twoda.py` | Port column header with sort/resize |
| 65 | `components/TwoDAEditorRow.tsx` | Row component for 2DA editor | `gui/editors/twoda.py` | Port row rendering improvements |

---

## 10. GUI Layout Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 66 | `components/tabs/tab-gui-editor/TabGUIEditor.tsx` | KotOR GUI menu layout editor (`.gui` files) -- 3D renderer with zoom/pan | `gui/editors/gff.py` (currently just GFF) | Port as dedicated GUI layout visual editor (currently no visual GUI editor exists) |

---

## 11. Path (PTH) Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 67 | `components/tabs/tab-pth-editor/TabPTHEditor.tsx` | 3D pathfinding editor -- select/add points, add connections between them | `gui/editors/pth.py` | Port 3D point/connection editing, improve over current basic editor |
| 68 | `states/tabs/TabPTHEditorState.tsx` | PTH editor state -- path points, connections, layout/walkmesh overlay | `gui/editors/pth.py` | Port state management for point/connection editing |

---

## 12. Script / Text Editor

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 69 | `components/tabs/tab-text-editor/TabTextEditor.tsx` | Monaco-based text/script editor for NSS/LYT/VIS/TXT with compile, diff-mode, linting | `gui/editors/nss.py` + `gui/editors/txt.py` | Port compile integration, diff mode, linting support |
| 70 | `components/tabs/tab-script-compile-log/TabScriptCompileLog.tsx` | NWScript compilation log display | `gui/editors/nss.py` | Port compilation log panel |
| 71 | `components/tabs/tab-script-error-log/TabScriptErrorLog.tsx` | Script error/warning diagnostics with click-to-navigate | `gui/editors/nss.py` | Port error log with click-to-line navigation |
| 72 | `components/tabs/tab-script-inspector/TabScriptInspector.tsx` | NCS bytecode disassembler showing assembly instructions | `gui/editors/nss.py` | Port bytecode inspector/disassembler view |
| 73 | `states/NWScriptLanguageService.ts` | NWScript language server -- parsing, linting, completion | `gui/common/language_server_client.py` | Reference for language server features |
| 74 | `states/LYTLanguageService.ts` | LYT file language service | No equivalent | Reference for LYT syntax support |

---

## 13. Image / Texture Viewer

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 75 | `components/tabs/tab-image-viewer/TabImageViewer.tsx` | TPC/TGA texture viewer with zoom, pixel data, and TXI metadata | `gui/editors/tpc.py` + `gui/widgets/renderer/texture_browser.py` | Port zoom controls, TXI metadata display |
| 76 | `components/TextureCanvas/TextureCanvas.tsx` | Canvas renders decoded TPC/TGA pixel data | `gui/widgets/texture_preview.py` | Port improved texture rendering |
| 77 | `components/LazyTextureCanvas/LazyTextureCanvas.tsx` | Lazy-loaded texture canvas (loads when visible) | `gui/widgets/texture_loader.py` | Port lazy loading for texture thumbnails |

---

## 14. Localized String / TLK

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 78 | `components/CExoLocStringEditor/CExoLocStringEditor.tsx` | Multi-language localized string editor with TLK resref lookup | `gui/dialogs/edit/locstring.py` + `gui/widgets/edit/locstring.py` | Port improved multi-language UI |
| 79 | `components/TLKSearchModal/TLKSearchModal.tsx` | TLK search modal -- query text, select string-ref | `gui/dialogs/edit/locstring.py` (already ported) | Already ported |

---

## 15. Resource Explorer / Project Browser

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 80 | `components/tabs/tab-resource-explorer/TabResourceExplorer.tsx` | Searchable tree-view of all game resources (BIF/ERF/override) with lazy loading | `gui/widgets/main_widgets.py` | Port lazy loading, improved search/filtering |
| 81 | `components/tabs/tab-project-explorer/TabProjectExplorer.tsx` | Project file hierarchy tree-view | No direct equivalent | Port project browser concept |
| 82 | `components/treeview/ForgeTreeView.tsx` | Base tree-view styling component | `gui/widgets/main_widgets.py` | Reference for tree-view styling |
| 83 | `components/treeview/ResourceListNode.tsx` | Resource list tree node | `gui/widgets/main_widgets.py` | Reference for resource node rendering |
| 84 | `components/treeview/ERFListNode.tsx` | ERF container tree node | `gui/widgets/main_widgets.py` | Reference for container node rendering |
| 85 | `components/treeview/ListItemNode.tsx` | Generic list item tree node | `gui/widgets/main_widgets.py` | Reference for node rendering |

---

## 16. Modals / Dialogs

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 86 | `components/modal/ModalBlueprintBrowser.tsx` | Browse/search game blueprints (all UT* types) to select one | `gui/dialogs/insert_instance.py` | Port blueprint browsing with search/filter |
| 87 | `components/modal/ModalItemBrowser.tsx` | Browse/search items (UTI) with texture thumbnails | `gui/dialogs/inventory.py` | Port item browser with thumbnails |
| 88 | `components/modal/ModalChangeGame.tsx` | Switch between K1/TSL game | `gui/dialogs/settings.py` | Reference for game-switching UI |
| 89 | `components/modal/ModalNewProject.tsx` | Create new modding project | No equivalent | Port project creation workflow |
| 90 | `components/modal/ModalGrantAccess.tsx` | Browser file system access grant dialog | N/A (desktop app) | Not applicable |

---

## 17. Application Shell / Layout

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 91 | `App.tsx` | Root app -- game directory, layout (explorer + tabs), loading screen | `gui/windoorws/main.py` | Reference for layout organization |
| 92 | `components/LayoutContainer/LayoutContainer.tsx` | Resizable docking-panel layout (N/S/E/W + center) with draggable splitters | `gui/windows/main.py` + `gui/windows/module_designer.py` | Port improved docking/splitting layout |
| 93 | `components/common/MenuBar.tsx` | Application menu bar | `gui/windows/main.py` | Reference for menu organization |
| 94 | `components/common/ContextMenu.tsx` | Reusable context menu component | Various editors | Reference for context menu patterns |
| 95 | `components/MenuTop.tsx` | Top menu bar items | `gui/windows/main.py` | Reference |
| 96 | `components/MenuItem.tsx` | Menu item component | `gui/windows/main.py` | Reference |
| 97 | `components/LoadingScreen.tsx` | Loading screen overlay | `gui/dialogs/async_loader.py` | Port loading screen improvements |
| 98 | `components/SectionContainer.tsx` | Collapsible section container | `gui/common/widgets/collapsible.py` | Compare / port improvements |
| 99 | `components/tabs/TabButton.tsx` | Tab button component | `gui/windows/main.py` | Reference for tab bar styling |
| 100 | `components/tabs/TabManager.tsx` | Tab strip that manages open editor tabs | `gui/windows/main.py` | Reference for tab management |
| 101 | `components/SubTabHost/SubTabHost.tsx` | Nested sub-tab container | Various editors | Reference for sub-tab pattern |
| 102 | `components/tabs/tab-quick-start/TabQuickStart.tsx` | Welcome/landing page with recent files and projects | `gui/windows/main.py` | Port welcome tab with recent files |

---

## 18. State Management / Infrastructure

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 103 | `states/ForgeState.ts` | Central app state -- project, tab managers, explorer tabs, recent files, NWScript parser, init | `data/settings.py` + `gui/windows/main.py` | Reference for centralized state management patterns |
| 104 | `managers/EditorTabManager.ts` | Tab management -- add/remove/show/hide, single-instance enforcement, tab events | `utils/window.py` | Port single-instance tab enforcement (already partially done) |
| 105 | `FileTypeManager.ts` | File-type router -- maps extensions to editor tab state classes | `utils/window.py` (open_resource_editor) | Reference for file-type dispatch |
| 106 | `EditorFile.ts` | Open file abstraction -- read/write from game FS/project FS/system FS, save state | `gui/editor/file.py` | Reference for file save-state tracking |
| 107 | `EditorModule.ts` | Minimal module wrapper | `gui/windows/module_designer.py` | Reference |
| 108 | `ForgeFileSystem.ts` | File system abstraction (Electron + browser FS API) | N/A (desktop app uses OS directly) | Not applicable |
| 109 | `ProjectFileSystem.ts` | Project-scoped virtual file system | No equivalent | Reference for project FS concept |
| 110 | `Project.ts` | Project model -- settings, module areas, project directory | No equivalent | Port project concept |
| 111 | `RecentProject.ts` | Recent project tracking | `data/settings.py` | Reference |
| 112 | `SceneGraphNode.ts` | Scene graph node data class | `gui/windows/module_designer.py` | Reference for scene graph data model |
| 113 | `EventListenerModel.ts` | Event listener model | N/A (Qt uses signals) | Not applicable |
| 114 | `FileBrowserNode.tsx` | File browser tree node | `gui/widgets/main_widgets.py` | Reference |

---

## 19. Styling / UI Components

| # | Forge File | What It Does | Toolset File | Merge Opportunity |
|---|-----------|-------------|-------------|-------------------|
| 115 | `components/forge-checkbox/forge-checkbox.tsx` | Custom styled checkbox | Qt native | Reference |
| 116 | `components/form-field/FormField.tsx` | Form field wrapper with label | Qt native | Reference |
| 117 | `components/info-bubble/info-bubble.tsx` | Info tooltip bubble | `gui/common/tooltip_utils.py` | Reference |
| 118 | `styles/_variables.scss` | Theme color/spacing variables | `gui/common/style/theme_manager.py` | Reference for theming values |
| 119 | `styles/audio-player.scss` | Audio player styles | `gui/widgets/media_player_widget.py` | Reference |
| 120 | `styles/component-keyframe.scss` | Keyframe timeline styles | N/A | Reference for timeline styling |
| 121 | `styles/keyframe-track.scss` | Keyframe track styles | N/A | Reference |
| 122 | `styles/UI3DToolPalette.scss` | Tool palette styles | N/A | Reference |

---

## 20. Helpers / Enums / Interfaces

| # | Forge File | What It Does |
|---|-----------|-------------|
| 123 | `helpers/UTxEditorHelpers.ts` | Shared helper functions for UT* blueprint editors |
| 124 | `helpers/PathParse.ts` | Path parsing utilities |
| 125 | `helpers/UseEffectOnce.ts` | React hook (N/A for Qt) |
| 126 | `enum/AppearanceLoaderType.ts` | Appearance loading options |
| 127 | `enum/EditorFileProtocol.ts` | File protocol types (game/project/system) |
| 128 | `enum/FileLocationType.ts` | File location types |
| 129 | `enum/ModuleEditorTabNode.ts` | Module editor sidebar tab identifiers |
| 130 | `enum/ProjectType.ts` | Project types |
| 131 | `interfaces/BaseTabProps.ts` | Base tab property interface |
| 132 | `interfaces/BaseTabStateOptions.ts` | Base tab state options |
| 133 | `interfaces/CreatureListEntry.ts` | Creature list entry interface |
| 134 | `interfaces/EditorFileOptions.ts` | Editor file options |
| 135 | `interfaces/EncounterDifficulty.ts` | Encounter difficulty settings |
| 136 | `interfaces/GameMap.ts` | Game map interface |
| 137 | `interfaces/ModuleEditorState.ts` | Module editor state interface |
| 138 | `interfaces/ProjectSettings.ts` | Project settings |
| 139 | `interfaces/TabStoreState.ts` | Tab store state interface |
| 140 | `interfaces/modal/BaseModalProps.ts` | Base modal property interface |
| 141 | `context/AppContext.tsx` | React app context provider |
| 142 | `context/LayoutContainerContext.tsx` | Layout context |
| 143 | `context/LoadingScreenContext.tsx` | Loading screen context |
| 144 | `context/TabManagerContext.tsx` | Tab manager context |
| 145 | `KotOR.ts` | KotOR.js library re-exports |
| 146 | `index.tsx` | Forge app entry point |
| 147 | `MenuTopItem.ts` | Menu top item data model |
| 148 | `states/MenuTopState.tsx` | Menu top state |
| 149 | `states/modal/ModalBlueprintBrowserState.tsx` | Blueprint browser modal state |
| 150 | `states/modal/ModalItemBrowserState.tsx` | Item browser modal state |
| 151 | `states/modal/ModalManagerState.tsx` | Modal manager state |
| 152 | `states/modal/ModalNewProjectState.tsx` | New project modal state |
| 153 | `states/modal/ModalState.tsx` | Base modal state class |
| 154 | `states/tabs/TabAudioPlayerState.tsx` | Audio player tab state |
| 155 | `states/tabs/TabBIKPlayerState.tsx` | BIK player tab state |
| 156 | `states/tabs/TabERFEditorState.tsx` | ERF editor tab state |
| 157 | `states/tabs/TabGFFEditorState.tsx` | GFF editor tab state |
| 158 | `states/tabs/TabGUIEditorState.tsx` | GUI editor tab state |
| 159 | `states/tabs/TabImageViewerState.tsx` | Image viewer tab state |
| 160 | `states/tabs/TabProjectExplorerState.tsx` | Project explorer tab state |
| 161 | `states/tabs/TabQuickStartState.tsx` | Quick start tab state |
| 162 | `states/tabs/TabResourceExplorerState.tsx` | Resource explorer tab state |
| 163 | `states/tabs/TabScriptCompileLogState.tsx` | Script compile log state |
| 164 | `states/tabs/TabScriptErrorLogState.tsx` | Script error log state |
| 165 | `states/tabs/TabScriptInspectorState.tsx` | Script inspector state |
| 166 | `states/tabs/TabState.tsx` | Base tab state class |
| 167 | `states/tabs/TabTextEditorState.tsx` | Text editor tab state |
| 168 | `states/tabs/TabTwoDAEditorState.tsx` | 2DA editor tab state |
| 169 | `states/tabs/TabUTCEditorState.tsx` | UTC editor tab state |
| 170 | `states/tabs/TabUTDEditorState.tsx` | UTD editor tab state |
| 171 | `states/tabs/TabUTEEditorState.tsx` | UTE editor tab state |
| 172 | `states/tabs/TabUTIEditorState.tsx` | UTI editor tab state |
| 173 | `states/tabs/TabUTMEditorState.tsx` | UTM editor tab state |
| 174 | `states/tabs/TabUTPEditorState.tsx` | UTP editor tab state |
| 175 | `states/tabs/TabUTSEditorState.tsx` | UTS editor tab state |
| 176 | `states/tabs/TabUTTEditorState.tsx` | UTT editor tab state |
| 177 | `states/tabs/TabUTWEditorState.tsx` | UTW editor tab state |
| 178 | `states/tabs/index.ts` | Tab state barrel exports |
| 179 | `app.scss` | Root app styles |
| 180 | `styles/_bootstrap-overrides.scss` | Bootstrap override styles |
| 181 | `styles/layout-custom.scss` | Custom layout styles |
| 182 | `styles/layout-default.scss` | Default layout styles |
| 183 | `styles/tab-manager.scss` | Tab manager styles |
| 184 | `styles/tabs/tab-gff-editor.scss` | GFF editor styles |
| 185 | `styles/tabs/tab-image-viewer.scss` | Image viewer styles |
| 186 | `styles/tabs/tab-script-error-log.scss` | Script error log styles |
| 187 | `styles/tabs/tab-twoda-editor.scss` | 2DA editor styles |
| 188 | `styles/tabs/tab-ute-editor.scss` | UTE editor styles |
| 189 | `styles/tabs/tab-uts-editor.scss` | UTS editor styles |
| 190 | `components/modal/ModalManager.tsx` | Modal stack manager |

---

## 21. Indoor Map Builder <--> Forge Module Editor / Walkmesh Editor / LYT+VIS Engine

The Toolset's Indoor Map Builder has **no direct Forge equivalent by name**, but Forge's **module editor**, **walkmesh editor**, and **LYT/VIS engine** collectively cover the same domain -- assembling rooms into a playable module with walkmeshes, doors, visibility, and game objects. The difference: Forge edits **existing** modules in 3D; the Toolset **creates new** indoor modules from kit pieces in 2D.

### 21a. Forge Files That Map to Indoor Builder Features

**Module-level editing** (cross-ref §2 #18-42 for the full module editor; listed here for indoor-relevant overlap):

| # | Forge File | What It Does | Indoor Builder Counterpart | What to Port |
|---|-----------|-------------|---------------------------|-------------|
| 191 | `module-editor/ForgeArea.ts` | Loads ARE+GIT+LYT+VIS, creates rooms, manages all GIT objects, caches walkmeshes for raycasting | `builder.py` + `pykotor.common.indoormap` | LYT/VIS-aware room management, GIT object lists, walkmesh cache for hit-testing |
| 192 | `module-editor/ForgeRoom.ts` | Loads room MDL/MDX + WOK walkmesh, tracks VIS-linked rooms, property-change reload | `pykotor.common.indoorkit` (`KitComponent`) | Per-room walkmesh loading, VIS room linking |
| 193 | `module-editor/ForgeModule.ts` | Module container -- IFO fields, entry point, area ownership | `pykotor.common.indoormap` (`IndoorMap.build()` generates IFO) | IFO field editing (entry pos, scripts, description) |
| 194 | `module-editor/ForgeDoor.ts` | Door with UTD blueprint + 3 walkmeshes (closed, open1, open2) | `builder.py` auto-generates doors from hook connections | Door walkmesh (DWK) handling, UTD property editing |
| 195 | `module-editor/ForgeGameObject.ts` | Base object -- position/rotation/scale, bounding box, GIT serialization | No equivalent (indoor builder has no GIT objects) | **NEW**: object placement base class |
| 196 | `module-editor/ForgeCreature.ts` | Creature with UTC blueprint + 3D model | No equivalent | **NEW**: creature placement in indoor modules |
| 197 | `module-editor/ForgePlaceable.ts` | Placeable with UTP blueprint + PWK walkmesh | No equivalent | **NEW**: placeable placement with PWK collision |
| 198 | `module-editor/ForgeTrigger.ts` | Trigger with editable polygon vertices + UTT blueprint | No equivalent | **NEW**: trigger zone placement with vertex editing |
| 199 | `module-editor/ForgeEncounter.ts` | Encounter with editable polygon + spawn points + UTE blueprint | No equivalent | **NEW**: encounter zone placement |
| 200 | `module-editor/ForgeWaypoint.ts` | Waypoint with UTW blueprint + map notes | Warp point only (single green crosshair) | Extend warp to full waypoint placement |
| 201 | `module-editor/ForgeSound.ts` | Sound emitter with UTS blueprint + positional audio | No equivalent | **NEW**: ambient sound placement |
| 202 | `module-editor/ForgeCamera.ts` | Camera with FOV/pitch/orientation + perspective preview inset | No equivalent | **NEW**: camera placement with preview |
| 203 | `module-editor/ForgeStore.ts` | Store with UTM blueprint | No equivalent | **NEW**: store placement |

**Walkmesh editing** (cross-ref §3 #43-44; listed here for indoor-specific overlap):

| # | Forge File | What It Does | Indoor Builder Counterpart | What to Port |
|---|-----------|-------------|---------------------------|-------------|
| 204 | `states/tabs/TabWOKEditorState.tsx` | WOK editor state -- face/vertex/edge selection, surface material editing, wireframe overlay, normal arrows, grid | `renderer.py` (material painting only) | Face/vertex/edge selection modes, vertex drag-editing, normal visualization |
| 205 | `components/tabs/tab-wok-editor/TabWOKEditor.tsx` | WOK editor UI -- 3D viewport, tool palette (Face/Vertex/Edge modes), sidebar with face properties | `renderer.py` + `builder.py` (paint mode) | Selection mode toolbar, face property sidebar (material + walkable flags + adjacency) |

**3D infrastructure** (cross-ref §2 #20-24; listed for what indoor builder lacks):

| # | Forge File | What It Does | Indoor Builder Counterpart | What to Port |
|---|-----------|-------------|---------------------------|-------------|
| 206 | `UI3DRenderer.tsx` | 3D engine -- gizmos, orbit/fly camera, raycaster, scene groups, walkmesh visibility toggle | `renderer.py` (2D QPainter only) | **MAJOR**: 3D viewport option with orbit camera, transform gizmos |
| 207 | `components/UI3DRendererView.tsx` | Canvas + camera-view menu (Top/Bottom/Left/Right/Front/Back) | Single 2D view | Camera view presets (at minimum: orthographic top-down) |
| 208 | `components/UI3DToolPalette.tsx` | Floating toolbar (Select/Move/Rotate/Scale/Add) | `builder.py` toolbar (separate Qt actions) | Unified floating tool palette widget |
| 209 | `managers/SceneGraphTreeViewManager.ts` | Builds scene tree grouped by type (Rooms, Doors, Creatures, etc.) | Room list widget in builder | Hierarchical scene tree showing rooms + objects per room |

**LYT/VIS engine** (parsers Forge uses that PyKotor already has equivalents for):

| # | Forge File | What It Does | PyKotor Equivalent | What to Port |
|---|-----------|-------------|-------------------|-------------|
| 210 | `resource/LYTObject.ts` | LYT parser -- rooms, doorhooks, tracks, obstacles | `pykotor.resource.formats.lyt` | **Doorhook export**: Toolset only writes room entries, not doorhooks/tracks |
| 211 | `resource/VISObject.ts` | VIS parser -- room-->visible-rooms graph | `pykotor.resource.formats.vis` | **Per-room VIS editing**: Toolset currently does `set_all_visible()` |

**Walkmesh engine** (runtime classes the WOK editor builds on):

| # | Forge File | What It Does | PyKotor Equivalent | What to Port |
|---|-----------|-------------|-------------------|-------------|
| 212 | `odyssey/OdysseyWalkMesh.ts` | Core walkmesh -- binary WOK read/write, face/vertex/edge/AABB, surface materials, perimeter building, geometry gen | `pykotor.resource.formats.bwm` | Already equivalent; use for vertex editing extensions |
| 213 | `odyssey/WalkmeshEdge.ts` | Edge with normal, transition index, face ref | `pykotor.resource.formats.bwm` (internal) | Edge selection/visualization data |
| 214 | `odyssey/OdysseyFace3.ts` | Face with surfacemat, adjacency, walk/walkCheck/lineOfSight bools, centroid, normal | `pykotor.resource.formats.bwm` (BWMFace) | Face selection and property display |
| 215 | `engine/SurfaceMaterial.ts` | Surface material definition (walk, walkCheck, lineOfSight, grass) from surfacemat.2da | `constants.py` (material colors) + surfacemat.2da | Surface material metadata for property sidebar |
| 216 | `engine/TileColor.ts` | Color per surface material for walkmesh rendering | `constants.py` (MATERIAL_COLOURS dict) | Already equivalent |

**Pathfinding engine** (PTH editor loads walkmeshes as background -- relevant to indoor builder):

| # | Forge File | What It Does | Indoor Relevance |
|---|-----------|-------------|-----------------|
| 217 | `states/tabs/TabPTHEditorState.tsx` | PTH editor loads LYT rooms + walkmeshes as background reference, places path points via walkmesh raycasting | Same walkmesh loading pattern as indoor builder |
| 218 | `engine/pathfinding/PathPoint.ts` | Pathfinding node (position, connections, A* state) | Could add optional PTH generation to indoor builder |

**Blueprint browser** (used by module editor for object placement):

| # | Forge File | What It Does | Indoor Relevance |
|---|-----------|-------------|-----------------|
| 219 | `states/modal/ModalBlueprintBrowserState.tsx` | Modal for selecting blueprints by type (creature/door/placeable/etc.), filters by resref | Needed if game object placement is added to indoor builder |

### 21b. Integration Strategy: Unified Module Designer (`module_designer.ui`)

Instead of keeping the "Indoor Builder" as a separate, limited 2D tool, all of its room layout generation features, as well as **Forge’s entire 3D walkmesh editing and object placement capabilities**, will be unified into the **Module Designer** (`module_designer.ui`). Forge acts as a unified scene editor; the Toolset should follow suit.

**How Forge's Walkmesh 3D Editor Works (The Target State):**
1. **Geometry & Rendering**: `OdysseyWalkMesh` parses `.wok`/`.dwk`/`.pwk` faces/vertices/edges into internal arrays. It generates dynamic `BufferGeometry` where each face is designated a color based on `SurfaceMaterial` (`TileColor`).
2. **Raycasting & Selection**: Raycasting checks against polygons marked with an `isWalkmesh` flag. Clicking a face selects it, applying a highlight overlay.
3. **Vertex/Edge Manipulation**: In Vertex mode, small 3D box helpers render at vertices. Clicking one attaches Three.js `TransformControls` (gizmos) to drag the vertex position on X/Y/Z. The underlying WOK arrays update and rebuild the mesh dynamically. Edges render with outward-pointing normal arrows for orientation debugging.
4. **UI Overlay**: A sidebar shows the selected face's properties: `walk`, `walkCheck`, `lineOfSight` booleans, the `surfacemat.2da` surface material dropdown, and adjacency routing.

**Redesigning `module_designer.ui` to Implement This:**

To absorb the Indoor Builder and Forge's Walkmesh Editor, `module_designer.ui` will be redesigned with these structural changes:

1. **Combining the UI & Logic (`indoor_builder.ui` / `indoor_builder` --> `module_designer.ui` / `module_designer.py`)**:
   - The entire contents/logic of `indoor_builder` must be migrated. The `leftDockWidget` and `rightDockWidget` from `indoor_builder.ui` (containing kit instances, room lists, builder properties) need to be ported into `module_designer.ui` as dockable panels or integrated into the existing sidebars. 
   - `indoor_builder.ui` and the standalone `indoor_builder` module will be fully deprecated once this functionality is mapped.
2. **Toolbar Mode Selector (The "Squish" Fix)**:
   - Because the 2D top-down view (and the UI in general) can get very crowded and "squished" with all these features, add prominent Toolbar buttons / Mode toggles to swap interaction contexts and declutter the view:
     - **Layout Mode** (merging `indoor_builder`): Places rooms on the 2D `WalkmeshRenderer` grid, snapping to doorhooks.
     - **Object/GIT Mode** (current MVP): Places GIT objects in the 3D `ModuleRenderer`, utilizing raycast ghost previews against walkmeshes.
     - **Walkmesh Mode** (Forge port): Locks object placement, enables raycast picking of walkmesh faces and vertices in the 3D canvas.
   - Mode switching should physically swap or hide irrelevant sidebars (e.g. hiding GIT tools when editing walkmeshes) to free up horizontal screen space.
3. **Left Panel Tabs (`leftPanel` expansion)**:
   - Keep `resourceTab` (blueprint browser) and `lytTab` (scene hierarchy).
   - Add **`walkmeshTab`**: A property inspector for the selected walkmesh face showing material dropdowns and boolean flags (porting Forge's WOK sidebar).
   - Add **`visTab`**: A comprehensive checkbox matrix for editing the VIS table (room-to-room visibility), rather than the current indoor builder’s `set_all_visible()` hack.
4. **ModuleKit Integration (`modulekit.py`)**:
   - The entirety of `pykotor.common.modulekit.py` must be utilized in the unified designer.
   - `ModuleKit` and `ModuleKitManager` provide lazy-loading of "implicit kits" from existing modules. Layout Mode should populate its library of available placeable rooms by leveraging `ModuleKitManager` alongside standard JSON indoor kits, making vanilla game rooms drag-and-droppable into custom modules.
5. **Renderer Widgets**:
   - The UI already contains `WalkmeshRenderer` (2D) and `ModuleRenderer` (3D). 
   - Upgrade `ModuleRenderer` to attach an OpenGL translation gizmo to clicked walkmesh vertices (porting Three.js `TransformControls`).

| Feature Gap | Forge Implementation | Module Designer Merge Action | Priority |
|---------|-----------|---------------------------|----------|
| **Unified Environment** | `TabModuleEditor` edits LYT, VIS, ARE, GIT, WOK in one 3D canvas | Merge Indoor Builder code into `module_designer.py` and retire the standalone `indoor_builder.ui` | **CRITICAL** |
| **Walkmesh vertex/face editing** | Face/vertex/edge selection modes, vertex drag via gizmo, normal viz | Enhance PyOpenGL `ModuleRenderer` to pick/drag walkmesh vertices via raycasting | **HIGH** |
| **WOK Property Sidebar** | Sidebar shows surface material, walk flags, adjacency list | Add `walkmeshTab` dock to `module_designer.ui` | **HIGH** |
| **Game object placement** | All GIT types placable via raycast ghost preview | Extend `ModuleRenderer` object editing to support drag-and-drop placement from the `resourceTab` | **HIGH** |
| **Per-room VIS matrix** | VIS parser + active bidirectional room linking | Add `visTab` with visibility checkbox matrix replacing `set_all_visible()` | **HIGH** |
| **Doorhook LYT export** | LYT exports doorhooks, tracks, obstacles | Update internal builder logic to export hook data via PyKotor | **MEDIUM** |
| **Transform gizmos** | Three.js translate/rotate/scale handles | Add OpenGL drag handles for selected 3D objects & vertices | **LOW** |

### 21c. Current Indoor File Inventory (23 files across 2 trees)

**Libraries/PyKotor/src/pykotor/** (headless core -- 6 files):

| # | Current Path | What It Does |
|---|-------------|-------------|
| 220 | `common/indoorkit.py` | Data model classes: `Kit`, `KitComponent`, `KitDoor`, `KitComponentHook`, `MDLMDXTuple` |
| 221 | `common/indoormap.py` | Data model + headless builder: `IndoorMap`, `IndoorMapRoom`, `.build_mod()`, `.to_dict()`/`.from_dict()` |
| 222 | `tools/indoorkit.py` | Workflow: `load_kits()`, `load_kits_with_missing_files()` -- parses kit JSON + resources from disk |
| 223 | `tools/indoormap.py` | Workflow: `build_mod_from_indoor_file()`, `extract_indoor_from_module()` -- high-level CLI ops |
| 224 | `cli/indoor_builder.py` | Tiny CLI helpers: `parse_game_argument()`, `determine_game_from_installation()` |
| 225 | `cli/commands/indoor_builder.py` | CLI command impls: `cmd_indoor_build()`, `cmd_indoor_extract()` |

**Tools/HolocronToolset/src/toolset/** (Qt UI -- 17 files):

| # | Current Path | What It Does |
|---|-------------|-------------|
| 226 | `data/indoormap.py` | Qt-only minimap renderer (`generate_mipmap()`), re-exports `IndoorMap`/`IndoorMapRoom` |
| 227 | `data/indoorkit/__init__.py` | Package init (re-exports) |
| 228 | `data/indoorkit/indoorkit_base.py` | **DEPRECATED** legacy Qt `Kit`/`KitComponent` classes (duplicates `pykotor.common.indoorkit`) |
| 229 | `data/indoorkit/indoorkit_loader.py` | Toolset wrapper: loads kits via `pykotor.tools.indoorkit` + attaches Qt `QImage` previews |
| 230 | `data/indoorkit/indoorkit_utils.py` | Legacy helpers: `process_padding_file()`, `process_texture_file()`, `process_lightmap_file()` |
| 231 | `data/indoorkit/qt_preview.py` | Qt preview image generation |
| 232 | `gui/windows/indoor_builder/__init__.py` | Package init + re-exports `IndoorMapBuilder`, `IndoorMapRenderer` |
| 233 | `gui/windows/indoor_builder/builder.py` | Main `IndoorMapBuilder` window (QMainWindow) |
| 234 | `gui/windows/indoor_builder/renderer.py` | `IndoorMapRenderer` widget -- 2D top-down walkmesh canvas |
| 235 | `gui/windows/indoor_builder/constants.py` | Material colors, walkmesh constants |
| 236 | `gui/windows/indoor_builder/kit_downloader.py` | `KitDownloader` dialog |
| 237 | `gui/windows/indoor_builder/undo_commands.py` | QUndoCommand subclasses for room operations |
| 238 | `gui/dialogs/indoor_settings.py` | `IndoorMapSettings` dialog |
| 239 | `uic/qtpy/windows/indoor_builder.py` | Auto-generated from `indoor_builder.ui` |
| 240 | `uic/qtpy/dialogs/indoor_settings.py` | Auto-generated from `indoor_settings.ui` |
| 241 | `uic/qtpy/dialogs/indoor_downloader.py` | Auto-generated from `indoor_downloader.ui` |
| 242 | UI files: `indoor_builder.ui`, `indoor_settings.ui`, `indoor_downloader.ui` |

### 21d. File Consolidation Plan

**Problem**: 8 files named `indoorkit.py` / `indoormap.py` / `indoor_builder.py` in different directories.

**Phase 1: Delete the deprecated duplicate**
- DELETE `data/indoorkit/indoorkit_base.py` -- marked DEPRECATED, duplicates `pykotor.common.indoorkit`

**Phase 2: Merge tiny Toolset data shims**
- MERGE `data/indoorkit/indoorkit_utils.py` --> `data/indoorkit/indoorkit_loader.py`
- RENAME result --> `data/indoorkit/kit_loader.py`
- RENAME `data/indoormap.py` --> `data/indoor_minimap.py`

**Phase 3: Merge tiny CLI files**
- MERGE `cli/indoor_builder.py` (60 lines, 2 functions) INTO `cli/commands/indoor_builder.py`

**Phase 4: Rename for clarity**
- RENAME `common/indoorkit.py` --> `common/indoor_kit.py`
- RENAME `common/indoormap.py` --> `common/indoor_map.py`
- RENAME `tools/indoorkit.py` --> `tools/indoor_kit_loader.py`
- RENAME `tools/indoormap.py` --> `tools/indoor_map_builder.py`

**Result: 23 files --> 19 files**, every filename unique and descriptive.

---

## Summary: Implementation Roadmap

**Primary Goal**: Transform the Module Designer into a **Unity/UE5-class all-in-one level editor**. See [docs/LEVEL_EDITOR_CHECKLIST.md](docs/LEVEL_EDITOR_CHECKLIST.md) for the comprehensive 200+ feature roadmap.

### Critical Path (Phase 1-6)

**Phase 1: Unified Environment** (Merge Indoor Builder --> Module Designer)
- [x] Integrate `indoor_builder` room-assembly logic into `module_designer.py` as "Layout Mode" -- EditorMode enum, mode selector, indoor state, kit/module selectors, renderer signals
- [ ] Retire standalone `indoor_builder.ui` and consolidate into mode-based workflow _(deferred until full builder.py migration)_
- [x] Add toolbar mode selector (Layout/Object/Walkmesh/Lighting/Terrain/NavMesh) -- QComboBox with Object/Layout/Walkmesh modes, tab visibility per mode
- [ ] Port doorhook snapping, room rotation/flip, multi-select from indoor builder _(done: snap checkboxes wired, all room ops ported -- place, delete, duplicate, merge, rotate, flip, clipboard, context menu)_

**Phase 2: Walkmesh Vertex Editing** (Forge Port)
- [ ] Implement face/vertex/edge raycast picking in PyOpenGL `ModuleRenderer`
- [ ] Add 3D vertex drag gizmo (translate handle with axis constraints)
- [ ] Create `walkmeshTab` sidebar panel with material dropdown, walkable flags, adjacency list
- [ ] Port normal arrow visualization for edges
- [ ] Add perimeter edge highlighting

**Phase 3: VIS Editor** (Replace `set_all_visible()` hack)
- [ ] Add `visTab` sidebar panel with room-to-room visibility checkbox matrix
- [ ] Visualize VIS relationships as colored connection lines in 3D viewport
- [ ] Implement bidirectional room linking (Forge-style)

**Phase 4: Scene Hierarchy & Object Placement** (Unity-style)
- [ ] Build hierarchical scene graph tree (Module --> Areas --> Rooms --> Objects)
- [ ] Implement blueprint browser drag-and-drop placement
- [ ] Add transform gizmos (translate/rotate/scale) with axis constraints
- [ ] Support all 11 GIT object types with property inspector
- [ ] Add ghost preview for object placement via walkmesh raycasting

**Phase 5: Multi-View Layout** (Hammer/Radiant-style)
- [ ] Implement 4-panel layout (Top/Front/Side/Perspective orthographic views)
- [ ] Add Unity-standard camera controls (WASD flythrough, Alt+LMB orbit, MMB pan)
- [ ] Add camera bookmarks (save/load positions with Ctrl+1-9)
- [ ] Implement camera view selector menu (Top/Bottom/Left/Right/Front/Back/Isometric)

**Phase 6: Polish & UX**
- [ ] Full undo/redo stack across all modes (QUndoStack for every operation)
- [ ] Keyboard shortcut system (Q/W/E/R for tools, F to focus, Ctrl+D to duplicate)
- [ ] Dockable panel system (drag-and-drop to rearrange Inspector/Hierarchy/Browser)
- [ ] Dark mode theme (Unity-inspired colors)

### Forge Feature Priorities (Ranked by Impact)

1. **Module Designer Unification** (#18-28, #42, #191-219, §21) -- **CRITICAL** -- Merge Indoor Builder + Walkmesh Editor into Module Designer with contextual modes
2. **Walkmesh Vertex Editing** (#43-44, #204-205) -- Face/vertex/edge selection, vertex drag gizmo, material sidebar
3. **Scene Graph Tree** (#23, #42, #209) -- Unity Hierarchy analog showing Module --> Areas --> Rooms --> Objects
4. **Transform Gizmos** (#24, #206) -- Three.js-style translate/rotate/scale handles with axis constraints
5. **Multi-View Layout** (#207) -- 4-panel orthographic + perspective (Hammer-standard)
6. **LIP Sync Editor** (#45-49) -- 3D head preview with live lip animation synced to audio, keyframe timeline
7. **Model Viewer** (#55-58) -- Animation timeline, scene graph sidebar, camera controls
8. **Blueprint 3D Previews** (#1-9) -- Inline 3D model previews in UTC/UTD/UTI/UTP editors
9. **Audio Waveform** (#50-52) -- Waveform visualization in audio player and UTS editor
10. **GUI Layout Editor** (#66) -- Visual `.gui` file editor (entirely new capability for Toolset)
11. **PTH Editor** (#67-68) -- 3D pathfinding point/connection editing with walkmesh background
12. **Blueprint Browser** (#86-87, #219) -- Search/filter modal with thumbnails, drag-to-place
13. **Script Inspector** (#72) -- NCS bytecode disassembler view
14. **BIK Video Player** (#53-54) -- Bink Video playback support
15. **2DA Editor** (#63-65) -- Cell editing and column header improvements
16. **Welcome Tab** (#102) -- Recent files landing page
17. **Indoor File Cleanup** (#220-242) -- Consolidate 23 --> 19 files, delete deprecated duplicate, merge shims

---

## Next Steps (How to Execute This Plan)

1. **Review the Checklist**: See [docs/LEVEL_EDITOR_CHECKLIST.md](docs/LEVEL_EDITOR_CHECKLIST.md) for the full feature roadmap organized by category.

2. **UI & Toolbar Overhaul (`module_designer.ui`)**:
   - Begin by gutting and reorganizing `module_designer.ui`. Add a top-level mode selector (Layout / Object / Walkmesh).
   - Ensure the mode buttons show/hide relevant sections of the UI, drastically reducing the visual "squish" in the 2D outliner.
   - Rip out the contents of the `indoor_builder.ui` sidebars and dock them appropriately into `module_designer.ui`. Then deprecate `indoor_builder.ui`.

3. **Backend Logic Transfer (`module_designer.py`)**:
   - Inherit/migrate the logic from the standalone `indoor_builder` (especially `builder.py` and `renderer.py`). 
   - Ensure the new "Layout Mode" context manages the `WalkmeshRenderer` using the same logic that `indoor_builder` previously relied upon.
   - Delete the redundant indoor files post-migration.

4. **Integrate `modulekit.py` for Implicit Kits**:
   - Fully integrate `pykotor.common.modulekit.py` into the new Layout Mode.
   - Use `ModuleKit` and `ModuleKitManager` so that level designers can seamlessly browse, preview, and drag-and-drop rooms from the vanilla modules directly into their new module workspace.
   - Ensure you read and understand the `ModuleKitManager` lazy-loading pipeline; don't reinvent module loading.

5. **Walkmesh Face / Vertex Picking**: Add raycast-based triangle picking in `ModuleRenderer` using PyOpenGL, returning the clicked `BWMFace` index -- this acts as the foundation for the new "Walkmesh Mode" vertex editing.

6. **Build the Scene Graph Tree**: Create a `QTreeView` widget that mirrors Unity's Hierarchy, populating it from the loaded module's ARE/GIT/LYT data with icons per object type.

7. **Iterative Prototyping**: Build in small increments, testing each feature in isolation before integrating. Use the existing `module_designer.py` as the base, extending rather than rewriting from scratch.

---

## Success Metrics

The Module Designer will be considered **feature-complete** when:

✅ A modder can **create a new module from scratch** (rooms, objects, walkmeshes, VIS) without leaving the editor  
✅ The **scene hierarchy** mirrors Unity's clarity (expand/collapse, search/filter, visibility toggles)  
✅ **4-panel orthographic view** matches Hammer/Radiant workflows for precise alignment  
✅ **Walkmesh vertex editing** is as intuitive as Blender's (click vertex --> drag gizmo --> update mesh)  
✅ **Build + Launch** compiles a playable `.mod` in < 30 seconds  
✅ **Undo/redo** works flawlessly for every operation (room placement, object transforms, walkmesh edits)  
✅ The UI is **intuitive enough** that a Unity/UE5 user can start editing with zero training  
✅ **No external tools** are needed for basic level design (100% self-contained workflow)

---

## Reference Materials

### Inspirations (Study These):
- **Unity Editor** (2020+): Scene view, Inspector, Hierarchy, Project browser, Gizmos, Multi-view
- **Unreal Engine 5**: Outliner, Details panel, Content browser, Viewport, Blueprint system
- **Valve Hammer** (Source SDK): 4-panel view, Texture browser, Entity properties, Vertex manipulation
- **GTKRadiant** (id Tech): Brush editing, Entity inspector, 3-point clipping, Grid snapping
- **Bethesda Creation Kit**: Navmesh editor, Cell browser, Reference dialog, Render window
- **Blender** (3D DCC): Outliner, Properties, 3D viewport, Transform gizmos, Modifier stack
- **Forge (KotOR.js)**: Module editor, WOK editor, Scene graph, Tool palette, Blueprint browser

### Key Design Principles:
1. **Everything in one window** -- No floating dialogs, no separate apps, no mode-switching hell
2. **Contextual tools** -- Right tool auto-selected based on selection (select object --> transform gizmo appears)
3. **Undo everything** -- Every action reversible with Ctrl+Z, even across modes
4. **Visual feedback** -- Gizmos, overlays, highlights for all interactions (no "invisible state")
5. **Non-destructive editing** -- Can always revert to original blueprints (changes saved to GIT, not blueprints)
6. **Keyboard-first** -- All common actions have shortcuts (W/E/R for tools, F to focus, Delete to remove)
7. **Instant feedback** -- No "Apply" buttons; changes reflected in viewport immediately
8. **Progressive disclosure** -- Advanced features hidden until needed (don't overwhelm beginners)

---

**End of Plan** -- See [docs/LEVEL_EDITOR_CHECKLIST.md](docs/LEVEL_EDITOR_CHECKLIST.md) for the detailed 200+ feature breakdown.
13. **Blueprint Browser** (#86-87, #219) -- Search/filter modal with thumbnails
14. **Welcome Tab** (#102) -- Recent files landing page
15. **Indoor File Cleanup** (#220-242) -- Consolidate 23 --> 19 files, delete deprecated duplicate, merge shims
