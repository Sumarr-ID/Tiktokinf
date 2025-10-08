#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TikTok User Info Scraper (Sumarr ID Edition v2)

import re,os
import json
import requests
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.rule import Rule

console = Console()
logo = """ ╔╦╗╦╦╔═╔╦╗╔═╗╦╔═
  ║ ║╠╩╗ ║ ║ ║╠╩╗
  ╩ ╩╩ ╩ ╩ ╚═╝╩ ╩ scraper v0.1
 Author : Sumarr ID
 Github : https://github.com/Sumarr-ID
 Tiktok : @sumarr.id"""

# === Banner ===
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 5)
    console.print(Panel(logo, title="Info Tiktok", 
                          subtitle="© 2025 Publik Version", 
                          style="bold red"))
    

# === Fungsi konversi waktu ===
def to_date(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "N/A"

# === Format angka besar ===
def format_number(n):
    try:
        return f"{int(n):,}"
    except:
        return n

# === Fungsi utama ===
def get_tiktok_info(username):
    url = f"https://www.tiktok.com/@{username}?isUniqueId=true&isSecured=true"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        console.print("[red]❌ Gagal terhubung ke TikTok. Periksa koneksi internet Anda.[/red]")
        return

    if res.status_code != 200:
        console.print("[red]❌ Username tidak ditemukan atau akun privat.[/red]")
        return

    source = res.text

    def extract(pattern):
        m = re.search(pattern, source)
        return m.group(1) if m else None

    # Ambil data utama
    data = {
        "ID": extract(r'"id":"(\d+)"'),
        "Username": extract(r'"uniqueId":"([^"]+)"'),
        "Nickname": extract(r'"nickname":"([^"]+)"'),
        "Bio": extract(r'"signature":"([^"]*)"'),
        "Private": extract(r'"privateAccount":(true|false)'),
        "Verified": extract(r'"verified":(true|false)'),
        "Region": extract(r'"region":"([^"]+)"'),
        "Language": extract(r'"language":"([^"]+)"'),
        "Followers": format_number(extract(r'"followerCount":(\d+)')),
        "Following": format_number(extract(r'"followingCount":(\d+)')),
        "Hearts": format_number(extract(r'"heartCount":(\d+)')),
        "Videos": format_number(extract(r'"videoCount":(\d+)')),
        "Friends": format_number(extract(r'"friendCount":(\d+)')),
        "Created At": to_date(extract(r'"createTime":(\d+)')),
        "SecUID": extract(r'"secUid":"([^"]+)"'),
    }

    if not data["Username"]:
        console.print("[red]❌ Username tidak ditemukan atau akun privat.[/red]")
        return

    # Tampilkan tabel info
    table = Table(title=f"📱 TikTok Info for @{data['Username']}", title_style="bold bright_cyan")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for k, v in data.items():
        if v:
            table.add_row(k, str(v))

    console.print(table)
    console.print(Rule(style="bright_magenta"))

    # Tampilkan panel bio & link profil
    panel_content = f"[bold yellow]Bio:[/bold yellow]\n{data['Bio'] or 'N/A'}\n\n" \
                    f"[bold green]🔗 https://www.tiktok.com/@{data['Username']}[/bold green]"
    console.print(Panel(panel_content, title="[bold magenta]User Profile[/bold magenta]", border_style="bright_magenta"))

# === Jalankan ===
if __name__ == "__main__":
    banner()
    username = input("Masukkan username TikTok (tanpa @): ").strip()
    get_tiktok_info(username)