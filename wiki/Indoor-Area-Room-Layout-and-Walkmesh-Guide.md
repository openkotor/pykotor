# Indoor area room layout and walkmesh guide

Goal: explain the practical workflow for adding, reusing, moving, and debugging indoor area rooms in KotOR, with special focus on layout, walkmeshes, roomlinks, doors, and testing.

## What this guide is for

Use this guide when you are trying to do any of the following:

- reuse an existing room model in a new place
- add a brand-new room to an existing module
- make two rooms connect so the player can actually walk between them
- replace fake door textures with real door transitions
- understand which files matter when indoor area modding goes wrong

This guide is intentionally written as a workflow document rather than a binary format reference. For the underlying format details, use the linked reference pages.

## Before you start

This is a hard part of KotOR modding. If you are stuck, that does not mean you are missing something obvious. The workflow is awkward because several different resources have to agree at the same time, and older community tools were built around assumptions that are not obvious to new modders.

If you remember only one thing before starting, remember this:

- **Indoor room crossing is a layout problem, a walkmesh problem, and a transition-link problem at the same time.**

It is almost never just one isolated mesh-editing task.

## Prerequisites

You do not need every tool in existence, but you do need a workflow that covers four jobs:

1. extract the area's room resources
2. load or edit the area with layout awareness
3. export updated walkmesh data
4. compile edited ASCII back to binary

In the source material you provided, the most repeatedly recommended combination is:

- **KOTORMax** for area/layout-aware editing and roomlink work
- **MDLEdit** for ASCII and binary conversion

You may still use Blender or other tools for geometry work, but if your specific goal is **make room crossing actually function**, the current evidence still points back to a roomlink-capable workflow.

## Quick glossary

These terms get mixed together a lot, so it helps to separate them early.

### Room

A room is one positioned area chunk in the LYT. In indoor modules, each room usually has its own model and its own walkmesh.

### Walkmesh seam

The seam is the physical boundary where two room walkmeshes meet. The seam has to line up geometrically.

### Roomlink / transition edge

This is the logic that says "if the player crosses this edge, they move into room X." A seam can look perfect and still fail if the roomlink is wrong.

### Door hook

A LYT door hook is a placement reference. It is **not** the same thing as a roomlink, and it is **not** the thing that makes crossing work.

### AABB

For indoor room work, AABB matters because room models can contain collision-related AABB data in the MDL. The WOK still carries the main pathfinding and room transition information.

## The mental model first

Before touching tools, keep this model in mind:

1. A room's **visual model** is the room MDL/MDX.
2. A room's **main gameplay walkmesh** is the WOK.
3. A room can also contain **AABB collision data inside the MDL**, which matters for camera collision and related engine behavior.
4. The **LYT** places rooms into the area and establishes their order.
5. The **VIS** decides which rooms are visible from which other rooms.
6. The **roomlinks / transition edges** in the walkmesh decide whether crossing an edge moves the player into another room.

The biggest trap is assuming that visual alignment is enough. It is not. Two rooms can line up perfectly in 3D space and still fail in-game because the transition data is wrong.

## The files that matter

### Room model: MDL/MDX

The room model contains the visible geometry. In practice, room models may also carry embedded AABB data used for camera collision. That means indoor room behavior is not controlled by a single file.

### Room walkmesh: WOK

The WOK is the main area walkmesh. It contains walkable faces, adjacency data, perimeter edges, and the transition IDs that tell the engine which neighboring room a boundary edge leads to.

### Layout: LYT

The LYT positions rooms in world space. Just as importantly for room transitions, the **order of rooms in the LYT defines the 0-based room index** used by walkmesh transition IDs.

If you add, remove, or reorder rooms, old transition IDs may become wrong even if the geometry still looks correct.

### Visibility: VIS

The VIS controls room-to-room visibility, not collision or transitions. When you are first trying to make a new room work, it is often useful to simplify VIS or temporarily leave it out so you can isolate layout and walkmesh problems first.

### Surface materials: `surfacemat.2da`

Walkmesh faces use material IDs that point into `surfacemat.2da`. The `walk` column determines whether a face is walkable. If the seam between rooms is painted with the wrong material, the engine may treat it as blocked even when the geometry is otherwise correct.

### GIT and ARE

The **GIT** handles dynamic things such as doors, placeables, creatures, triggers, and transitions. The **ARE** room entries are useful for room-related data such as ambient audio, but they do not by themselves make room crossing work.

One common misunderstanding is to treat LYT door hooks as the thing that creates room-to-room traversal. They do not. They are placement references. Actual crossing still depends on walkmesh transitions and the rest of the area setup.

## What has to agree before room crossing works

For room crossing to work reliably, all of these must agree:

1. The rooms must be positioned correctly in the layout.
2. The walkmesh seam between both rooms must physically line up.
3. The roomlinks must point to the correct neighboring room indices.
4. The LYT and VIS must include the correct rooms.
5. The room's updated WOK must actually be exported.
6. Any edited ASCII resources must be compiled back to binary.

If you only do the first two steps, you can get a room that looks correct and still blocks crossing.

## Recommended workflow

The currently documented community workflow is strongly centered on **loading the whole area layout first**, then editing inside that layout-aware scene. This matters because roomlinks depend on room context, not just on the local mesh.

### Step 1: decide what kind of change you are making

There are three common jobs:

- **Reusing an existing room in a new place**
- **Creating a new custom room**
- **Turning a fake doorway into a real transition**

All three use the same general pipeline, but the amount of walkmesh and door work increases from left to right.

### Step 2: build a complete working folder

For serious indoor room work, do not operate on isolated files if you can avoid it. Gather the area resources into one working folder:

- the room models you want to work on
- the corresponding walkmeshes
- the area's LYT
- the area's VIS
- any related door resources if you are working on doors

This matches the practical workflow described by modders working on new rooms: keep the layout, visibility, models, and walkmeshes together so the editing tool has full context.

As a practical rule, also consider converting the **adjoining rooms** you plan to test against into the same editable form, not just the one room you care about. That reduces variables when you are debugging a seam.

### Step 3: use a layout-aware workflow, not an isolated model workflow

This is the single most important practical rule:

- **Load the area through the layout workflow**
- **Do not try to solve room transitions by importing one room model in isolation**

Community guidance around KOTORMax is explicit on this point: **you load a LYT via Area Tools**. Trying to feed a `.lyt` file into a model importer is what produces the familiar "invalid ascii" style failure, because the importer expects model ASCII, not a layout file.

Related rule: **`Use Layout Position` is not a substitute for loading the LYT**. That option is only useful when the model ASCII already contains layout-position data from a previous export. Vanilla-decompiled room models generally do not have that embedded data.

### Step 4: convert models to the form your editor expects

For the currently documented KOTORMax-centered workflow, room editing normally happens through the ASCII model pipeline:

1. Extract the binary model resources.
2. Convert them to ASCII using a modern compiler/decompiler workflow.
3. Load the layout and models in the editor.
4. Make the changes.
5. Export ASCII again.
6. Compile back to binary.

Community documentation consistently recommends **MDLEdit** over older MDLOps for this workflow because old MDLOps builds can ignore data or crash on newer KOTORMax output.

### Step 5: treat KOTORMax import options correctly

The source material repeatedly calls out two options that confuse people:

#### `Export WOK File`

This is exactly what it sounds like: when enabled, the exported room includes updated WOK data. If you change walkmesh-related information and this is off, you can do all the right editing work and still test the old walkmesh in-game.

For area room work, assume this should be on unless you have a specific reason not to write WOK.

#### `Use Layout Position`

This option is often misunderstood. It is **not** a replacement for loading the layout itself. Community discussion indicates it only helps when the ASCII model already has layout-position data embedded in its header from a previous export. That usually does **not** apply to vanilla-decompiled rooms.

So:

- use **Area Tools / layout import** to load the actual area
- do **not** rely on `Use Layout Position` to magically line up vanilla room models against a loose LYT

### Step 6: simplify first, then add complexity back

When you are making a seam work for the first time, reduce variables:

- keep the test focused on one connection
- postpone fancy visibility tuning
- postpone door polish if you are only testing traversal
- if necessary, temporarily simplify or remove VIS during early testing

Several sources in your provided material treat VIS as something you can leave out while proving the seam and roomlinks first, then bring back once the crossing works.

## Reusing an existing room in a new place

This is the case that confuses most modders because it looks deceptively simple.

### What people expect

They duplicate a room, move it somewhere else, line the geometry up, maybe adjust the walkmesh, and expect the player to walk across.

### What actually happens

The duplicated room still carries transition assumptions based on its old adjacency. If the room's old walkmesh linked to its original neighbors, those transition IDs are now wrong for the new layout.

### The correct approach

1. Give the duplicated room **new, unique names**.
2. Put the new room into the layout.
3. Align the new room's walkmesh seam to the neighboring room.
4. Reassign the roomlinks so each side points at the correct room index in the current LYT.
5. Export the updated walkmesh.
6. Compile and test.

The crucial point is this: **reusing vanilla room geometry is fine, but reusing vanilla roomlinks is not** once the room is in a different place.

### Can you reuse part of the same walkmesh?

Yes, but only as a **starting shape**.

Using a copied chunk of the original walkmesh can help you block out a doorway or threshold quickly, but the game will not treat that copied piece as a valid new room transition unless you also:

- make sure the seam itself is correct
- give the new room its own valid walkmesh boundary
- assign correct roomlinks between the old room and the new one

This is why "I copied the black-highlighted section from the existing room" often produces something that looks close but still never becomes traversable.

## Creating a brand-new room in an existing area

When making a new room, think in layers.

### Layer 1: visual geometry

Build or modify the visible room geometry first. This is the part that makes the room look right.

### Layer 2: room walkmesh

Create or modify the room's walkmesh so the floor area is actually walkable, the walls are not, and the seam aligns with any neighboring room you want to connect to.

### Layer 3: materials

Paint or assign correct walkmesh materials. Use `surfacemat.2da` as the meaning table:

- walkable floor surfaces should use walkable materials
- wall and blocked regions should use non-walkable materials
- doorway thresholds should use the correct material for the intended interaction

### Layer 4: roomlinks

This is where many attempts fail. The new room needs proper boundary transitions, and the neighboring room needs reciprocal transitions back into the new room.

If the two sides do not reference each other correctly, the player can hit a visually perfect seam and still be blocked.

### Layer 5: layout and visibility

Add the room to the LYT and, when needed, to the VIS. If the room is missing from the layout, the transition IDs cannot line up correctly. If the VIS is wrong, the room may render badly or disappear, even though collision is correct.

### Layer 6: naming and identity

Give new resources unique names. If you duplicate an existing room and keep old names, you make it much harder to reason about:

- which room the LYT is actually referencing
- which walkmesh belongs to which room
- which transition ID should point where

The source material you provided explicitly notes that changing adjacency often goes hand in hand with using **custom room names** rather than continuing to point at vanilla room identities.

## Doors and fake door replacements

Replacing a fake door texture with a real door is more than a model swap.

### You need all of these pieces

- a real door model
- a door walkmesh (`DWK`) with the proper states
- a threshold that uses the correct walkmesh material
- a roomlink arrangement that makes sense on both sides
- dynamic area data in the GIT

Door walkmesh naming matters. Community documentation repeatedly points to the closed/open state naming pattern:

- `_wg_closed`
- `_wg_open1`
- `_wg_open2`

If the door setup is incomplete, you may get a visible door that still does not behave like a real traversal point.

### Door hooks vs real door behavior

Do not confuse these:

- **LYT door hooks** suggest where a door belongs
- **GIT data** defines the actual dynamic door instance
- **DWK and walkmesh transitions** determine whether crossing and door behavior feel correct in play

Another way to say it: LYT can help you place a door, but it does not replace the rest of the door setup.

### Are fake door textures easier to replace by extending one room?

Sometimes people consider extending one room's walkmesh deep into the new space instead of creating a proper second room. That can work as a crude shortcut, but it also collapses behavior you may want to keep separate, such as room-based ambient audio and cleaner room-to-room logic.

If your goal is a proper new room, treat it as a proper new room.

## What not to rely on

These things do **not** solve room crossing on their own:

- lining up visible room meshes
- combining walkmeshes into one big surface
- repainting materials without fixing transitions
- changing the ARE room list and expecting traversal to update
- editing roomlinks by hand in ASCII and assuming the compiler will preserve incomplete or invalid linkage
- relying on LYT door hooks as if they were the traversal system

These may be part of the workflow, but none of them replace proper roomlink assignment.

## Tool choice in practice

Based on the currently available documentation and community reports:

- **KOTORMax** is the workflow most consistently described as supporting layout import/export, VIS import/export, and roomlink editing for indoor rooms.
- **KOTORBlender** is useful for geometry work, but the sources you provided repeatedly describe it as incomplete or unreliable for final room-to-room transition work.
- **MDLEdit** is the safer modern choice for compiling and decompiling ASCII in this workflow.

That does not mean other tools are useless. It means that if the specific problem is **indoor room crossing**, the existing evidence points to a layout-aware, roomlink-capable workflow as the most reliable path.

## A KOTORMax-centered walkthrough

The current source material is not clean enough to document every button label with full certainty across different versions of GMax and 3ds Max. What it does support clearly is the overall workflow.

### 1. Prepare the folder

Put these together:

- the room models you need to work on
- the room walkmeshes
- the area's LYT
- the area's VIS, if you are using it during import

If the tool expects ASCII models for layout-aware loading, make sure the rooms you actually need to edit are available in ASCII form.

### 2. Open the area through the layout workflow

Do **not** load the LYT through the model-loading panel.

Instead:

- open the layout using the **Area Tools** style workflow
- enable options like loading the VIS or loading models at the same time if your version exposes them
- work inside the scene produced by that import

This is the step that gives you room context.

### 3. Confirm the scene contains what you expect

Before editing anything else, confirm:

- the right rooms are present
- the room you want to modify is actually the one you are editing
- the adjoining room is present if you need to inspect the seam

If the adjoining room is missing, stop and fix the scene setup before touching walkmeshes.

### 4. Make the physical seam correct

Adjust the new or reused room so the boundary physically lines up with the neighboring room. This includes:

- floor height
- edge shape
- threshold width
- doorway opening

Do not worry yet about whether the seam is traversable. At this stage you are making it geometrically correct.

### 5. Make the walkmesh correct

Now inspect the walkmesh itself:

- is the threshold actually part of a walkable floor
- are the wall faces still non-walkable
- does the seam line up in walkmesh space, not just visual model space

If you are using a copied walkmesh piece, reshape it into the threshold you actually need rather than treating the copied chunk as finished data.

### 6. Reassign the roomlinks

This is the step people skip.

For each side of the seam:

- identify the boundary edge(s)
- assign the correct neighboring room index
- make sure the connection is reciprocal

If room A points to room B, room B must also point back to room A at the corresponding seam.

### 7. Export with WOK enabled

Make sure the export is writing out the updated WOK. If not, you are not testing your walkmesh changes.

### 8. Compile and test

Compile the ASCII back to binary using a modern toolchain, then test in-game.

If the seam still fails, do not immediately start changing five more things. Return to the troubleshooting section below and isolate the failure.

## A practical end-to-end sequence

If you want one checklist to follow, use this:

1. Extract the room models, walkmeshes, LYT, and VIS into one working folder.
2. Convert the room models you need into ASCII using a modern toolchain.
3. Load the area through the layout workflow, not through isolated model import.
4. If supported by the tool, load the layout together with the models and VIS.
5. Duplicate or create the room with **new unique names**.
6. Move the room into place in the layout.
7. Align the seam between the new room's walkmesh and the neighboring room's walkmesh.
8. Assign walkmesh materials correctly.
9. Reassign the roomlinks for **both** sides of the connection.
10. If the change involves doors, finish the door model, DWK, threshold, and GIT-side setup.
11. Export the updated room with **WOK export enabled**.
12. Compile ASCII back to binary.
13. Test in-game with a simplified VIS if necessary.
14. Only after traversal works should you spend time polishing visibility, doors, and audio details.

## How to test intelligently

Do not test everything at once. Use a layered test order.

### Test 1: does the new room appear

If the room is missing entirely, check the layout first.

### Test 2: can the player stand on the floor

If not, inspect walkmesh materials and export state.

### Test 3: can the player cross the seam

If not, assume roomlinks are wrong until proven otherwise.

### Test 4: does visibility behave

If geometry pops in or vanishes incorrectly, inspect VIS.

### Test 5: do doors behave like real doors

If not, inspect DWK, threshold material, and dynamic area setup.

### Test 6: did you actually test the updated resources

If nothing seems to change from one build to the next, verify the most boring explanation first:

- are the updated binaries the ones the game is loading
- did the compile step succeed
- did the exported WOK actually update
- are you mixing old binary resources with new ASCII assumptions

## Troubleshooting by symptom

### The rooms line up visually, but crossing is blocked

Most likely cause: the roomlinks still point to the old neighbor or were never assigned correctly for the new seam.

### The room exists, but only part of the floor works

Most likely cause: incorrect walkmesh materials, bad seam alignment, or an outdated WOK export.

### The room seems correct, but it disappears or draws badly

Most likely cause: VIS needs to be updated or simplified for debugging.

### A copied room still behaves like the old room

Most likely cause: the room was duplicated visually, but the model naming, walkmesh linkage, or layout context still reflects the original room.

### Editing roomlinks in ASCII does not seem to survive recompilation

Treat this as a warning sign that the workflow is bypassing the proper layout-aware roomlink step. The source material you provided includes examples of this exact failure.

### The LYT import throws an "invalid ascii" style error

Most likely cause: the LYT is being loaded through a model importer instead of the area/layout workflow.

Secondary cause: the layout is trying to pull in models that are not available in the form the editor expects for that workflow.

### The seam looks right, but the player still collides strangely with the camera

Do not forget the split between WOK behavior and MDL-embedded AABB behavior. Traversal may come from one resource while camera behavior comes from another.

### The room crossing works, but the room audio or presentation feels wrong

This often means you fixed traversal first but have not finished the rest of the area integration yet. That is normal. Finish crossing first, then return to ARE, GIT, VIS, and door polish.

## Common myths and corrections

### "If the LYT has door hooks, that is the room connection system"

No. Door hooks are placement references. They are not the same thing as roomlinks.

### "If I repaint the seam as metal or stone, crossing will start working"

No. Correct material assignment matters, but it does not replace valid roomlinks.

### "If I can load one model successfully, I do not need the layout"

Not for indoor room transition work. The layout is what establishes room context.

### "VIS is part of collision"

No. VIS is visibility. It can still confuse debugging, which is why simplifying it early can be helpful.

### "ARE room entries are enough to define the new room"

No. They may matter for room metadata such as ambient audio, but they do not create traversal by themselves.

## If you are completely stuck

Return to the simplest possible case:

1. one existing room
2. one adjacent room
3. no fancy visibility tuning
4. one seam
5. one traversal goal

Then verify, in this order:

- the LYT scene is correct
- the seam is physically correct
- the threshold is walkable
- the roomlinks are reciprocal
- the WOK was exported
- the compiled binaries are the ones being tested

If that minimal case works, add complexity back one layer at a time.

## The most important rules to remember

- Each room keeps its own walkmesh.
- Transition IDs point to **room indices in the LYT**.
- Layout context matters; isolated model editing is not enough for roomlinks.
- WOK export matters; if the updated walkmesh is not written out, nothing else matters.
- Visual success is not traversal success.

## Community references

These sources informed the workflow described here and are worth reading when you need tool-specific details:

- [KOTORmax file by bead-v](https://deadlystream.com/files/file/1151-kotormax/)
- [KOTORmax release topic](https://deadlystream.com/topic/5731-kotormax/)
- [Adding existing rooms to a module](https://deadlystream.com/topic/8517-adding-existing-rooms-to-a-module/)
- [[K1] Creating a new room in an existing module](https://deadlystream.com/topic/11729-k1-creating-a-new-room-in-an-existing-module/)

### See also

- [Area Modding and Room Transitions](Area-Modding-and-Room-Transitions)
- [BWM File Format](BWM-File-Format)
- [MDL/MDX File Format](MDL-MDX-File-Format)
- [LYT File Format](LYT-File-Format)
- [VIS File Format](VIS-File-Format)
- [2DA surfacemat](2DA-surfacemat)
- [Blender Integration](Blender-Integration)
- [Indoor Map Builder User Guide](Indoor-Map-Builder-User-Guide)
