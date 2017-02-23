#!/usr/bin/python
"""
Converts the Hearthstone card JSON data from https://hearthstonejson.com/ into
a .sql file containing insert row commands for a Oracle 11g database.
"""

import sys, getopt
import json, re

def main(argv):
	inputfile = ''
	outputfile = 'card_insert.sql'

	try:
		opts, args = getopt.getopt(argv, "i:o:", ["input=", "output="])
	except:
		print("card_json_to_sql.py -i <input> -o <output")
		sys.exit(5)

	for opt, arg in opts:
		if opt in ("-i", "--input"):
			inputfile = arg;
		elif opt in ("-o", "--output"):
			outputfile = arg

	cards = json_file_to_dict(inputfile)
	remove_non_collectible_cards(cards)
	#log_found_cards(cards)	
	write_sql_file(cards, outputfile)

def json_file_to_dict(inputfile):
	f_read = open(inputfile, 'r', encoding="utf8")
	cards_dict = json.loads(str(f_read.read()))
	f_read.close()
	return cards_dict

#Deprecated
def remove_non_collectible_cards2(cards):
	del cards['Credits']
	del cards['Debug']
	del cards['Hero Skins']
	del cards['Missions']
	del cards['System']
	del cards['Tavern Brawl']

	#Removes cards that don't follow the format <Collection ID>_<3 digit number>
	for exp in cards:
		list_copy = list(cards[exp])
		for card in list_copy:
			match_result = re.match(r"^[a-zA-Z0-9]+_[0-9]{3}$", card['id'])
			if not match_result:
				cards[exp].remove(card)

	#Remove Game Mechanic cards
	remove_cards_with_regex(cards, r"^GAME_.+$", 'Basic')

	#Remove Spare Part cards
	remove_cards_with_regex(cards, r"^PART_.+$", 'Goblins vs Gnomes')

	remove_cards_with_regex(cards, r"^NAXM_[0-9]+$", 'Curse of Naxxramas')

	#Remove all other tokens
	deletion_list = ['CS2_050', 'CS2_051', 'CS2_052', 'NEW1_009', 'NEW1_034', 'NEW1_033', 'NEW1_032', 'FP1_006', 'LOE_030',
						'EX1_598', 'CS2_152']
	remove_card_ids(cards, deletion_list)

	#Remove hero powers
	heropower_list = ['CS2_102', 'CS2_034', 'CS1h_001', 'CS2_056', 'CS2_101', 'CS2_017', 'DS1h_292', 'CS2_049', 'CS2_082']
	remove_card_ids(cards, heropower_list)

def remove_non_collectible_cards(cards):
	del cards['Credits']
	del cards['Debug']
	del cards['Hero Skins']
	del cards['Missions']
	del cards['System']
	del cards['Tavern Brawl']

	for exp in cards:
		list_copy = list(cards[exp])
		for card in list_copy:
			if 'collectible' not in card.keys():
				cards[exp].remove(card)

	remove_cards_with_regex(cards, r"^HERO_", 'Basic')
	remove_card_ids(cards, ['NEW1_037e', 'LOE_030'])

def remove_cards_with_regex(cards, pattern, expansion=None):
	if expansion is not None:
		cards_copy = list(cards[expansion])
		for card in cards_copy:
			if (re.match(pattern, card['id'])):
				cards[expansion].remove(card)
	else:
		for exp in cards:
			cards_copy = list(cards[exp])
			for card in cards_copy:
				if re.match(pattern, card['id']):
					cards[exp].remove(card)

def remove_card_ids(cards, cards_to_remove):
	for exp in cards:
		for exp in cards:
			cards_copy = list(cards[exp])
			for card in cards_copy:
				if card['id'] in cards_to_remove:
					cards[exp].remove(card)

def log_found_cards(cards):
	f_debug = open("output.log", "w", encoding="utf8")
	for exp in cards:	
		for card in cards[exp]:
			f_debug.write(card['id'] + ' ' + card['name'] + ' ' + exp + '\n')

	for exp in cards:
		f_debug.write(exp + ': ' + str(len(cards[exp])) + '\n')
	f_debug.close()

def write_sql_file(cards, outputfile):
	f_sql = open(outputfile, "w", encoding="utf8")
	for exp in cards:
		for card in cards[exp]:
			f_sql.write(create_insert_statement('Card', card) + '\n')

def create_insert_statement(table_name, card):
	card_type = str(card['type'])

	def create_insert_parameters(columns, values):

		def create_list_string(iterable):
			list_string = ""
			if iterable is not None:
				for element in iterable:
					list_string = list_string + ', ' + str(element)
				#removes leading comma and enclose string in parantheses
				list_string = '(' + list_string[2:] + ')'
			return list_string

		columns_list = create_list_string(columns)
		values_list = create_list_string(values)

		return columns_list + ' ' + 'values' + values_list + ';'

	base_insert_string = 'INSERT INTO ' + table_name 

	q = lambda x: '\'' + x + '\''

	if card_type == 'Minion':
		elite = 1 if 'elite' in card.keys() else 0

		values = [q(card['id']), q(card['name']), q(card['type']), card['cost'], card['attack'], card['health'], q(card['rarity']), elite]
		columns = ['cardID', 'cardName', 'type', 'manaCost', 'attack', 'health', 'rarity', 'isLegendary']

		if 'text' in card.keys():
			values.append(q(card['text']))
			columns.append('cardText')

		if 'race' in card.keys():
			values.append(q(card['race']))
			columns.append('race')

		if 'playerClass' in card.keys():
			values.append(q(card['playerClass']))
			columns.append('class')

		return base_insert_string + create_insert_parameters(columns, values)

	elif card_type == 'Spell':
		elite = 1 if 'elite' in card.keys() else 0

		values = [q(card['id']), q(card['name']), q(card['type']), card['cost'], q(card['text']), q(card['rarity']), elite]
		columns = ['cardID', 'cardName', 'type', 'manaCost', 'cardText', 'rarity', 'isLegendary']

		if 'playerClass' in card.keys():
			values.append(q(card['playerClass']))
			columns.append('class')

		return base_insert_string + create_insert_parameters(columns, values)

	elif card_type == 'Weapon':
		elite = 1 if 'elite' in card.keys() else 0

		values = [q(card['id']), q(card['name']), q(card['type']), card['attack'], card['durability'], q(card['rarity']), elite, q(card['playerClass'])]
		columns = ['cardID', 'cardName', 'type', 'manaCost', 'rarity', 'isLegendary', 'class']

		if 'text' in card.keys():
			values.append(q(card['text']))
			columns.append('cardText')

		return base_insert_string + create_insert_parameters(columns, values)

if __name__ == "__main__":
	main(sys.argv[1:])

