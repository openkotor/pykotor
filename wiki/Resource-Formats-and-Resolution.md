# Resource formats and resolution

This page is the **table of contents for KotOR/TSL file format documentation** on this wiki, the **canonical hex resource type ID table** ([below](#resource-type-identifiers)), and a **short** resolution-order reminder. Full narrative (resource manager *demands*, KEY’s role, override/MOD/[RIM](RIM-File-Format)): [Concepts](Concepts#resource-resolution-order). Glossary topics (override folder, BIF/KEY, MOD/ERF/RIM, GFF, 2DA, language IDs): [Concepts](Concepts).

## Resource resolution order

Full prose (resource manager *demands*, KEY’s role, override vs MOD/ERF/[RIM](RIM-File-Format)): **[Concepts — Resource resolution order](Concepts#resource-resolution-order)**.

**Quick reference:** 1. `override/` 2. loaded [MOD](ERF-File-Format)/[ERF](ERF-File-Format)/[RIM](RIM-File-Format) for the active module 3. loaded save / SAV-side data (when applicable) 4. [KEY](KEY-File-Format)/[BIF](BIF-File-Format) 5. engine defaults.

## ResRef and resource type

**ResRef** (name string, length rules, examples) and how it pairs with a **resource type** in lookups: **[Concepts — ResRef](Concepts#resref-resource-reference)**. GFF field typing: [GFF-File-Format](GFF-File-Format#gff-data-types).

**Resource type IDs:** the **wiki SSOT** hex/label table is the **Resource Type Identifiers** section below (extensions like `.utc`, `.2da`, `.mdl` follow the same mapping for loose files).

**Language IDs** (`dialog.tlk`, localization): [Concepts — Language IDs](Concepts#language-ids-kotor).

## Resource Type Identifiers

*KotOR* uses numeric resource type IDs inherited from the *Aurora* line and extended for *Odyssey* and *Eclipse*. The table below lists types seen across *BioWare* engines; many rows are unused in *KotOR* (marked in the **Description** column).

| Resource Name | Type ID | Description                                    |
| ------------- | ------- | ---------------------------------------------- |
| RES           | 0x0000  | Used for `.res` resources within the [save game containers](ERF-File-Format)                     |
| BMP           | 0x0001  | Bitmap image                         |
| MVE           | 0x0002  | Movie/video file       Not used in *KotOR*                   |
| [TGA](https://en.wikipedia.org/wiki/Truevision_TGA)           | 0x0003  | TarGA image format                          |
| [WAV](WAV-File-Format)           | 0x0004  | Wave audio file (see [WAV File Format](WAV-File-Format)) |
| [INI](https://en.wikipedia.org/wiki/INI_file)           | 0x0007  | Configuration file (e.g., `swkotor.ini`, `swkotor2.ini`)                          |
| BMU           | 0x0008  | Unknown  Not used in *KotOR*                                |
| MPG           | 0x0009  | MPEG video  Not used in *KotOR*                            |
| [TXT](https://en.wikipedia.org/wiki/Text_file)           | 0x000A  | Text file  Not used in *KotOR*                                  |
| PLH           | 0x07D0  | *PLaceable Header* type.  Not used in *KotOR*                      |
| TEX           | 0x07D1  | Texture. Not used in *KotOR*                      |
| [MDL](MDL-MDX-File-Format)           | 0x07D2  | 3D [model](MDL-MDX-File-Format) file (see [MDL/MDX File Format](MDL-MDX-File-Format))                                   |
| THG           | 0x07D3  | Unknown. Not used in *KotOR*                                |
| FNT           | 0x07D5  | Font file. Not used in *KotOR*                                  |
| Lua           | 0x07D7  | Lua script. Not used in *KotOR*                             |
| SLT           | 0x07D8  | Unknown. Not used in *KotOR*                               |
| [NSS](NSS-File-Format)           | 0x07D9  | *NWScript* source code (see [NSS File Format](NSS-File-Format))                            |
| [NCS](NCS-File-Format)           | 0x07DA  | *Compiled NWScript* bytecode (see [NCS File Format](NCS-File-Format))                     |
| [MOD](ERF-File-Format)           | 0x07DB  | [*Module* ERF archive/container](ERF-File-Format)                         |
| [ARE](GFF-File-Format#are-area)           | 0x07DC  | *Area* definition (see [GFF-ARE](GFF-ARE))                                 |
| SET           | 0x07DD  | Unknown.  Not used in *KotOR*                               |
| [IFO](GFF-File-Format#ifo-module-info)           | 0x07DE  | *Module* InFOrmation (see [GFF-IFO](GFF-IFO))                              |
| BIC           | 0x07DF  | BlueprInt Creature. *KotOR* supports these but nobody uses them, use [UTC](GFF-UTC) instead.                  |
| [WOK](BWM-File-Format)           | 0x07E0  | *Walkmesh* (see [BWM File Format](BWM-File-Format))                                |
| [2DA](2DA-File-Format)           | 0x07E1  | *Two-Dimensional Array* data (see [2DA File Format](2DA-File-Format))                      |
| [TLK](TLK-File-Format)           | 0x07E2  | *Talk Table* (Localized Strings, see [TLK File Format](TLK-File-Format))                 |
| [TXI](TXI-File-Format)           | 0x07E6  | [TeXture Information](TXI-File-Format)                            |
| [GIT](GFF-File-Format#git-game-instance-template)           | 0x07E7  | [Game Instance Template](GFF-File-Format#git-game-instance-template) (see [GFF-GIT](GFF-GIT))                          |
| BTI           | 0x07E8  | Blueprint Template Item. *KotOR* supports these but nobody uses them, use [UTI](GFF-UTI) instead.                 |
| [UTI](GFF-File-Format#uti-item)           | 0x07E9  | [item templates](GFF-File-Format#uti-item) (see [GFF-UTI](GFF-UTI))                                   |
| BTC           | 0x07EA  | Blueprint Template Creature. *KotOR* supports these but nobody uses them, use [UTC](GFF-UTC) instead.                |
| [UTC](GFF-File-Format#utc-creature)           | 0x07EB  | [Creature Template](GFF-File-Format#utc-creature) (see [GFF-UTC](GFF-UTC))                               |
| [DLG](GFF-File-Format#dlg-dialogue)           | 0x07ED  | Dialogue/conversation (see [GFF-DLG](GFF-DLG))                           |
| [ITP](Bioware-Aurora-PaletteITP)           | 0x07EE  | *ITP* format (see [Bioware-Aurora-PaletteITP](Bioware-Aurora-PaletteITP)).                         |
| BTT           | 0x07EF  | *Blueprint Template Trigger*. *KotOR* supports these but nobody uses them, use [UTT](GFF-UTT) instead.                 |
| [UTT](GFF-File-Format#utt-trigger)           | 0x07F0  | *Trigger Template* (see [GFF-UTT](GFF-UTT)).                                |
| DDS           | 0x07F1  | *DirectDraw Surface Texture* (see [DDS File Format](DDS-File-Format)).                                |
| [UTS](GFF-File-Format#uts-sound)           | 0x07F3  | *Sound Template* (see [GFF-UTS](GFF-UTS)).                                |
| LTR           | 0x07F4  | *Letter Format* (see [LTR File Format](LTR-File-Format)). Not used in *KotOR*                                |
| [GFF](GFF-File-Format)           | 0x07F5  | Generic file format (container, see [GFF File Format](GFF-File-Format))                 |
| [FAC](GFF-File-Format#fac-faction)           | 0x07F6  | Faction                               |
| BTE           | 0x07F7  | Blueprint encounter                   |
| [UTE](GFF-File-Format#ute-encounter)           | 0x07F8  | [encounter template](GFF-File-Format#ute-encounter) (see [GFF-UTE](GFF-UTE))                              |
| BTD           | 0x07F9  | Blueprint door    Not used in *KotOR*     |
| [UTD](GFF-File-Format#utd-door)           | 0x07FA  | [door templates](GFF-File-Format#utd-door) (see [GFF-UTD](GFF-UTD))                                   |
| BTP           | 0x07FB  | Blueprint placeable   Not used in *KotOR*  |
| [UTP](GFF-File-Format#utp-placeable)           | 0x07FC  | [placeable templates](GFF-File-Format#utp-placeable) (see [GFF-UTP](GFF-UTP))                              |
| DTF           | 0x07FD  | Unknown  Not used in *KotOR*                                |
| GIC           | 0x07FE  | Unknown  Not used in *KotOR*                                |
| [GUI](GFF-File-Format#gui-graphical-user-interface)           | 0x07FF  | User interface definition (see [GFF-GUI](GFF-GUI))                       |
| CSS           | 0x0800  | Unknown  Not used in *KotOR*                                |
| CCS           | 0x0801  | Unknown  Not used in *KotOR*                                |
| BTM           | 0x0802  | Blueprint merchant.  *KotOR* supports these but nobody uses them, use [UTM](GFF-UTM) instead.              |
| [UTM](GFF-File-Format#utm-merchant)           | 0x0803  | [Merchant/store template](GFF-File-Format#utm-merchant) (see [GFF-UTM](GFF-UTM))                         |
| [DWK](BWM-File-Format)           | 0x0804  | [Door walkmesh](BWM-File-Format) (see [BWM File Format](BWM-File-Format))                                |
| [PWK](BWM-File-Format)           | 0x0805  | [Placeable walkmesh](BWM-File-Format) (see [BWM File Format](BWM-File-Format))                                |
| BTG           | 0x0806  | Blueprint trigger  Not used in *KotOR*       |
| UTG           | 0x0807  | Unknown            Not used in *KotOR*   |
| [JRL](GFF-File-Format#jrl-journal)           | 0x0808  | Journal/quest log (see [GFF-JRL](GFF-JRL))                               |
| SAV           | 0x0809  | [Save game containers](ERF-File-Format) (see [ERF File Format](ERF-File-Format))                               |
| [UTW](GFF-File-Format#utw-waypoint)           | 0x080A  | [Waypoint Template](GFF-File-Format#utw-waypoint)                               |
| 4PC           | 0x080B  | Unknown  Not used in *KotOR*          |
| [SSF](SSF-File-Format)           | 0x080C  | [Sound Set Files](SSF-File-Format) (see [SSF File Format](SSF-File-Format))                                  |
| HAK           | 0x080D  | Hak pak container. Not used in *KotOR*                                |
| NWM           | 0x080E  | *Neverwinter Nights* module (Not used in *KotOR*)                                 |
| BIK           | 0x080F  | BInK video format                                |
| PTM           | 0x0811  | Unknown       Not used in *KotOR*         |
| PTT           | 0x0812  | Unknown       Not used in *KotOR*         |
| [ERF](ERF-File-Format)           | 0x270D  | [Encapsulated Resource File](ERF-File-Format) (see [ERF File Format](ERF-File-Format))                      |
| [BIF](BIF-File-Format)           | 0x270E  | [Bioware Index File](BIF-File-Format) (container, see [BIF File Format](BIF-File-Format))                    |
| [KEY](KEY-File-Format)           | 0x270F  | [KEY](KEY-File-Format) table ([BIF](BIF-File-Format) index, see [KEY File Format](KEY-File-Format))                          |

## File format index

### File formats

- **[MDL/MDX File Format](MDL-MDX-File-Format)** ← Complete reference for 3D [model](MDL-MDX-File-Format) files
  - **[2DA File Format](2DA-File-Format)** ← Complete reference for Two-Dimensional array format (see also [Official Bioware 2DA Documentation](Bioware-Aurora-2DA)). All individual 2DA file documentation has been inlined into this document.
  - [acbonus.2da](2DA-File-Format#acbonus2da)
  - [ambientmusic.2da](2DA-File-Format#ambientmusic2da)
  - [ambientsound.2da](2DA-File-Format#ambientsound2da)
  - [ammunitiontypes.2da](2DA-File-Format#ammunitiontypes2da)
  - [animations.2da](2DA-File-Format#animations2da)
  - [appearance.2da](2DA-File-Format#appearance2da)
  - [appearancesndset.2da](2DA-File-Format#appearancesndset2da)
  - [baseitems.2da](2DA-File-Format#baseitems2da)
  - [bindablekeys.2da](2DA-File-Format#bindablekeys2da)
  - [bodybag.2da](2DA-File-Format#bodybag2da)
  - [camerastyle.2da](2DA-File-Format#camerastyle2da)
  - [classes.2da](2DA-File-Format#classes2da)
  - [classpowergain.2da](2DA-File-Format#classpowergain2da)
  - [combatanimations.2da](2DA-File-Format#combatanimations2da)
  - [creaturespeed.2da](2DA-File-Format#creaturespeed2da)
  - [cursors.2da](2DA-File-Format#cursors2da)
  - [dialoganimations.2da](2DA-File-Format#dialoganimations2da)
  - [difficultyopt.2da](2DA-File-Format#difficultyopt2da)
  - [disease.2da](2DA-File-Format#disease2da)
  - [doortypes.2da](2DA-File-Format#doortypes2da)
  - [droiddischarge.2da](2DA-File-Format#droiddischarge2da)
  - [effecticon.2da](2DA-File-Format#effecticon2da)
  - [emotion.2da](2DA-File-Format#emotion2da)
  - [encdifficulty.2da](2DA-File-Format#encdifficulty2da)
  - [exptable.2da](2DA-File-Format#exptable2da)
  - [facialanim.2da](2DA-File-Format#facialanim2da)
  - [feat.2da](2DA-File-Format#feat2da)
  - [featgain.2da](2DA-File-Format#featgain2da)
  - [feedbacktext.2da](2DA-File-Format#feedbacktext2da)
  - [footstepsounds.2da](2DA-File-Format#footstepsounds2da)
  - [forceshields.2da](2DA-File-Format#forceshields2da)
  - [fractionalcr.2da](2DA-File-Format#fractionalcr2da)
  - [gender.2da](2DA-File-Format#gender2da)
  - [genericdoors.2da](2DA-File-Format#genericdoors2da)
  - [globalcat.2da](2DA-File-Format#globalcat2da)
  - [grenadesnd.2da](2DA-File-Format#grenadesnd2da)
  - [guisounds.2da](2DA-File-Format#guisounds2da)
  - [heads.2da](2DA-File-Format#heads2da)
  - [inventorysnds.2da](2DA-File-Format#inventorysnds2da)
  - [iprp_abilities.2da](2DA-File-Format#iprp_abilities2da)
  - [iprp_acmodtype.2da](2DA-File-Format#iprp_acmodtype2da)
  - [iprp_aligngrp.2da](2DA-File-Format#iprp_aligngrp2da)
  - [iprp_ammotype.2da](2DA-File-Format#iprp_ammotype2da)
  - [iprp_combatdam.2da](2DA-File-Format#iprp_combatdam2da)
  - [iprp_costtable.2da](2DA-File-Format#iprp_costtable2da)
  - [iprp_damagecost.2da](2DA-File-Format#iprp_damagecost2da)
  - [iprp_damagetype.2da](2DA-File-Format#iprp_damagetype2da)
  - [iprp_immunity.2da](2DA-File-Format#iprp_immunity2da)
  - [iprp_lightcol.2da](2DA-File-Format#iprp_lightcol2da)
  - [iprp_monstdam.2da](2DA-File-Format#iprp_monstdam2da)
  - [iprp_mosterhit.2da](2DA-File-Format#iprp_mosterhit2da)
  - [iprp_onhit.2da](2DA-File-Format#iprp_onhit2da)
  - [iprp_paramtable.2da](2DA-File-Format#iprp_paramtable2da)
  - [iprp_protection.2da](2DA-File-Format#iprp_protection2da)
  - [iprp_saveelement.2da](2DA-File-Format#iprp_saveelement2da)
  - [iprp_savingthrow.2da](2DA-File-Format#iprp_savingthrow2da)
  - [iprp_walk.2da](2DA-File-Format#iprp_walk2da)
  - [itempropdef.2da](2DA-File-Format#itempropdef2da)
  - [itemprops.2da](2DA-File-Format#itemprops2da)
  - [keymap.2da](2DA-File-Format#keymap2da)
  - [loadscreenhints.2da](2DA-File-Format#loadscreenhints2da)
  - [loadscreens.2da](2DA-File-Format#loadscreens2da)
  - [masterfeats.2da](2DA-File-Format#masterfeats2da)
  - [modulesave.2da](2DA-File-Format#modulesave2da)
  - [movies.2da](2DA-File-Format#movies2da)
  - [pazaakdecks.2da](2DA-File-Format#pazaakdecks2da)
  - [placeableobjsnds.2da](2DA-File-Format#placeableobjsnds2da)
  - [placeables.2da](2DA-File-Format#placeables2da)
  - [planetary.2da](2DA-File-Format#planetary2da)
  - [plot.2da](2DA-File-Format#plot2da)
  - [poison.2da](2DA-File-Format#poison2da)
  - [portraits.2da](2DA-File-Format#portraits2da)
  - [prioritygroups.2da](2DA-File-Format#prioritygroups2da)
  - [racialtypes.2da](2DA-File-Format#racialtypes2da)
  - [ranges.2da](2DA-File-Format#ranges2da)
  - [regeneration.2da](2DA-File-Format#regeneration2da)
  - [repute.2da](2DA-File-Format#repute2da)
  - [skills.2da](2DA-File-Format#skills2da)
  - [soundset.2da](2DA-File-Format#soundset2da)
  - [spells.2da](2DA-File-Format#spells2da)
  - [stringtokens.2da](2DA-File-Format#stringtokens2da)
  - [subrace.2da](2DA-File-Format#subrace2da)
  - [surfacemat.2da](2DA-File-Format#surfacemat2da)
  - [texpacks.2da](2DA-File-Format#texpacks2da)
  - [traps.2da](2DA-File-Format#traps2da)
  - [tutorial.2da](2DA-File-Format#tutorial2da)
  - [upcrystals.2da](2DA-File-Format#upcrystals2da)
  - [upgrade.2da](2DA-File-Format#upgrade2da)
  - [videoeffects.2da](2DA-File-Format#videoeffects2da)
  - [visualeffects.2da](2DA-File-Format#visualeffects2da)
  - [weaponsounds.2da](2DA-File-Format#weaponsounds2da)
  - [xptable.2da](2DA-File-Format#xptable2da)
- **[TLK File Format](TLK-File-Format)** ← Complete reference for [Talk Table](TLK-File-Format) format
- [BIF File Format](BIF-File-Format) ← BioWare Infinity format
- [KEY File Format](KEY-File-Format) ← [KEY](KEY-File-Format) file format
- **[BWM File Format](BWM-File-Format)** ← Complete reference for Binary [walkmesh](BWM-File-Format) format
- **[GUI File Format](GFF-GUI)** ← Complete reference for Graphical User Interface format
- [ERF File Format](ERF-File-Format) ← Encapsulated Resource format (MOD, SAV, HAK; [RIM comparison](ERF-File-Format#rim-versus-erf))
- **[Kit Structure Documentation](Kit-Structure-Documentation)** ← Complete reference for indoor kit structure and generation
- [GFF File Format](GFF-File-Format) ← Generic file Format (see also [Official Bioware GFF Documentation](Bioware-Aurora-GFF))
  - [ARE (Area)](GFF-ARE)
  - [DLG (Dialogue)](GFF-DLG)
  - [GIT (Game Instance Template)](GFF-GIT)
  - [GUI (Graphical User Interface)](GFF-GUI)
  - [IFO (Module Info)](GFF-IFO)
  - [JRL (Journal)](GFF-JRL)
  - [PTH (Path)](GFF-PTH)
  - [UTC (Creature)](GFF-UTC)
  - [UTD (Door)](GFF-UTD)
  - [UTE (Encounter)](GFF-UTE)
  - [UTI (Item)](GFF-UTI)
  - [UTM (Merchant)](GFF-UTM)
  - [UTP (Placeable)](GFF-UTP)
  - [UTS (Sound)](GFF-UTS)
  - [UTT (Trigger)](GFF-UTT)
  - [UTW (Waypoint)](GFF-UTW)
- [DDS File Format](DDS-File-Format) ← DirectDraw Surface texture format
- [LIP File Format](LIP-File-Format) ← [LIP](LIP-File-Format) sync format
- [LTR File Format](LTR-File-Format) ← [Letter](LTR-File-Format) format
- [LYT File Format](LYT-File-Format) ← [Layout](LYT-File-Format) format
- [NCS File Format](NCS-File-Format) ← [NwScript Compiled Script](NCS-File-Format) format
- [NSS File Format](NSS-File-Format) ← [NwScript Source](NSS-File-Format) format (*nwscript.nss*, function/constant definitions)
- [RIM File Format](RIM-File-Format) ← [Resource Image](RIM-File-Format) format
- [SSF File Format](SSF-File-Format) ← [Sound Set Files](SSF-File-Format) format
- [TPC File Format](TPC-File-Format) ← [Texture Pack Container](TPC-File-Format) format
- [TXI File Format](TXI-File-Format) ← [Texture Info](TXI-File-Format) format
- [VIS File Format](VIS-File-Format) ← [Visibility](VIS-File-Format) format
- [WAV File Format](WAV-File-Format) ← [Wave](WAV-File-Format) audio format

### See also

- [Concepts](Concepts) — Override, BIF/KEY, MOD/ERF/RIM, GFF, 2DA, language IDs
- [KEY-File-Format](KEY-File-Format) — KEY binary layout and index role
- [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#file-priority-and-where-to-put-your-files) — Where to install files
- [Home](Home) — Wiki hub
- [Reverse Engineering Findings — Resource Management System](reverse_engineering_findings#resource-management-system) — Engine `CExoResMan` / resource loading (conceptual)
