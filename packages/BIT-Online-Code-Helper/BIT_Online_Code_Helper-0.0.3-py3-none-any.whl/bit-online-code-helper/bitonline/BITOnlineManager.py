import requests
from bitonline.LoginManager import *
from bitonline.ProblemManager import *
from bitonline.LocalTestCodeManager import *
from bitonline.OnlineTestCodeManager import *
from log.LogManager import *
import pickle


class _BITOnlineManager:
    def __init__(self):
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36 '
        }
        self.__session = requests.session()

        self.__login_manager = login_manager
        self.__problem_manager = problem_manager
        self.__local_test_code_manager = local_test_code_manager
        self.__commit_online_manager = commit_online_manager

        self.__login_manager.set_session(self.__session)
        self.__problem_manager.set_session(self.__session)
        self.__commit_online_manager.set_session(self.__session)

        self.__is_login = False
        self.__cookie_file_path = './cookies.bch'

        self.__load_cookie()

    def __load_cookie(self):
        try:
            cookie_file = open(self.__cookie_file_path, 'rb')
            self.__session.cookies.update(pickle.load(cookie_file))
            cookie_file.close()
        except FileNotFoundError:
            pass

    def output_helper_baseinfo(self):
        divide_line()
        tip(HelperBaseInfoLogs.NAME)
        tip(HelperBaseInfoLogs.AUTHOR)
        divide_line()

    def login(self):
        self.__login_manager.login()
        self.__is_login = self.__login_manager.get_is_login()

        if self.__is_login:
            cookie_file = open(self.__cookie_file_path, 'wb')
            pickle.dump(self.__session.cookies, cookie_file)
            cookie_file.close()

        divide_line()

    def __get_problem_info(self, problem_url):
        return self.__problem_manager.get_problem_info(problem_url)

    def local_test_code(self, problem_url, source_file_path):
        problem_info = self.__get_problem_info(problem_url)
        return self.__local_test_code_manager.run(source_file_path, problem_info)

    def online_test_code(self, problem_url, source_file_path):
        self.__commit_online_manager.run(source_file_path, problem_url)

    def local_and_online_test_code(self, problem_url, source_file_path):
        if self.local_test_code(problem_url, source_file_path):
            self.online_test_code(problem_url, source_file_path)


bit_online_manager = _BITOnlineManager()
