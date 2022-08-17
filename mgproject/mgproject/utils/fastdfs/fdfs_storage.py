from django.conf import settings
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """自定义文件存储系统，修改存储的方案"""

    def __init__(self,fdfs_base_url=None):
        """
        构造方法，可以不带参数，也可以携带参数
        :param base_url: Storage的IP
        """
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def url(self, name):
        """
        返回name所指文件的绝对URL
        :param name: 图片存在数据库中的相对地址
        :return
        """
        return self.fdfs_base_url + name