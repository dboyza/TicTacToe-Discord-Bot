import discord
import datetime
from datetime import datetime

# Ununsed board piece
blank = '⬜'


# Emoji list
move_emojis = ['↖️', '⬆️', '↗️', '⬅️', '⏹️', '➡️', '↙️', '⬇️', '↘️', '🛑']


# Prints the game board
def print_board(player1, player2, board):
    game_board = (
        board[0] + '⬛' + board[1] + '⬛' + board[2] + '\n' +
        '⬛' + '⬛' + '⬛' + '⬛' + '⬛' + '\n' +
        board[3] + '⬛' + board[4] + '⬛' + board[5] + '\n' +
        '⬛' + '⬛' + '⬛' + '⬛' + '⬛' + '\n' +
        board[6] + '⬛' + board[7] + '⬛' + board[8])
    return game_board


# (!play) Displays how to play the game
async def playinfo(ctx):
    await ctx.message.add_reaction('👍')

    # Create a Discord embed
    game_info = discord.Embed(
        title="Tic-Tac-Toe",
        description="Challenge an opponent to a game of Tic-Tac-Toe!",
        url="https://en.wikipedia.org/wiki/Tic-tac-toe",
        timestamp=datetime.now(),
        color=0x1abc9c)

    # Field 1
    game_info.add_field(name="Starting the Game",
                        value="Use the command\n \"!challenge\" \nto challenge a server member\n")

    # Field 2
    game_info.add_field(name="Instructions",
                        value="Each player will use reactions to input their choice during each turn")

    # Print the embed
    await ctx.reply(embed=game_info)


# (!challenge) Sets up an instance of Tic Tac Toe
async def playgame(ctx, client):
    # Usable emojis
    available_emojis = ['↖️', '⬆️', '↗️', '⬅️',
                        '⏹️', '➡️', '↙️', '⬇️', '↘️', '🛑']

    # Game board
    board = [
        blank, blank, blank,
        blank, blank, blank,
        blank, blank, blank]

    await ctx.message.add_reaction('👍')
    current_player = 0

    # Get 1st player's icon
    await ctx.send("@here Who wants to play Tic-Tac-Toe?")
    player1 = await get_character(ctx, client, current_player + 1)

    # Get 2nd player's icon
    player2 = await get_character(ctx, client, current_player + 2)

    # Clean up messages via purge
    await ctx.channel.purge(limit=4)

    # Return true if the bot did not react
    def check_bot(reaction, user):
        return user != client.user

    turn = 1
    # Loop for players to make moves until one wins or board is full
    while check_win(player1, player2, board) == blank and turn <= 9:
        await ctx.send(f"Player {current_player % 2 + 1}'s Turn")
        msg = await ctx.send(print_board(player1, player2, board))
        for i in range(len(available_emojis)):
            await msg.add_reaction(available_emojis[i])

        reaction, user = await client.wait_for("reaction_add", timeout=30.0, check=check_bot)

        # Stop the game
        if reaction.emoji == '🛑':
            turn = 10
            await ctx.channel.purge(limit=2)
            await ctx.send(f"Player {current_player + 1} has ended the game.")
            break
        # Place the player's chosen emoji on the board
        else:
            if current_player % 2 == 0:
                player_move(reaction.emoji, available_emojis, player1, board)
            else:
                player_move(reaction.emoji, available_emojis, player2, board)

            # Clean up messages via purge
            await ctx.channel.purge(limit=2)

        # Check for a winner ask for rematch, reset board and emojies
        winner = check_win(player1, player2, board)
        if winner != blank and turn <= 9:
            await ctx.send(f"Player {current_player % 2 + 1} won!\n Do you want a rematch?")
            msg = await ctx.send(print_board(player1, player2, board))
            await msg.add_reaction("✔️")
            await msg.add_reaction("❌")
            reaction, user = await client.wait_for("reaction_add", timeout=30.0, check=check_bot)

            if str(reaction.emoji) == "✔️":
                available_emojis = ['↖️', '⬆️', '↗️', '⬅️',
                                    '⏹️', '➡️', '↙️', '⬇️', '↘️', '🛑']
                board = [
                    blank, blank, blank,
                    blank, blank, blank,
                    blank, blank, blank]
                current_player = 1
                turn = 0
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send("Thanks for playing Tic-Tac-Toe! - Boyza")

        # Tie game, ask for a rematch, reset board and emojies
        elif turn >= 9:
            await ctx.send("Tie game! Do you want a rematch?")
            msg = await ctx.send(print_board(player1, player2, board))
            await msg.add_reaction("✔️")
            await msg.add_reaction("❌")
            reaction, user = await client.wait_for("reaction_add", timeout=30.0, check=check_bot)

            if str(reaction.emoji) == "✔️":
                available_emojis = ['↖️', '⬆️', '↗️', '⬅️',
                                    '⏹️', '➡️', '↙️', '⬇️', '↘️', '🛑']
                board = [
                    blank, blank, blank,
                    blank, blank, blank,
                    blank, blank, blank]
                current_player = 1
                turn = 0
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send("Thanks for playing Tic-Tac-Toe! - Boyza")

        current_player += 1
        turn += 1


# Remove reaction emoji from list when player makes a move
# Add player emoji to the board
def player_move(emoji, available_emojis, player_emoji, board):
    for i in range(len(move_emojis)):
        if move_emojis[i] == emoji:
            board[i] = player_emoji
            available_emojis.remove(emoji)
            break


# Check for win condiitions (rows, columns, diagonals)
def check_win(player1, player2, board):
    row1 = check_pieces(0, 1, 2, player1, player2, board)
    if row1 != blank:
        return row1
    row2 = check_pieces(3, 4, 5, player1, player2, board)
    if row2 != blank:
        return row2
    row3 = check_pieces(6, 7, 8, player1, player2, board)
    if row3 != blank:
        return row3
    col1 = check_pieces(0, 3, 6, player1, player2, board)
    if col1 != blank:
        return col1
    col2 = check_pieces(1, 4, 7, player1, player2, board)
    if col2 != blank:
        return col2
    col3 = check_pieces(2, 5, 8, player1, player2, board)
    if col3 != blank:
        return col3
    diag1 = check_pieces(0, 4, 8, player1, player2, board)
    if diag1 != blank:
        return diag1
    diag2 = check_pieces(2, 4, 6, player1, player2, board)
    if diag2 != blank:
        return diag2
    return blank


# Check if the 3 lined up board pieces match
def check_pieces(pos1, pos2, pos3, player1, player2, board):
    # Determine if player has won
    if (board[pos1] == board[pos2] == board[pos3]) and (board[pos3] != blank):
        if board[pos1] == player1:
            return player1
        elif board[pos1] == player2:
            return player2
    # Return blank if win condition is not satisfied
    else:
        return blank


# Players may pick their characters via reactions in Discord
async def get_character(ctx, client, current_player):
    await ctx.send("Player " + str(current_player) + ": Pick your Tic-Tac-Toe character! React to this message with an emoji.")

    # Return true if the bot did not react
    def check_bot(reaction, user):
        return user != client.user

    # Get the reaction the user inputs
    reaction, user = await client.wait_for("reaction_add", timeout=30.0, check=check_bot)

    # Return the emoji
    return str(reaction.emoji)
