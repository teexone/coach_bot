import telebot
import user
import selector
import messenger
import os

bot = telebot.TeleBot(os.environ['TELEGRAMAPI'])

keyboards = {
    'main_menu': telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        .row('Problem', 'Configure handle')
        .row('Help'),
    'confirm': telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        .row('Yes', 'No')
        .row('Cancel'),
    'cancel': telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row('Cancel'),
    'help': telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).row('Tag list', 'How to combine tags').row(
        'Cancel'),
}
user.init_load()


@bot.message_handler(commands=['start'])
def on_start(message):
    bot.send_message(message.chat.id,
                     'Hello. I am a coach bot for competitive programming. I can help you in selecting the problems to '
                     'solve. Also I may track your results and show your progress on a specific classes of problems'
                     '\n\n'
                     'You may use options provided below. If you need some help press "Help".',
                     reply_markup=keyboards['main_menu'])


def on_update(messages):
    for msg in messages:
        answer(msg)


def answer(message):
    user_state = user.get_udata(message.from_user.id)
    uid = message.from_user.id
    if message.text == 'Cancel':
        return_to_main(uid, message.chat.id, 'Canceled')
        return
    elif message.text == 'Help':
        bot.send_message(message.chat.id, 'You may use '
                                          'buttons below this message to get useful information',
                         reply_markup=keyboards['help'])
        return
    elif message.text == 'Tag list':
        bot.send_message(message.chat.id, 'greedy\n'
                                          'math\n'
                                          'sortings\n'
                                          'brute force\n'
                                          'dfs and similar\n'
                                          'dp\n'
                                          'interactive\n'
                                          'trees\n'
                                          'constructive algorithms\n'
                                          'geometry\n'
                                          'data structures\n'
                                          'dsu\n'
                                          'graphs\n'
                                          'combinatorics\n'
                                          'number theory\n'
                                          'binary search\n'
                                          'games\n'
                                          'divide and conquer\n'
                                          'shortest paths\n'
                                          'implementation\n'
                                          'string suffix structures\n'
                                          'strings\n'
                                          'two pointers\n'
                                          'flows\n'
                                          'graph matchings\n'
                                          'bitmasks\n'
                                          'ternary search\n'
                                          'matrices\n'
                                          'meet-in-the-middle\n'
                                          'hashing\n'
                                          'probabilities\n'
                                          'fft\n'
                                          '*special\n'
                                          '2-sat\n'
                                          'expression parsing\n'
                                          'chinese remainder theorem\n'
                                          'schedules\n', reply_markup=keyboards['help'])
        return
    elif message.text == 'How to combine tags':
        bot.send_message(message.chat.id, 'You may combine tags into compound statements in the following way:'
                                          '\n\n'
                                          '1\. If you want the problems I find to include either one tag or another, '
                                          'you '
                                          'have to separate these tags with comma'
                                          '\n\nFor example:``` math, dp```\n\n'
                                          '2\. If you want the problems I find to include both tags, you have to '
                                          'combine '
                                          'them with plus sign\n\nFor example: ``` math + implementation```\n\n3\. '
                                          'Make '
                                          'compound '
                                          'statements to select problem you want'
                                          '\n\n``` math + dp, implementation + dp, graphs + dp, bruteforce```',
                         reply_markup=keyboards['help'], parse_mode='MarkdownV2')
    elif user_state['dialog'] == user.UserDialog.NO_DIALOG:
        if message.text == 'Problem':
            user.update_dialog(uid, user.UserDialog.ASK_FOR_PROBLEM)
            bot.send_message(message.chat.id, 'Write the lower bound for complexity of problems you want me to find. '
                                              'The complexity of a problem I am going to find will be at least '
                                              'the number you write next. ', reply_markup=keyboards['cancel'])
            user.update_dialog_state(uid, user.AskForProblemDialog.LOWER_DF)
        if message.text == 'Configure handle':
            user.update_dialog(uid, user.UserDialog.CONFIGURE_HANDLE)
            bot.send_message(message.chat.id, 'Send your codeforces.com handle', reply_markup=keyboards['cancel'])
            user.update_dialog_state(uid, user.ConfigureHandleDialog.SEND_HANDLE)
    elif user_state['dialog'] == user.UserDialog.ASK_FOR_PROBLEM:
        if user_state['dialog_state'] == user.AskForProblemDialog.LOWER_DF:
            txt = message.text.strip().split()
            if len(txt) > 1:
                throw_error_tou(uid, message.chat.id)
                return
            user.put_into_cache(uid, 'lower_bound', int(txt[0]))
            bot.send_message(message.chat.id, 'Write the upper bound for complexity of problems you want me to find. '
                                              'The complexity of a problem I am going to find will be at most '
                                              'the number you write next. ', reply_markup=keyboards['cancel'])
            user.update_dialog_state(uid, user.AskForProblemDialog.UPPER_DF)
        elif user_state['dialog_state'] == user.AskForProblemDialog.UPPER_DF:
            txt = message.text.strip().split()
            if len(txt) > 1:
                throw_error_tou(uid, message.chat.id)
                return
            user.put_into_cache(uid, 'upper_bound', int(txt[0]))
            bot.send_message(message.chat.id, 'Should I exclude problems that you have already solved?',
                             reply_markup=keyboards['confirm'])
            user.update_dialog_state(uid, user.AskForProblemDialog.EXCLUDE_SOLVED)
        elif user_state['dialog_state'] == user.AskForProblemDialog.EXCLUDE_SOLVED:
            txt = message.text.strip()
            if not txt == 'Yes' and not txt == 'No':
                throw_error_tou(uid, message.chat.id)
                return
            handle = user.get_handle(uid)
            if txt == 'Yes' and handle is None:
                user.update_dialog_state(uid, user.AskForProblemDialog.INLINE_HANDLE_CONFIG)
                bot.send_message(message.chat.id, 'Your handle is not configured. Please, send me your handle',
                                 reply_markup=keyboards['cancel'])
                return
            user.put_into_cache(uid, 'exclude_solved', txt == 'Yes')
            bot.send_message(message.chat.id, 'List tags for problems I am supposed to find. Separate them by a '
                                              'comma or combine with "+". '
                                              'For example: implementation, math + dp.\n\nIf you do not want me to '
                                              'narrow searching with tags, put a single star "*"',
                             reply_markup=keyboards['cancel'])
            user.update_dialog_state(uid, user.AskForProblemDialog.TAGS)
        elif user_state['dialog_state'] == user.AskForProblemDialog.INLINE_HANDLE_CONFIG:
            txt = message.text.strip().split()
            if len(txt) > 1:
                bot.send_message(message.chat.id, 'Too many words. Try again')
                return
            user.change_handle(uid, txt[0])
            bot.send_message(message.chat.id, 'Your handle has been successfully attached')
            bot.send_message(message.chat.id, 'Should I exclude problems that you have already solved?',
                             reply_markup=keyboards['confirm'])
            user.update_dialog_state(uid, user.AskForProblemDialog.EXCLUDE_SOLVED)

        elif user_state['dialog_state'] == user.AskForProblemDialog.TAGS:
            txt = message.text.strip()
            tags = [[y.strip() for y in x.strip().split('+')] for x in txt.split(',')]
            user.put_into_cache(uid, 'tags', tags)
            bot.send_message(message.chat.id, 'How many problems you want me to find?')
            user.update_dialog_state(uid, user.AskForProblemDialog.QUANTITY)
        elif user_state['dialog_state'] == user.AskForProblemDialog.QUANTITY:
            try:
                int(message.text)
            except ValueError:
                throw_error_tou(uid, message.chat.id)
                return
            user.put_into_cache(uid, 'quantity', message.text)
            bot.send_message(message.chat.id, 'Your problems are on their way!')
            problems = get_problem(uid)
            if problems is None:
                return_to_main(uid, message.chat.id, "No problems were found according to data you have provided")
                return
            txt = ''
            for x in problems.values():
                if 'contestId' not in x:
                    continue
                new_txt = messenger.problem_info(x)
                if len(txt) + len(new_txt) > 4096:
                    bot.send_message(message.chat.id, txt, parse_mode='Markdown', disable_web_page_preview=True)
                    txt = ''
                txt += new_txt
            return_to_main(uid, message.chat.id, txt)
    elif user_state['dialog'] == user.UserDialog.CONFIGURE_HANDLE:
        txt = message.text.strip().split()
        if len(txt) > 1:
            bot.send_message(message.chat.id, 'Too many words. Try again')
            return
        user.change_handle(uid, txt[0])
        return_to_main(uid, message.chat.id, 'Your handle has been successfully attached')


def throw_error_tou(uid, chat):
    return_to_main(uid, chat, 'It seems the data you have provided is invalid')


def return_to_main(uid, chat, message):
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            bot.send_message(chat, message[x:x + 4096], reply_markup=keyboards['main_menu'], parse_mode='Markdown',
                             disable_web_page_preview=True)
    else:
        bot.send_message(chat, message, reply_markup=keyboards['main_menu'], parse_mode='Markdown',
                         disable_web_page_preview=True)
    user.update_dialog(uid, user.UserDialog.NO_DIALOG)
    user.clear_cache(uid)


def get_problem(uid):
    data = user.userdata[str(uid)]
    cache = data['cache']
    return selector.fetch_problems(cache['quantity'], (cache['lower_bound'], cache['upper_bound']), cache['tags'],
                                   data['handle'] if cache['exclude_solved'] else None)


