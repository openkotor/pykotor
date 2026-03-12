# JRL (Journal)

Part of the [GFF File Format Documentation](GFF-File-Format).

[JRL files](GFF-File-Format#jrl-journal) define the structure of the player's [quest journal](GFF-File-Format#jrl-journal). They organize [quests](GFF-File-Format#jrl-journal) into categories and track progress through individual [journal entries](GFF-File-Format#jrl-journal). JRL files are loaded with the same [resource resolution order](KEY-File-Format#key-file-purpose) as other resources (override, MOD/SAV, KEY/BIF).

**Official Bioware Documentation:** For the authoritative Bioware Aurora Engine Journal format specification, see [Bioware Aurora Journal Format](Bioware-Aurora-Journal).

**For mod developers:** Journal updates are typically driven by [DLG](GFF-DLG) Quest/QuestEntry and scripts (`AddJournalQuestEntry`); see [TSLPatcher GFFList Syntax](TSLPatcher-GFFList-Syntax) and [HoloPatcher README for Mod Developers](HoloPatcher-README-for-mod-developers.).

**Related formats:** JRL is referenced by [DLG](GFF-DLG) (Quest, QuestEntry), [NCS](NCS-File-Format) (journal API), and [2DA](2DA-File-Format) (e.g. journal.2da for XP).

## References

**PyKotor:**

- [`Libraries/PyKotor/src/pykotor/resource/generics/jrl.py`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/jrl.py) - JRL [GFF](GFF-File-Format) parsing and field definitions

**HolocronToolset:**

- Journal (JRL) editing in dialogue and module context

**Vendor Implementations:**

- reone/xoreos journal (JRL) GFF parsers

## Quest structure

[JRL](GFF-File-Format#jrl-journal) files contain a list of `Categories` (Quests), each containing a list of `EntryList` (States).

| field | type | Description |
| ----- | ---- | ----------- |
| `Categories` | [List](GFF-File-Format#gff-data-types) | List of quests |

## Quest Category (JRLQuest)

| field | type | Description |
| ----- | ---- | ----------- |
| `Tag` | [CExoString](GFF-File-Format#gff-data-types) | Unique quest identifier |
| `Name` | [CExoLocString](GFF-File-Format#gff-data-types) | Quest title |
| `Comment` | [CExoString](GFF-File-Format#gff-data-types) | Developer comment |
| `Priority` | [int32](GFF-File-Format#gff-data-types) | Sorting priority (0=Highest, 4=Lowest) |
| `PlotIndex` | [int32](GFF-File-Format#gff-data-types) | Legacy plot index |
| `PlanetID` | [int32](GFF-File-Format#gff-data-types) | Planet association (unused) |
| `EntryList` | [List](GFF-File-Format#gff-data-types) | List of quest states |

**Priority Levels:**

- **0 (Highest)**: Main quest line
- **1 (High)**: Important side quests
- **2 (Medium)**: Standard side quests
- **3 (Low)**: Minor tasks
- **4 (Lowest)**: Completed/Container

## Quest Entry (JRLEntry)

| field | type | Description |
| ----- | ---- | ----------- |
| `ID` | [int32](GFF-File-Format#gff-data-types) | State identifier (referenced by scripts/dialogue) |
| `Text` | [CExoLocString](GFF-File-Format#gff-data-types) | [Journal](GFF-File-Format#jrl-journal) text displayed for this state |
| `End` | [byte](GFF-File-Format#gff-data-types) | 1 if this state completes the quest |
| `XP_Percentage` | [float](GFF-File-Format#gff-data-types) | XP reward multiplier for reaching this state |

**Quest Updates:**

- Scripts use `AddJournalQuestEntry("Tag", ID)` to update quests.
- Dialogues use `Quest` and `QuestEntry` fields.
- Only the highest ID reached is typically displayed (unless `AllowOverrideHigher` is set in `global.jrl` logic).
- `End=1` moves the quest to the "Completed" tab.

## Implementation Notes

- **global.jrl**: The master [journal files](GFF-File-Format#jrl-journal) for the entire game.
- **Module JRLs**: Not typically used; most quests are global.
- **XP Rewards**: `XP_Percentage` scales the `journal.2da` XP value for the quest.

## See also

- [GFF File Format](GFF-File-Format) - Generic format underlying JRL
- [GFF-DLG (Dialogue)](GFF-DLG) - Quest/QuestEntry updates from conversations
- [NCS File Format](NCS-File-Format) - Scripts that call journal API
- [Bioware Aurora Journal Format](Bioware-Aurora-Journal) - Official journal specification
