import json
import tkinter as tk
from tkinter import messagebox, ttk
from pytube import YouTube
class Song:#add a class called Song
    def __init__(self, song_name, artist, duration, channel, popularity):
        self.song_name = song_name
        self.artist = artist
        self.duration = duration
        self.channel = channel
        self.popularity = popularity
        self.next = None #Initialize a next pointer to None

class PlaylistApp: #add a class called PlaylistApp
    def __init__(self, root): #initialize the self and root variable
        self.playlist = self.load_data() #let self.playlist is  = Load data from playlist_data file in () can be add file path
        self.sort_ascending = True #from high to low
        self.root = root
        self.root.title("Blusic App")
        self.ui()
        self.sorted_playlist = None
    def load_data(self): # loading data from .json file
        try:
            with open("playlist_data.json", 'r') as file:
                playlist_data = json.load(file)
                return self.create_playlist_from_data(playlist_data)
        except FileNotFoundError:
            return None
    def ui(self):#define UI
#Add title and insert link box for youtube link
        font_style = ("Space Grotesk", 12) # Set the Space Grotesk font
        self.root.configure(bg="#b1cce0") # Add background color
        tk.Label(self.root, text="YouTube Link:", font=font_style, bg="#b1dce0").pack()
        self.youtube_link_entry = tk.Entry(self.root, font=font_style) #block for insert link
        self.youtube_link_entry.pack()
#Add "add link" button
        add_button = tk.Button(self.root, text="Add YouTube Link", command=self.add_link, font=font_style)
        add_button.pack()
# Add a label and an entry box for searching songs
        tk.Label(self.root, text="Search for Song:", font=font_style, bg="#b1dce0").pack()
        self.search_entry = tk.Entry(self.root, font=font_style)
        self.search_entry.pack()
# Add a "Search" button
        search_button = tk.Button(self.root, text="Search Song", command=self.search_song, font=font_style)
        search_button.pack()
#Add title and insert the order numeber in box for removing song at that order
        tk.Label(self.root, text="Remove Song at Position:", font=font_style, bg="#b1dce0").pack()
        self.remove_position_entry = tk.Entry(self.root, font=font_style)
        self.remove_position_entry.pack()
#Add "remove button"
        remove_button = tk.Button(self.root, text="Remove Song", command=self.remove_song, font=font_style)
        remove_button.pack()

#Add sort pack
        tk.Label(self.root, text="Sorting option: ", font=font_style, bg="#b1dce0").pack()
        self.sort_var = tk.StringVar(value="Song Name A-Z")
        sort_menu = ttk.Combobox(self.root, textvariable=self.sort_var, values=["Song Name A-Z", "Song Name Z-A", "Popularity High to Low", "Popularity Low to High"],font=font_style)
        sort_menu.pack()
        
#Add confirm button
        confirm_button = tk.Button(self.root, text="Confirm", command=self.option, font=font_style)
        confirm_button.pack()
#Add Display button
        display_button = tk.Button(self.root, text="Display Playlist", command=self.display_playlist, font=font_style)
        display_button.pack()

        
#set the size of display area
        self.playlist_text = tk.Text(self.root, width=80, height=20, font=font_style)
        self.playlist_text.pack()
        
    def option(self):#Define option function (function of sort type in the option box)
        #Checking the option box
        sort_option = self.sort_var.get()
        if sort_option == "Song Name A-Z":
            self.sort_by_song_name_ascending()
        elif sort_option == "Song Name Z-A":
            self.sort_by_song_name_descending()
        elif sort_option == "Popularity High to Low":
            self.sort_by_popularity_descending()
        elif sort_option == "Popularity Low to High":
            self.sort_by_popularity_ascending()

    def add_link(self): #Define the add youtube link fuction 
        link = self.youtube_link_entry.get()
        try:
            yt_video = YouTube(link)
            # Extract relevant information from the YouTube video
            song_name = yt_video.title
            artist = yt_video.author
            duration = yt_video.length
            channel = yt_video.author
            popularity = yt_video.views

            new_song = Song(song_name, artist, duration, channel, popularity)            # Create a new song variable
            # Add the new song to the playlist
            if not self.playlist:
                self.playlist = new_song
            else:
                current_song = self.playlist
                while current_song.next:
                    current_song = current_song.next
                current_song.next = new_song
            self.save_playlist_data()# Save the updated playlist data
            self.display_playlist()#display playlist
            messagebox.showinfo("Success", "YouTube link added to the playlist.")
            self.youtube_link_entry.delete(0, tk.END)# Clear the input boxes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add YouTube link: {str(e)}")
            self.youtube_link_entry.delete(0, tk.END)# Clear the input boxes
    def remove_song(self):
        try:
            position = int(self.remove_position_entry.get())
            if position <= 0:
                messagebox.showerror("Error", "Song position must be a positive integer.")
                self.remove_position_entry.delete(0, tk.END)
                return

            if self.sorted_playlist:
                if position <= len(self.sorted_playlist):
                    song_to_remove = self.sorted_playlist[position - 1]
                    self.sorted_playlist.pop(position - 1)  # Remove from the sorted playlist

                    # Now remove the song from the original playlist based on the song_to_remove
                    prev_song = None
                    current_song = self.playlist

                    while current_song and current_song != song_to_remove:
                        prev_song = current_song
                        current_song = current_song.next

                    if current_song:
                        if prev_song:
                            prev_song.next = current_song.next
                        else:
                            self.playlist = current_song.next

                        messagebox.showinfo("Success", "Song removed from the playlist.")
                        self.save_playlist_data()
                        self.remove_position_entry.delete(0, tk.END)
                        self.display_playlist(self.sorted_playlist)  # Display the updated sorted playlist
                    else:
                        messagebox.showerror("Error", "Song not found at the specified position.")
                else:
                    messagebox.showerror("Error", "Song not found at the specified position.")
            else:
                messagebox.showerror("Error", "Playlist is empty.")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid song position.")
            self.remove_position_entry.delete(0, tk.END)
    def format_duration(self, duration): #Define format time function (change second to minute)
        minutes = duration // 60
        seconds = duration % 60
        return f"{minutes} min {seconds} sec"
    def display_playlist(self, playlist=None):#Define a dispaly fuction
        self.playlist_text.delete('1.0', tk.END)  # Clear previous content
        if not playlist:#check if the playlist is None or False
            playlist = self.playlist
        if not playlist:#check if the playlist is None or False
            self.playlist_text.insert(tk.END, "Playlist is empty.")
            return

        song_number = 1
        if isinstance(playlist, list): #check the playlist is list
            for song in playlist:
                self.playlist_text.insert(tk.END, f"{song_number}. Song: {song.song_name}\n")
                self.playlist_text.insert(tk.END, f"   Artist: {song.artist}\n")
                self.playlist_text.insert(tk.END, f"   Duration: {self.format_duration(song.duration)}\n")
                self.playlist_text.insert(tk.END, f"   Channel: {song.channel}\n")
                self.playlist_text.insert(tk.END, f"   Popularity: {song.popularity} views\n")
                self.playlist_text.insert(tk.END, "\n")
                song_number += 1
        else:#If playlist is a not list (linked list)
            while playlist:
                self.playlist_text.insert(tk.END, f"{song_number}. Song: {playlist.song_name}\n")
                self.playlist_text.insert(tk.END, f"   Artist: {playlist.artist}\n")
                self.playlist_text.insert(tk.END, f"   Duration: {self.format_duration(playlist.duration)}\n")
                self.playlist_text.insert(tk.END, f"   Channel: {playlist.channel}\n")
                self.playlist_text.insert(tk.END, f"   Popularity: {playlist.popularity} views\n")
                self.playlist_text.insert(tk.END, "\n")
                playlist = playlist.next
                song_number += 1
    
    #////////////////////////////////////////
    def binary_search_by_position(self, position):
        sorted_playlist = self.sort_playlist(lambda song: song.song_name.lower())
        left = 0
        right = len(sorted_playlist) - 1
        while left <= right:
            mid = left + (right - left) // 2
            mid_song = sorted_playlist[mid]
            mid_position = mid + 1
            if mid_position == position:
                return mid_song
            elif mid_position < position:
                left = mid + 1
            else:
                right = mid - 1
        return None
    def get_middle(self, playlist):
        if not playlist:
            return None
        slow = playlist
        fast = playlist
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow
    def merge_sort(self, playlist, key_function=lambda x: x, reverse=False):
        if not playlist or not playlist.next:
            return playlist
        middle = self.get_middle(playlist)
        second_half = middle.next
        middle.next = None
        # Recursively sort the first and second halves
        sorted_first_half = self.merge_sort(playlist, key_function=key_function, reverse=reverse)
        sorted_second_half = self.merge_sort(second_half, key_function=key_function, reverse=reverse)
        return self.merge(sorted_first_half, sorted_second_half, key_function=key_function, reverse=reverse)
    def merge(self, left, right, key_function=lambda x: x.song_name.lower(), reverse=False):
        if not left:
            return right
        if not right:
            return left
        if reverse:
            if key_function(left) > key_function(right):
                result = left
                result.next = self.merge(left.next, right, key_function=key_function, reverse=reverse)
            else:
                result = right
                result.next = self.merge(left, right.next, key_function=key_function, reverse=reverse)
        else:
            if key_function(left) < key_function(right):
                result = left
                result.next = self.merge(left.next, right, key_function=key_function, reverse=reverse)
            else:
                result = right
                result.next = self.merge(left, right.next, key_function=key_function, reverse=reverse)
        return result
    def sort_by_song_name_ascending(self):
        sorted_playlist = self.sort_playlist(lambda song: song.song_name.lower())
        self.display_playlist(sorted_playlist)
    def sort_by_song_name_descending(self):
        sorted_playlist = self.sort_playlist(lambda song: song.song_name.lower(), reverse=True)
        self.display_playlist(sorted_playlist)
    def sort_by_popularity_descending(self):
        sorted_playlist = self.sort_playlist(lambda song: song.popularity, reverse=True)
        self.display_playlist(sorted_playlist)
    def sort_by_popularity_ascending(self):
        sorted_playlist = self.sort_playlist(lambda song: song.popularity)
        self.display_playlist(sorted_playlist)
    def sort_playlist(self, key_function, reverse=False):
        if not self.playlist:
            return None
        # Convert linked list to a list for sorting
        playlist_list = []
        current_song = self.playlist
        while current_song:
            playlist_list.append(current_song)
            current_song = current_song.next
        sorted_playlist = sorted(playlist_list, key=key_function, reverse=reverse)
        self.sorted_playlist = sorted_playlist
        return sorted_playlist
    def save_playlist_data(self):
        if self.playlist:
            playlist_data = self.serialize_playlist(self.playlist)
            try:
                with open("playlist_data.json", 'w') as file:
                    json.dump(playlist_data, file)
            except IOError:
                messagebox.showerror("Error", "Failed to save playlist data.")
    def serialize_playlist(self, playlist):
        if not playlist:
            return []
        serialized_data = {
            'song_name': playlist.song_name,
            'artist': playlist.artist,
            'duration': playlist.duration,
            'channel': playlist.channel,
            'popularity': playlist.popularity}
        # Recursively serialize the rest of the playlist
        serialized_data['next'] = self.serialize_playlist(playlist.next) if playlist.next else []
        return [serialized_data]
    def create_playlist_from_data(self, playlist_data):
        if not playlist_data:
            return None
        playlist = Song(playlist_data[0]['song_name'], playlist_data[0]['artist'], playlist_data[0]['duration'], playlist_data[0]['channel'], playlist_data[0]['popularity'])
        next_song_data = playlist_data[0].get('next', [])
        if next_song_data:
            current = playlist
            for song_data in next_song_data:
                current.next = self.create_playlist_from_data([song_data])
                current = current.next
        return playlist
    
    def search_song(self):
            query = self.search_entry.get().strip()
            if query:
                search_results = self.find_songs_by_name(query)
                if search_results:
                    self.display_playlist(search_results)
                else:
                    messagebox.showinfo("Search Results", "No matching songs found.")
            else:
                messagebox.showerror("Search Error", "Please enter a search query.")

    def find_songs_by_name(self, query):
        matching_songs = []
        current_song = self.playlist

        while current_song:
            if query.lower() in current_song.song_name.lower():
                matching_songs.append(current_song)
            current_song = current_song.next

        return matching_songs

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()