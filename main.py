from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from mg import get_map_cell
markdown = """
    *bold text*
    _italic text_
    [text](URL)
    ```Mono```
    """


bot = Bot('5559855551:AAGhk_su6k5NWQUjo7KAtbCZK6265D3bXys')
dp = Dispatcher(bot)
cols, rows = 4, 4	


maps = {}

def get_map_str(map_cell, player):
	map_str = ""
	for y in range(rows * 2 - 1):
		for x in range(cols * 2 - 1):
			if map_cell[x + y * (cols * 2 - 1)]:
				map_str += "⬛"
			elif (x, y) == player:
				map_str += "🔵"
			elif x == cols * 2 - 2 and y == rows * 2 - 2:
				map_str += "🟩"
			else:
				map_str += "⬜"
		map_str += "\n"
	return map_str

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer_animation("https://t.me/svgpngforcoding/19")
    await message.answer(f"*Здравствуйте *" + str(message.from_user.first_name) + "*\n\nЧтобы начать игру отправьте /play*" + "*\nСообщить об ошибке /help*", parse_mode='Markdown')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	await message.answer("*Автор бота👤: @ABDU_UYGHUR\nЕсли не ответил, напишите ещё раз. Если снова не ответил, то подождите🔰*", parse_mode='markdown')

@dp.message_handler(commands=['play'])
async def play_message(message):
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row( InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('⬆', callback_data='up'),
	InlineKeyboardButton('ㅤ', callback_data='...') )
	keyboard.row( InlineKeyboardButton('⬅️', callback_data='left'),
	InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('➡️', callback_data='right') )
	keyboard.row( InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('⬇️', callback_data='down'),
	InlineKeyboardButton('ㅤ', callback_data='...') )

	map_cell = get_map_cell(cols, rows)

	user_data = {
		'map': map_cell,
		'x': 0,
		'y': 0
	}

	maps[message.chat.id] = user_data

	await bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data)
async def callback_func(call: CallbackQuery):
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row( InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('⬆', callback_data='up'),
	InlineKeyboardButton('ㅤ', callback_data='...') )
	keyboard.row( InlineKeyboardButton('⬅️', callback_data='left'),
	InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('➡️', callback_data='right') )
	keyboard.row( InlineKeyboardButton('ㅤ', callback_data='...'),
	InlineKeyboardButton('⬇️', callback_data='down'),
	InlineKeyboardButton('ㅤ', callback_data='...') )
	user_data = maps[call.message.chat.id]
	new_x, new_y = user_data['x'], user_data['y']

	if call.data == 'left':
		new_x -= 1
	if call.data == 'right':
		new_x += 1
	if call.data == 'up':
		new_y -= 1
	if call.data == 'down':
		new_y += 1

	if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
		return None
	if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
		return None

	user_data['x'], user_data['y'] = new_x, new_y

	if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
		await call.message.edit_text("*Вы выиграли поздравляю вас!\n\nЧтобы играть снова напишите /play\nСообщить об ошибке /help*", parse_mode='markdown')
		return None

	await call.message.edit_text(get_map_str(user_data['map'], (new_x, new_y)), reply_markup=keyboard)

executor.start_polling(dp, skip_updates=True)
