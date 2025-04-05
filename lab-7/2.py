import pygame
import time

pygame.init()

pygame.mixer.init()

music_files = ["Ezio's Family.mp3", "I Am Rock.mp3", "Overworld Day.mp3"]
current_track = 0


screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)

def display_text(text):
    screen.fill((0, 0, 0))
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (50, 80))
    pygame.display.update()

def play_music(track):
    pygame.mixer.music.load(music_files[track])
    pygame.mixer.music.play()
    display_text(f"Playing: {music_files[track]}")

def stop_music():
    pygame.mixer.music.stop()
    display_text("Music Stopped")

def next_track():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    play_music(current_track)

def previous_track():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    play_music(current_track)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_p]:
        if not pygame.mixer.music.get_busy():
            play_music(current_track)
    elif keys[pygame.K_s]:
        stop_music()
    elif keys[pygame.K_n]:
        next_track()
    elif keys[pygame.K_b]:
        previous_track()

    time.sleep(0.1)