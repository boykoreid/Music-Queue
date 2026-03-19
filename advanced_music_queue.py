# =================================================================
# CMPUT 175 - Introduction to the Foundations of Computation II
# Lab 6 - Advanced Music Queue
#
# ~ Created by CMPUT 175 Team ~
# ============================================================

# Install ytmusicapi using pip
from ytmusicapi import YTMusic
from structures import DLinkedListNode, DLinkedList, Song, time_to_seconds
import os

NO_OF_RESULTS = 5

def clear():
    '''
    Clears the screen based on the operating system.
    '''
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')

def extract_artists(song):
    """
    Input: A dictionary containing song information
    Returns: A string of artist names separated by commas
    Working:
    This function extracts and returns a comma-separated string of artist names from the song dictionary.
    """
    if len(song['artists']) == 0:
        return 'NA'
    else:
        artists = []
        try:
            artist_info = song['artists'] #This key's value is a list which contains dictionaries with the name and id of each artist
            for dictionary in artist_info:
                artists.append(dictionary['name'])
            string = ", ".join(artists)
            return string
        except:
            raise Exception('Artist not found')



def song_search(query):
    """
    Input: Search query
    Returns: Top "NO_OF_RESULTS" i.e. 5 results from the retrieved data
    Working:
    This function invokes the search method on YTMusic object with required arguments
    """
    yt = YTMusic()
    results = yt.search(query, filter='songs')
    return results[:NO_OF_RESULTS]

def filter_info(results):
    """
    Input: Search results in a JSON like format
    Returns: List of Song Objects
    Working:
    This function is supposed to extract the required information from the JSON,
    create Song objects and append them to a list. If an error occurs, raise an
    exception.
    """
    songs = []

    if type(results) is list:
        for dictionary in results:
            try:
                title = dictionary['title']
            except:
                raise Exception('Title not found')
            try:
                duration = dictionary['duration_seconds']
            except:
                raise Exception('Song duration not found')
            try: 
                artists = extract_artists(dictionary)
            except Exception as e:
                raise e

            song = Song(title, artists, duration)
            songs.append(song)
        return songs
    else:
        raise Exception("Input must be a JSON")

def print_song_results(results):
    """
    Input: A list of Song objects
    Returns: None
    Working:
    This function prints the list of Song objects in a formatted manner.
    """
    assert type(results[0]) == Song, "The list to be printed doesn't have the items of type 'Song'"

    print("RESULTS:")
    for i in range(len(results)):
        print(f"{i+1}. {results[i]}")

def search():
    """
    Input: None
    Return: A Song object representing the song the user wants to add into the Queue, or None if the user wants to go back
    Working:
    1. This function takes search query from the user
    2. Searches for the song using song_search function
    3. Filters the information using filter_info function
    4. Prints the song results using print_song_results function
    5. Asks for user choice
    6. Returns the chosen song information
    7. If the user wants to go back, it returns None
    """
    again = True
    while again:
        query = input('Search: ').strip().lower()
        results = song_search(query)
        songs = filter_info(results)
        print_song_results(songs)

        #Gets user input for which song to choose
        print()
        print("Choose one of the following options:")
        print('\tEnter a number (1-5) to add a song to a playlist')
        print("\tEnter '0' to search again")
        print("\tEnter 'q' to go back")
        print()

        valid = False
        while not valid:
            option = input('>> ').strip().lower()
            try:
                option = int(option)
                if option in range(1, NO_OF_RESULTS + 1):
                    valid = True
                    again = False
                    return songs[option - 1]
                elif option == 0:
                    valid = True
                else:
                    print('Invalid Input')
            except:
                if option == 'q':
                    valid = True
                    again = False
                    return None
                else:
                    print("Invalid Input")

def main():
    """
    Initializes the music queue and provides an interactive menu to manage songs.
    Users can add songs, navigate to next or previous songs, remove the current song,
    display or clear the queue, and quit the program.

    NOTE: You need to modify the main function to use the DLinkedList class to manage the music queue. 
          Add the new features that are needed for this Lab assignment as per the description.

          ** MAKE SURE YOU READ THE DESCRIPTION CAREFULLY AND UNDERSTAND THE REQUIREMENTS. **
    """
    queue = DLinkedList()
    clear()
    print("WELCOME\n")
    choice_str = """Choose one of the following options:
                \t1. Add Song
                \t2. Next Song
                \t3. Previous Song
                \t4. Remove Current Song
                \t5. Show Queue
                \t6. Clear Queue
                \t7. Quit
                Enter the choice (eg: 2)
                """
    contBuild = True
    try:
        while contBuild:

            print('Currently playing:')
            try: 
                current = queue.get_current() 
                print('  ',current,'\n')
            except: 
                print('  ',"None",'\n')

            print(choice_str)
            choice = input('>> ')
            while choice not in ['1','2','3','4','5','6','7']:
                print('Invalid Input.')
                choice = input('>> ')
            
            if choice == '1':
                song = search()
                if song != None:
                    if queue.is_empty():
                        queue.add_next(song)
                    else:
                        place = input("Where would you like to add the song:\n\t1. Add Next\n\t2. Add to the End\n>> ")
                        while place not in ['1','2']:
                            print('Invalid Input.')
                            place = input('>> ')
                        
                        if place == '1':
                            queue.add_next(song)
                        elif place == '2':
                            queue.add_last(song)
                    print("Song added successfully!")
                    input("\nPress enter key to continue...")

            elif choice == '2':
                clear()
                if queue.is_empty():
                    print('Error: Queue is empty')
                else:
                    if queue.play_next() == True:
                        song = queue.get_current()
                        print('Now playing:')
                        print("  ",song)
                    else:
                        print("   No Songs Ahead in queue")
                input("\nPress enter key to continue...")

            elif choice == '3':
                clear()
                if queue.is_empty():
                    print('Error: Queue is empty')
                else:
                    if queue.play_previous() == True:
                        song = queue.get_current()
                        print('Now playing:')
                        print("  ",song)
                    else:
                        print("   No Songs Behind in queue")
                input("\nPress enter key to continue...")


            elif choice == '4':
                clear()
                try:
                    song = queue.remove_current()
                    name = song.get_name()
                    print(f"{name} removed successfully!")
                except Exception as e:
                    print(e)
                input("\nPress enter key to continue...")

            elif choice == '5':
                clear()
                try:
                    print(queue)
                    input("\nPress enter key to continue...")
                except Exception as e:
                    print(e)
            
            elif choice == '6':
                clear()
                queue.clear()
                print('The queue has been cleared!')
                input("\nPress enter key to continue...")

            elif choice == '7':
                contBuild = False
            
            clear()

    except Exception as e:
        print(e)

    print("Thanks for listening!")

if __name__ == "__main__":
    main()