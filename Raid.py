import disnake
from disnake.ext import commands
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import zoneinfo

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
TEST_GUILD_ID = YOUR_GUILD_ID  # айдишник вашей гильдии. Это нужно только для того, чтобы слеш комманды заработали моментально. Я использовал этот подход для тестирования, под еще в стадии разработки

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

# --- ХРАНИЛИЩЕ ДАННЫЪ ---
DATA_FILE = "events_data.json"

def load_events():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
            except json.JSONDecodeError:
                return {}
    return {}

def save_events():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(events_data, f, ensure_ascii=False, indent=4)

events_data = load_events()


def render_event_embed(title, description, timestamp, signups):
    """Генерация красивого Embed-сообщения рейда"""
    discord_time = f"<t:{timestamp}:F> (<t:{timestamp}:R>)"

    embed = disnake.Embed(
        title=f"🛡️ ГИЛЬДЕЙСКИЙ ИВЕНТ: {title}",
        description=f"**📅 Время проведения:**\n{discord_time}\n\n{description}",
        color=disnake.Color.dark_red()
    )
    
    tanks_list = "\n".join([f"<@{uid}>" for uid in signups["tanks"]]) or "_Никого_"
    dps_list = "\n".join([f"<@{uid}>" for uid in signups["dps"]]) or "_Никого_"
    heals_list = "\n".join([f"<@{uid}>" for uid in signups["heals"]]) or "_Никого_"
    
    embed.add_field(name=f"🛡️ Танки ({len(signups['tanks'])})", value=tanks_list, inline=True)
    embed.add_field(name=f"⚔️ ДД ({len(signups['dps'])})", value=dps_list, inline=True)
    embed.add_field(name=f"💖 Хилы ({len(signups['heals'])})", value=heals_list, inline=True)
    
    embed.set_footer(text="Выберите свою роль 👇")
    return embed


class EventButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_signup(self, interaction: disnake.MessageInteraction, role: str):
        msg_id = interaction.message.id
        user_id = interaction.user.id
        
        if msg_id not in events_data:
            await interaction.response.send_message("❌ Ошибка: Этот ивент не найден в базе данных.", ephemeral=True)
            return

        for r in ["tanks", "dps", "heals"]:
            if user_id in events_data[msg_id]["signups"][r]:
                events_data[msg_id]["signups"][r].remove(user_id)

        if role != "leave":
            events_data[msg_id]["signups"][role].append(user_id)
            role_names = {"tanks": "Танк 🛡️", "dps": "ДД ⚔️", "heals": "Хил 💖"}
            await interaction.response.send_message(f"✅ Вы успешно записались как **{role_names[role]}**", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Вы отменили запись на ивент.", ephemeral=True)

        save_events()

        ev = events_data[msg_id]
        new_embed = render_event_embed(ev["title"], ev["description"], ev["timestamp"], ev["signups"])
        await interaction.message.edit(embed=new_embed)

    @disnake.ui.button(label="Танк", style=disnake.ButtonStyle.blurple, emoji="🛡️", custom_id="btn_tank")
    async def tank_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.handle_signup(interaction, "tanks")

    @disnake.ui.button(label="ДД", style=disnake.ButtonStyle.danger, emoji="⚔️", custom_id="btn_dps")
    async def dps_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.handle_signup(interaction, "dps")

    @disnake.ui.button(label="Хил", style=disnake.ButtonStyle.success, emoji="💖", custom_id="btn_heal")
    async def heal_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.handle_signup(interaction, "heals")

    @disnake.ui.button(label="Ливнуть", style=disnake.ButtonStyle.secondary, emoji="❌", custom_id="btn_leave")
    async def leave_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.handle_signup(interaction, "leave")


@bot.event
async def on_ready():
    bot.add_view(EventButtons())
    print(f"⚔️ Бот {bot.user} готов к рейдам!")


@bot.slash_command(
    name="ивент", 
    description="Создать регистрацию на гильдейское событие",
    guild_ids=[TEST_GUILD_ID] 
)
@commands.has_permissions(administrator=True)
async def create_event(
    inter: disnake.ApplicationCommandInteraction, 
    title: str = commands.Param(name="название", description="Название события (например: Осада, Босс)"), 
    description: str = commands.Param(name="описание", description="Описание, требования, сбор"), 
    day: int = commands.Param(name="день", description="День месяца (1-31)", min_value=1, max_value=31),
    month: int = commands.Param(name="месяц", description="Месяц (1-12)", min_value=1, max_value=12),
    time_str: str = commands.Param(name="время", description="Время в формате ЧЧ:ММ (например, 19:30 или 20:00)"),
    tz_name: str = commands.Param(
        name="часовой_пояс", 
        description="В каком часовом поясе вы указываете время?",
        choices=[
            disnake.OptionChoice("Калининград (UTC+2)", "Europe/Kaliningrad"),
            disnake.OptionChoice("Москва / Минск (UTC+3)", "Europe/Moscow"),
            disnake.OptionChoice("Самара (UTC+4)", "Europe/Samara"),
            disnake.OptionChoice("Екатеринбург (UTC+5)", "Asia/Yekaterinburg"),
            disnake.OptionChoice("Омск (UTC+6)", "Asia/Omsk"),
            disnake.OptionChoice("Новосибирск / Красноярск (UTC+7)", "Asia/Krasnoyarsk"),
            disnake.OptionChoice("Иркутск (UTC+8)", "Asia/Irkutsk"),
            disnake.OptionChoice("Якутск (UTC+9)", "Asia/Yakutsk"),
            disnake.OptionChoice("Владивосток (UTC+10)", "Asia/Vladivostok"),
            disnake.OptionChoice("UTC / GMT", "UTC")
        ]
    ),
    year: int = commands.Param(name="год", description="По умолчанию — текущий год", default=None)
):
    try:
        
        if year is None:
            year = datetime.now().year


        if ":" not in time_str:
            raise ValueError("Неверный формат времени")
            
        hour_str, minute_str = time_str.split(":")
        hour = int(hour_str)
        minute = int(minute_str)


        chosen_tz = zoneinfo.ZoneInfo(tz_name)


        local_dt = datetime(year, month, day, hour, minute, tzinfo=chosen_tz)
        

        unix_timestamp = int(local_dt.timestamp())
        
    except ValueError:
        await inter.response.send_message(
            "❌ Ошибка заполнения полей! Проверьте правильность введенных чисел.\n"
            "Убедитесь, что время указано через двоеточие, например: `20:00` или `18:30`.", 
            ephemeral=True
        )
        return

    signups = {"tanks": [], "dps": [], "heals": []}
    
    embed = render_event_embed(title, description, unix_timestamp, signups)
    view = EventButtons()
    
    await inter.response.send_message(embed=embed, view=view)
    
    msg = await inter.original_response()
    events_data[msg.id] = {
        "title": title,
        "description": description,
        "timestamp": unix_timestamp,
        "signups": signups
    }
    save_events()

bot.run(TOKEN)