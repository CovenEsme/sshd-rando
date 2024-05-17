; Start using subsdk8 0x500 bytes into the .text section
; Please leave 0x1000 bytes for this landingpad

.offset 0x712e0a5500

; custom item gets
cmp w8, #0
b.eq handle_custom_item_get

; don't set AC boko flag on death
cmp w8, #1
b.eq 0x712e0a6500

; startflags
cmp w8, #2
b.eq handle_startflags

; set goddess sword pulled scene flag
cmp w8, #3
b.eq set_goddess_sword_pulled_story_flag

; freestanding item y offset
cmp w8, #4
b.eq fix_freestanding_item_y_offset

; fix sandship boat
cmp w8, #5
b.eq fix_sandship_boat

; handle er cases
cmp w8, #6
b.eq handle_er_cases

; handle er action states
cmp w8, #7
b.eq handle_er_action_states

; fix Sky Keep entrance
cmp w8, #8
b.eq set_stone_of_trials_placed_flag

; update day/night storyflag
cmp w8, #9
b.eq update_day_night_storyflag

cmp w8, #10
b.eq check_night_storyflag

cmp w8, #11
b.eq fix_sky_keep_exit

cmp w8, #12
b.eq check_bucha_local_sceneflag

cmp w8, #13
b.eq handle_crest_hit_give_item

cmp w8, #14
b.eq drop_arrows_bombs_seeds

cmp w8, #15
b.eq drop_nothing

cmp w8, #16
b.eq fix_item_get

cmp w8, #17
b.eq activation_checks_for_goddess_walls

cmp w8, #18
b.eq remove_timeshift_stone_cutscenes

cmp w8, #19
b.eq fix_light_pillars

cmp w8, #20
b.eq custom_event_commands

cmp w8, #21
b.eq warp_to_start

cmp w8, #22
b.eq update_crystal_count

cmp w8, #23
b.eq check_and_modify_item_actor

cmp w8, #24
b.eq npc_traps

cmp w8, #25
b.eq spawned_actor_traps

cmp w8, #26
b.eq fix_tbox_traps

cmp w8, #27
b.eq handle_effect_timers

cmp w8, #28
b.eq setup_traps

cmp w8, #29
b.eq give_squirrel_item

cmp w8, #30
b.eq should_spawn_eldin_platforms

cmp w8, #31
b.eq horwell_always_interactable

cmp w8, #32
b.eq rotate_freestanding_items

cmp w8, #33
b.eq fix_items_in_sand_piles

cmp w8, #34
b.eq init_appearing_chest_subtype

cmp w8, #35
b.eq spawn_appeared_chest

cmp w8, #36
b.eq hide_appearing_chest

cmp w8, #37
b.eq set_correct_boss_key_positions

cmp w8, #38
b.eq set_random_boss_key_positions

cmp w8, #39
b.eq prevent_minigame_death

cmp w8, #40
b.eq is_kikwi_found

cmp w8, #41
b.eq check_and_set_trial_completion_flag

cmp w8, #42
b.eq try_end_pumpkin_archery

cmp w8, #43
b.eq tgreact_spawn_custom_item

cmp w8, #44
b.eq academy_bell_give_custom_item

cmp w8, #45
b.eq after_item_collection_hook

cmp w8, #46
b.eq get_arc_model_from_item

cmp w8, #47
b.eq get_item_model_name_ptr

cmp w8, #48
b.eq change_model_scale

cmp w8, #49
b.eq main_loop_inject

cmp w8, #50
b.eq activate_back_in_time

cmp w8, #51
b.eq handle_closet_traps

cmp w8, #52
b.eq handle_bucha_traps

cmp w8, #53
b.eq handle_ac_boko_and_heartco_and_digspot_traps

cmp w8, #54
b.eq init_rainbow_colors

cmp w8, #55
b.eq check_stage_on_bucha_interaction

ret ; this should never be reached

; ends at 0x712e0a7000
