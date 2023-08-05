# coding=utf-8


class PostType:
    """
    انواع پست
    """

    def __init__(self):
        pass

    """ محصول """
    PRODUCT = 1

    """ خبر """
    NEWS = 2

    """ قرعه کشی """
    POLL = 4

    """ مسابقه """
    MATCH = 8

    """ فروش ویژه """
    SPECIAL_SALE = 16

    """ رای گیری """
    VOTING = 32

    """ قرعه کشی مسابقه """
    LOTTERY_MATCH = 64

    """ اعلام قرعه کشی """
    LOTTERY_RESULT = 128

    """ قرعه کشی نطرسنجی """
    LOTTERY_POLL = 512

    """ قرعه کشی رای گیری """
    LOTTERY_VOTING = 1024

    """ قرعه کشی """
    LOTTERY = 2048

    """ پست سفارشی """
    CUSTOM_POST = 4096

