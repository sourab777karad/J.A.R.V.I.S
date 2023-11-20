# Importing necessary libraries
import subprocess       
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr                         
import pyttsx3                                          #text-to-speech library
import webbrowser
from googlesearch import search
from youtube_search import YoutubeSearch  # External library for searching YouTube

# Additional libraries for various functionalities
import random
import datetime
import psutil                       #retrieving information on running processes and system utlization
import sys 
import os

# Function to listen to user's voice command
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error connecting to Google API: {e}")
        return ""
    
    
# Function to speak responses to the user
def speak(text):
    engine = pyttsx3.init()
    
    # Setting up voice properties
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Index 1 typically corresponds to a female voice
    engine.say(text)
    engine.runAndWait()

# Function to check if the wake word is present in the user's command
def is_wake_word(command):
    return "hello jarvis" in command.lower()

# Function to extract the name from a "say hello to" command
def extract_name(command):
    parts = command.split("say hello to")
    if len(parts) > 1:
        return parts[1].strip()
    else:
        return None

# Function to open the YouTube website
def open_youtube():
    speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")

# Function to open a specified URL
def open_url(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

# Function to restart the Jarvis program
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
# Function to take a note and store it in a file
def take_note():
    speak("Sure, please dictate the note.")
    note = listen()

    with open("notes.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {note}\n")

    speak("Note added successfully!")

# Function to open the first video from a YouTube search query
def open_first_video(query):
    try:
        # Construct the YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query}"

        # Send a GET request to the search URL
        response = requests.get(search_url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first video link in the search results
        video_link = soup.find('a', {'id': 'video-title'}).get('href')
        # Construct the full video URL
        full_video_url = f"https://www.youtube.com{video_link}"
        # Open the first video using the default web browser
        subprocess.Popen(['open', full_video_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        speak(f"Error opening the first YouTube video: {e}")

# Function to search Google and open the first result
def search_google(query):
    speak(f"Searching Google for {query}.")

    try:
        search_results = list(search(query, num=1, stop=1))
        if search_results:
            open_url(search_results[0])
            page_title = get_page_info(search_results[0])
            if page_title:
                speak(f"The page is titled: {page_title}")
    except sr.UnknownValueError:
        speak("I'm sorry, I couldn't read the search result. Please check it manually.")
    except sr.RequestError as e:
        speak(f"Error connecting to Google API: {e}")

# Function to search YouTube and play the first video
def search_youtube(query):
    speak(f"Searching YouTube for {query}.")
    results = YoutubeSearch(query, max_results=1).to_dict()
    
    if results:
        video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
        speak("Playing the first video.")
        webbrowser.open(video_url)
    else:
        speak("Sorry, I couldn't find any videos.")

# Function to get system information (CPU usage, memory usage, battery percentage)
def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    battery_info = psutil.sensors_battery()

    system_info = f"CPU Usage: {cpu_usage}%\nMemory Usage: {memory_info.percent}%\n"
    if battery_info:
        system_info += f"Battery: {battery_info.percent}%"
    
    return system_info

# Main function to control the Jarvis program
def main():
    speak("Hello! I am Jarvis. Voice recognition required to activate.")

    while True:
        command = listen()

        if is_wake_word(command):
            speak("Voice recognition matched. Welcome SOURAB KARAD. How can I help you today?")
            
            while True:
                command = listen()

                if "close" in command:
                    speak("Goodbye!")
                    break
                if "jarvis" in command:
                    speak("Yes sir!")
                elif "say hello to" in command:
                    name = extract_name(command)
                    if name:
                        speak(f"Hello, sir or madam {name}! I am glad that you are a friend of Sourab sir. Hence you are a friend of mine.")
                    else:
                        speak("I'm sorry sir, I didn't catch the name.")
                elif "restart" in command:
                    speak("Restarting Jarvis.")
                    restart_program()
                elif "hello" in command:
                    speak("Hello there! How can I assist you?")
                elif "open notepad" in command:
                    speak("Opening Notepad.")
                    subprocess.Popen(["notepad.exe"])
                elif "open browser" in command:
                    speak("Opening web browser.")
                    webbrowser.open("https://www.google.com")  # Replace with your preferred website
                elif "open calculator" in command:
                    speak("Opening calculator.")
                    subprocess.Popen(["calc.exe"])
                elif "open spotify" in command:
                    speak("Opening Spotify.")
                    subprocess.Popen(["spotify.exe"])
                elif "how are you" in command:
                    speak("I'm just a program, but thanks for asking!")
                elif "scold him" in command:
                    speak("Is he your friend?")
                    if "yes" in command:
                        speak(random.choice(["Bitch.", "Chutiya.", "Bhosdike.", "Backchodi mat kar lode."]))
                    elif "no" in command:
                        speak("Sorry.")
                elif "open YouTube" in command:
                    open_youtube()
                elif "search for" in command:
                    try:
                        query = command.split("search for")[1].strip()
                        search_google(query)
                    except IndexError:
                        speak("I'm sorry, I didn't catch the search query.")
                elif "find" in command:
                    try:
                        query = command.split("find")[1].strip()
                        search_youtube(query)
                    except IndexError:
                        speak("I'm sorry, I didn't catch the YouTube search query.")
                elif "system info" in command:
                    system_info = get_system_info()
                    speak(system_info)
                elif "take a note" in command:
                    take_note()
                elif "take rest" in command:
                    speak("Okay, I'll stop listening. Say 'Jarvis' to wake me up again.")
                    break
                else:
                    speak("Pardon sir")
        
        elif "shutdown" in command:
            speak("Powering off. See you soon sir!")
            break

if __name__ == "__main__":
    main()
