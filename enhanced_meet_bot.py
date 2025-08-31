import asyncio
import sys
import os
import json
import threading
import time
from playwright.async_api import async_playwright
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class NiaMeetBot:
    def __init__(self):
        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize Gemini AI
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Bot state
        self.is_listening = False
        self.conversation_context = []
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 Nia says: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_for_speech(self):
        """Listen for speech input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        print(f"👤 Heard: {text}")
                        self.process_speech(text)
                        
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Speech recognition error: {e}")
                    
        except Exception as e:
            print(f"Microphone setup error: {e}")
    
    def process_speech(self, text):
        """Process heard speech and generate response"""
        # Add to conversation context
        self.conversation_context.append(f"Human: {text}")
        
        # Generate AI response
        context = "\n".join(self.conversation_context[-10:])  # Keep last 10 exchanges
        prompt = f"""
        You are Nia, an AI assistant in a Google Meet call. 
        Respond naturally and helpfully to the conversation.
        Keep responses concise and conversational.
        
        Recent conversation:
        {context}
        
        Respond to the latest message:
        """
        
        try:
            response = self.model.generate_content(prompt)
            ai_response = response.text.strip()
            
            self.conversation_context.append(f"Nia: {ai_response}")
            self.speak(ai_response)
            
        except Exception as e:
            print(f"AI response error: {e}")
            self.speak("Sorry, I'm having trouble processing that right now.")

    async def join_meeting(self, meet_link):
        """Join Google Meet with enhanced capabilities"""
        async with async_playwright() as p:
            # Launch browser with audio permissions
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--use-fake-ui-for-media-stream',
                    '--use-fake-device-for-media-stream',
                    '--allow-running-insecure-content',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            context = await browser.new_context(
                permissions=['microphone', 'camera']
            )
            
            page = await context.new_page()
            
            try:
                print(f"🔗 Navigating to: {meet_link}")
                await page.goto(meet_link)
                
                # Wait for page to load
                await page.wait_for_timeout(3000)
                
                # Handle different Google Meet UI states
                await self.handle_meet_ui(page)
                
                # Start speech recognition in background
                self.is_listening = True
                speech_thread = threading.Thread(target=self.listen_for_speech)
                speech_thread.daemon = True
                speech_thread.start()
                
                self.speak("Hello everyone! Nia has joined the meeting.")
                
                # Keep the meeting alive
                print("✅ Nia is now in the meeting and listening...")
                await page.wait_for_timeout(1800000)  # Stay for 30 minutes
                
            except Exception as e:
                print(f"❌ Error during meeting: {e}")
                self.speak("I'm having trouble with the meeting connection.")
            
            finally:
                self.is_listening = False
                await browser.close()

    async def handle_meet_ui(self, page):
        """Handle various Google Meet UI elements"""
        try:
            # Wait for the page to stabilize
            await page.wait_for_timeout(2000)
            
            # Try to turn off camera and microphone
            camera_selectors = [
                '[aria-label*="camera" i][aria-label*="off" i]',
                '[aria-label*="Turn off camera"]',
                '[data-tooltip*="camera"]'
            ]
            
            mic_selectors = [
                '[aria-label*="microphone" i][aria-label*="off" i]',
                '[aria-label*="Turn off microphone"]',
                '[data-tooltip*="microphone"]'
            ]
            
            for selector in camera_selectors:
                try:
                    await page.click(selector, timeout=1000)
                    print("📷 Camera turned off")
                    break
                except:
                    continue
            
            for selector in mic_selectors:
                try:
                    await page.click(selector, timeout=1000)
                    print("🎤 Microphone turned off")
                    break
                except:
                    continue
            
            # Try to join the meeting
            join_selectors = [
                'text="Join now"',
                'text="Ask to join"',
                '[aria-label*="Join"]',
                'button:has-text("Join")'
            ]
            
            for selector in join_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    print("🚪 Clicked join button")
                    break
                except:
                    continue
            
            # Wait a bit for the meeting to load
            await page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"⚠️ UI handling error: {e}")

async def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python enhanced_meet_bot.py <meeting_link>")
        return
    
    meet_link = sys.argv[1]
    bot = NiaMeetBot()
    await bot.join_meeting(meet_link)

if __name__ == "__main__":
    asyncio.run(main())