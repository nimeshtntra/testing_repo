import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from validation import TravelValidation
from traveldata import UserInsertDb, DistributorFilterData, DistributorInsertDb, UserPrivetMessage, UserFilterData
import environ
import logging
import re
import datetime

LOG_FORMAT=('{lineno} *** {name} *** {asctime} *** {message}')
logging.basicConfig(filename='.log', level=logging.DEBUG, format=LOG_FORMAT, style='{')
env = environ.Env()
env.read_env('/home/er/telegram_search/travel_search_bot/.env')
TOKEN = env('USER_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_dict = {}


def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton('Vehicle Agency', callback_data='Agency'),
        InlineKeyboardButton('User', callback_data='User'),
    )
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'Agency':
        agency_welcome(call.message)
    if call.data == 'User':
        user_welcome(call.message)


@bot.message_handler(commands=['start'])
def bot_welcome(message):
    bot.reply_to(message, """\
    Hello, I'm a User and Agency nnnn Vehicle Bot has select one option for this button !!! """, reply_markup=markup_inline())


class Agency:
    def __init__(self, agency_name):
        self.agency_name = agency_name
        self.agency_number = None
        self.agency_origin = None
        self.agency_destination = None
        self.agency_travel_dates = None
        self.passenger_capacity = None
        self.agency_chat_id = None


@bot.message_handler(commands=['agency'])
def agency_welcome(message):
    msg = bot.reply_to(message, """\
    Hi, I'm Vehicle Agency Bot.
    I will help you to find vehicle for your journey.
    
    What is the name of your Agency? """)
    bot.register_next_step_handler(msg, agency_name_step)


def agency_name_step(message):
    try:
        chat_id = message.chat.id
        agency_name = message.text.capitalize()
        try:
            new_name = TravelValidation.string_validate(agency_name)
        except ValueError:
            msg = bot.reply_to(message, 'No more than 8 characters for a Name . Please tell us what your Name is ?')
            bot.register_next_step_handler(msg, agency_name_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="agency_name_step error ",
                    class_name="agency_name_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, "A character's Name should be used. Please tell us Whats is your Name ? ")
            bot.register_next_step_handler(msg, agency_name_step)
            return
        user = Agency(new_name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'What is your Mobile Number? Please enter your Mobile Number')
        bot.register_next_step_handler(msg, agency_number_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def agency_number_step(message):
    try:
        chat_id = message.chat.id
        agency_number = message.text
        try:
            new_number = TravelValidation.number_validate(agency_number)
        except Exception as e:
            logging.error(
                dict(
                    message="agency_number_step errors",
                    class_name="agency_number_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'A Mobile Number should be just that: a Number. Please tell us What is your Mobile Number ?')
            bot.register_next_step_handler(msg, agency_number_step)
            return
        else:
            pattern = re.compile("(0|91)?[6-9][0-9]{9}")
            if not pattern.match(agency_number):
                msg = bot.reply_to(message, 'This Mobile Number is Not Correct. Please tell us What is your Mobile Number ?  ')
                bot.register_next_step_handler(msg, agency_number_step)
                return
            if len(agency_number) != 10:
                msg = bot.reply_to(message,
                                   'The Mobile Number should only be 10 digit only.Please tell us What is your Mobile Number ? ')
                bot.register_next_step_handler(msg, agency_number_step)
                return
        user = user_dict[chat_id]
        user.agency_number = new_number
        msg = bot.reply_to(message, 'Agency Vehicle Origin Station ? Enter Origin Name')
        bot.register_next_step_handler(msg, agency_origin_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def agency_origin_step(message):
    try:
        chat_id = message.chat.id
        agency_origin = message.text.capitalize()
        try:
            new_origin = TravelValidation.string_validate(agency_origin)
        except ValueError:
            msg = bot.reply_to(message, 'Origin Character no more than 10 .Please tell us What is Origin ? ')
            bot.register_next_step_handler(msg, agency_origin_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="agency_origin_step error ",
                    class_name="agency_origin_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Origin should be a character. Please tell us What is Origin ? ')
            bot.register_next_step_handler(msg, agency_origin_step)
            return
        user = user_dict[chat_id]
        user.agency_origin = new_origin
        msg = bot.reply_to(message, 'Agency Vehicle Destination ? Enter Destination Name ? ')
        bot.register_next_step_handler(msg, agency_destination_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def agency_destination_step(message):
    try:
        chat_id = message.chat.id
        agency_destination = message.text.capitalize()
        try:
            new_destination = TravelValidation.string_validate(agency_destination)
        except ValueError:
            msg = bot.reply_to(message, 'Destination Character no more than 10 .Please tell us your  Destination name ? ')
            bot.register_next_step_handler(msg, agency_destination_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="agency_destination_step error ",
                    class_name="agency_destination_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Destination should be a character. Please tell us your  Destination name? ')
            bot.register_next_step_handler(msg, agency_destination_step)
            return
        user = user_dict[chat_id]
        user.agency_destination = new_destination
        msg = bot.reply_to(message, 'When Do you want to go Agency Vehicle ? say dates like : YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD any one Format ')
        bot.register_next_step_handler(msg, agency_date_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def agency_date_step(message):
    try:
        chat_id = message.chat.id
        agency_travel_dates = message.text
        try:
            new_date = TravelValidation.date_validate(agency_travel_dates)
            today_date = datetime.datetime.today().date()
        except Exception as e:
            logging.error(
                dict(
                    message="agency_date_step error ",
                    class_name="agency_date_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Incorrect data format, should be Date Enter Date this YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD Format ')
            bot.register_next_step_handler(msg, agency_date_step)
            return
        if new_date.date() >= today_date:
            new_date = new_date
        else:
            msg = bot.reply_to(message, 'Past Date is not valid. Enter Correct Date')
            bot.register_next_step_handler(msg, agency_date_step)
            return
        user = user_dict[chat_id]
        user.agency_travel_dates = new_date.date()
        msg = bot.reply_to(message, 'How Many Passenger Capacity your Vehicle ? Enter Passenger Capacity ?')
        bot.register_next_step_handler(msg, agency_passenger_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def agency_passenger_step(message):
    chat_id = message.chat.id
    passenger_capacity = message.text
    try:
        new_passenger = TravelValidation.number_validate(passenger_capacity)
    except Exception as e:
        logging.error(
            dict(
                message="agency_passenger_step error ",
                class_name="agency_passenger_step",
                errors=e,
            )
        )
        msg = bot.reply_to(message, 'Passenger Capacity should be a number. Enter How Many Passenger Capacity ?')
        bot.register_next_step_handler(msg, agency_passenger_step)
        return
    else:
        if int(passenger_capacity) > 51:
            msg = bot.reply_to(message, 'Passenger Capacity no more than 51 .Please Enter How Many Passenger Capacity ?')
            bot.register_next_step_handler(msg, agency_passenger_step)
            return
    user = user_dict[chat_id]
    user.passenger_capacity = new_passenger
    bot.send_message(chat_id, 'Nice to meet you ' + user.agency_name +' !!! ' + '\n Number No. : ' + str(user.agency_number) + '\n Your Origin : ' + str(user.agency_origin) + '\n Your Destination : ' + str(user.agency_destination) + '\n Date : ' + str(user.agency_travel_dates) + '\n Passenger : ' + str(user.passenger_capacity))
    DistributorInsertDb().distributor_data(user.agency_name, user.agency_number, user.agency_origin, user.agency_destination, user.agency_travel_dates, user.passenger_capacity, chat_id)
    result = UserFilterData().user_filter(user.agency_origin, user.agency_destination, user.agency_travel_dates)
    if result:
        for messages in result:
            result_chat_id = messages.user_chat_id
            seat = '\n Origin : ' + str(user.agency_origin) + '\n Destination : ' + str(user.agency_destination) + '\n Date : ' + str(user.agency_travel_dates)+' \n This route vehicle is available right now, so call Agency this Mobile Number  ' + str(user.agency_number) + ' immediately !!! '
            UserPrivetMessage().send_msg(seat, result_chat_id)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.number = None
        self.origin = None
        self.destination = None
        self.dates = None
        self.passenger = None


@bot.message_handler(commands=['user'])
def user_welcome(message):
    msg = bot.reply_to(message, """\
    Hi, I'm Vehicle User Bot.
    I will help you to find vehicle for your journey.
    
    What is your name? """)
    bot.register_next_step_handler(msg, user_name_step)


def user_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text.capitalize()
        try:
            new_name = TravelValidation.string_validate(name)
        except ValueError:
            msg = bot.reply_to(message, 'Name Character no more than 8 . Please tell us Whats is your Name ')
            bot.register_next_step_handler(msg, user_name_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="user_name_step error ",
                    class_name="user_name_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Name should be a character. Please tell us Whats is your Name')
            bot.register_next_step_handler(msg, user_name_step)
            return
        user = User(new_name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Whats is your mobile Number ? Enter Mobile Number')
        bot.register_next_step_handler(msg, user_number_step)
    except Exception as e:
        bot.reply_to(e, 'oooops')


def user_number_step(message):
    try:
        chat_id = message.chat.id
        number = message.text
        try:
            new_number = TravelValidation.number_validate(number)
        except Exception as e:
            logging.error(
                dict(
                    message="user_number_step error ",
                    class_name="user_number_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, ' Mobile number should be a number. Please tell us Whats is your mobile Number ')
            bot.register_next_step_handler(msg, user_number_step)
            return
        else:
            pattern = re.compile("(0|91)?[6-9][0-9]{9}")
            if len(number) != 10:
                msg = bot.reply_to(message, 'The Mobile Number should only be 10 digit only.Please tell us What is your Mobile Number ? ')
                bot.register_next_step_handler(msg, agency_number_step)
                return
            if not pattern.match(number):
                msg = bot.reply_to(message,
                                   'This Mobile Number is Not Correct. Please tell us What is your Mobile Number ?  ')
                bot.register_next_step_handler(msg, agency_number_step)
                return
        user = user_dict[chat_id]
        user.number = new_number
        msg = bot.reply_to(message, 'Whats is your origin ? Enter Origin Name ')
        bot.register_next_step_handler(msg, user_origin_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def user_origin_step(message):
    try:
        chat_id = message.chat.id
        origin = message.text.capitalize()
        try:
            new_origin = TravelValidation.string_validate(origin)
        except ValueError:
            msg = bot.reply_to(message, 'Origin Character no more than 10.Please tell us What your Origin Name ?')
            bot.register_next_step_handler(msg, user_origin_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="user_origin_step error ",
                    class_name="user_origin_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Origin should be a character. Please tell us What your Origin Name ?')
            bot.register_next_step_handler(msg, user_origin_step)
            return
        user = user_dict[chat_id]
        user.origin = new_origin
        msg = bot.reply_to(message, 'Where are you going From ? Enter Destination Name')
        bot.register_next_step_handler(msg, user_destination_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def user_destination_step(message):
    try:
        chat_id = message.chat.id
        destination = message.text.capitalize()
        try:
            new_destination = TravelValidation.string_validate(destination)
        except ValueError:
            msg = bot.reply_to(message, 'Destination Character no more than 10 .Please tell us What is your destination name ?')
            bot.register_next_step_handler(msg, user_destination_step)
            return
        except Exception as e:
            logging.error(
                dict(
                    message="user_destination_step error ",
                    class_name="user_destination_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Destination should be a character. Please tell us What is Your destination name ?')
            bot.register_next_step_handler(msg, user_destination_step)
            return
        user = user_dict[chat_id]
        user.destination = new_destination
        msg = bot.reply_to(message, 'When Do you want to go your destination ? say dates like : YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD any one Format')
        bot.register_next_step_handler(msg, user_date_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def user_date_step(message):
    try:
        chat_id = message.chat.id
        dates = message.text
        try:
            new_date = TravelValidation.date_validate(dates)
            today_date = datetime.datetime.today().date()
        except Exception as e:
            logging.error(
                dict(
                    message="user_date_step error ",
                    class_name="user_date_step",
                    errors=e,
                )
            )
            msg = bot.reply_to(message, 'Incorrect data format, should be Date Enter Date this YYYY-MM-DD or YYYY/MM/DD or YYYY MM DD Format')
            bot.register_next_step_handler(msg, user_date_step)
            return
        if new_date.date() >= today_date:
            new_date = new_date
        else:
            msg = bot.reply_to(message, 'Past Date is not valid. Enter Correct Date')
            bot.register_next_step_handler(msg, user_date_step)
            return
        user = user_dict[chat_id]
        user.dates = new_date.date()
        msg = bot.reply_to(message, 'How Many Passenger join this route ? Enter Passenger Number')
        bot.register_next_step_handler(msg, user_passenger_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def user_passenger_step(message):
    chat_id = message.chat.id
    passenger = message.text
    try:
        new_passenger = TravelValidation.number_validate(passenger)
    except Exception as e:
        logging.error(
            dict(
                message="user_passenger_ste error ",
                class_name="user_passenger_ste",
                errors=e,
            )
        )
        msg = bot.reply_to(message, 'Passenger should be a number. Enter How Many Passenger join this route ?')
        bot.register_next_step_handler(msg, user_passenger_step)
        return
    else:
        if int(passenger) > 51:
            msg = bot.reply_to(message, 'Passenger no more than 51 .Please tell us How Many Passenger join this route')
            bot.register_next_step_handler(msg, user_passenger_step)
            return
    user = user_dict[chat_id]
    user.passenger = new_passenger

    bot.send_message(chat_id, 'Nice to meet you ' + user.name +' !!! ' + '\n Number No. : ' + str(user.number) + '\n Your Origin : ' + str(user.origin) + '\n Your Destination : ' + str(user.destination) + '\n Date : ' + str(user.dates) + '\n Passenger : ' + str(user.passenger))

    UserInsertDb().travel_data(user.name, user.number, user.origin, user.destination, user.dates, user.passenger, chat_id)

    result = DistributorFilterData().distributor_filter(user.origin, user.destination, user.dates)
    if result:
        bot.send_message(chat_id, ' Thanks for your quick response, '+ user.name +  ' !!! Your Vehicle Ticket has been booked. ')
    else:
        bot.send_message(chat_id, ' Thank you ' + user.name + ' If There any update I will inform you !!!  ')


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()
bot.infinity_polling()