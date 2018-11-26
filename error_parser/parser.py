import os
import re
import json


class JsonParams:
    """
    Constants to store output json parameters
    """

    def __init__(self):
        self.FILE_NAME = 'filename'
        self.EXCEPTIONS = 'exceptions'
        self.LINE = 'line'
        self.ERROR_FILE = 'file'
        self.TYPE = 'type'
        self.MESSAGE = 'message'


class LogRegexp:
    """
    Constants to store regexp for parsing errors in files
    """

    def __init__(self):
        self.TRACEBACK = re.compile('^Traceback')
        self.ERROR_TYPE = re.compile('^[A-Z]\w+Error')
        self.ERROR_PLACE = re.compile('^\s+File\s')
        self.ERROR_LINE = re.compile('line\s\d+')
        self.ERROR_FILE = re.compile('"[^"]*"')


class LogParser:

    output_params = JsonParams()
    log_regexp = LogRegexp()

    def __init__(self, path, files=None):
        self.path = path
        if type(files) is str:
            self.files = [files]
        else:
            self.files = files

    def print_errors(self):
        """
        Prints parsed errors
        """

        print(json.dumps(self.files_to_json(), indent=2))

    def files_to_json(self):
        """
        Collects parsed error info from all files

        :return: array of info about exceptions in files
        """

        if not os.path.exists(self.path):
            return 'Path does not exist'
        if self.files is not None:
            self._path_files_format()
        if self.files is None:
            self.files = self._path_files()
        if self.files is None:
            return 'No files to parse'

        json_output = []

        for file in self.files:
            file_json = self._parse_file_errors(file)
            json_output.append({self.output_params.FILE_NAME: file,
                                self.output_params.EXCEPTIONS: file_json})

        return json_output

    def _parse_file_errors(self, file):
        """
        Reads file and extracts all traceback info

        :param file: path to the file to read and parse
        :return: array of file errors
        """

        with open(file, 'r') as lines:
            errors = []

            for line in lines:
                if self.log_regexp.TRACEBACK.match(line):
                    errors.append({})

                if self.log_regexp.ERROR_PLACE.match(line):
                    code_line = re.search(self.log_regexp.ERROR_LINE, line)[0]
                    error_file = re.search(self.log_regexp.ERROR_FILE, line)[0]
                    errors[-1][self.output_params.LINE] = int(code_line.split()[1])
                    errors[-1][self.output_params.ERROR_FILE] = error_file.strip('"')

                if self.log_regexp.ERROR_TYPE.match(line):
                    type_error = re.search(self.log_regexp.ERROR_TYPE, line)[0]
                    message = line[len(type_error)+1:]
                    errors[-1].update({self.output_params.TYPE: type_error})
                    errors[-1].update({self.output_params.MESSAGE: message.strip()})

            return errors

    def _path_files(self):
        """
        Extracts all files from the path and subpathes of self.path

        :return: array of files
        """

        if not os.path.exists(self.path):
            return None

        directory_content = os.listdir(self.path)
        files = []

        while len(directory_content) != 0:

            if not directory_content[0].startswith(self.path):
                directory_obj = os.path.join(self.path, directory_content[0])
            else:
                directory_obj = directory_content[0]

            if os.path.isfile(directory_obj):
                files.append(directory_obj)
            elif os.path.exists(directory_obj):
                temp_directory_content = os.listdir(directory_obj)
                for obj in temp_directory_content:
                    directory_content.append(os.path.join(directory_obj, obj))
            directory_content.pop(0)

        return files

    def _path_files_format(self):
        """
        Checks if files from constructor have a correct path
        """

        correct_files = []

        for file in self.files:
            if not file.startswith(self.path):
                correct_files.append(os.path.join(self.path, file))
            else:
                correct_files.append(file)

        self.files = correct_files


