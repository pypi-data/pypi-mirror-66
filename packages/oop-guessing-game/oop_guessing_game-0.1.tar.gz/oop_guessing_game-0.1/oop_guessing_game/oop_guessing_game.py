{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from random import randint\n",
    "from time import sleep"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Game:\n",
    "    \n",
    "    \"\"\" Representing a game of guessing a computer generated number within a set range. \n",
    "             \n",
    "    \"\"\"\n",
    "    \n",
    "    def __init__(self, players, max_number):\n",
    "        self.max_number = max_number\n",
    "        self.players = players        \n",
    "                  \n",
    "    def play_game(self):\n",
    "        \n",
    "        \"\"\" Starts a game of guessing a computer generated number within a set range. \n",
    "        \n",
    "        Attributes:\n",
    "        players (list) representing the Computer player and the Player \n",
    "            who interacts with the program\n",
    "        max_number (int) representing the max limmit of the range of integerswithin \n",
    "            which the computer chooses a randomn integer  \n",
    "\n",
    "        \"\"\"\n",
    "        \n",
    "        attempts = 1\n",
    "        picked_number = self.players[0].pick_number(self.max_number)   \n",
    "        guess = self.players[1].guess_number(self.max_number, response=None)\n",
    "        \n",
    "#         print(guess)\n",
    "        \n",
    "        while guess != picked_number:\n",
    "            print(guess)\n",
    "            \n",
    "            if guess > picked_number:\n",
    "                response = 'lower' \n",
    "                print(\"Too high. The generated number is lower.\")\n",
    "#                 output = int(input(\"Try again. The number is between 0 and {}.\".format(max_number)))\n",
    "                \n",
    "        \n",
    "            if guess < picked_number:\n",
    "                response = 'higher'\n",
    "                print(\"Too low. The number is greater than {}.\".format(guess))\n",
    "#                 output = int(input(\"Try again. The number is between 0 and {}.\".format(max_number)))    \n",
    "\n",
    "            attempts += 1\n",
    "            guess = self.players[1].guess_number(self.max_number, response=response)\n",
    "        \n",
    "        print(guess)\n",
    "        print(\"Dobre! You made it on {} attempt(s).\".format(attempts))\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Player:\n",
    "    \n",
    "    def __init__(self, name):\n",
    "        self.name = name\n",
    "\n",
    "    def pick_number(self, max_number):\n",
    "        \"\"\"\n",
    "        Returns an int\n",
    "        \"\"\"\n",
    "        raise NotImplementedError\n",
    "        \n",
    "    def guess_number(self, max_number, response=None):\n",
    "        \"\"\"\n",
    "        Returns an int\n",
    "        \"\"\"\n",
    "        raise NotImplementedError\n",
    "        "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "class ComputerPlayer(Player):\n",
    "    \n",
    "    def __init__(self):\n",
    "        super().__init__(name = 'computersko')\n",
    "        self.previous_guess = None\n",
    "        \n",
    "    def pick_number(self, max_number):\n",
    "        return randint(0, max_number)\n",
    "    \n",
    "    def guess_number(self,max_number, response = None):\n",
    "        sleep(1)\n",
    "        if response is None:\n",
    "            self.previous_guess = randint(0, max_number)\n",
    "        elif response == 'lower':\n",
    "            self.previous_guess = randint(0, self.previous_guess)\n",
    "        elif response == 'higher':\n",
    "            self.previous_guess = randint(self.previous_guess, max_number)\n",
    "\n",
    "        return self.previous_guess\n",
    "        \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "computersko = ComputerPlayer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "class PersonPlayer(Player):\n",
    "    \n",
    "    def pick_number(self, max_number):\n",
    "        return int(input(\"Pick a number within 0 and {} and let the Computer guess.\".format(max_number)))\n",
    "    \n",
    "    def guess_number(self, max_number, response=None):\n",
    "        return int(input(\"Guess a number within the range of 0 and {}\".format(max_number)))\n",
    "        "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "person = PersonPlayer('katzko')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "gamesko = Game(players = [person, computersko], max_number=20) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Pick a number within 0 and 20. 1\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "13\n",
      "Too high. The generated number is lower.\n",
      "5\n",
      "Too high. The generated number is lower.\n",
      "2\n",
      "Too high. The generated number is lower.\n",
      "0\n",
      "Too low. The number is greater than 0.\n",
      "19\n",
      "Too high. The generated number is lower.\n",
      "13\n",
      "Too high. The generated number is lower.\n",
      "10\n",
      "Too high. The generated number is lower.\n",
      "5\n",
      "Too high. The generated number is lower.\n",
      "2\n",
      "Too high. The generated number is lower.\n",
      "2\n",
      "Too high. The generated number is lower.\n",
      "1\n",
      "Dobre! You made it on 11 attempt(s).\n"
     ]
    }
   ],
   "source": [
    "gamesko.play_game()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# testing\n",
    "\n",
    "# def play_game(max_number, generated_number):\n",
    "#     attempts = 1\n",
    "\n",
    "#     players_guess = input(\"Computer chose a random integer between 0 and {}. Can you guess the number?\".format(max_nunmber))\n",
    "#     output = int(players_guess)\n",
    "#     while output != generated_number:\n",
    "\n",
    "#         if output > generated_number:\n",
    "#             attempts += 1\n",
    "#             print(\"Too high. The generated number is lower.\")\n",
    "#             output = int(input(\"Computer chose a random integer between 0 and {}. Can you guess the number?\".format(max_number)))\n",
    "\n",
    "#         if output < generated_number:\n",
    "#             attempts += 1\n",
    "#             print(\"Too low. The number is greater than {}.\".format(players_guess))\n",
    "#             output = int(input(\"Computer chose a random integer between 0 and {}. Can you guess the number?\".format(max_number)))    \n",
    "                \n",
    "#     print(\"Dobre! You made it on {} attempt(s).\".format(attempts))\n",
    "\n",
    "        \n",
    "# play_game(20,17)\n",
    "        "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# testing\n",
    "\n",
    "# def random_number(max_number):\n",
    "#     print(randint(0, max_number))\n",
    "        \n",
    "# random_number(20)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# testing\n",
    "\n",
    "# def random_number(max_number):\n",
    "#     return input(\"Computer chose a random integer between 0 and {}. Can you guess the number?\".format(max_number))\n",
    "    \n",
    "# #     print(randint(0, max_number))\n",
    "\n",
    "# random_number(20)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#testing data types\n",
    "\n",
    "# players_guess = input(\"Computer chose a random integer between 0 and {}. Can you guess the number?\".format(17))\n",
    "# players_guess\n",
    "# type(players_guess)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# players_guess = int(players_guess)\n",
    "# type(players_guess)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
