#!/usr/bin/env python3
"""CLI runner for Connect 4 with an AI opponent."""
from connect4 import Connect4
from ai import choose_move
import os


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def prompt_player_move(game):
	valid = game.valid_moves()
	while True:
		try:
			col = input('Enter column (1-7): ').strip()
			if col.lower() in ('q', 'quit', 'exit'):
				return None
			c = int(col) - 1
			if c in valid:
				return c
			print('Invalid move; column full or out of range.')
		except ValueError:
			print('Please enter a number 1-7 or q to quit.')


def choose_difficulty():
	options = {'1': 'easy', '2': 'medium', '3': 'hard'}
	print('Choose difficulty: 1) easy  2) medium  3) hard')
	while True:
		c = input('> ').strip()
		if c in options:
			return options[c]
		print('Enter 1, 2, or 3')


def main():
	clear()
	print('Welcome to Connect 4 — play against a personalized AI!')
	name = input('Your name: ').strip() or 'Player'
	difficulty = choose_difficulty()

	game = Connect4()
	player_id = 1
	ai_id = 2

	turn = 1  # 1 = player starts
	while True:
		clear()
		print(f"{name} (X) vs AI (O) — difficulty: {difficulty}")
		print(game.render())

		if game.check_win() != 0 or game.is_full():
			winner = game.check_win()
			if winner == player_id:
				print(f'Congrats {name}, you win!')
			elif winner == ai_id:
				print('AI wins — good game!')
			else:
				print('Draw!')
			if input('Play again? (y/N): ').strip().lower() == 'y':
				game = Connect4()
				continue
			break

		if turn == 1:
			mv = prompt_player_move(game)
			if mv is None:
				print('Goodbye!')
				break
			game.drop_piece(mv, player_id)
			turn = 2
		else:
			print('AI is thinking...')
			mv = choose_move(game, ai_id, difficulty)
			game.drop_piece(mv, ai_id)
			turn = 1


if __name__ == '__main__':
	main()

