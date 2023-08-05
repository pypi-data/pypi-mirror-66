import datetime
from .conf.config import LoggerConfig
from .writer.log_writer import LogWriter
from .util.utils import create_softlink, delete_file, link_exists, \
    rel_to_abs_path

class TextStyle:
    normal = '0'
    bold = '1'
    crisp = '2'
    italic = '3'
    blink = '5'

class TextColor:
    black = '30'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    purple = '35'
    cyan = '36'
    white = '37'

class TextBackgroundColor:
    black = '40'
    red = '41'
    green = '42'
    yellow = '43'
    blue = '44'
    purple = '45'
    cyan = '46'
    white = '47'

class TextHeaderFactory:
    def __init__(self, style: TextStyle, text_color: TextColor, text_background_color: TextBackgroundColor):
        self.style = style
        self.color = text_color
        self.text_background_color = text_background_color
        self.header = "\033[{};{};{}m".format(style, text_color, text_background_color)

class TextHeaderFactoryHandler:
    def get_std_header(self):
        return "\033[0m"

    def get_simple_header(self, text_color: TextColor):
        return TextHeaderFactory(TextStyle.bold, text_color, TextBackgroundColor.black).header

    def get_debug_header(self, style: TextStyle):
        return TextHeaderFactory(style, TextColor.green, TextBackgroundColor.white).header

    def get_message_header(self, text_color: TextColor):
        return TextHeaderFactory(TextStyle.bold, text_color, TextBackgroundColor.black).header

class TextHeader:
    # Standard
    std = TextHeaderFactoryHandler().get_std_header()
    
    # Simple
    black = TextHeaderFactoryHandler().get_simple_header(TextColor.black)
    red = TextHeaderFactoryHandler().get_simple_header(TextColor.red)
    green = TextHeaderFactoryHandler().get_simple_header(TextColor.green)
    yellow = TextHeaderFactoryHandler().get_simple_header(TextColor.yellow)
    blue = TextHeaderFactoryHandler().get_simple_header(TextColor.blue)
    purple = TextHeaderFactoryHandler().get_simple_header(TextColor.purple)
    cyan = TextHeaderFactoryHandler().get_simple_header(TextColor.cyan)
    white = TextHeaderFactoryHandler().get_simple_header(TextColor.white)

    # Debug
    debug_normal = TextHeaderFactoryHandler().get_debug_header(TextStyle.normal)
    debug_bold = TextHeaderFactoryHandler().get_debug_header(TextStyle.bold)
    debug_crisp = TextHeaderFactoryHandler().get_debug_header(TextStyle.crisp)
    debug_italic = TextHeaderFactoryHandler().get_debug_header(TextStyle.italic)
    debug_blink = TextHeaderFactoryHandler().get_debug_header(TextStyle.blink)

    # Message
    good = TextHeaderFactoryHandler().get_message_header(TextColor.green)
    info = TextHeaderFactoryHandler().get_message_header(TextColor.cyan)
    warning = TextHeaderFactoryHandler().get_message_header(TextColor.yellow)
    error = TextHeaderFactoryHandler().get_message_header(TextColor.red)
    system = TextHeaderFactoryHandler().get_message_header(TextColor.white)

class Logger:
    def __init__(self):
        # Global
        self.cumulative_log = {}

        # Simple
        self.red_log = {}
        self.green_log = {}
        self.yellow_log = {}
        self.blue_log = {}
        self.purple_log = {}
        self.cyan_log = {}
        self.white_log = {}

        # Debug
        self.debug_normal_log = {}
        self.debug_bold_log = {}
        self.debug_crisp_log = {}
        self.debug_italic_log = {}
        self.debug_blink_log = {}

        # Messages
        self.good_log = {}
        self.info_log = {}
        self.warning_log = {}
        self.error_log = {}
        self.system_log = {}

        # Log Writer
        self.log_link_path = None
        self.log_writer = LogWriter(self)
        self.log_writer.init_log_dir()

        self.system("Logger initialized.")

    def link_log_dir(self, log_dir: str):
        if self.log_link_path is not None:
            if link_exists(self.log_link_path):
                delete_file(self.log_link_path)
        self.log_link_path = log_dir
        create_softlink(src_path=LoggerConfig.logs_dir, dst_path=log_dir)
        self.system(f"Linked {LoggerConfig.logs_dir} to {rel_to_abs_path(log_dir)}")

    def _template(
        self, text: str, show_flag: bool, write_flag: bool, header: TextHeader,
        logtype_label: str, log_dict: dict, logname: str, logdir: str
    ):
        text_str = str(text)
        if LoggerConfig.show_log and show_flag:
            print("{}{}{}".format(header, text_str, TextHeader.std))
        data = {
            'LogType': logtype_label,
            'time': str(datetime.datetime.now()),
            'text': text_str
        }
        if write_flag:
            log_dict[len(log_dict)] = data
            if LoggerConfig.append_mode:
                self.log_writer.append_line(
                    logname=logname,
                    logdir=logdir,
                    data=data
                )
        if LoggerConfig.write_cumulative_log:
            self.cumulative_log[len(self.cumulative_log)] = data
            if LoggerConfig.append_mode:
                self.log_writer.append_line(
                    logname='cumulative',
                    logdir=LoggerConfig.logs_dir,
                    data=data
                )

    # Simple
    def red(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_red_log,
            write_flag=LoggerConfig.write_red_log,
            header=TextHeader.red,
            logtype_label='Red',
            log_dict=self.red_log,
            logname='red',
            logdir=LoggerConfig.simple_logs_dir
        )

    def green(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_green_log,
            write_flag=LoggerConfig.write_green_log,
            header=TextHeader.green,
            logtype_label='Green',
            log_dict=self.green_log,
            logname='green',
            logdir=LoggerConfig.simple_logs_dir
        )

    def yellow(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_yellow_log,
            write_flag=LoggerConfig.write_yellow_log,
            header=TextHeader.yellow,
            logtype_label='Yellow',
            log_dict=self.yellow_log,
            logname='yellow',
            logdir=LoggerConfig.simple_logs_dir
        )

    def blue(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_blue_log,
            write_flag=LoggerConfig.write_blue_log,
            header=TextHeader.blue,
            logtype_label='Blue',
            log_dict=self.blue_log,
            logname='blue',
            logdir=LoggerConfig.simple_logs_dir
        )

    def purple(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_purple_log,
            write_flag=LoggerConfig.write_purple_log,
            header=TextHeader.purple,
            logtype_label='Purple',
            log_dict=self.purple_log,
            logname='purple',
            logdir=LoggerConfig.simple_logs_dir
        )

    def cyan(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_cyan_log,
            write_flag=LoggerConfig.write_cyan_log,
            header=TextHeader.cyan,
            logtype_label='Cyan',
            log_dict=self.cyan_log,
            logname='cyan',
            logdir=LoggerConfig.simple_logs_dir
        )

    def white(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_white_log,
            write_flag=LoggerConfig.write_white_log,
            header=TextHeader.white,
            logtype_label='White',
            log_dict=self.white_log,
            logname='white',
            logdir=LoggerConfig.simple_logs_dir
        )

    # Debug
    def debug_normal(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_debug_normal_log,
            write_flag=LoggerConfig.write_debug_normal_log,
            header=TextHeader.debug_normal,
            logtype_label='Debug Normal',
            log_dict=self.debug_normal_log,
            logname='debug_normal',
            logdir=LoggerConfig.debug_logs_dir
        )

    def debug_bold(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_debug_bold_log,
            write_flag=LoggerConfig.write_debug_bold_log,
            header=TextHeader.debug_bold,
            logtype_label='Debug Bold',
            log_dict=self.debug_bold_log,
            logname='debug_bold',
            logdir=LoggerConfig.debug_logs_dir
        )

    def debug_crisp(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_debug_crisp_log,
            write_flag=LoggerConfig.write_debug_crisp_log,
            header=TextHeader.debug_crisp,
            logtype_label='Debug Crisp',
            log_dict=self.debug_crisp_log,
            logname='debug_crisp',
            logdir=LoggerConfig.debug_logs_dir
        )

    def debug_italic(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_debug_italic_log,
            write_flag=LoggerConfig.write_debug_italic_log,
            header=TextHeader.debug_italic,
            logtype_label='Debug Italic',
            log_dict=self.debug_italic_log,
            logname='debug_italic',
            logdir=LoggerConfig.debug_logs_dir
        )

    def debug_blink(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_debug_blink_log,
            write_flag=LoggerConfig.write_debug_blink_log,
            header=TextHeader.debug_blink,
            logtype_label='Debug Blink',
            log_dict=self.debug_blink_log,
            logname='debug_blink',
            logdir=LoggerConfig.debug_logs_dir
        )

    # Messages
    def good(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_good_log,
            write_flag=LoggerConfig.write_good_log,
            header=TextHeader.good,
            logtype_label='Good',
            log_dict=self.good_log,
            logname='good',
            logdir=LoggerConfig.messages_logs_dir
        )

    def info(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_info_log,
            write_flag=LoggerConfig.write_info_log,
            header=TextHeader.info,
            logtype_label='Info',
            log_dict=self.info_log,
            logname='info',
            logdir=LoggerConfig.messages_logs_dir
        )

    def warning(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_warning_log,
            write_flag=LoggerConfig.write_warning_log,
            header=TextHeader.warning,
            logtype_label='Warning',
            log_dict=self.warning_log,
            logname='warning',
            logdir=LoggerConfig.messages_logs_dir
        )

    def error(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_error_log,
            write_flag=LoggerConfig.write_error_log,
            header=TextHeader.error,
            logtype_label='Error',
            log_dict=self.error_log,
            logname='error',
            logdir=LoggerConfig.messages_logs_dir
        )

    def system(self, text):
        self._template(
            text=text,
            show_flag=LoggerConfig.show_system_log,
            write_flag=LoggerConfig.write_system_log,
            header=TextHeader.system,
            logtype_label='System',
            log_dict=self.system_log,
            logname='system',
            logdir=LoggerConfig.messages_logs_dir
        )

    def test_logger(self):
        print('Hi')
        self.good('Good')
        print('Hi')
        self.info('Info')
        print('Hi')
        self.warning('Warning')
        print('Hi')
        self.error('Error')
        print('Hi')
        self.system('System')
        print('Hi')
        self.debug_normal('Debug Normal')
        print('Hi')
        self.debug_bold('Debug Bold')
        print('Hi')
        self.debug_crisp('Debug Crisp')
        print('Hi')
        self.debug_italic('Debug Italic')
        print('Hi')
        self.debug_blink('Debug Blink')
        print('Hi')
        self.red('Red')
        print('Hi')
        self.green('Green')
        print('Hi')
        self.yellow('Yellow')
        print('Hi')
        self.blue('Blue')
        print('Hi')
        self.purple('Purple')
        print('Hi')
        self.cyan('Cyan')
        print('Hi')
        self.white('White')
        print('Hi')


logger = Logger()