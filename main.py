import random
from hangman_words import word_list
from hangman_art import logo, stages
from hangman_ranking import save_score, print_ranking
import socket
import pickle
import struct



MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', MULTICAST_PORT))
group = socket.inet_aton(MULTICAST_GROUP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL',group, socket.INADDR_ANY))


def main_menu():
    print("Multicast Server is ready...")
    message, client_address = receive()

    print(f"Received from {client_address}: {message}")
    client_name = message['client_id']
    print(client_name)
    print(client_address)
    while True:
        print("1. Start new game")
        print("2. Show ranking")
        print("3. Quit")

        send("""
    1. Start new game
    2. Show ranking
    3. Quit
    Choose an option:
            """, client_address)

        response, _ = receive()

        choice = response['message']


        #choice = input("Choose an option: ")

        if choice == '1':
            start_game(client_name, client_address)
        elif choice == '2':
           ranking_str = ""
           ranking = print_ranking()
           for name, score in ranking.items():
               ranking_str = ranking_str + f"{name}: {score}\n"
           send(ranking_str, client_address)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")
            send("Invalid option. Please try again.", client_address)

def receive():
    data, client_address = sock.recvfrom(1024)
    message = pickle.loads(data)
    return message, client_address

def send(message, client_address):
    data = pickle.dumps(message)
    sock.sendto(data, client_address)

def start_game(client_name, client_address):
    # player_name = input("Enter your name: ")
    print(f"Name: {client_name}")
    send(f"Your name is: {client_name}", client_address)
    send(logo, client_address)
    print(logo)

    chosen_word = random.choice(word_list)
    word_length = len(chosen_word)

    end_of_game = False
    lives = 6

    display = []
    for _ in range(word_length):
        display += "_"

    guessed_letters = []

    while not end_of_game:
        # guess = input("Guess a letter: ").lower()
        send('Guess a letter', client_address)
        letter, _ = receive()
        guess = letter['message'].lower()
        if guess in guessed_letters:
            print("You've already guessed this letter.")
            send("You've already guessed this letter.", client_address)
        else:
            guessed_letters.append(guess)

            for position in range(word_length):
                letter = chosen_word[position]
                if letter == guess:
                    display[position] = letter

            if guess not in chosen_word:
                print("This letter is not in the word.")
                send("This letter is not in the word.", client_address)
                lives -= 1
                if lives == 0:
                    end_of_game = True
                    print("You lose.")
                    send("You lose", client_address)

        print(f"{' '.join(display)}")
        send(f"{' '.join(display)}", client_address)
        if "_" not in display:
            end_of_game = True
            print("You win.")
            send("You win", client_address)

        print(stages[lives])
        send(stages[lives], client_address)
    save_score(client_name, lives)

if __name__ == "__main__":
    main_menu()
