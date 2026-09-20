================================================================================
 NeutronTools configuration - Terranova pack
 Last updated: 2026-09-20
================================================================================

GOAL
----
Integrate every item from the Aether and Deeper and Darker mods into the
vanilla Minecraft creative tabs, and hide their standalone mod tabs, so the
creative menu only keeps the vanilla-style tab layout with all the mod
content living inside the normal places.

HIDDEN TABS (disabled_tabs.json)
--------------------------------
Aether:        building_blocks, armor_and_accessories, functional_blocks,
               natural_blocks, redstone_blocks, ingredients, food_and_drinks,
               dungeon_blocks, spawn_eggs, equipment_and_utilities
DeeperDark:    deeper_darker
plus the other non-vanilla tabs disabled before this task (create_dragons_plus,
railways:tracks, mowziesmobs, create_enchantment_industry, simulatedcoasters,
cataclysm:cataclysm_block, escalated, kubejs, catools, numismatics, aeroworks).

Disabled tabs no longer appear in the creative bar (the mod removes them from
the bar population). Their items are still registered and now routed into the
vanilla tabs via tab_edits/minecraft.json.

VANILLA TAB ROUTING (tab_edits/minecraft.json)
-----------------------------------------------
This is the ONLY file that edits minecraft:* tabs (single source of truth).

  minecraft:building_blocks       174 items added (79 Aether + 95 DeeperDark)
  minecraft:natural_blocks        Aether via match_tab (30, from aether:natural_blocks
                                  cache) + 30 DeeperDark names + everycomp
                                  hedges/carpets (match_name) + forge:ores (match_tags)
  minecraft:functional_blocks     21 items (13 Aether + 8 DeeperDark) +
                                  farmersdelight "kitchen" blocks (match_name)
  minecraft:redstone_blocks       31 items (8 Aether + 23 DeeperDark)
  minecraft:tools_and_utilities   70 items (47 Aether + 23 DeeperDark)
  minecraft:combat                82 items (70 Aether + 11 DeeperDark) +
                                  supplementaries:cannon
  minecraft:food_and_drinks       11 items (8 Aether + 3 DeeperDark)
  minecraft:ingredients           20 items (6 Aether + 14 DeeperDark)
  minecraft:spawn_eggs            aether:spawn_eggs (match_tab, 20) +
                                  DeeperDark/Northstar/generic spawn eggs (match_name)

Classification choices: wood/stone/glass/dungeon blocks -> building; ores/leaves/
saplings/aerclouds -> natural; signs/beds/machines/chests -> functional;
buttons/pressure plates/trapdoors/transmitters -> redstone; tools/buckets/boats/
keys/discs/staffs -> tools; swords/armor/accessories/dart shooters -> combat;
berries/food -> food; gems/sticks/powders/templates -> ingredients; moa/spawn eggs
-> spawn_eggs.

Items with no names (match_tab / match_name / match_tags rules) resolve against
the creative-tab cache on every launch, so they stay in sync automatically.

CONFIG LAYOUT & SYNC (IMPORTANT)
--------------------------------
There are TWO copies of this directory:

  1. pack/config/neutrontools/          <- source of truth, git tracked
  2. minecraft/config/neutrontools/     <- live copy the running game reads/writes

To ship changes: run build.sh at the instance root (or copy the edited files
from pack/ into minecraft/config/neutrontools/). Both copies are kept in sync.

The game WRITES at run time: cached_original_tabs.json (snapshot of every tab's
contents post-edit, used for match_tab/aether:natural_blocks & aether:spawn_eggs
resolution), keybinds.json, generated/ (item registry listing for authoring).
Do not delete cached_original_tabs.json - match_tab rules depend on it.

CRITICAL GOTCHA (why tabs were not filling before)
--------------------------------------------------
NeutronTools keys tab-edits by target tab id in a map. When MORE THAN ONE file
in tab_edits/ contains the same target tab, the LAST file processed (alphabetical
file order) OVERWRITES the earlier ones for that tab - edits are NOT merged.

Previously the pack had aether.json AND deeperdarker.json both editing the same
minecraft:* tabs, plus minecraft.json re-editing several of them. Result: for
every tab edited by more than one file only the alphabetically-last definition
survived (e.g. building_blocks only received DeeperDark; natural/functional/
combat/food/ingredients received NOTHING from aether.json/deeperdarker.json).
That is the fix history behind this task.

RESOLUTION: every minecraft:* tab is defined in exactly ONE tab_edits file
(minecraft.json). aether.json and deeperdarker.json were deleted after their
rules were merged into minecraft.json. The verify step below now asserts there
is never more than one file per target tab.

ABOUT THE "index" / "hide_old_tab" FIELDS
------------------------------------------
The rules for everycomp/forge:ores carry "index"/"hide_old_tab" fields copied
verbatim from the previous working config. The 1.13.0 source does not implement
them; the installed version is 1.14.0 (see below). They are harmless either way
(ignored if unsupported, honoured if supported) - kept to preserve prior
behaviour.

VERSION NOTES
-------------
Installed mod:   neutrontools-1.14.0.jar (verified in game log 2026-09-20)
Source studied:  MC-NeutronTools git repo at v1.13.0 (1.14.0 source not seen)
Build event:     handler runs at EventPriority.LOWEST on the mod bus, so modded
                 tab additions run before the NeutronTools edits.
Tab caching:     NeutronCreativeTabs caches each tab's display items at the end
                 of buildContents, THEN clears disabled tab content.
Ordering:        ordered_tabs.json defines the bar sequence; tabs not listed are
                 appended automatically unless disabled.

VERIFICATION (2026-09-20)
-------------------------
- All JSON files parse (python json.load).
- Coverage vs the live registry snapshot: none of the 216 DeeperDark items and
  none of the 271 Aether items are left unrouted.
- No tab target appears in more than one tab_edits file (conflict-free).
- Per-tab routed counts shown above, confirmed against cache.
- Survival rule proven against the 2026-09-20 17:14 game-run cache: the previous
  run applied edits ONLY to building_blocks - exactly matching the predicted
  last-file-wins behaviour, confirming the root cause.

INTERSTELLAR / NORTHSTAR TABS (space.json)
------------------------------------------
The Northstar ("space") tabs are organised as space / space_2 / space_3:
  northstar:blocks  -> space
  northstar:items   -> space_2
  northstar:tech    -> space_3
Tabs 2 and 3 have been COMBINED: the 24 northstar:tech items are routed into
northstar:items via { "after": "northstar:oxygen_bucket", "match_tab":
"northstar:tech" } so they land AT THE TOP of the combined tab (right after the
tab's first item). northstar:tech is now disabled (disabled_tabs.json) and
removed from the bar (ordered_tabs.json). The `after` anchor chains correctly
(inserted stacks maintain their original order) and `match_tab` resolves from
cached_original_tabs.json, so the tech list stays correct even after the tech
tab is hidden. NOTE: items inserted with an `after` anchor are added with
PARENT_TAB_ONLY visibility (they will not appear in the creative Search tab).

HOW TO TEST
-----------
1. Sync (build.sh) so minecraft/config/neutrontools matches pack/.
2. Launch, open the creative menu.
3. Expect: only ordered bar tabs remain; Aether and DeeperDark items present in
   their mapped vanilla tabs at the END of each tab (appended-if-not-present).
4. If a specific rule seems to miss items, check minecraft/logs/latest.log for
   NeutronTools errors, and re-check cached_original_tabs.json after a launch
   (match_tab rules read it).

NOTES / OUT OF SCOPE
--------------------
- minecraft:op_blocks / op_blockss and op.json tab edits are untouched legacy
  content (creator-only admin items), unrelated to this task.
- "routed" counts may exceed per-mod cached totals by a few items; that is just
  the same item appearing in more than one mapping target, which is intentional
  and matches the vanilla pattern (e.g. logs in building + natural).