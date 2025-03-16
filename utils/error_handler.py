import inspect
import os


def exception_log_message(exc_tb, extra_message=''):
    # exc_tb: traceback object containing information about the error
    # extra_message: additional message to be included in the log
    #   Usage Example:
    #   log_message = exception_log_message(sys.exc_info()[2])
    #   logger.error(log_message)
    ######### sys.exc_info()[2] :  Return information about the most recent exception caught by an except

    log_message = ''
    source_lines, _ = inspect.findsource(exc_tb.tb_frame)
    error_line = source_lines[exc_tb.tb_lineno - 1].strip()
    if extra_message:
        log_message += extra_message
        log_message += ' - '
    log_message += f'Error: {exc_tb.tb_frame.f_locals.get("error","no specific error")} File: "{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}", line {exc_tb.tb_lineno} - {error_line}'
    return log_message
