import os
import pygame


class SoundManager:

  def __init__(self, sound_path="assets/sonar_ping.wav"):
    self.sound_path = sound_path
    self.sound = None
    self.enabled = True

    try:
      # Initialize pygame mixer for audio playback
      if not pygame.mixer.get_init():
        pygame.mixer.init()

      if os.path.exists(self.sound_path):
        self.sound = pygame.mixer.Sound(self.sound_path)
      else:
        print(f"[Warning] Sound file not found at {self.sound_path}. Muting audio.")
        self.enabled = False
    except Exception as e:
      print(f"[Warning] Could not initialize sound manager: {e}")
      self.enabled = False

  def play_ping(self):
    """Plays the radar sonar ping sound effect if enabled."""
    if self.enabled and self.sound:
      try:
        self.sound.play()
      except Exception as e:
        print(f"[Error] Failed to play sound: {e}")

  def toggle_audio(self, state: bool):
    """Enables or disables audio playback dynamically."""
    self.enabled = state