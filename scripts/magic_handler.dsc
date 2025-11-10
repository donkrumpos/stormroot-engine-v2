spellbook_transform_world:
    type: world
    debug: false
    events:
        # When player swaps items to offhand
        on player swaps items:
        - if <context.offhand.has_flag[spellbook]>:
            - wait 1t
            - run transform_hotbar_task def:<player>
        - else if <player.item_in_offhand.has_flag[spellbook]>:
            - run restore_hotbar_task def:<player>
        
        # Prevent sigils from being moved/dropped
        on player clicks item_flagged:spell_sigil in inventory:
        - determine cancelled
        
        on player drops item_flagged:spell_sigil:
        - determine cancelled
        
setup_player_command:
    type: command
    name: magicsetup
    description: Sets up your magic stats
    script:
    # Set Intelligence to 10 (this determines max mana)
    - flag <player> stat.intelligence.level:10
    
    # Max mana = Intelligence × 2
    # So with 10 INT, player gets 20 max mana
    - define max_mana <player.flag[stat.intelligence.level].mul[2]>
    
    # Start player at full mana
    - flag <player> stat.mana.current:<[max_mana]>
    - flag <player> stat.mana.max:<[max_mana]>
    
    - narrate "<green>Magic initialized! INT: <player.flag[stat.intelligence.level]>, Mana: <player.flag[stat.mana.current]>/<player.flag[stat.mana.max]>"


learn_spell_command:
    type: command
    name: learn
    description: Learn a spell
    script:
    # Get the spell name from the command
    - define spell_name <context.args.get[1]||null>
    
    # Check if they provided a spell name
    - if <[spell_name]> == null:
        - narrate "<red>Usage: /learn <spell_name>"
        - stop
    
    # Check if the spell exists in our data
    - if <script[spell_data].data_key[spells.<[spell_name]>]||null> == null:
        - narrate "<red>That spell doesn't exist!"
        - stop
    
    # Add the spell to the player's known spells list
    - flag <player> known_spells:->:<[spell_name]>
    
    # Get the display name
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    
    - narrate "<green>You have learned: <[display]>!"

cast_command:
    type: command
    name: cast
    description: Cast a spell at your target
    script:
    # Get the spell name from command
    - define spell_name <context.args.get[1]||null>
    
    # Check if they provided a spell name
    - if <[spell_name]> == null:
        - narrate "<red>Usage: /cast <spell_name>"
        - stop
    
    # Check if player knows this spell
    - if <player.flag[known_spells].contains[<[spell_name]>].not>:
        - narrate "<red>You don't know that spell!"
        - stop
    
    # Get target
    - define target <player.target>
    
    # Call the casting task
    - run cast_spell_task def:<[spell_name]>|<player>|<[target]>


mana_regen_world:
    type: world
    debug: false
    events:
        # This runs when the server starts
        on server start:
        - run mana_regen_task

mana_regen_task:
    type: task
    debug: false
    script:
    - while true:
        - foreach <server.online_players> as:player:
            
            # Check if player is meditating (sneaking + not moving)
            # Check if player has moved since last check
            - define last_location <[player].flag[last_meditation_location]||null>
            - define current_location <[player].location.simple>
            
            # Player must be sneaking AND in same spot as last tick
            - if <[player].is_sneaking> && <[last_location]> == <[current_location]>:
                # Start meditation if not already
                - if <[player].has_flag[meditating].not>:
                    - flag <[player]> meditating
                    - narrate "<aqua>You begin to meditate..." targets:<[player]>
                    - playsound <[player]> block_enchantment_table_use pitch:1.5 volume:0.5
                
                - define regen_amount 1
            
            # If they were meditating but stopped
            - else if <[player].has_flag[meditating]>:
                - flag <[player]> meditating:!
                - narrate "<gray>You stop meditating." targets:<[player]>
                - define regen_amount 0.33
            
            # Normal regen
            - else:
                - define regen_amount 0.33
            
            # Store location for next check
            - flag <[player]> last_meditation_location:<[current_location]>
            
            # Get their max mana
            - define max_mana <[player].flag[stat.mana.max]||20>
            
            # Get their current mana
            - define current_mana <[player].flag[stat.mana.current]||<[max_mana]>>
            
            # Only regen if not at max
            - if <[current_mana]> < <[max_mana]>:
                - define new_mana <[current_mana].add[<[regen_amount]>].min[<[max_mana]>]>
                - flag <[player]> stat.mana.current:<[new_mana]>
        
        - wait 1s


prepare_spell_command:
    type: command
    name: prepare
    description: Prepare a spell for quick casting
    script:
    # Get the spell name
    - define spell_name <context.args.get[1]||null>
    
    # Check if they provided a spell
    - if <[spell_name]> == null:
        - narrate "<red>Usage: /prepare <spell_name>"
        - stop
    
    # Check if they know this spell
    - if <player.flag[known_spells].contains[<[spell_name]>].not>:
        - narrate "<red>You haven't learned that spell yet!"
        - stop
    
    # Check how many spells already prepared (max 9)
    - define prepared_list <player.flag[prepared_spells]||<list>>
    - if <[prepared_list].size> >= 9:
        - narrate "<red>You can only prepare 9 spells! Use /unprepare first."
        - stop
    
    # Check if already prepared
    - if <[prepared_list].contains[<[spell_name]>]>:
        - narrate "<yellow>That spell is already prepared!"
        - stop
    
    # Add to prepared list
    - flag <player> prepared_spells:->:<[spell_name]>
    
    # Get display name
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    
    # Show confirmation
    - narrate "<green>Prepared <[display]> in slot <[prepared_list].size.add[1]>"

spellbook_command:
    type: command
    name: spellbook
    description: Get your spellbook
    script:
    # Remove any existing spellbooks first (prevent dupes)
    - foreach <player.inventory.list_contents>:
        - if <[value].has_flag[spellbook]>:
            - take <[value]>
            - narrate "<yellow>Removed old spellbook."
    
    # Check if offhand is empty
    - if <player.item_in_offhand.material.name> != air:
        - narrate "<red>Your offhand must be empty to summon your spellbook!"
        - stop
    
    # Create the spellbook
    - define book <item[spellbook_item]>
    
    # Give directly to offhand
    - inventory set o:<[book]> d:<player.inventory> slot:offhand
    
    - narrate "<green>Your spellbook materializes in your offhand!"
    - playsound <player> block_enchantment_table_use pitch:1.5
    
    # MANUALLY trigger the transform (since inventory set doesn't fire swap event)
    - run transform_hotbar_task def:<player>


spellbook_item:
    type: item
    material: enchanted_book
    display name: <&b>Spellbook
    lore:
    - <&7>Your grimoire of magical knowledge
    flags:
        spellbook: true

        
# spellbook_transform_world:
#     type: world
#     debug: false
#     events:
#         on player right clicks block:
#         - narrate "<red>SIGIL RIGHT CLICK DETECTED!!!!"
#         - determine cancelled
#         # on player right clicks block with:spellbook_item:
#         # - if <player.item_in_offhand.has_flag[spellbook]>:
#         #     - determine cancelled
#         # When player swaps items to offhand
#         on player swaps items:
#         - if <context.offhand.has_flag[spellbook]>:
#             - wait 1t
#             - run transform_hotbar_task def:<player>
#         - else if <player.item_in_offhand.has_flag[spellbook]>:
#             - run restore_hotbar_task def:<player>
        
#         # RIGHT CLICK WITH SIGIL IN HAND (spellbook in offhand)
#         on player right clicks block with:item_flagged:spell_sigil:
#         - if <player.item_in_offhand.has_flag[spellbook]>:
#             - determine cancelled
#             - define spell_name <player.item_in_hand.flag[spell_name]>
#             - define target <player.target>
#             - run cast_spell_task def:<[spell_name]>|<player>|<[target]>
        
#         on player right clicks entity with:item_flagged:spell_sigil:
#         - if <player.item_in_offhand.has_flag[spellbook]>:
#             - determine cancelled
#             - define spell_name <player.item_in_hand.flag[spell_name]>
#             - run cast_spell_task def:<[spell_name]>|<player>|<context.entity>
        
#         # Prevent sigils from being moved/dropped
#         on player clicks item_flagged:spell_sigil in inventory:
#         - determine cancelled
        
#         on player drops item_flagged:spell_sigil:
#         - determine cancelled
        
#         # Cleanup on logout
#         on player quits:
#         - if <player.item_in_offhand.has_flag[spellbook]>:
#             - run restore_hotbar_task def:<player>
   

transform_hotbar_task:
    type: task
    definitions: player
    script:
    # Check if already transformed
    - if <[player].has_flag[hotbar_saved]>:
        - stop
    
    # Check if they have prepared spells
    - define prepared_list <[player].flag[prepared_spells]||<list>>
    - if <[prepared_list].is_empty>:
        - narrate "<red>No spells prepared! Use /prepare <spell>" targets:<[player]>
        - stop
    
    # Save current hotbar items (slots 1-9)
    - repeat 9:
        - define slot <[value]>
        - define item <[player].inventory.slot[<[slot]>]>
        - flag <[player]> saved_hotbar.<[slot]>:<[item]>
    
    # Mark as saved
    - flag <[player]> hotbar_saved:true
    
    # Clear hotbar
    - repeat 9:
        - inventory set o:air slot:<[value]>
    
    # Place spell sigils
    - define slot_num 1
    - foreach <[prepared_list]> as:spell_name:
        # Create sigil for this spell
        - define sigil <proc[create_spell_sigil_proc].context[<[spell_name]>|<[slot_num]>]>
        
        # Place in hotbar
        - inventory set o:<[sigil]> slot:<[slot_num]>
        
        - define slot_num <[slot_num].add[1]>
    
    # Feedback
    - narrate "<green>Spellbook activated! Press 1-9 to cast." targets:<[player]>
    - playsound <[player]> block_enchantment_table_use pitch:1.2

restore_hotbar_task:
    type: task
    definitions: player
    script:
    # Check if hotbar was saved
    - if <[player].has_flag[hotbar_saved].not>:
        - stop
    
    # Remove all spell sigils from hotbar
    - repeat 9:
        - define slot <[value]>
        - define item <[player].inventory.slot[<[slot]>]>
        - if <[item].has_flag[spell_sigil]>:
            - inventory set o:air slot:<[slot]>
    
    # Restore original items
    - repeat 9:
        - define slot <[value]>
        - define saved_item <[player].flag[saved_hotbar.<[slot]>]>
        - inventory set o:<[saved_item]> slot:<[slot]>
    
    # Clear saved data
    - flag <[player]> saved_hotbar:!
    - flag <[player]> hotbar_saved:!
    
    # Feedback
    - narrate "<gray>Spellbook stowed." targets:<[player]>
    - playsound <[player]> block_enchantment_table_use pitch:0.8

cast_spell_task:
    type: task
    definitions: spell_name|caster|target
    debug: false
    script:
    # Check if spell exists
    - if <script[spell_data].data_key[spells.<[spell_name]>]||null> == null:
        - narrate "<red>That spell doesn't exist!" targets:<[caster]>
        - stop
    
    # Check cooldown
    - if <[caster].has_flag[cooldown.<[spell_name]>]>:
        - define time_left <[caster].flag_expiration[cooldown.<[spell_name]>].from_now.formatted>
        - narrate "<red>Spell on cooldown! (<[time_left]> remaining)" targets:<[caster]>
        - stop
    
    # Get spell data
    - define mana_cost <script[spell_data].data_key[spells.<[spell_name]>.mana_cost]>
    - define base_damage <script[spell_data].data_key[spells.<[spell_name]>.base_damage]>
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    
    # Deduct mana (but don't go below 0)
    - define current_mana <[caster].flag[stat.mana.current]>
    - define new_mana <[current_mana].sub[<[mana_cost]>].max[0]>
    - flag <[caster]> stat.mana.current:<[new_mana]>
    
    # Calculate damage based on current mana
    - define mana_percent <[new_mana].div[<[caster].flag[stat.mana.max]>]>
    - define damage_multiplier <[mana_percent].sqrt>
    - define final_damage <[base_damage].mul[<[damage_multiplier]>]>
    
    # Check if they're targeting something valid
    - if <[target]> == null || <[target].is_living.not>:
        - narrate "<red>You must target a living entity!" targets:<[caster]>
        - flag <[caster]> stat.mana.current:+:<[mana_cost]>
        - stop
    
    # Deal the damage
    - hurt <[final_damage]> <[target]>
    
    # Visual feedback
    - narrate "<green>Cast <[display]>! <yellow><[final_damage].round_to[1]> damage <gray>(<[mana_cost]> mana | <[new_mana]> remaining)" targets:<[caster]>
    - playsound <[caster]> entity_blaze_shoot pitch:2
    
    # Set cooldown
    - define cooldown_time <script[spell_data].data_key[spells.<[spell_name]>.cooldown]>
    - flag <[caster]> cooldown.<[spell_name]> expire:<[cooldown_time]>s


reset_magic_command:
    type: command
    name: resetmagic
    description: Reset all magic system flags and items
    permission: magic.admin
    script:
    # Remove all spell sigils from inventory
    - foreach <player.inventory.list_contents>:
        - if <[value].has_flag[spell_sigil]>:
            - take <[value]>
    
    # Remove all spellbooks
    - foreach <player.inventory.list_contents>:
        - if <[value].has_flag[spellbook]>:
            - take <[value]>
    
    # Clear all magic flags
    - flag <player> known_spells:!
    - flag <player> prepared_spells:!
    - flag <player> saved_hotbar:!
    - flag <player> hotbar_saved:!
    - flag <player> current_spell_index:!
    - flag <player> stat.mana.current:!
    - flag <player> stat.mana.max:!
    - flag <player> stat.intelligence.level:!
    
    # Clear all cooldowns
    - flag <player> cooldown:!
    
    - narrate "<green>All magic systems reset!"


create_spell_sigil_proc:
    type: procedure
    definitions: spell_name|slot_number
    script:
    # Get display name
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    
    # For MVP: Use different materials as placeholders
    - define materials <list[red_dye|orange_dye|yellow_dye|lime_dye|light_blue_dye|blue_dye|purple_dye|magenta_dye|pink_dye]>
    - define material <[materials].get[<[slot_number]>]>
    
    # Create the sigil item
    - define sigil <item[<[material]>].with[display_name=<&b><[display]>;lore=<list[<&7>Slot <[slot_number]>]>].with_flag[spell_sigil:true].with_flag[spell_name:<[spell_name]>].with_flag[slot:<[slot_number]>]>
    
    - determine <[sigil]>