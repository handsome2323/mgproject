from .models import NewsChannel


def get_channels(request):

    '''

    获取导航信息
    :param request:
    :return:
    '''
    channels = NewsChannel.objects.order_by('id')


    return {'channels':channels}


