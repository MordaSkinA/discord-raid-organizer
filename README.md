**BOT IS STILL IN DEVELOPEMENT**
A feature-rich Discord bot built with **Disnake** for managing guild events, raid sign-ups, and roster management in MMORPG *Where Winds Meet* for NA-guild

---

## Features

### Event Creation & Presets
- **Customizable Presets**: Preset templates for **Guild War / Siege**, **World Boss**, **Dungeon / Raid**, and **Custom Events**.
- **Timezone Selection**: Pre-configured IANA timezones (Europe, America, CIS, Asia, UTC) via dropdown slash commands to prevent manual entry errors.
- **Dynamic Time Stamps**: Uses Discord's native `<t:timestamp:R>` for localized countdowns across all member timezones.
- **Roster Limits**: Configurable main roster participant limits with automated waitlist (Bench) handling.

### Profile & One-Click Sign-Up
- **`/profile` Management**: Members can save their preferred **Role** and **Build** once.
- **Instant Sign-Up**: Click **Join Event** to immediately register with pre-saved profile settings.
- **Build Selection**: Supports custom builds (e.g., *Bellstrike - Splendor*, *Stonesplit - Might*, *Silkbind - Jade*, *Bamboocut - Wind*, etc.).
- **Flexible Statuses**: Sign up as **Main Roster**, **Benched / Reserve**, **Late**, or **Absence**.

### Automated Bench Promotion
- **Auto-Promote**: When a Main Roster participant leaves (`Leave Event`) or is kicked, the bot automatically promotes the first benched participant to Main Roster and sends them a Direct Message notification.

### Slash Commands Overview
- `/event` - Create an interactive event signup sheet
- `/profile` - Set or update default role and build
- `/schedule`	- View all upcoming scheduled events
- `/edit_event`- Modify event details or roster limits
- `/cancel_event`	- Cancel an event and notify participants	
- `/raid_kick` - Kick a player from an event roster	
- `/raid_move` - Move a player between roster tiers	
- `/event_summary` - Export event attendance report	
- `/setup_leader_role` - Configure raid leader role permissions	

### Centralized Schedule
- **`/schedule`**: View all upcoming active events in a single clean embed with direct clickable links to event messages.

---

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: `disnake` (Discord API wrapper)
- **Data Persistence**: JSON Storage (`events_data.json`, `server_configs.json`)
- **Environment Management**: `python-dotenv`

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher installed.
- A Discord Bot account created via the [Discord Developer Portal](https://discord.com/developers/applications).
- Bot Intents enabled: **Server Members Intent**, **Message Content Intent**.

### 2. Clone / Download Repository

### 3. Install Dependencies
- `pip install disnake python-dotenv`

### 4. Configuration
- Edit a .env file:
`BOT_TOKEN=your bot token`
`ADMIN_ID=your account id`
- in raid.py:
`TEST_GUILD_ID = YOUR_GUILD_ID`

### 5. Run the bot
- `python Raid.py`

