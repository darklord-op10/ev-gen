import os
import asyncio
import requests
import zendriver as zd
import random
import string
import json
import re
import socket
import httpx
import base64
import tls_client
import time
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from dateutil.parser import isoparse
from colorama import Fore, Style, init
from pystyle import Colorate, Colors, Center
import websocket
from notifypy import Notify
from tls_client import Session
import warnings
import sys
import logging

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)

import asyncio
asyncio.get_event_loop().set_exception_handler(lambda loop, context: None)

init(autoreset=True)

INCOGNITO_API = "https://api.incognitomail.co/"

sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

def send_notification(title, message):
    try:
        notification = Notify()
        notification.application_name = "Kyra evs gen"
        notification.title = title
        notification.message = message
        notification.send()
    except Exception as e:
        pass

def log(type, message):
    if type.upper() in ["SUCCESS", "ERROR"]:
        now = datetime.now().strftime("%H:%M:%S")
        type_map = {
            "SUCCESS": Fore.GREEN + "SUCCESS" + Style.RESET_ALL,
            "ERROR": Fore.RED + "ERROR" + Style.RESET_ALL
        }
        tag = type_map.get(type.upper(), type.upper())
        print(f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {tag} • {message}")

def log(type, message):
    now = datetime.now().strftime("%H:%M:%S")
    type_map = {
        "SUCCESS": Fore.GREEN + "SUCCESS" + Style.RESET_ALL,
        "ERROR": Fore.RED + "ERROR" + Style.RESET_ALL,
        "INFO": Fore.CYAN + "INFO" + Style.RESET_ALL,
        "WARNING": Fore.YELLOW + "WARNING" + Style.RESET_ALL,
        "INPUT": Fore.MAGENTA + "INPUT" + Style.RESET_ALL
    }
    tag = type_map.get(type.upper(), type.upper())

    if type.upper() == "INFO":
        message = f"{Fore.LIGHTBLACK_EX}{message}{Style.RESET_ALL}"
    elif type.upper() == "INPUT":
        pass
    elif ':' in message:
        parts = message.split(':', 1)
        key = parts[0].upper().strip()
        val = parts[1].strip()
        message = f"{key}: {Fore.LIGHTBLACK_EX}{val}{Style.RESET_ALL}"

    print(f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {tag} • {message}")

def console_title(title="#1 EVS GEN - Kyra ^| .gg/leak-hub ^| @trainedtobeef ^| @composee"):
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end='', flush=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cleanup_zendriver():
    try:
        import gc
        gc.collect()
        
        try:
            import zendriver as zd
            zd.stop_all()
        except (ValueError, Exception):
            pass
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        
        all_tasks = asyncio.all_tasks(loop)
        zendriver_tasks = []
        other_tasks = []
        
        for task in all_tasks:
            if not task.done():
                task_name = str(task)
                if any(keyword in task_name.lower() for keyword in ['listener_loop', 'zendriver', 'websocket', 'connection']):
                    zendriver_tasks.append(task)
                else:
                    other_tasks.append(task)
        
        for task in zendriver_tasks:
            try:
                task.cancel()
            except:
                pass
        
        for task in other_tasks:
            try:
                task.cancel()
            except:
                pass
        
        if zendriver_tasks:
            try:
                done, pending = loop.run_until_complete(
                    asyncio.wait(zendriver_tasks, timeout=1.0, return_when=asyncio.ALL_COMPLETED)
                )
                
                for task in done:
                    try:
                        if not task.cancelled():
                            task.result()
                    except (ValueError, ConnectionError, OSError, asyncio.CancelledError):
                        pass
                    except Exception:
                        pass
                
                for task in pending:
                    try:
                        task.cancel()
                    except:
                        pass
                        
            except (asyncio.TimeoutError, asyncio.CancelledError, RuntimeError):
                pass
            except Exception:
                pass
        
        if other_tasks:
            try:
                done, pending = loop.run_until_complete(
                    asyncio.wait(other_tasks, timeout=0.5, return_when=asyncio.ALL_COMPLETED)
                )
                
                for task in pending:
                    try:
                        task.cancel()
                    except:
                        pass
                        
            except (asyncio.TimeoutError, asyncio.CancelledError, RuntimeError):
                pass
            except Exception:
                pass
        
        gc.collect()
                
    except Exception:
        pass

async def async_cleanup_zendriver():
    try:
        import gc
        gc.collect()
        
        try:
            import zendriver as zd
            zd.stop_all()
        except (ValueError, Exception):
            pass
        
        await asyncio.sleep(0.3)
        
        try:
            loop = asyncio.get_running_loop()
            all_tasks = asyncio.all_tasks(loop)
            
            zendriver_tasks = []
            other_tasks = []
            
            for task in all_tasks:
                if not task.done():
                    task_name = str(task)
                    if any(keyword in task_name.lower() for keyword in ['listener_loop', 'zendriver', 'websocket', 'connection']):
                        zendriver_tasks.append(task)
                    else:
                        other_tasks.append(task)
            
            for task in zendriver_tasks:
                try:
                    task.cancel()
                except:
                    pass
            
            if zendriver_tasks:
                try:
                    done, pending = await asyncio.wait(zendriver_tasks, timeout=1.0, return_when=asyncio.ALL_COMPLETED)
                    
                    for task in done:
                        try:
                            if not task.cancelled():
                                task.result()
                        except (ValueError, ConnectionError, OSError, asyncio.CancelledError):
                            pass
                        except Exception:
                            pass
                    
                    for task in pending:
                        try:
                            task.cancel()
                        except:
                            pass
                except:
                    pass
            
            for task in other_tasks:
                try:
                    task.cancel()
                except:
                    pass
            
            if other_tasks:
                try:
                    await asyncio.wait(other_tasks, timeout=0.2, return_exceptions=True)
                except:
                    pass
                    
        except RuntimeError:
            pass
        
        gc.collect()
                
    except Exception:
        pass

def Slow(text, delay=0.03):
    lines = text.split('\n')
    for line in lines:
        print(line)
        time.sleep(delay)

def vg(lines, start_rgb=(0, 255, 200), end_rgb=(0, 100, 180)):
    total = len(lines)
    result = []
    for i, line in enumerate(lines):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i // max(1, total - 1)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i // max(1, total - 1)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i // max(1, total - 1)
        result.append(f'\033[38;2;{r};{g};{b}m{line}\033[0m')
    return result

def al():
    ascii_art = [
        "███████╗██╗     ███████╗ ██████╗████████╗██████╗  ██████╗ ███╗   ██╗",
        "██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║",
        "█████╗  ██║     █████╗  ██║        ██║   ██████╔╝██║   ██║██╔██╗ ██║",
        "██╔══╝  ██║     ██╔══╝  ██║        ██║   ██╔══██╗██║   ██║██║╚██╗██║",
        "███████╗███████╗███████╗╚██████╗   ██║   ██║  ██║╚██████╔╝██║ ╚████║",
        "╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝"
    ]

    print('\n' * 2)
    gradient_lines = vg(ascii_art)
    ascii_text = '\n'.join([Center.XCenter(colored_line) for colored_line in gradient_lines])
    Slow(ascii_text, delay=0.05)
    print('\n' * 2)

def grs(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def ru():
    return 'kyra' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def get_inp(prompt):
    now = datetime.now().strftime("%H:%M:%S")
    input_text = f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {Fore.MAGENTA}INPUT{Style.RESET_ALL} • {Fore.MAGENTA}{prompt}{Style.RESET_ALL}"
    return input(input_text)

class IncognitoMailClient:
    def __init__(self, domain="vorlentis.xyz"):
        self.email = None
        self.inbox_id = None
        self.inbox_token = None
        self.session = requests.Session()
        self.secret_key = None
        self.domain = domain
        self._initialize_secret()

    def _initialize_secret(self):
        scrambled = "4O)QqiTV+(U+?Vi]qe|6..Xe"
        self.secret_key = ''.join([chr(ord(c) - 2) for c in scrambled])

    def _sign_payload(self, payload: dict) -> str:
        message = json.dumps(payload, separators=(',', ':')).encode()
        key = self.secret_key.encode()
        return hmac.new(key, message, hashlib.sha256).hexdigest()

    def _get_random_fr_ip(self):
        return f"90.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

    def debug_inbox_status(self):
        if not self.inbox_id or not self.inbox_token:
            log("ERROR", "No inbox credentials for debugging")
            return False
            
        try:
            ts = int(time.time() * 1000)
            payload = {
                "inboxId": self.inbox_id,
                "inboxToken": self.inbox_token,
                "ts": ts
            }
            payload["key"] = self._sign_payload(payload)
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.post(
                f"{INCOGNITO_API}inbox/v1/list", 
                json=payload, 
                headers=headers, 
                timeout=10
            )
            
            log("INFO", f"API Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                log("INFO", f"Inbox accessible, {len(items)} emails found")
                
                for i, item in enumerate(items[:3]):
                    log("INFO", f"Email {i+1}: messageURL present = {bool(item.get('messageURL'))}")
                    
                return True
            else:
                log("ERROR", f"API Error: {response.text[:100]}")
                return False
                
        except Exception as e:
            log("ERROR", f"Exception: {e}")
            return False

    async def create_temp_email(self):
        for attempt in range(1, 3):
            try:
                timestamp = int(time.time() * 1000)
                payload = {
                    "ts": timestamp,
                    "domain": self.domain
                }
                payload["key"] = self._sign_payload(payload)
                
                fake_ip = self._get_random_fr_ip()
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
                    "X-Forwarded-For": fake_ip,
                    "X-Real-IP": fake_ip,
                    "Via": fake_ip
                }
                
                response = httpx.post(
                    f"{INCOGNITO_API}inbox/v2/create", 
                    json=payload, 
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "id" in data and "token" in data:
                        self.inbox_id = data["id"]
                        self.inbox_token = data["token"]
                        self.email = self.inbox_id
                        log("SUCCESS", f"Email created: {self.email}")
                        return self.email
                
            except Exception as e:
                if attempt == 2:
                    log("ERROR", f"Failed to create email: {e}")
                await asyncio.sleep(2)
                    
        return None

    def check_verification_email(self):
        if not self.inbox_id or not self.inbox_token:
            return None
            
        for attempt in range(1, 30):
            try:
                ts = int(time.time() * 1000)
                payload = {
                    "inboxId": self.inbox_id,
                    "inboxToken": self.inbox_token,
                    "ts": ts
                }
                payload["key"] = self._sign_payload(payload)
                
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                response = requests.post(
                    f"{INCOGNITO_API}inbox/v1/list", 
                    json=payload, 
                    headers=headers, 
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    
                    if items:
                        for item in items:
                            message_url = item.get("messageURL")
                            if message_url:
                                try:
                                    email_data = requests.get(message_url, timeout=5).json()
                                    subject = email_data.get("subject", "")
                                    
                                    if "verify" in subject.lower():
                                        content = str(email_data.get("text", "")) + str(email_data.get("html", ""))
                                        
                                        patterns = [
                                            r'https:\/\/click\.discord\.com[^\s"\'\'<>\\]+',
                                            r'https://click\.discord\.com[^\s"\'\'<>\\]+',
                                            r'https://discord\.com/verify[^\s"\'\'<>\\]+'
                                        ]
                                        
                                        for pattern in patterns:
                                            match = re.search(pattern, content)
                                            if match:
                                                link = match.group(0).replace('\\/', '/').split("\n")[0].strip()
                                                link = link.replace('&amp;', '&')
                                                log("SUCCESS", "Verification link found")
                                                return link
                                except:
                                    continue
                    
            except:
                pass
            
            time.sleep(0.5)
        
        log("ERROR", "Verification email not received")
        return None

def check_chrome_installation():
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return True
    
    log("ERROR", "Chrome not found")
    return False


class BrowserManager:
    def __init__(self):
        self.browser = None

    async def start(self, url):
        self.browser = await zd.start()
        page = await self.browser.get(url)
        await page.wait_for_ready_state('complete', timeout=30000)
        log("SUCCESS", "Registration page opened")
        return page

    async def stop(self):
        if self.browser:
            try:
                await self.browser.stop()
            except Exception as e:
                pass
            finally:
                self.browser = None
            log("SUCCESS", "Browser terminated")

class DiscordFormFiller:
    def __init__(self, domain="vorlentis.xyz"):
        self.mail_client = IncognitoMailClient(domain)
        self.browser_mgr = BrowserManager()
        self.password = None
        self.email = None
        self.token = None

    async def fill_form(self):
        start_time = time.time()
        try:
            send_notification("Kyra Evs Gen", "Generating new account...")
            
            email = await self.mail_client.create_temp_email()
            if not email:
                send_notification("Error", "Failed to create temporary email")
                log("ERROR", "Failed to create email")
                return None

            self.email = email
            page = await self.browser_mgr.start("https://discord.com/register")

            try:
                await self._fill_basic_fields(page, email)
                log("SUCCESS", "Fields filled!")
                
                await self._select_birth_date(page)
                
                await self._wait_for_captcha_completion(page)
                
                token = await self._verify_email()
                
                if token:
                    end_time = time.time()
                    time_taken = end_time - start_time
                    return token, time_taken
                else:
                    send_notification("Error", "Failed to complete account verification")
                    return None, 0
                
            except Exception as e:
                log("ERROR", f"Form filling failed: {e}")
                try:
                    await self.browser_mgr.stop()
                except Exception as cleanup_error:
                    log("WARNING", f"Browser cleanup failed: {cleanup_error}")
                return None, 0
                
        except Exception as e:
            log("ERROR", f"Account generation failed: {e}")
            try:
                await self.browser_mgr.stop()
            except:
                pass
            return None, 0
            
    async def _countdown_timer(self, duration):
        for i in range(duration):
            remaining = duration - i
            log("INFO", f"Waiting... {remaining}s remaining")
            await asyncio.sleep(1)

    async def _fill_basic_fields(self, page, email):
        display_name = "kyra is legit"
        username = ru()
        password = self.mail_client.inbox_token
        
        if not password:
            password = "maker" + grs(8) + "@7836"

        email_field = await page.wait_for('input[name="email"]', timeout=15000)
        await email_field.send_keys(self.mail_client.inbox_id)
        await asyncio.sleep(0.02)

        display_name_field = await page.wait_for('input[name="global_name"]', timeout=15000)
        await display_name_field.send_keys(display_name)
        await asyncio.sleep(0.02)

        username_field = await page.wait_for('input[name="username"]', timeout=15000)
        await username_field.send_keys(username)
        await asyncio.sleep(0.02)

        password_field = await page.wait_for('input[name="password"]', timeout=15000)
        await password_field.send_keys(password)
        
        self.password = password
        self.email = self.mail_client.inbox_id

    async def _select_birth_date(self, page):
        try:
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            random_year = random.randint(1995, 2000)
            random_day = random.randint(1, 28)

            month_attempts = 0
            while month_attempts < 3:
                month_attempts += 1
                random_month = random.choice(months)
                try:
                    month_dropdown = await page.wait_for('div[role="button"][aria-label="Month"]', timeout=15000)
                    await month_dropdown.click()
                    await asyncio.sleep(0.1)

                    month_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            month_map = {"january": 0, "february": 1, "march": 2, "april": 3, "may": 4, "june": 5,
                                         "july": 6, "august": 7, "september": 8, "october": 9, "november": 10, "december": 11}
                            month_index = month_map.get(random_month.lower(), 0)
                            if 0 <= month_index < len(options):
                                month_option = options[month_index]
                            if not month_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and random_month.lower() in text_content.strip().lower():
                                            month_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding month options: {e}")

                    if month_option:
                        await month_option.click()
                        break
                    else:
                        log("WARNING", f"Retrying month")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Month dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            day_attempts = 0
            while day_attempts < 3:
                day_attempts += 1
                try:
                    day_dropdown = await page.wait_for('div[role="button"][aria-label="Day"]', timeout=15000)
                    await day_dropdown.click()
                    await asyncio.sleep(0.1)

                    day_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            day_index = min(random_day - 1, len(options) - 1)
                            if 0 <= day_index < len(options):
                                day_option = options[day_index]
                            if not day_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and str(random_day) in text_content.strip():
                                            day_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding day options: {e}")

                    if day_option:
                        await day_option.click()
                        break
                    else:
                        random_day = random.randint(1, 28)
                        log("WARNING", f"Retrying day")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Day dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            year_attempts = 0
            while year_attempts < 3:
                year_attempts += 1
                try:
                    year_dropdown = await page.wait_for('div[role="button"][aria-label="Year"]', timeout=15000)
                    await year_dropdown.click()
                    await asyncio.sleep(0.1)

                    year_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            current_year = 2024
                            year_index = current_year - random_year
                            if 0 <= year_index < len(options):
                                year_option = options[year_index]
                            if not year_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and str(random_year) in text_content.strip():
                                            year_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding year options: {e}")

                    if year_option:
                        await year_option.click()
                        log("SUCCESS", "Selected Dob")
                        break
                    else:
                        random_year = random.randint(1995, 2002)
                        log("WARNING", f"Retrying year")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Year dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            checkbox = await page.query_selector('input[type="checkbox"]')
            if checkbox:
                await checkbox.click()
                await asyncio.sleep(0.1)

            submit_btn = await page.query_selector('button[type="submit"]')
            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(1)


        except Exception as e:
            log("ERROR", f"Birth date selection failed: {e}")

    async def _wait_for_captcha_completion(self, page):
        try:
            await asyncio.sleep(0.2)
            
            captcha_detected = False
            for attempt in range(120):
                try:
                    captcha_elements = [
                        'iframe[src*="hcaptcha"]',
                        'iframe[src*="recaptcha"]',
                        'iframe[title*="captcha"]',
                        'iframe[title*="CAPTCHA"]',
                        'div[class*="captcha"]',
                        'div[id*="captcha"]',
                        'div[id*="CAPTCHA"]',
                        '.h-captcha',
                        '.g-recaptcha',
                        '[data-sitekey]'
                    ]
                    
                    captcha_found = False
                    sitekey_value = None
                    for selector in captcha_elements:
                        try:
                            captcha = await page.query_selector(selector)
                            if captcha:
                                is_visible = True
                                try:
                                    is_visible = await captcha.is_visible()
                                except:
                                    pass
                                if is_visible:
                                    captcha_found = True
                                    try:
                                        if selector == '[data-sitekey]':
                                            sitekey_value = await page.evaluate('(el) => el.getAttribute("data-sitekey")', captcha)
                                    except:
                                        pass
                                    break
                        except:
                            continue
                    
                    if captcha_found and not captcha_detected:
                        if sitekey_value:
                            log("INFO", f"Captcha detected (sitekey: {sitekey_value[:10]}...)")
                        else:
                            log("INFO", "Captcha detected")
                        send_notification("Captcha Detected", "Please solve the captcha to continue!")
                        captcha_detected = True
                    
                    if not captcha_found:
                        if captcha_detected:
                            log("SUCCESS", "Captcha solved successfully!")
                            try:
                                await self.browser_mgr.stop()
                            except:
                                pass
                        return True
                    
                    await asyncio.sleep(0.5)
                        
                except Exception:
                    pass
                    
            return True
            
        except Exception as e:
            return True

    async def get_token(self, inbox_id=None, inbox_token=None, save_to_files=True):
        try:
            login_id = inbox_id or self.mail_client.inbox_id
            login_password = inbox_token or self.mail_client.inbox_token
            
            if not login_id or not login_password:
                return None
                
            payload = {
                'login': login_id,
                'password': login_password
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Origin': 'https://discord.com',
                'Referer': 'https://discord.com/login'
            }
            
            res = requests.post('https://discord.com/api/v9/auth/login', json=payload, headers=headers)
            
            if res.status_code == 200:
                try:
                    response_data = res.json()
                    if 'token' in response_data:
                        token = response_data['token']
                        if save_to_files:
                            token_display = f"{token[:24]}{'*' * 12}"
                            log("SUCCESS", f"TOKEN: {token_display}")
                            os.makedirs("output", exist_ok=True)
                            with open("output/tokens.txt", "a", encoding="utf-8") as tf:
                                tf.write(token + "\n")
                            with open("output/accounts.txt", "a", encoding="utf-8") as af:
                                af.write(f"{login_id}:{login_password}:{token}\n")
                            with open("output/itok.txt", "a", encoding="utf-8") as itf:
                                itf.write(f"{self.mail_client.inbox_token}\n")
                            self.token = token
                        return token
                except json.JSONDecodeError:
                    pass
                
        except Exception:
            pass
        return None

    def _save_credentials(self, token):
        try:
            os.makedirs("output", exist_ok=True)
            with open("output/tokens.txt", "a", encoding="utf-8") as tf:
                tf.write(token + "\n")
            with open("output/accounts.txt", "a", encoding="utf-8") as af:
                af.write(f"{self.mail_client.inbox_id}:{self.mail_client.inbox_token}:{token}\n")
            with open("output/itok.txt", "a", encoding="utf-8") as itf:
                itf.write(f"{self.mail_client.inbox_token}\n")
            self.token = token
        except Exception:
            pass

    def _remove_saved_credentials(self, token):
        try:
            patterns = [
                token,
                str(self.mail_client.inbox_token) if self.mail_client and self.mail_client.inbox_token else None,
                str(self.mail_client.inbox_id) if self.mail_client and self.mail_client.inbox_id else None
            ]
            patterns = [p for p in patterns if p]
            files = [
                ("output/tokens.txt", lambda line: token in line),
                ("output/accounts.txt", lambda line: any(p in line for p in patterns)),
                ("output/itok.txt", lambda line: any(p in line for p in patterns))
            ]
            for filepath, matcher in files:
                try:
                    if not os.path.exists(filepath):
                        continue
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    with open(filepath, 'w', encoding='utf-8') as f:
                        for line in lines:
                            if not matcher(line):
                                f.write(line)
                except Exception:
                    continue
        except Exception:
            pass

    def verify_st(self, token):
        url = "https://discord.com/api/v9/users/@me"
        headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                verified = data.get("verified", False)
                email = data.get("email", "No Email")
                return verified, email
            else:
                return None, None
        except:
            return None, None

    def lock_dtc(self, token):
        url = "https://discordapp.com/api/v9/users/@me/library"
        headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code
        except:
            return None

    async def _verify_email(self):
        for attempt in range(150):
            verification_link = self.mail_client.check_verification_email()
            if verification_link:
                break
            await asyncio.sleep(0.05)
        
        if not verification_link:
            return None

        verification_browser = None
        try:
            log("SUCCESS", "Opening verification link...")
            try:
                await self.browser_mgr.stop()
            except:
                pass
            verification_browser = await zd.start()
            page = await verification_browser.get(verification_link)
            await asyncio.sleep(0.2)


            token = None
            for check_attempt in range(80):
                token = await self.get_token(self.mail_client.inbox_id, self.mail_client.inbox_token, save_to_files=False)
                if token:
                    break
                await asyncio.sleep(0.02)

            if not token:
                return None

            verification_complete = False
            
            for verify_attempt in range(300):
                verified, email_address = self.verify_st(token)
                if verified:
                    verification_complete = True
                    log("SUCCESS", "Email verified successfully!")
                    
                    library_status = self.lock_dtc(token)
                    if library_status == 403:
                        token_display = f"{token[:24]}{'*' * 12}"
                        log("WARNING", f"Locked Token: {Fore.LIGHTBLACK_EX}{token_display}{Style.RESET_ALL}")
                        self._remove_saved_credentials(token)
                        log("SUCCESS", "Exiting!")
                        return "LOCKED"
                    break
                await asyncio.sleep(0.01)
            
            if not verification_complete:
                return None
                
            try:
                await verification_browser.stop()
            except:
                pass
            
            try:
                token_display = f"{token[:24]}{'*' * 12}"
                log("SUCCESS", f"TOKEN: {token_display}")
            except Exception:
                pass
            self._save_credentials(token)
            return token
            
        except Exception as e:
            return None
        finally:
            if verification_browser:
                try:
                    await verification_browser.stop()
                except:
                    pass

    async def _wait_for_verification_captcha_completion(self, page):
        return True

async def main():
    clear_screen()
    console_title()
    
    import warnings
    import sys
    from contextlib import redirect_stderr
    import io
    
    class ZendriverErrorFilter:
        def __init__(self, original_stderr):
            self.original_stderr = original_stderr
            
        def write(self, message):
            if any(keyword in message.lower() for keyword in [
                'task exception was never retrieved',
                'listener.listener_loop',
                'no websocket connection',
                'zendriver',
                'connection.py'
            ]):
                return
            self.original_stderr.write(message)
            
        def flush(self):
            self.original_stderr.flush()
    
    sys.stderr = ZendriverErrorFilter(sys.stderr)
    
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            domain = config.get("domain", "vorlentis.xyz").strip()
            vpn_enabled = config.get("vpn", True)
    except:
        log("ERROR", "FAILED TO LOAD CONFIG.JSON")
        return

    print()
    
    if not check_chrome_installation():
        log("ERROR", "Chrome not installed")
        log("INFO", "Press Enter to exit...")
        input()
        return

    al()
    
    try:
        max_runs = int(get_inp("How many accounts to gen 0 = ∞: "))
    except ValueError:
        max_runs = 1
    
    run_count = 0
    total_start_time = time.time()
    successful_tokens = 0
    
    try:
        while True:
            if max_runs != 0 and run_count >= max_runs:
                break
                
            run_count += 1
            log("SUCCESS", f"Starting account {run_count} generation...")
            
            try:
                filler = DiscordFormFiller(domain)
                result = await filler.fill_form()
                
                if result and len(result) == 2:
                    token, time_taken = result
                    if token == "LOCKED":
                        successful_tokens += 1
                        break
                    elif token:
                        log("SUCCESS", f"Account created successfully ({Fore.GREEN}{time_taken:.1f}s{Style.RESET_ALL})")
                        successful_tokens += 1
                    else:
                        log("ERROR", f"Account {run_count} generation failed")
                else:
                    log("ERROR", f"Account {run_count} generation failed")
            except asyncio.CancelledError:
                break
            except Exception as e:
                log("ERROR", f"Account generation error: {e}")
                continue

            if max_runs == 1:
                try:
                    await asyncio.sleep(2)
                except asyncio.CancelledError:
                    break
                break
            elif max_runs != 0 and run_count >= max_runs:
                try:
                    await asyncio.sleep(2)
                except asyncio.CancelledError:
                    break
                break
            else:
                if vpn_enabled:
                    log("INFO", "Waiting for 10 secs change ur ip....")
                    try:
                        await asyncio.sleep(10)
                    except asyncio.CancelledError:
                        break
                else:
                    log("INFO", "Waiting for 100 secs....")
                    try:
                        await asyncio.sleep(100)
                    except asyncio.CancelledError:
                        break
                
    except KeyboardInterrupt:
        log("SUCCESS", "Exiting...")
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
    except asyncio.CancelledError:
        pass
    except Exception as e:
        log("ERROR", f"Generation error: {e}")
        try:
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            pass
    finally:
        try:
            await async_cleanup_zendriver()
        except Exception:
            pass
    
    total_end_time = time.time()
    total_time_taken = total_end_time - total_start_time
    log("INFO", f"Generated {successful_tokens} valid tokens in {Fore.WHITE}({Fore.GREEN}{total_time_taken:.1f}s{Fore.WHITE}){Style.RESET_ALL}")
    
    try:
        await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass
    
    try:
        await async_cleanup_zendriver()
        await asyncio.sleep(0.5)
        
        try:
            loop = asyncio.get_running_loop()
            remaining_tasks = [task for task in asyncio.all_tasks(loop) if not task.done()]
            
            zendriver_tasks = []
            other_tasks = []
            
            for task in remaining_tasks:
                task_name = str(task)
                if any(keyword in task_name.lower() for keyword in ['listener_loop', 'zendriver', 'websocket', 'connection']):
                    zendriver_tasks.append(task)
                else:
                    other_tasks.append(task)
            
            for task in remaining_tasks:
                try:
                    task.cancel()
                except:
                    pass
            
            if zendriver_tasks:
                try:
                    done, pending = await asyncio.wait(zendriver_tasks, timeout=1.0, return_when=asyncio.ALL_COMPLETED)
                    
                    for task in done:
                        try:
                            if not task.cancelled():
                                task.result()
                        except (ValueError, ConnectionError, OSError, asyncio.CancelledError):
                            pass
                        except Exception:
                            pass
                except:
                    pass
            
            if other_tasks:
                try:
                    await asyncio.gather(*other_tasks, return_exceptions=True)
                except:
                    pass
        except:
            pass
            
    except Exception:
        pass

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    
    def suppress_exceptions(loop, context):
        exception = context.get('exception')
        if exception and isinstance(exception, (ValueError, ConnectionError, OSError)):
            if 'websocket' in str(exception).lower() or 'connection' in str(exception).lower():
                return
        pass
    
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(suppress_exceptions)
        
        try:
            import asyncio_atexit
            try:
                asyncio_atexit.unregister(loop=None)
            except Exception:
                pass
        except Exception:
            pass
        
        try:
            loop.run_until_complete(main())
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            log("INFO", "Interrupted by user")
        except Exception as e:
            if not any(keyword in str(e).lower() for keyword in ['websocket', 'connection', 'zendriver']):
                print(f"Error: {e}")
        finally:
            try:
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except:
                pass
            try:
                loop.close()
            except Exception:
                pass
            
    except Exception as e:
        if not any(keyword in str(e).lower() for keyword in ['websocket', 'connection', 'zendriver']):
            print(f"Critical error: {e}")
    finally:
        try:
            cleanup_zendriver()
        except Exception:
            pass
        
        log("INFO", "Press Enter to exit...")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass