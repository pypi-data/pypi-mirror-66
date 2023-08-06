import re


def get_class_name(model_class):
    """
    Returns Normalized class name
    :param model_class: Must be class, not instance
    :return: str
    """
    if "'" in str(model_class):
        return re.findall("\'(.*?)\'", str(model_class))[0]
    return "None"


def parse_quotes(text: str) -> list:
    between_quotes = re.findall("\"(.*?)\"", text)
    for between in between_quotes:
        text = text.replace(between,between.replace(' ','§'))

    no_spaces_list = text.split(' ')
    for i in range(len(no_spaces_list)):
        no_spaces_list[i] = no_spaces_list[i].replace('§',' ')

    return no_spaces_list


