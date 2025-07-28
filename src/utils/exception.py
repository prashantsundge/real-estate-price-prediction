
import sys
import traceback

class RealEstateException(Exception):
    def __init__(self, error_message:str, error_detail:sys):
        _,_, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_type = type(error_message).__name__
        
        detailed_message =(
            f"Exception Type : {error_type} | "
            f"File : {file_name} |"
            f"Line : {line_number} |"
            f"Message : {error_message}"
        )

        super().__init__(detailed_message)

    def __str__(self):
        return self.args[0]
    