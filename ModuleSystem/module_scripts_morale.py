from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from ID_troops import *
from ID_factions import *
from module_troops import *

from module_info import wb_compile_switch as is_a_wb_script

# This file contains a heavily modified and improved version
# of Chel's morale scripts. If you modify it, please leave a 
# note telling what you did. -CC

morale_scripts = [
	
	# script_cf_correct_party_icon
	# This script sets an icon of a party relative to it's faction
	# param0 = party_id
	("cf_correct_party_icon",
	[
		(store_script_param, ":party_id", 1),
		(gt, ":party_id", -1),
		(store_faction_of_party, ":faction", ":party_id"),
		#(party_get_num_companions, ":size", ":party_id"),
		(assign, ":icon", icon_orc),
		#(assign, ":icon_med", icon_orc),
		#(assign, ":icon_big", icon_orc),
		(try_begin),
			(eq, ":faction", "fac_gondor"),
			(assign, ":icon", icon_footman_gondor),
		(else_try),
			(eq, ":faction", "fac_dwarf"),
			(assign, ":icon", icon_dwarf),
		(else_try),
			(eq, ":faction", "fac_rohan"),
			(assign, ":icon", icon_knight_rohan),
		(else_try),
			(eq, ":faction", "fac_lorien"),
			(assign, ":icon", icon_lorien_elf_a),
		(else_try),
			(eq, ":faction", "fac_imladris"),
			(assign, ":icon", icon_rivendell_elf),
		(else_try),
			(eq, ":faction", "fac_woodelf"),
			(assign, ":icon", icon_mirkwood_elf),
		(else_try),
			(eq, ":faction", "fac_dale"),
			(assign, ":icon", icon_generic_knight),
		(else_try),
			(eq, ":faction", "fac_harad"),
			(assign, ":icon", icon_harad_horseman),
		(else_try),
			(eq, ":faction", "fac_rhun"),
			(assign, ":icon", icon_easterling_horseman),
		(else_try),
			(eq, ":faction", "fac_khand"),
			(assign, ":icon", icon_cataphract),
		(else_try),
			(eq, ":faction", "fac_umbar"),
			(assign, ":icon", icon_umbar_corsair),
		(else_try),
			(eq|this_or_next, ":faction", "fac_isengard"),
			(eq|this_or_next, ":faction", "fac_mordor"),
			(eq|this_or_next, ":faction", "fac_guldur"),
			(eq|this_or_next, ":faction", "fac_moria"),
			(eq, ":faction", "fac_gundabad"),
			(assign, ":icon", icon_orc),
		(else_try),
			(eq, ":faction", "fac_dunland"),
			(assign, ":icon", icon_dunlander),
		(else_try),
			(eq, ":faction", "fac_beorn"),
			(assign, ":icon", icon_axeman),
		(try_end),
		(party_set_icon, ":party_id", ":icon"),
	]),

	# script_cf_agent_get_tier_morale
	# This script stores the agents tier morale based on level in reg0.
	# param0 = agent
	("cf_agent_get_tier_morale",
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, 0),
		(agent_get_troop_id,":troop", ":agent_no"),
		(store_character_level, ":level", ":troop"),	
		(try_begin),
			(is_between, ":level", 0, 7),
			(assign, reg0, 3),
		(else_try),
			(is_between, ":level", 7, 15),
			(assign, reg0, 6),
		(else_try),
			(is_between, ":level", 15, 23),
			(assign, reg0, 12),
		(else_try),
			(is_between, ":level", 23, 32),
			(assign, reg0, 18),
		(else_try),
			(assign, reg0, 25),
		(try_end),
	]),

	# script_cf_agent_get_leader
	# This script finds an agent's leader (heroes only), and stores his agent id in reg0. reg0 is set to -1 if
	# there is no hero leader.
	# param0 = agent
	("cf_agent_get_leader", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_party_id, ":party_no", ":agent_no"),
		(ge, ":party_no", 0),
		(party_stack_get_troop_id, ":troop", ":party_no", 0),
		(assign, ":continue", 1),
		(try_for_agents, ":cur_agent"),
			(eq, ":continue", 1),
			(agent_is_human, ":cur_agent"),
			(agent_get_troop_id, ":troop_no", ":cur_agent"),
			(troop_is_hero, ":troop"),
			(eq, ":troop", ":troop_no"),
			(assign, reg0, ":cur_agent"),
			(assign, ":continue", 0),
		(try_end),
	]),

	# script_cf_agent_get_leader_troop
	# This script finds an agent's leader, and stores his troop id in reg0.
	# param0 = agent
	("cf_agent_get_leader_troop", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_party_id, ":party_no", ":agent_no"),
		(gt, ":party_no", -1),
		(party_stack_get_troop_id, ":troop", ":party_no", 0),
		(try_begin),
			(troop_is_hero, ":troop"),
			(assign, reg0, ":troop"),
		(try_end),
	]),

	# script_cf_agent_get_faction
	# This script finds an agent's faction, and stores it in reg0.
	# param0 = agent
	("cf_agent_get_faction", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, -1),
		(ge, ":agent_no", 0),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(store_troop_faction, ":faction", ":troop_no"),
		(assign, reg0, ":faction"),
	]),

	# script_cf_agent_get_morale
	# This script calculates an agents morale, and stores it in reg1.
	# param0 = agent
	("cf_agent_get_morale", 
	[
		(store_script_param, ":agent_no", 1),
		(ge, ":agent_no", 0),
		(agent_get_class, ":class", ":agent_no"),
		(store_agent_hit_points,":hitpoints",":agent_no",0),
		(agent_get_troop_id,":troop_type", ":agent_no"),
		(troop_get_type, ":race", ":troop_type"),
		(store_character_level, ":troop_level", ":troop_type"),	
		(assign, ":leader", 0),
		(try_begin),
			(call_script, "script_cf_agent_get_leader_troop", ":agent_no"),
			(gt, reg0, -1),
			(store_skill_level,":leader","skl_leadership",reg0),
		(try_end),
		(val_div,":troop_level", 10),
        (val_div,":hitpoints", 2),
        (assign,reg1,100),		
                    
        (val_sub,reg1,":hitpoints"),
        (val_sub,reg1,":leader"),
        (val_sub,reg1,":troop_level"),

		(try_begin), # Ents, spies and berserkers don't flee.
			(eq|this_or_next, ":troop_type", "trp_ent"),
			(eq|this_or_next, ":troop_type", "trp_spy"),
			(eq|this_or_next, ":troop_type", "trp_spy_evil"),
			(eq|this_or_next, ":troop_type", "trp_spy_partner"),
			(eq|this_or_next, ":troop_type", "trp_spy_partner_evil"),
			(eq|this_or_next, ":troop_type", "trp_i5_beorning_carrock_berserker"),
			(eq|this_or_next, ":troop_type", "trp_i5_khand_pit_master"),
			(is_between|this_or_next, ":troop_type", "trp_moria_troll", "trp_multiplayer_profile_troop_male"), #Kham - Trolls do not flee.
			(eq, ":troop_type", "trp_i6_isen_uruk_berserker"),
			(assign, reg1, -100),
		(else_try), # Wargs more likely to flee
			(is_between, ":troop_type", warg_ghost_begin, warg_ghost_end),
			(agent_get_horse, ":horse_no", ":agent_no"),
			(assign, reg1, 0),
			(try_begin),
				(ge, ":horse_no", 0),
				(assign, reg1, 100),
				(store_agent_hit_points,":hitpoints",":horse_no",0),
				(val_sub, reg1, ":hitpoints"),
			(try_end),
		(else_try), #Troll and quest parties never flee
			(agent_get_party_id, ":party_no", ":agent_no"),
			(party_is_active, ":party_no"),  # Kham - added a validator to check
			(party_get_template_id, ":template", ":party_no"),
			(eq|this_or_next, ":template", "pt_wild_troll"),
			(eq, ":template", "pt_raging_trolls"),
			(assign, reg1, -100),
		(else_try),
		
		# #Map Morale Bonus / penalty - Kham #disabled, party morale now affects coherence instead
		
		# (try_begin),
			# (agent_get_party_id, ":party_no", ":agent_no"),
			# (eq, ":party_no", "p_main_party"), #Only for Player Troops, so there are less AI routing.
			# (ge, ":party_no", 0),
			# (party_get_morale, ":map_morale", ":party_no"),
			# (try_begin),
				# (ge, ":map_morale", 75),
				# (val_sub, reg1, 15),
			# (else_try),
				# (is_between, ":map_morale", 50, 75),
				# (val_sub, reg1, 10),
			# (else_try),
				# (is_between, ":map_morale", 25, 50),
				# (val_add, reg1, 5),
			# (else_try),
				# (lt, ":map_morale", 25),
				# (val_add, reg1, 10),
			# (try_end),
		# (try_end),


    # Coherence bonus / penalty (Invain)
        (try_begin),
            (agent_is_ally, ":agent_no"),
            (assign, ":coherence", "$allies_coh"),
        (else_try),
            (assign, ":coherence", "$enemies_coh"),
        (try_end),
        
        (val_sub, ":coherence", 50), #coherence below increases chance of fleeing
        (val_sub, reg1, ":coherence"),
        

		# leader bonuses -CC
		(try_begin),
			(call_script, "script_cf_agent_get_leader", ":agent_no"),
			(gt, reg0, -1),
			(try_begin),
				(eq|this_or_next, ":race", tf_evil_man),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_important),
			(else_try),
				(eq|this_or_next, ":race", tf_gondor),
				(eq, ":race", tf_dunland),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_bonus),
			(else_try),
				(eq, ":race", tf_dwarf),
				(agent_is_alive|neg, reg0),
				(val_sub, reg1, tld_morale_leader_avenge),
			(else_try),
				(eq, ":race", tf_urukhai),
				(agent_is_alive|neg, reg0),
				(val_sub, reg1, tld_morale_leader_urukhai),
			(else_try),
				(agent_is_alive, reg0),
				(val_sub, reg1, tld_morale_leader_average),
			(try_end),
		(try_end),
	
		# What are the variables for enemy formations? -CC
		(assign, ":formation", formation_none),
		(try_begin),
			(agent_is_ally, ":agent_no"),
			(try_begin),
				(eq, ":class", grc_infantry),
				(assign, ":formation", "$infantry_formation_type"),
			(else_try),
				(eq, ":class", grc_archers),
				(assign, ":formation", "$archer_formation_type"),
			(else_try),
				(eq, ":class", grc_cavalry),
				(assign, ":formation", "$cavalry_formation_type"),
				(val_sub, reg1, 5), # slight bonus for cavalry units, a horse makes you a bit more bold. -CC
			(try_end),
		(try_end),

		# Formation bonuses. -CC
		(try_begin),
			(eq|this_or_next, ":race", tf_gondor),
			(eq|this_or_next, ":race", tf_male),
			(eq, ":race", tf_dunland),
			(gt, ":formation", formation_none),
			(val_sub, reg1, tld_morale_formation_bonus),
		(try_end),

		# Race bonuses / penalties. -CC
		(try_begin),
			(eq, ":race", tf_orc),
			(val_sub, reg1, tld_morale_poor),
		(else_try),
			(eq|this_or_next, ":race", tf_rohan),
			(eq, ":race", tf_dunland),
			(val_sub, reg1, tld_morale_average),
		(else_try),
			(eq|this_or_next, ":race", tf_male),
			(eq|this_or_next, ":race", tf_female),
			(eq|this_or_next, ":race", tf_gondor),
			(eq|this_or_next, ":race", tf_lorien),
			(eq|this_or_next, ":race", tf_woodelf),
			(eq, ":race", tf_uruk),
			(val_sub, reg1, tld_morale_good),
		(else_try),
			(eq|this_or_next, ":race", tf_imladris),
			(eq|this_or_next, ":race", tf_urukhai),
			(eq|this_or_next, ":race", tf_harad),
			(eq|this_or_next, ":race", tf_dwarf),
			(eq, ":race", tf_evil_man),
			(val_sub, reg1, tld_morale_very_good),
		(else_try),
			(val_sub, reg1, tld_morale_average),
		(try_end),

		# Nazgul modifier -CC
		(try_begin),
			(gt, "$nazgul_in_battle", 0),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_begin),
				(teams_are_enemies, ":team_a", "$nazgul_team"),
				(store_mul, ":nazgul_modifier", "$nazgul_in_battle", 20),
				(val_add, reg1, ":nazgul_modifier"),
			(else_try),
				(store_mul, ":nazgul_modifier", "$nazgul_in_battle", 20),
				(val_sub, reg1, ":nazgul_modifier"),
			(try_end),
		(try_end),

		# faction bonuses. (mostly for easterlings: khand and haradrim). -CC
		(try_begin),
			(call_script, "script_cf_agent_get_faction", ":agent_no"),
			(gt, reg0, -1),
			(try_begin),
				(eq|this_or_next, reg0, fac_harad),
				(eq, reg0, fac_khand),
				(val_sub, reg1, tld_morale_bonus_easterlings),
			(else_try),
				(eq|this_or_next, reg0, fac_lorien), # Elves get a morale boost
				(eq|this_or_next, reg0, fac_imladris),
				(eq, reg0, fac_woodelf),
				(val_sub, reg1, tld_morale_bonus_elves), 
			(try_end),
		(try_end),
		
		# Rallied agents are 20% less likely to flee. #InVain: We use that slot for storing the general agent morale modifier instead, allows much more flexibility
		# (try_begin),
			# (agent_slot_eq, ":agent_no", slot_agent_morale_modifier, 1),
			# (val_sub, reg1, 20),
		# (try_end),
        
        #agent morale modifier (affected by ingame events)
        (agent_get_slot, ":morale_modifier", ":agent_no", slot_agent_morale_modifier),
        (val_sub, reg1, ":morale_modifier"),
        
        #normalise it with every check
        (val_mul, ":morale_modifier", 2),
        (val_div, ":morale_modifier", 3),
        (agent_set_slot, ":agent_no", slot_agent_morale_modifier, ":morale_modifier"),

		# Tier morale
		(call_script, "script_cf_agent_get_tier_morale", ":agent_no"),
			(val_sub, reg1, reg0),		
		(try_end),

		(try_begin),
			(call_script, "script_count_ally_agents_around_agent", ":agent_no", 600),
			(store_mul, ":morale_bonus", reg0, 3),
			(val_sub, reg1, ":morale_bonus"),
		(try_end),


	]),

	# script_cf_spawn_routed_parties
	# This script spawns the routed parties nearby the player OR if there already is a routed party nearby,
	# it adds the routed troops to them.
	("cf_spawn_routed_parties", 
	[
		# Clear the parties if the morale option has been turned off.
		(try_begin),
			(eq, "$tld_option_morale", 0),
			(party_clear, "p_routed_troops"),
			(party_clear, "p_routed_allies"),
			(party_clear, "p_routed_enemies"),
			(assign, "$g_spawn_allies_routed", 0),
			(assign, "$g_spawn_enemies_routed", 0),
		(try_end),

		(try_begin),
			(neq, 0, cheat_switch),
			(party_get_num_companions, reg10, "p_routed_troops"),
			(party_get_num_companions, reg11, "p_routed_allies"),
			(party_get_num_companions, reg12, "p_routed_enemies"),
			#(display_message, "@DEBUG: Routed Troops: {reg10}, Routed Allies: {reg11}, Routed Enemies: {reg12}"),
			(assign, reg10, "$g_spawn_allies_routed"),
			(assign, reg11, "$g_spawn_enemies_routed"),
			#(display_message, "@DEBUG: Spawn Allies: {reg10}, Spawn Enemies: {reg11}"),
		(try_end),

		# Clear the parties if the total count is greater/equal to than the maximum.
		(try_begin),
			(assign, ":total_parties", 0),
      			(try_for_parties, ":unused"),
        			(val_add, ":total_parties", 1),
      			(try_end),
      			(ge, ":total_parties", "$tld_option_max_parties"),
			(assign, "$g_spawn_allies_routed", 0),
			(assign, "$g_spawn_enemies_routed", 0),
			(party_clear, "p_routed_troops"),
			(party_clear, "p_routed_allies"),
			(party_clear, "p_routed_enemies"),
		(try_end),

		(eq, "$tld_option_morale", 1),

		# Don't spawn parties with less than 75% of player's party size. -CC
		# these values can be edited in module_constants.py
		(party_get_num_companions, reg3, "p_main_party"),
		(val_mul, reg3, tld_rout_party_spawn_ratio_numerator),
		(val_div, reg3, tld_rout_party_spawn_ratio_denominator),

		# Clear empty parties
		(try_begin),
			(party_get_num_companions, ":size_us", "p_routed_troops"),
			(party_get_num_companions, ":size_allies", "p_routed_allies"),
			(store_add, ":total_size", ":size_us", ":size_allies"),
			(le, ":total_size", 0),
			(party_clear, "p_routed_troops"),
			(party_clear, "p_routed_allies"),
			(assign, "$g_spawn_enemies_routed", 0),
		(try_end),
		(try_begin),
			(party_get_num_companions, ":size_enemy", "p_routed_enemies"),
			(lt|this_or_next, ":size_enemy", reg3),
			(le, ":size_enemy", 0),
			(party_clear, "p_routed_enemies"),
			(assign, "$g_spawn_enemies_routed", 0),
		(try_end),
		(try_begin),
			(eq, "$g_spawn_allies_routed", 1),
			(try_begin),
				(assign, ":target_party", 0),
				(assign, ":found_party", 0),
      				(try_for_parties, ":cur_party"),
      				(party_is_active, ":cur_party"),
					(neq, ":found_party", 1),
					(party_get_template_id, ":template", ":cur_party"),
					(eq, ":template", "pt_routed_allies"),
					(store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_party"),
					(lt, ":dist", 8),
					(assign, ":target_party", ":cur_party"),
					(assign, ":found_party", 1),
      				(try_end),
				(eq, ":found_party", 1),
				(call_script, "script_party_add_party", ":target_party", "p_routed_troops"),
				(call_script, "script_party_add_party", ":target_party", "p_routed_allies"),
				(party_clear, "p_routed_troops"),
				(party_clear, "p_routed_allies"),
				(assign, "$g_spawn_allies_routed", 0),
			(else_try),
				(assign, ":total_parties", 0),
      				(try_for_parties, ":unused"),
        				(val_add, ":total_parties", 1),
      				(try_end),
      				(le, ":total_parties", "$tld_option_max_parties"),
				
				
				(set_spawn_radius, 3),
            			(spawn_around_party, "p_main_party", "pt_routed_allies"),

            			
            			(assign, ":routed_party", reg0),
				(call_script, "script_party_add_party", ":routed_party", "p_routed_troops"),
				(call_script, "script_party_add_party", ":routed_party", "p_routed_allies"),
				(party_stack_get_troop_id, ":troop", ":routed_party", 0),
				(store_troop_faction, ":faction", ":troop"),
				(party_set_faction, ":routed_party", ":faction"),
				(try_begin),
					(call_script, "script_cf_correct_party_icon", ":routed_party"),
				(try_end),
				(assign, ":max_dist", 99999),
				(assign, ":target_center", -1),	
				(try_for_range, ":cur_center", centers_begin, centers_end),
					(is_between, ":faction", kingdoms_begin, kingdoms_end),
					(party_is_active, ":cur_center"),
		     			(party_slot_eq, ":cur_center", slot_center_destroyed, 0),
		     			(party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
					(store_distance_to_party_from_party, ":dist", ":routed_party", ":cur_center"),
					(lt, ":dist", ":max_dist"),
					(store_faction_of_party, ":party_faction", ":cur_center"),
					(faction_get_slot, ":faction_side", ":faction", slot_faction_side),
					(faction_slot_eq,":party_faction",slot_faction_side,":faction_side"),
					(assign, ":target_center", ":cur_center"),
					(assign, ":max_dist", ":dist"),
				(try_end),
				(try_begin),
					(gt, ":target_center", -1),
					(party_set_ai_behavior, ":routed_party", ai_bhvr_travel_to_party),
					(party_set_ai_object, ":routed_party", ":target_center"),
					(party_set_slot, ":routed_party", slot_party_ai_state, spai_undefined),
					(party_set_slot, ":routed_party", slot_party_ai_object, ":target_center"),
					(party_set_flags, ":routed_party", pf_default_behavior, 1), #kham - fix						
				(try_end),	
				(party_clear, "p_routed_troops"),
				(party_clear, "p_routed_allies"),
				(assign, "$g_spawn_allies_routed", 0),
			(try_end),
		(try_end),
	
		(try_begin),
			(eq, "$g_spawn_enemies_routed", 1),
			(try_begin),
				(assign, ":target_party", 0),
				(assign, ":found_party", 0),
      				(try_for_parties, ":cur_party"),
      				(party_is_active, ":cur_party"),
					(neq, ":found_party", 1),
					(party_get_template_id, ":template", ":cur_party"),
					(eq, ":template", "pt_routed_enemies"),
					(store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_party"),
					(lt, ":dist", 8),
					(assign, ":target_party", ":cur_party"),
					(assign, ":found_party", 1),
      				(try_end),
				(eq, ":found_party", 1),
				(call_script, "script_party_add_party", ":target_party", "p_routed_enemies"),
				(party_clear, "p_routed_enemies"),
				(assign, "$g_spawn_enemies_routed", 0),
			(else_try),
				(assign, ":total_parties", 0),
      				(try_for_parties, ":unused"),
        				(val_add, ":total_parties", 1),
      				(try_end),
      				(le, ":total_parties", "$tld_option_max_parties"),
				(eq, "$g_spawn_enemies_routed", 1),
				
				

				(set_spawn_radius, 3),
            			(spawn_around_party, "p_main_party", "pt_routed_enemies"),

            			
            			(assign, ":routed_party", reg0),
            			(party_set_slot, ":routed_party", slot_party_commander_party, -1), #Kham - fix
				(call_script, "script_party_add_party", ":routed_party", "p_routed_enemies"),
				(party_stack_get_troop_id, ":troop", ":routed_party", 0),
				(store_troop_faction, ":faction", ":troop"),
				(store_relation, ":relation", ":faction", "$players_kingdom"),
				(try_begin),
					(lt, ":relation", 0),
					(party_set_faction, ":routed_party", ":faction"),
				(else_try),
					(party_set_faction, ":routed_party", "$g_encountered_party_faction"),	
				(try_end),
				(try_begin),
					(call_script, "script_cf_correct_party_icon", ":routed_party"),
				(try_end),
				(assign, ":max_dist", 99999),
				(assign, ":target_center", -1),	
				(try_for_range, ":cur_center", centers_begin, centers_end),
					(is_between, ":faction", kingdoms_begin, kingdoms_end),
					(party_is_active, ":cur_center"),
		     			(party_slot_eq, ":cur_center", slot_center_destroyed, 0),
		     			(party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
					(store_distance_to_party_from_party, ":dist", ":routed_party", ":cur_center"),
					(lt, ":dist", ":max_dist"),
					(store_faction_of_party, ":party_faction", ":cur_center"),
					(faction_get_slot, ":faction_side", ":faction", slot_faction_side),
					(faction_slot_eq,":party_faction",slot_faction_side,":faction_side"),
					(assign, ":target_center", ":cur_center"),
					(assign, ":max_dist", ":dist"),
				(try_end),
				(try_begin),
					(gt, ":target_center", -1),
					(party_set_ai_behavior, ":routed_party", ai_bhvr_travel_to_party),
					(party_set_ai_object, ":routed_party", ":target_center"),
					(party_set_slot, ":routed_party", slot_party_ai_state, spai_undefined),
					(party_set_slot, ":routed_party", slot_party_ai_object, ":target_center"),	
					(party_set_flags, ":routed_party", pf_default_behavior, 1), #kham - fix			
				(try_end),				
				(party_clear, "p_routed_enemies"),
				(assign, "$g_spawn_enemies_routed", 0),
			(try_end),
		(try_end),
	]),

	# script_count_ally_agents_around_agent
	# This script checks an agent for being surrounded by allied agents, reg0 stores the number of agents
	# param1: agent to check; param2: max_distance
	("count_ally_agents_around_agent", 
	[
		(store_script_param, ":agent_no", 1),
		(store_script_param, ":distance", 2),
		(assign, reg0, 0),
		(try_begin),
			(ge, ":agent_no", 0),
			(agent_get_position, pos1, ":agent_no"),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_for_agents, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_is_alive, ":cur_agent"),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos1, pos2),
				(lt, ":dist", ":distance"),
				(agent_get_team, ":team_b", ":cur_agent"),
				(neg|teams_are_enemies, ":team_a", ":team_b"),
				(val_add, reg0, 1),
			(try_end),
		(try_end),
	]),

	# script_count_enemy_agents_around_agent
	# This script checks an agent for being surrounded by enemy agents, reg0 stores the number of agents
	# param1: agent to check; param2: max_distance
	("count_enemy_agents_around_agent", 
	[
		(store_script_param, ":agent_no", 1),
		(store_script_param, ":distance", 2),
		(assign, reg0, 0),
		(try_begin),
			(ge, ":agent_no", 0),
			(agent_get_position, pos1, ":agent_no"),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_for_agents, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_is_alive, ":cur_agent"),
				(agent_get_position, pos2, ":cur_agent"),
				(get_distance_between_positions, ":dist", pos1, pos2),
				(lt, ":dist", ":distance"),
				(agent_get_team, ":team_b", ":cur_agent"),
				(teams_are_enemies, ":team_a", ":team_b"),
				(val_add, reg0, 1),
			(try_end),
		(try_end),
	]),

	# script_count_dead_ally_agents
	# This script checks for dead allied agents
	# param1: agent to check;
	("count_dead_ally_agents", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, 0),
		(try_begin),
			(ge, ":agent_no", 0),
			(agent_get_position, pos1, ":agent_no"),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_for_agents, ":cur_agent"),
				(agent_is_human, ":cur_agent"),
				(agent_is_alive|neg, ":cur_agent"),
				(agent_get_team, ":team_b", ":cur_agent"),
				(teams_are_enemies|neg, ":team_a", ":team_b"),
				(val_add, reg0, 1),
			(try_end),
		(try_end),
	]),

	# script_count_agents
	# This script counts an agent's enemies, and his allies
	# param1: agent to check; param2: max_distance
	# Output: reg0 = allies, reg1 = enemies
	("count_team_agents", 
	[
		(store_script_param, ":agent_no", 1),
		(assign, reg0, 0),
		(assign, reg1, 0),
		(try_begin),
			(ge, ":agent_no", 0),
			(agent_get_team, ":team_a", ":agent_no"),
			(try_for_agents, ":cur_agent"),
				(agent_get_team, ":team_b", ":cur_agent"),
				(try_begin),
					(teams_are_enemies, ":team_a", ":team_b"),
					(val_add, reg1, 1),
				(else_try),
					(val_add, reg0, 1),
				(try_end),
			(try_end),
		(try_end),
	]),
	# script_remove_agent_from_field
	# This script removes an agent from a battle and adds it to a routed party.
	# param1: agent to remove
	("remove_agent_from_field", 
	[
		(store_script_param, ":agent_no", 1),
		(agent_get_troop_id, ":troop_no", ":agent_no"),

		# Does agent have a horse? -CC
		(agent_get_horse, ":horse_no", ":agent_no"),

		# If so, remove it. -CC
		(try_begin),
			(ge, ":horse_no", 0),
			(call_script, "script_remove_agent", ":horse_no"),	
		(try_end),

		(try_begin),
			# Tell the player when a hero has left the battle. -CC
			(troop_is_hero, ":troop_no"),
      			(str_store_troop_name, s1, ":troop_no"),
			(assign, ":news_color", color_good_news),
			(try_begin),
        			(agent_is_ally, ":agent_no"),
				(assign, ":news_color", color_bad_news),
			(try_end),
			(display_message, "@{s1} has fled the battle!", ":news_color"),
			(agent_set_slot, ":agent_no", slot_agent_routed, 2),
			(call_script, "script_remove_agent", ":agent_no"),
		(else_try),
			# If the troop is not a hero and not a riderless warg, add it to a temp party. -CC
			(is_between|neg, ":troop_no", warg_ghost_begin, warg_ghost_end),
			(try_begin),
				(agent_is_ally, ":agent_no"),				
				(agent_get_party_id, ":party_no", ":agent_no"),
				(agent_get_kill_count, ":agent_killed", ":agent_no"),
				(agent_get_kill_count, ":agent_wounded", ":agent_no", 1),
				(agent_set_slot, ":agent_no", slot_agent_routed, 2),
				(call_script, "script_remove_agent", ":agent_no"),
				(agent_get_kill_count, ":agent_killed_2", ":agent_no"),
				(agent_get_kill_count, ":agent_wounded_2", ":agent_no", 1),
				(try_begin),
					# agent was killed
					(gt, ":agent_killed_2", ":agent_killed"),
			        	(try_begin),
						(eq, ":party_no", "p_main_party"),
						(party_add_members, "p_routed_troops", ":troop_no", 1),
					(else_try),
						(party_add_members, "p_routed_allies", ":troop_no", 1),
					(try_end),
					(assign, "$g_spawn_allies_routed", 1),
				(else_try),
					# agent was wounded
					(gt, ":agent_wounded_2", ":agent_wounded"),
					(party_remove_members,":party_no",":troop_no", 1),
			        	(try_begin),
						(eq, ":party_no", "p_main_party"),
						(party_add_members, "p_routed_troops", ":troop_no", 1),
					(else_try),
						(party_add_members, "p_routed_allies", ":troop_no", 1),
					(try_end),
					(assign, "$g_spawn_allies_routed", 1),
				(try_end),
			(else_try),	
			        (party_add_members, "p_routed_enemies", ":troop_no", 1),
				(try_begin),
					(agent_is_wounded, ":agent_no"),
					(party_wound_members, "p_routed_enemies", ":troop_no", 1),
				(try_end),
				(call_script, "script_remove_agent", ":agent_no"),
				(agent_set_slot, ":agent_no", slot_agent_routed, 2),
				(assign, "$g_spawn_enemies_routed", 1),
			(try_end),
		(try_end),
	]),

	# This script finds a position at the border nearest to the agent
	# script_find_exit_position_at_pos4
	("find_exit_position_at_pos4", 
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(le, ":agent_no", -1),
			(get_scene_boundaries, pos3, pos4),
			(position_get_x,":xmin",pos3),
			(position_get_y,":ymin",pos3),
			(position_get_x,":xmax",pos4),
			(position_get_y,":ymax",pos4),
			(init_position, pos20),
			(init_position, pos21),
			(init_position, pos22),
			(init_position, pos23),
			(store_random_in_range, ":rand_x", ":xmin", ":xmax"),
			(store_random_in_range, ":rand_y", ":ymin", ":ymax"),
			(position_set_x,pos20,":xmin"),
			(position_set_y,pos20,":rand_y"),
			(position_set_x,pos21,":xmax"),
			(position_set_y,pos21,":rand_y"),
			(position_set_x,pos22,":rand_x"),
			(position_set_y,pos22,":ymin"),
			(position_set_x,pos23,":rand_x"),
			(position_set_y,pos23,":ymax"),
			(store_random_in_range, ":rout_point", 0, 4),
			(val_add, ":rout_point", pos20),
			(copy_position, pos4, ":rout_point"),
			(position_set_z_to_ground_level, pos4),
		(else_try),
			(get_scene_boundaries, pos3, pos4),
			(agent_get_position, pos1, ":agent_no"),
			(position_set_z_to_ground_level, pos1),
			(position_set_z_to_ground_level, pos3),
			(position_set_z_to_ground_level, pos4),
			(position_get_x,":xmin",pos3),
			(position_get_y,":ymin",pos3),
			(position_get_x,":xmax",pos4),
			(position_get_y,":ymax",pos4),
			(position_get_x,":agent_x",pos1),
			(position_get_y,":agent_y",pos1),
			(init_position, pos20),
			(init_position, pos21),
			(init_position, pos22),
			(init_position, pos23),
			(position_set_x,pos20,":xmin"),
			(position_set_y,pos20,":agent_y"),
			(position_set_x,pos21,":xmax"),
			(position_set_y,pos21,":agent_y"),
			(position_set_x,pos22,":agent_x"),
			(position_set_y,pos22,":ymin"),
			(position_set_x,pos23,":agent_x"),
			(position_set_y,pos23,":ymax"),
			(position_set_z_to_ground_level, pos20),
			(position_set_z_to_ground_level, pos21),
			(position_set_z_to_ground_level, pos22),
			(position_set_z_to_ground_level, pos23),
			(assign, ":last_dist", 4000000),
			(try_for_range, ":index", 0, 4),
				(store_add, ":rout_point", ":index", pos20),
				(get_distance_between_positions, ":dist", pos1, ":rout_point"),
				(lt, ":dist", ":last_dist"),
				(assign, ":last_dist", ":dist"),
				(copy_position, pos4, ":rout_point"),
			(try_end),
		(try_end),
	]),

  #script_healthbars
    ("healthbars",
    [
	(assign,reg1,"$allies_coh"),
	(assign,reg2,"$enemies_coh"),
	(assign,reg3,"$allies_coh_modifier"),
	(display_message,"@Your side is at {reg1}% cohesion ({reg3}% recent events), the enemy at {reg2}%!",0x6495ed),
     ]),

  #script_morale_check
    ("morale_check",
    [
	(try_begin),
		(lt,"$allies_coh",75),
        (store_random_in_range,":routed",1,101),
        (assign,":chance_ply",80),
        (val_sub,":chance_ply","$allies_coh"),
        (try_begin),            
            (le,":routed",":chance_ply"),                   
            (call_script, "script_rout_allies"),
            (display_message,"@Morale of your troops wavers!",color_bad_news),      
        (try_end),
	(try_end),

	(try_begin),
        (lt,"$enemies_coh",75),
        (store_random_in_range,":routed",1,101),
        (assign,":chance_ply",80),
        (val_sub,":chance_ply","$enemies_coh"),
		(try_begin),  
            (le,":routed",":chance_ply"),                        
            (call_script, "script_rout_enemies"),
            (display_message,"@Morale of your enemies wavers!",color_good_news), 
		(try_end),            
	(try_end),
     ]),

  #script_rout_check

  #swy-- this comes from script_rout_enemies/script_rout_allies and shows morale-related messages about fleeeing troops in battlefield.
  #      reg0: should be allies/enemies_total | reg1: should be allies/enemies_total
  #      why not just use globals for this? low registers have a high chance of getting overwritten

  #cpp-- it's not really needed for this, since the script fires during this script, and the registers aren't used to store consistent data.
  #	 I've isolated the division by zero error, and made some tweaks to correct it.

    ("rout_check",
    [
	(assign,":ally","$allies_coh"),
	(assign,":enemy","$enemies_coh"),
	(val_sub,":ally",":enemy"),

	(try_begin),
		(ge,":ally",tld_morale_rout_enemies),		
		(call_script, "script_rout_enemies"),

		(store_mul, ":enemies_ratio", reg1, 100),

		(try_begin),
			(gt, reg0, 0), # At least a few enemies remain in battle
			(val_div, ":enemies_ratio", reg0),
			(try_begin),
				(gt, ":enemies_ratio", 80),
				(display_message,"@Your enemies flee in terror!",color_good_news),  
			(else_try),
				(gt, ":enemies_ratio", 50),
				(display_message,"@Many of your enemies are fleeing from battle.",color_good_news),  
			(else_try),
				(gt, ":enemies_ratio", 25),
				(display_message,"@Some of your enemies are fleeing from battle.",color_good_news),  
			(else_try),
				(gt, ":enemies_ratio", 10),
				(display_message,"@A few of your enemies are fleeing from battle.", color_good_news),  
			(try_end),
		(try_end),

		#(assign, reg0, ":enemies_ratio"),
		#(display_message, "@Enemies Ratio: {reg0}"),
	(try_end),

	(try_begin),
		(le,":ally",tld_morale_rout_allies),
		(call_script, "script_rout_allies"),
		(val_sub, reg0, 1), # Remove player from agents
		(store_mul, ":allies_ratio", reg1, 100),
		(try_begin),
		(gt, reg0, 0), # At least a few allies remain in battle
		(val_div, ":allies_ratio", reg0),
			(try_begin),
				(gt, ":allies_ratio", 80),
				(display_message,"@Your troops flee in terror!",color_bad_news),  
			(else_try),
				(gt, ":allies_ratio", 50),
				(display_message,"@Many of your troops are fleeing from battle.",color_bad_news),  
			(else_try),
				(gt, ":allies_ratio", 25),
				(display_message,"@Some of your troops are fleeing from battle.",color_bad_news),  
			(else_try),
				(gt, ":allies_ratio", 10),
				(display_message,"@A few of your troops are fleeing from battle.",color_bad_news),  
			(try_end),
		(try_end),
	(try_end),
     ]),


##==============================================##
## 		FLEEING SCRIPTS 		##
##==============================================##

    #script_flee_allies
    ("flee_allies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
		 
	(store_skill_level,":leader","skl_leadership","trp_player"),
	(try_for_agents,":agent"),
        	(agent_is_alive,":agent"),
        	(agent_is_human,":agent"),
        	(agent_is_ally,":agent"),
        	(store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
		(val_div,":troop_level",10),
		(val_add,":hitpoints",":troop_level"),		 
        	(assign,":chance_ply",100),
        	(val_sub,":chance_ply",":hitpoints"),
        	(val_sub,":chance_ply",":leader"),
        	(val_div,":chance_ply",2),
        	(store_random_in_range,":routed",1,101),
		(try_begin),
        
        (le,":routed",":chance_ply"),
        (agent_get_position,pos2,":agent"),
        (position_move_z,pos2,200,0),
                (agent_clear_scripted_mode,":agent"),

        ] + ((is_a_wb_script==1) and [
        
        ## WB has an operation for fleeing - Kham
        (agent_start_running_away, ":agent"),
        (agent_set_slot, ":agent", slot_agent_is_running_away, 1),
        
        ] or [
        
        (call_script, "script_find_exit_position_at_pos4", ":agent"),
        (agent_set_scripted_destination,":agent",pos4,1),

        ]) + [

        (try_end),
	(end_try),	
     ]),

    #script_flee_enemies
	("flee_enemies",
	[
	(call_script, "script_find_exit_position_at_pos4", -1),

	(try_for_agents,":agent"),
        (agent_is_alive,":agent"),
        (agent_is_human,":agent"),
        (neg|agent_is_ally,":agent"),
        (store_agent_hit_points,":hitpoints",":agent",0),
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
		(val_div,":troop_level",10),
		(val_add,":hitpoints",":troop_level"),		 
        (assign,":chance_ply",100),
        (val_sub,":chance_ply",":hitpoints"),
        (val_sub,":chance_ply",4),
        (val_div,":chance_ply",2),
            
        (store_random_in_range,":routed",1,101),
	 	(try_begin),
            (le,":routed",":chance_ply"),
            (agent_get_position,pos2,":agent"),
            (position_move_z,pos2,200,0),
            (agent_clear_scripted_mode,":agent"),

            ] + ((is_a_wb_script==1) and [

            ## WB has an operation for fleeing - Kham
            (agent_start_running_away, ":agent"),
            (agent_set_slot, ":agent", slot_agent_is_running_away, 1),
            
            ] or [
            
            (call_script, "script_find_exit_position_at_pos4", ":agent"),
            (agent_set_scripted_destination,":agent",pos4,1),
            
            ]) + [

        (try_end),
	(end_try),	
	]),

##==============================================##
## 		ROUTING SCRIPTS 		##
##==============================================##

    #script_rout_allies
    ("rout_allies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
	(assign, ":allies_routed", 0),
	(assign, ":allies_total", 0),
	(try_for_agents,":agent"),
        (agent_is_alive,":agent"),
        (agent_is_human,":agent"),
        (agent_is_ally,":agent"),
		(get_player_agent_no, ":player_agent"),
		(neq, ":player_agent", ":agent"),
		(val_add, ":allies_total", 1),
		#(assign, reg0, ":chance_ply"),
		#(assign, reg1, ":routed"),
		#(display_message, "@{reg1} less than {reg0}"),
        (try_begin),
			(call_script, "script_cf_agent_get_morale", ":agent"),
            (assign, ":chance_ply", reg1),
            (store_random_in_range,":routed",0,101),
            (le,":routed",":chance_ply"),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 0),
		   	(agent_set_slot, ":agent", slot_agent_routed, 1),
            (agent_get_position,pos2,":agent"),
		 	(position_move_z,pos2,200,0),
            (agent_clear_scripted_mode,":agent"),
                    
            ] + ((is_a_wb_script==1) and [
                
            ## WB has an operation for fleeing - Kham
            (agent_start_running_away, ":agent"),
            (agent_set_slot, ":agent", slot_agent_is_running_away, 1),
            
            ] or [
            
            (call_script, "script_find_exit_position_at_pos4", ":agent"),
            (agent_set_scripted_destination,":agent",pos4,1),

            ]) + [

        (try_end),
		
        (try_begin),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 1),
			(val_add, ":allies_routed", 1),
       		(store_random_in_range,":rand",1,101),
			(lt, ":rand", 33), # 33% chance.
			(agent_get_horse, ":horse", ":agent"),
			(try_begin),
				#(gt, ":horse", -1),
          			#(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"),
			#(else_try),
			(le, ":horse", -1),
          	(agent_set_animation, ":agent", "anim_nazgul_noooo_short"),	
			(try_end),
		(try_end),
	(try_end),
	(assign, reg0, ":allies_total"),
	(assign, reg1, ":allies_routed"),	
    (val_sub, "$allies_coh_modifier", ":allies_routed")
     ]),

    #script_rout_enemies
    #output: 
    #reg1 = enemies_routed
    #reg0 = enemies_total
    ("rout_enemies",
    [
	(call_script, "script_find_exit_position_at_pos4", -1),
	(assign, ":enemies_routed", 0),
	(assign, ":enemies_total", 0),
	(try_for_agents,":agent"),
         	(agent_is_alive,":agent"),
         	(agent_is_human,":agent"),
         	(neg|agent_is_ally,":agent"),
		(val_add, ":enemies_total", 1),
	 	(try_begin),
			(call_script, "script_cf_agent_get_morale", ":agent"),
         		(assign, ":chance_ply", reg1),
         		(store_random_in_range,":routed",0,101),
                   	(le,":routed",":chance_ply"),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 0),
		   	(agent_set_slot, ":agent", slot_agent_routed, 1),
                	(agent_get_position,pos2,":agent"),
		 	(position_move_z,pos2,200,0),
                        (agent_clear_scripted_mode,":agent"),
			        
			        ] + ((is_a_wb_script==1) and [
						
		            ## WB has an operation for fleeing - Kham
		            (agent_start_running_away, ":agent"),
		            (agent_set_slot, ":agent", slot_agent_is_running_away, 1),
		            
		            ] or [
					
					(call_script, "script_find_exit_position_at_pos4", ":agent"),
					(agent_set_scripted_destination,":agent",pos4,1),

					]) + [
					
               	(try_end),
		(try_begin),
		   	(agent_slot_eq, ":agent", slot_agent_routed, 1),
			(val_add, ":enemies_routed", 1),
       			(store_random_in_range,":rand",1,101),
			(lt, ":rand", 33), # 33% chance.
			(agent_get_horse, ":horse", ":agent"),
			(try_begin),
				#(gt, ":horse", -1),
          			#(agent_set_animation, ":agent", "anim_nazgul_noooo_mounted_short"),
			#(else_try),
				(le, ":horse", -1),
          			(agent_set_animation, ":agent", "anim_nazgul_noooo_short"),	
			(try_end),
		(try_end),
	(try_end),
	(assign, reg0, ":enemies_total"),
	(assign, reg1, ":enemies_routed"),
    (val_sub, "$enemies_coh_modifier", ":enemies_routed")
    ]),  

  

  #script_coherence, overhauled by InVain
    ("coherence",
    [
	(get_scene_boundaries, pos3, pos4),	
	 
	(assign,":num_allies",0),
	(assign,":coh_allies",0),
	(assign,":num_enemies",0),
	(assign,":coh_enemies",0),
	# (assign,":num_allies_alive",0),
	# (assign,":num_enemies_alive",0),
	(assign,":num_allies_rallied",0),
	(assign,":num_enemies_rallied",0),
 	(assign,":num_allies_routed",0),
	(assign,":num_enemies_routed",0),
 	(assign,":leadership_allies",0),
	(assign,":leadership_enemies",0),      

	(try_for_agents,":agent"), #allies
		(agent_is_human,":agent"),
        (agent_is_alive, ":agent"),
		#(store_agent_hit_points,":hitpoints",":agent",0), #Invain: get rid of hitpoints on coherence level, only matters for agent morale 
		(agent_get_troop_id,":troop_type", ":agent"),
		(store_character_level, ":troop_level", ":troop_type"),
		(val_mul,":troop_level",4),  

        (try_begin),
            (agent_is_ally,":agent"), #allies
            (val_add,":num_allies", 1), # troop count
            (val_add,":coh_allies",":troop_level"), # average level
            (try_begin),
                (agent_slot_eq,":agent",slot_agent_morale_modifier,1),
                (val_add, ":num_allies_rallied", 1),
            (try_end),
            (try_begin),
                (agent_slot_eq,":agent",slot_agent_routed,1),
                (val_add, ":num_allies_routed", 1),
            (try_end),
            (try_begin),
                (troop_is_hero,":troop_type"),
                (store_skill_level, ":troop_leaderskip", skl_leadership, ":troop_type"),
                (val_add, ":leadership_allies", ":troop_leaderskip"),
                (this_or_next|eq, ":troop_type", "trp_player"), #double bonus for player or lords
                (is_between, ":troop_type", kingdom_heroes_begin, kingdom_heroes_end),
                (val_add, ":leadership_allies", ":troop_leaderskip"),
            (try_end),
            (try_begin),
                (this_or_next|eq, ":troop_type", "trp_lothlorien_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i6_rivendell_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_isen_uruk_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_mordor_uruk_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (val_add, ":leadership_allies", 2),
            (try_end),
            (try_begin),
                (this_or_next|eq, ":troop_type", "trp_a6_ithilien_leader"),
                (this_or_next|eq, ":troop_type", "trp_i6_loss_leader"),
                (this_or_next|eq, ":troop_type", "trp_i6_pel_leader"),
                (this_or_next|eq, ":troop_type", "trp_a6_pel_marine_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_lam_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_pinnath_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_amroth_leader"),
                (eq, ":troop_type", "trp_captain_of_gondor"),
                (val_add, ":leadership_allies", 3),
            (try_end),
        
        (else_try), # enemies
            (val_add,":num_enemies", 1), # troop count
            (val_add,":coh_enemies",":troop_level"), # average level
            (try_begin),
                (agent_slot_eq,":agent",slot_agent_morale_modifier,1),
                (val_add, ":num_enemies_rallied", 1),
            (try_end),
            (try_begin),
                (agent_slot_eq,":agent",slot_agent_routed,1),
                (val_add, ":num_enemies_routed", 1),
            (try_end),
        (try_end),        
        (try_begin),
                (troop_is_hero,":troop_type"),
                (store_skill_level, ":troop_leaderskip", skl_leadership, ":troop_type"),
                (val_add, ":leadership_enemies", ":troop_leaderskip"),
                (this_or_next|eq, ":troop_type", "trp_player"), #double bonus for player or lords
                (is_between, ":troop_type", kingdom_heroes_begin, kingdom_heroes_end),
                (val_add, ":leadership_enemies", ":troop_leaderskip"),
            (try_end),
            (try_begin),
                (this_or_next|eq, ":troop_type", "trp_lothlorien_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i6_rivendell_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_isen_uruk_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_mordor_uruk_standard_bearer"),
                (this_or_next|eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (eq, ":troop_type", "trp_i5_greenwood_standard_bearer"),
                (val_add, ":leadership_enemies", 2),
            (try_end),
            (try_begin),
                (this_or_next|eq, ":troop_type", "trp_a6_ithilien_leader"),
                (this_or_next|eq, ":troop_type", "trp_i6_loss_leader"),
                (this_or_next|eq, ":troop_type", "trp_i6_pel_leader"),
                (this_or_next|eq, ":troop_type", "trp_a6_pel_marine_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_lam_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_pinnath_leader"),
                (this_or_next|eq, ":troop_type", "trp_c6_amroth_leader"),
                (eq, ":troop_type", "trp_captain_of_gondor"),
                (val_add, ":leadership_enemies", 3),
            (try_end),
        
    (try_end), #end try for agents

	(try_begin),
		(gt,":num_allies",0),
		(val_div,":coh_allies",":num_allies"),
	(else_try),
        (assign, ":num_allies", 1),
		(assign, ":coh_allies", 0),
	(try_end),

	(try_begin),
		(gt,":num_enemies",0),
		(val_div,":coh_enemies",":num_enemies"),
	(else_try),
		(assign, ":coh_enemies", 0),
	(try_end),

    # (assign, reg74, ":num_allies"),
    # (assign, reg75, ":coh_allies"),
    # (assign, reg76, ":leadership_allies"),

    # (display_message, "@allies: {reg74}, base coherence {reg75}, leaderhsip {reg76}"),
    
    # (assign, reg74, ":num_enemies"),
    # (assign, reg75, ":coh_enemies"),
    # (assign, reg76, ":leadership_enemies"),
    
    # (display_message, "@enemies: {reg74}, base coherence {reg75}, leaderhsip {reg76}"), 
    
	# Difference between in battle agents.
	#(store_sub, ":advantage", ":num_allies", ":num_enemies"), #InVain: use relative advantage instead
    (store_mul, ":advantage", ":num_enemies", 100),
    (val_div, ":advantage", ":num_allies"),
    (val_clamp, ":advantage", 50, 200), #up to twice outnumbered for any side
    (val_sub, ":advantage", 100), #reduce gap: -50 to 100
    (val_div, ":advantage", 3), #-16 to 33; tweakable
    (val_add, ":advantage", 100), #84 to 133

    # (assign, reg74, ":advantage"),
    # (display_message, "@advantage {reg74}"),   

    (val_mul, ":coh_allies", 100),
    (val_div, ":coh_allies", ":advantage"), #75 to 119 %    
    
	(val_add, ":coh_allies", ":num_allies_rallied"),
	(assign,"$allies_coh",":coh_allies"),
    
    (val_mul, ":coh_enemies", ":advantage"),
    (val_div, ":coh_enemies", 100), #84 to 133%, slight buff for enemies

	(assign,"$enemies_coh",":coh_enemies"),    
	(val_add, "$enemies_coh", ":num_enemies_rallied"),


    #leadership bonus and player kills
    (assign, "$allies_leadership", ":leadership_allies"), #store collective leadership for outside use
    #(val_div, ":leadership_allies", 2), #tweakable
	(val_add,"$allies_coh",":leadership_allies"),
	(val_add,"$allies_coh","$new_kills"),

    #(val_div, ":leadership_enemies", 2), #tweakable
	(val_add,"$enemies_coh",":leadership_enemies"),

    #party morale (allies only) - get average of party morale and base coherence
    (party_get_morale, ":party_morale", p_main_party),
    (val_add, "$allies_coh", ":party_morale"),
    (val_div, "$allies_coh", 2),

    #coherence modifier (battle events, normalized over time)
    (val_add, "$allies_coh", "$allies_coh_modifier"),
    (val_add, "$enemies_coh", "$enemies_coh_modifier"),

	(try_begin),
		(lt, "$allies_coh", 0),
		(assign, "$allies_coh", 0),
	(try_end),

	# Nazgul penalty
	(try_begin),
		(gt, "$nazgul_in_battle", 0),
		(store_mul, ":nazgul_penalty", "$nazgul_in_battle", 15),
		(get_player_agent_no, ":player"),
		(agent_get_team, ":player_team", ":player"),
		(try_begin),
			(teams_are_enemies, "$nazgul_team", ":player_team"),
			(val_sub, "$allies_coh", ":nazgul_penalty"),
			(val_add, "$enemies_coh", ":nazgul_penalty"),
		(else_try),
			(val_sub, "$enemies_coh", ":nazgul_penalty"),
			(val_add, "$allies_coh", ":nazgul_penalty"),
		(try_end),
	(try_end),

		# Morale Buffs/Debuffs of Encounter Effects (moved from agent morale)

 	] + ((is_a_wb_script==1) and [
		(try_begin),

			(party_get_slot, ":encounter_effect", "p_main_party", slot_party_battle_encounter_effect),
			(ge, ":encounter_effect", LORIEN_MIST), #Encounter effect present

			(faction_get_slot, ":allies_faction_side", "$players_kingdom", slot_faction_side),
            (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
            (faction_get_slot, ":enemies_faction_side", ":enemy_faction", slot_faction_side),            

			(try_begin), #good side effects
				(eq, ":encounter_effect", LORIEN_MIST),
				(try_begin),
					(eq, ":allies_faction_side", faction_side_good),
					(val_add, "$allies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
                    (val_sub, "$enemies_coh", ENCOUNTER_EFFECT_MORALE_DEBUFF),
				(else_try),
					(val_sub, "$allies_coh", ENCOUNTER_EFFECT_MORALE_DEBUFF),
                    (val_add, "$enemies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
				(try_end),
			(else_try), #evil side effects
				(is_between, ":encounter_effect", SAURON_DARKNESS, END_EFFECTS),
				(try_begin),
					(eq, ":allies_faction_side", faction_side_good),
					(val_sub, "$allies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
                    (val_add, "$enemies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
				(else_try),
                    (eq, ":enemies_faction_side", faction_side_good),
					(val_sub, "$allies_coh", ENCOUNTER_EFFECT_MORALE_DEBUFF),
                    (val_add, "$enemies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
                (else_try), #if both sides are evil (hand vs. eye), both get buffed
                    (val_add, "$allies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
                    (val_add, "$enemies_coh", ENCOUNTER_EFFECT_MORALE_BUFF),
				(try_end),
			(try_end),
		(try_end),
	] or []) + [

	(try_begin),
		(lt|this_or_next, "$enemies_coh", 0),
		(eq, ":num_enemies", 0),
		(assign, "$enemies_coh", 0),
	(try_end),
	(try_begin),
		(lt|this_or_next, "$allies_coh", 0),
		(eq, ":num_allies", 0),
		(assign, "$allies_coh", 0),
	(try_end),
     ]),  

  #script_normalize_coherence_modifier by InVain: Reduces any temporary positive or negative coherence effects by 2/3 per tick
    ("normalize_coherence_modifier",
    [
	(val_mul,"$allies_coh_modifier", 2),
    (val_div,"$allies_coh_modifier", 3),
	(val_mul,"$enemies_coh_modifier", 2),
    (val_div,"$enemies_coh_modifier", 3),
     ]),
]