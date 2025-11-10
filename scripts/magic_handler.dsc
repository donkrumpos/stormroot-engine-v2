# ===================================
# PLAYER SETUP
# ===================================

setup_player_command:
    type: command
    name: magicsetup
    description: Sets up your magic stats
    script:
    - flag <player> stat.intelligence.level:10
    - define max_mana <player.flag[stat.intelligence.level].mul[2]>
    - flag <player> stat.mana.current:<[max_mana]>
    - flag <player> stat.mana.max:<[max_mana]>
    - narrate "<green>Magic initialized! INT: <player.flag[stat.intelligence.level]>, Mana: <player.flag[stat.mana.current]>/<player.flag[stat.mana.max]>"

# ===================================
# SPELL LEARNING
# ===================================

learn_spell_command:
    type: command
    name: learn
    description: Learn a spell
    script:
    - define spell_name <context.args.get[1]||null>
    
    - if <[spell_name]> == null:
        - narrate "<red>Usage: /learn <spell_name>"
        - stop
    
    - if <script[spell_data].data_key[spells.<[spell_name]>]||null> == null:
        - narrate "<red>That spell doesn't exist!"
        - stop
    
    - flag <player> known_spells:->:<[spell_name]>
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    - narrate "<green>You have learned: <[display]>!"

# ===================================
# SPELL PREPARATION
# ===================================

prepare_spell_command:
    type: command
    name: prepare
    description: Prepare a spell for quick casting
    script:
    - define spell_name <context.args.get[1]||null>
    
    - if <[spell_name]> == null:
        - narrate "<red>Usage: /prepare <spell_name>"
        - stop
    
    - if <player.flag[known_spells].contains[<[spell_name]>].not>:
        - narrate "<red>You haven't learned that spell yet!"
        - stop
    
    - define prepared_list <player.flag[prepared_spells]||<list>>
    - if <[prepared_list].size> >= 9:
        - narrate "<red>You can only prepare 9 spells!"
        - stop
    
    - if <[prepared_list].contains[<[spell_name]>]>:
        - narrate "<yellow>That spell is already prepared!"
        - stop
    
    - flag <player> prepared_spells:->:<[spell_name]>
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    - narrate "<green>Prepared <[display]> in slot <[prepared_list].size.add[1]>"

# ===================================
# SPELLBOOK
# ===================================

spellbook_command:
    type: command
    name: spellbook
    description: Get your spellbook
    script:
    - foreach <player.inventory.list_contents>:
        - if <[value].has_flag[spellbook]>:
            - take <[value]>
    
    - if <player.item_in_offhand.material.name> != air:
        - narrate "<red>Your offhand must be empty!"
        - stop
    
    - define book <item[spellbook_item]>
    - inventory set o:<[book]> d:<player.inventory> slot:offhand
    - narrate "<green>Spellbook equipped!"

spellbook_item:
    type: item
    material: knowledge_book
    display name: <&b>Spellbook
    lore:
    - <&7>Your grimoire of magical knowledge
    flags:
        spellbook: true

# ===================================
# CASTING SYSTEM
# ===================================

cast_spell_task:
    type: task
    definitions: spell_name|caster|target
    debug: false
    script:
    - if <script[spell_data].data_key[spells.<[spell_name]>]||null> == null:
        - narrate "<red>That spell doesn't exist!" targets:<[caster]>
        - stop
    
    - if <[caster].has_flag[cooldown.<[spell_name]>]>:
        - define time_left <[caster].flag_expiration[cooldown.<[spell_name]>].from_now.formatted>
        - narrate "<red>Spell on cooldown! (<[time_left]>)" targets:<[caster]>
        - stop
    
    - define mana_cost <script[spell_data].data_key[spells.<[spell_name]>.mana_cost]>
    - define base_damage <script[spell_data].data_key[spells.<[spell_name]>.base_damage]>
    - define display <script[spell_data].data_key[spells.<[spell_name]>.display_name]>
    
    - define current_mana <[caster].flag[stat.mana.current]>
    - define new_mana <[current_mana].sub[<[mana_cost]>].max[0]>
    - flag <[caster]> stat.mana.current:<[new_mana]>
    
    - define mana_percent <[new_mana].div[<[caster].flag[stat.mana.max]>]>
    - define damage_multiplier <[mana_percent].sqrt>
    - define final_damage <[base_damage].mul[<[damage_multiplier]>]>
    
    - if <[target]> == null || <[target].is_living.not>:
        - narrate "<red>You must target a living entity!" targets:<[caster]>
        - flag <[caster]> stat.mana.current:+:<[mana_cost]>
        - stop
    
    - hurt <[final_damage]> <[target]>
    - narrate "<green>Cast <[display]>! <yellow><[final_damage].round_to[1]> damage <gray>(<[new_mana]> mana)" targets:<[caster]>
    - playsound <[caster]> entity_blaze_shoot pitch:2
    
    - define cooldown_time <script[spell_data].data_key[spells.<[spell_name]>.cooldown]>
    - flag <[caster]> cooldown.<[spell_name]> expire:<[cooldown_time]>s

simple_cast_world:
    type: world
    debug: false
    events:
        on player right clicks block:
        - if <player.item_in_hand.material.name> == air:
            - if <player.item_in_offhand.has_flag[spellbook]>:
                - determine cancelled
                - define slot <player.held_item_slot>
                - define prepared_list <player.flag[prepared_spells]||<list>>
                
                - if <[prepared_list].size> >= <[slot]>:
                    - define spell_name <[prepared_list].get[<[slot]>]>
                    - define target <player.target>
                    - run cast_spell_task def:<[spell_name]>|<player>|<[target]>
        
        on player right clicks entity:
        - if <player.item_in_hand.material.name> == air:
            - if <player.item_in_offhand.has_flag[spellbook]>:
                - determine cancelled
                - define slot <player.held_item_slot>
                - define prepared_list <player.flag[prepared_spells]||<list>>
                
                - if <[prepared_list].size> >= <[slot]>:
                    - define spell_name <[prepared_list].get[<[slot]>]>
                    - run cast_spell_task def:<[spell_name]>|<player>|<context.entity>

# ===================================
# MANA REGENERATION
# ===================================

mana_regen_world:
    type: world
    debug: false
    events:
        on delta time secondly:
        - define per_second 5
        - define wait_time <element[1].div[<[per_second]>]>
        - repeat <[per_second]>:
            - foreach <server.online_players> as:player:
                - run mana_tick_task def:<[player]>
            - wait <[wait_time]>

mana_tick_task:
    type: task
    definitions: player
    debug: false
    script:
    - define last_location <[player].flag[last_meditation_location]||null>
    - define current_location <[player].location.simple>
    
    - if <[player].is_sneaking> && <[last_location]> == <[current_location]>:
        - if <[player].has_flag[meditating].not>:
            - flag <[player]> meditating
            - narrate "<aqua>You begin to meditate..." targets:<[player]>
        - define regen_amount 1.0
    - else if <[player].has_flag[meditating]>:
        - flag <[player]> meditating:!
        - narrate "<gray>You stop meditating." targets:<[player]>
        - define regen_amount 0.33
    - else:
        - define regen_amount 0.33
    
    - flag <[player]> last_meditation_location:<[current_location]>
    
    - define max_mana <[player].flag[stat.mana.max]||20>
    - define current_mana <[player].flag[stat.mana.current]||<[max_mana]>>
    
    - if <[current_mana]> < <[max_mana]>:
        - define new_mana <[current_mana].add[<[regen_amount]>].min[<[max_mana]>]>
        - flag <[player]> stat.mana.current:<[new_mana]>