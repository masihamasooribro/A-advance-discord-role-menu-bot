import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'MTM1ODAzNjI4MTI5MjIzMDk3OA.GuxRpV.JvTVSefHGEMutcbwYil7gYv91gdPjvJLxgvCew'  # Replace with your actual bot token

intents = discord.Intents.default()
intents.members = True  # Enable member intents
intents.message_content = True  # Enable message content intent if needed

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


class AddRoleView(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__()
        self.user = user
        self.add_select()

    def add_select(self):
        roles = [role for role in self.user.guild.roles if role != self.user.guild.default_role]  # Exclude @everyone
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        select = discord.ui.Select(placeholder="Select a role to add...", options=options)
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        if isinstance(interaction.data["component_type"], int) and interaction.data["component_type"] == 3:  # check if it is select menu interaction
            role_id = int(interaction.data["values"][0])
            role = discord.utils.get(self.user.guild.roles, id=role_id)
            await self.user.add_roles(role)
            await interaction.response.send_message(f"Added role {role.name} to {self.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("This is not a select menu interaction.", ephemeral=True)


class RemoveRoleView(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__()
        self.user = user
        self.add_select()

    def add_select(self):
        roles = [role for role in self.user.roles if role != self.user.guild.default_role]  # Exclude @everyone
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]
        select = discord.ui.Select(placeholder="Select a role to remove...", options=options)
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        if isinstance(interaction.data["component_type"], int) and interaction.data["component_type"] == 3:  # check if it is select menu interaction
            role_id = int(interaction.data["values"][0])
            role = discord.utils.get(self.user.guild.roles, id=role_id)
            await self.user.remove_roles(role)
            await interaction.response.send_message(f"Removed role {role.name} from {self.user.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("This is not a select menu interaction.", ephemeral=True)


@bot.tree.command(name="rolemenu", description="Creates a role menu for a specific user.")
async def rolemenu(interaction: discord.Interaction, user: discord.Member):
    """
    Creates a role menu for a specific user.
    """
    guild = interaction.guild

    embed = discord.Embed(title="Role Menu", description=f"This menu corresponds to the following targets:\n- {user.mention} ({user.name})", color=discord.Color.dark_grey())
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

    # Create the buttons
    add_role_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Add A Role")
    remove_role_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Remove A Role")

    # Create the view and add the buttons
    view = discord.ui.View()
    view.add_item(add_role_button)
    view.add_item(remove_role_button)

    # Send the message with the embed and view
    await interaction.response.send_message(embed=embed, view=view)

    # Define the callback functions for the buttons
    async def add_role_callback(interaction: discord.Interaction):
        await interaction.response.send_message("Select a role to add:", view=AddRoleView(user), ephemeral=True)

    async def remove_role_callback(interaction: discord.Interaction):
        await interaction.response.send_message("Select a role to remove:", view=RemoveRoleView(user), ephemeral=True)

    # Assign the callbacks to the buttons
    add_role_button.callback = add_role_callback
    remove_role_button.callback = remove_role_callback


bot.run(TOKEN)