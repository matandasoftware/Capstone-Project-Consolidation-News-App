# Defining the Album class
class Album:
    def __init__(self, album_name, number_of_songs, album_artist):
        self.album_name = album_name
        self.number_of_songs = number_of_songs
        self.album_artist = album_artist

    # Method to display album information
    def display_album_info(self):
        print(
            f"Album: {self.album_name}, "
            f"Artist: {self.album_artist}, "
            f"Number of Songs: {self.number_of_songs}"
        )


# Creating a list of Album objects
albums1 = [
    Album("Made in the A.M.", 12, "One Direction"),
    Album("Dark Sky Island", 16, "Enya"),
    Album("Reputation", 15, "Taylor Swift"),
    Album("Thank U, Next", 12, "Ariana Grande"),
    Album("When We All Fall Asleep, Where Do We Go?", 14, "Billie Eilish"),
]

# Displaying all albums in albums1
for album in albums1:
    album.display_album_info()

# Sorting the albums by number of songs using a lambda function as the key
sorted_albums = sorted(albums1, key=lambda x: x.number_of_songs)
print("\nAlbums sorted by number of songs:")
for album in sorted_albums:
    album.display_album_info()

# Swapping index 0 parameters with index 1
albums1[0], albums1[1] = albums1[1], albums1[0]
print("\nAlbums after swapping first two albums:")
for album in albums1:
    album.display_album_info()

# Creating another list of Album objects and displaying them
albums2 = [
    Album("25", 11, "Adele"),
    Album("Lover", 18, "Taylor Swift"),
    Album("÷ (Divide)", 16, "Ed Sheeran"),
    Album("Future Nostalgia", 11, "Dua Lipa"),
    Album("Fine Line", 12, "Harry Styles"),
]
for album in albums2:
    album.display_album_info()

# Copying all albums from albums1 to albums2 and displaying the combined list
albums2.extend(albums1)
print("\nAlbums after merging two lists:")
for album in albums2:
    album.display_album_info()

# Adding new albums to albums2 and displaying the updated list
new_album1 = Album("Dark Side of the Moon", 9, "Pink Floyd")
new_album2 = Album("Ooops!... I Did it Again", 16, "Britney Spears")
albums2.append(new_album1)
albums2.append(new_album2)
print("\nAlbums after adding new albums:")
for album in albums2:
    album.display_album_info()

# Sorting the albums by album name alphabetically using a lambda function as the key
sorted_albums_by_name = sorted(albums2, key=lambda x: x.album_name)
print("\nAlbums sorted by album name:")
for album in sorted_albums_by_name:
    album.display_album_info()

# Searching for an album by name and displaying its index
search_name = "Dark Side of the Moon"
for index, album in enumerate(albums2):
    if album.album_name == search_name:
        print(f"\nAlbum '{search_name}' found at index: {index}")
        break
else:
    print(f"\nAlbum '{search_name}' not found in the list.")



