# coding=utf-8
import json
from os import path
from pod_base import PodBase, calc_offset, ConfigException

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class PodSocial(PodBase):

    def __init__(self, api_token, token_issuer="1", server_type="sandbox", config_path=None,
                 sc_api_key="", sc_voucher_hash=None):
        here = path.abspath(path.dirname(__file__))
        self._services_file_path = path.join(here, "services.json")
        super(PodSocial, self).__init__(api_token, token_issuer, server_type, config_path, sc_api_key, sc_voucher_hash,
                                        path.join(here, "json_schema.json"))

    def __get_private_call_address(self):
        """
        دریافت آدرس سرور پرداخت از فایل کانفیگ

        :return: str
        :raises: :class:`ConfigException`
        """
        private_call_address = self.config.get("private_call_address", self._server_type)
        if private_call_address:
            return private_call_address

        raise ConfigException("config `private_call_address` in {} not found".format(self._server_type))

    @staticmethod
    def __convert_list_to_str(items, index, delimiter=","):
        if index in items:
            items[index] = [str(val) for val in items[index]]
            return delimiter.join(items[index])
        return ""

    @staticmethod
    def __remove_empty_items(items):
        return {key: value for key, value in items.items() if value != "" and value is not None and value != {}}

    def add_custom_post(self, name, content, can_comment=True, can_like=True, can_rate=True, enable=True, **kwargs):
        """
        ایجاد پست سفارشی

        :param str name: نام پست
        :param str content: محتوا
        :param bool can_comment: آیا امکان ثبت نظر وجود دارد؟
        :param bool can_like: آیا امکان ثبت لایک وجود دارد؟
        :param bool can_rate: آیا امکان امتیازدهی وجود دارد؟
        :param bool enable: آیا پست فعال است؟

        :return: dict
        """
        params = kwargs.copy()
        params["name"] = name
        params["content"] = content
        params["canComment"] = can_comment
        params["canLike"] = can_like
        params["canRate"] = can_rate
        params["enable"] = enable

        self._validate(params, "addCustomPost")
        if "metadata" in params:
            params["metadata"] = json.dumps(params["metadata"])

        params["tags"] = self.__convert_list_to_str(params, "tags")
        params["tagTreeCategoryName"] = self.__convert_list_to_str(params, "tagTreeCategoryName")
        params["tagTrees"] = self.__convert_list_to_str(params, "tagTrees")
        params = self.__remove_empty_items(params)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/addCustomPost", method_type="post"),
            params=params, headers=self._get_headers(), **kwargs)

    def get_custom_post_list(self, business_id, page=1, size=50, token=None, **kwargs):
        """
        لیست پست های سفارشی

        :param int business_id: شناسه کسب و کار
        :param int page: شماره صفحه
        :param int size: تعداد رکورد در هر صفحه
        :param str|None token: اکسس توکن کاربر - اگر ارسال نشود، توکن کسب و کار ارسال می شود.

        :return: list
        """
        params = kwargs.copy()
        params["businessId"] = business_id
        if "lastId" not in params and "firstId" not in params:
            params["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)

        params["size"] = size

        self._validate(params, "getCustomPostList")
        params["id"] = self.__convert_list_to_str(params, "id")
        params["uniqueId"] = self.__convert_list_to_str(params, "uniqueId")
        params["tags"] = self.__convert_list_to_str(params, "tags")
        params["tagTrees"] = self.__convert_list_to_str(params, "tagTrees")
        params["tagTreeCategoryName"] = self.__convert_list_to_str(params, "tagTreeCategoryName")
        params = self.__remove_empty_items(params)

        headers = self._get_headers()
        if token is not None:
            headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/customPostList"), params=params, headers=headers,
            **kwargs)

    def add_custom_post_list(self, posts, **kwargs):
        """
        اضافه کردن گروهی پست سفارشی

        :param list posts: لیست اطلاعات پست ها

        :return: list
        """
        self._validate({"posts": posts}, "addCustomPostList")
        posts = self.__prepare_posts(posts=posts)

        params = {
            "data": json.dumps(posts)
        }

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/addCustomPostList", method_type="post"),
            params=params, headers=self._get_headers(), **kwargs)

    def __prepare_posts(self, posts):
        output = []
        for post in posts:
            if "metadata" in post:
                post["metadata"] = json.dumps(post["metadata"])

            post["tags"] = self.__convert_list_to_str(post, "tags")
            post["tagTreeCategoryName"] = self.__convert_list_to_str(post, "tagTreeCategoryName")
            post["tagTrees"] = self.__convert_list_to_str(post, "tagTrees")

            output.append(self.__remove_empty_items(post))

        return output

    def update_custom_post(self, entity_id, name, content, can_comment=True, can_like=True, can_rate=True, enable=True,
                           **kwargs):
        """
        ویرایش پست سفارشی ثبت شده توسط کسب و کار

        :param int entity_id: شناسه پست سفارشی
        :param str name: نام پست
        :param str content: محتوا
        :param bool can_comment: آیا امکان ثبت نظر وجود دارد؟
        :param bool can_like: آیا امکان ثبت لایک وجود دارد؟
        :param bool can_rate: آیا امکان امتیازدهی وجود دارد؟
        :param bool enable: آیا پست فعال است؟

        :return: dict
        """
        params = kwargs.copy()
        params["entityId"] = entity_id
        params["name"] = name
        params["content"] = content
        params["canComment"] = can_comment
        params["canLike"] = can_like
        params["canRate"] = can_rate
        params["enable"] = enable

        self._validate(params, "updateCustomPost")
        if "metadata" in params:
            params["metadata"] = json.dumps(params["metadata"])

        params["tags"] = self.__convert_list_to_str(params, "tags")
        params["tagTreeCategoryName"] = self.__convert_list_to_str(params, "tagTreeCategoryName")
        params["tagTrees"] = self.__convert_list_to_str(params, "tagTrees")
        params = self.__remove_empty_items(params)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/updateCustomPost"), params=params,
            headers=self._get_headers(), **kwargs)

    def update_user_post(self, entity_id, name, content, token, can_comment=True, can_like=True, enable=True, **kwargs):
        """
        ویرایش پست سفارشی ثبت شده توسط کاربر

        :param int entity_id: شناسه پست سفارشی
        :param str name: نام پست
        :param str content: محتوا
        :param str token: اکسس توکن کاربر
        :param bool can_comment: آیا امکان ثبت نظر وجود دارد؟
        :param bool can_like: آیا امکان ثبت لایک وجود دارد؟
        :param bool enable: آیا پست فعال است؟

        :return: dict
        """
        params = kwargs.copy()
        params["entityId"] = entity_id
        params["name"] = name
        params["content"] = content
        params["canComment"] = can_comment
        params["canLike"] = can_like
        params["enable"] = enable

        self._validate(params, "updateUserPost")
        if "metadata" in params:
            params["metadata"] = json.dumps(params["metadata"])

        params["tags"] = self.__convert_list_to_str(params, "tags")
        params = self.__remove_empty_items(params)

        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/updateUserPost"), params=params,
            headers=headers, **kwargs)

    def add_comment(self, post_id, comment, token, **kwargs):
        """
        ثبت نظر برای یک پست

        :param int post_id: شناسه پست
        :param str comment: نظر کاربر
        :param str token: اکسس توکن کاربر

        :return: int
        """
        kwargs["postId"] = post_id
        kwargs["text"] = comment
        self._validate(kwargs, "addComment")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/comment"), params=kwargs, headers=headers, **kwargs)

    def get_comment_list(self, post_id, page=1, size=50, **kwargs):
        """
        دریافت لیست نظرات

        :param int post_id: شناسه پست
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """
        kwargs["postId"] = post_id
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getCommentList")

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/commentList"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def confirm_comment_of_custom_post(self, comment_id, **kwargs):
        """
        تایید کردن نظر پست سفارشی

        :param int comment_id: شناسه نظر

        :return: bool
        """
        kwargs["commentId"] = comment_id

        self._validate(kwargs, "confirmCommentOfCustomPost")

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/confirmComment"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def un_confirm_comment_of_custom_post(self, comment_id, **kwargs):
        """
        عدم تایید کردن نظر پست سفارشی

        :param int comment_id: شناسه نظر

        :return: bool
        """
        kwargs["commentId"] = comment_id

        self._validate(kwargs, "unconfirmCommentOfCustomPost")

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/unconfirmComment"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def get_confirm_comments(self, post_id, token, page=1, size=50, **kwargs):
        """
        دریافت لیست نظرات کاربران

        :param int post_id: شناسه پست
        :param str token: اکسس توکن کاربر
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """
        kwargs["postId"] = post_id
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getCommentList")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/commentList"), params=kwargs, headers=headers,
            **kwargs)

    def like_post(self, post_id, token, **kwargs):
        """
        لایک پست

        :param int post_id: شناسه پست
        :param str token: اکسس توکن کاربر

        :return: bool
        """
        kwargs["postId"] = post_id

        self._validate(kwargs, "likePost")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(super(PodSocial, self)._get_sc_product_settings("/nzh/like"), params=kwargs,
                                  headers=headers, **kwargs)

    def dislike_post(self, post_id, token, **kwargs):
        """
        دیس لایک پست

        :param int post_id: شناسه پست
        :param str token: اکسس توکن کاربر

        :return: bool
        """
        kwargs["postId"] = post_id

        self._validate(kwargs, "dislikePost")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(super(PodSocial, self)._get_sc_product_settings("/nzh/dislikePost"), params=kwargs,
                                  headers=headers, **kwargs)

    def get_like_list(self, post_id, token, page=1, size=50, **kwargs):
        """
        دریافت لیست لایک های یک پست

        :param int post_id: شناسه پست
        :param str token: اکسس توکن کاربر
        :param int page: شماره صفحه
        :param int size: تعداد رکورد در هر صفحه

        :return: list
        """
        kwargs["postId"] = post_id
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getLikeList")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(super(PodSocial, self)._get_sc_product_settings("/nzh/likeList"), params=kwargs,
                                  headers=headers, **kwargs)

    def like_comment(self, comment_id, token, **kwargs):
        """
        لایک کامنت

        :param int comment_id: شناسه نظر
        :param str token: اکسس توکن کاربر

        :return: bool
        """
        return self.__like_dislike_comment(comment_id=comment_id, token=token, **kwargs)

    def dislike_comment(self, comment_id, token, **kwargs):
        """
        دیس لایک کامنت

        :param int comment_id: شناسه نظر
        :param str token: اکسس توکن کاربر

        :return: bool
        """
        return self.__like_dislike_comment(comment_id=comment_id, token=token, dislike=True, **kwargs)

    def __like_dislike_comment(self, comment_id, token, dislike=False, **kwargs):
        """
        لایک /دیس لایک کامنت

        :param int comment_id: شناسه نظر
        :param str token: اکسس توکن کاربر
        :param bool dislike: لایک یا دیس لایک

        :return: list
        """
        kwargs["commentId"] = comment_id
        kwargs["dislike"] = dislike

        self._validate(kwargs, "likeComment")
        kwargs["dislike"] = str(kwargs["dislike"]).lower()
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(super(PodSocial, self)._get_sc_product_settings("/nzh/likeComment"), params=kwargs,
                                  headers=headers, **kwargs)

    def get_comment_like_list(self, comment_id, token, page=1, size=50, **kwargs):
        """
        دریافت لیست لایک های یک نظر

        :param int comment_id: شناسه نظر
        :param str token: اکسس توکن کاربر
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """
        kwargs["commentId"] = comment_id
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getCommentLikeList")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/commentLikeList"), params=kwargs, headers=headers,
            **kwargs)

    def get_business_time_line(self, page=1, size=50, **kwargs):
        """
        نمایش تایم لاین مربوط به کسب و کار

        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getBusinessTimeline")
        kwargs["postId"] = self.__convert_list_to_str(kwargs, "postId")
        kwargs["uniqueId"] = self.__convert_list_to_str(kwargs, "uniqueId")
        kwargs["guildCodes"] = self.__convert_list_to_str(kwargs, "guildCodes")
        kwargs["tags"] = self.__convert_list_to_str(kwargs, "tags")
        kwargs["tagTreeCategoryName"] = self.__convert_list_to_str(kwargs, "tagTreeCategoryName")
        kwargs["tagTrees"] = self.__convert_list_to_str(kwargs, "tagTrees")
        if "metadata" in kwargs:
            kwargs["metadata"] = json.dumps(kwargs["metadata"])
        kwargs = self.__remove_empty_items(kwargs)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/timeline"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def get_time_line(self, token, page=1, size=50, **kwargs):
        """
        نمایش تایم لاین

        :param str token: اکسس توکن کاربر
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "getTimeline")
        kwargs["postId"] = self.__convert_list_to_str(kwargs, "postId")
        kwargs["uniqueId"] = self.__convert_list_to_str(kwargs, "uniqueId")
        kwargs["guildCodes"] = self.__convert_list_to_str(kwargs, "guildCodes")
        kwargs["tags"] = self.__convert_list_to_str(kwargs, "tags")
        kwargs["tagTreeCategoryName"] = self.__convert_list_to_str(kwargs, "tagTreeCategoryName")
        kwargs["tagTrees"] = self.__convert_list_to_str(kwargs, "tagTrees")
        if "metadata" in kwargs:
            kwargs["metadata"] = json.dumps(kwargs["metadata"])
        kwargs = self.__remove_empty_items(kwargs)
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/timeline"), params=kwargs, headers=headers,
            **kwargs)

    def search_time_line_by_metadata(self, meta_query, page=1, size=50, **kwargs):
        """
        جستجو در تایم لاین براساس متادیتا

        :param dict meta_query: عبارت جستجو در متادیتا
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """

        kwargs["metaQuery"] = meta_query
        kwargs["offset"] = calc_offset(page, size)
        kwargs["size"] = size
        self._validate(kwargs, "searchTimelineByMetadata")
        kwargs["metaQuery"] = json.dumps(meta_query)
        kwargs["postIds"] = self.__convert_list_to_str(kwargs, "postIds")
        kwargs["orderBy"] = self.__convert_list_to_str(kwargs, "orderBy")
        kwargs = self.__remove_empty_items(kwargs)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/searchTimelineByMetadata"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def full_text_search(self, query, page=1, size=50, **kwargs):
        """
        جستجوی کامل متنی

        :param str query: عبارت جستجو در متادیتا
        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه

        :return: list
        """

        kwargs["query"] = query
        kwargs["offset"] = calc_offset(page, size)
        kwargs["size"] = size
        self._validate(kwargs, "fullTextSearch")
        kwargs["guildCodes"] = self.__convert_list_to_str(kwargs, "guildCodes")
        kwargs["tags"] = self.__convert_list_to_str(kwargs, "tags")
        kwargs["tagTree"] = self.__convert_list_to_str(kwargs, "tagTree")
        kwargs["tagTreeCodes"] = self.__convert_list_to_str(kwargs, "tagTreeCodes")
        kwargs = self.__remove_empty_items(kwargs)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/biz/search"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def add_user_post(self, name, content, token, can_comment=True, can_like=True, can_rate=True, enable=True,
                      **kwargs):
        """
        ایجاد پست کاربری

        :param str name: نام پست
        :param str content: محتوای پست
        :param str token: اکسس توکن کاربر
        :param bool can_comment: آیا امکان ثبت نظر وجود دارد؟
        :param bool can_like: آیا امکان ثبت لایک وجود دارد؟
        :param bool can_rate: آیا امکان امتیازدهی وجود دارد؟
        :param bool enable: آیا پست فعال است؟

        :return: dict
        """

        kwargs["name"] = name
        kwargs["content"] = content
        kwargs["canComment"] = can_comment
        kwargs["canLike"] = can_like
        kwargs["canRate"] = can_rate
        kwargs["enable"] = enable
        self._validate(kwargs, "addUserPost")
        kwargs["tags"] = self.__convert_list_to_str(kwargs, "tags")

        if "metadata" in kwargs:
            kwargs["metadata"] = json.dumps(kwargs["metadata"])

        kwargs = self.__remove_empty_items(kwargs)

        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/addUserPost"), params=kwargs, headers=headers,
            **kwargs)

    def user_post_list(self, page=1, size=50, token=None, **kwargs):
        """
        لیست پست های کاربری

        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه
        :param str|None token: اکسس توکن کاربر - اگر ارسال نشود توکن کسب و کاری ارسال می شود

        :return: list
        """
        if "lastId" not in kwargs and "firstId" not in kwargs:
            kwargs["offset"] = calc_offset(page, size)
        else:
            kwargs.pop("offset", 0)
        kwargs["size"] = size

        self._validate(kwargs, "userPostList")
        kwargs["tags"] = self.__convert_list_to_str(kwargs, "tags")
        kwargs = self.__remove_empty_items(kwargs)
        headers = self._get_headers()
        if token is not None:
            headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/userPostList"), params=kwargs, headers=headers,
            **kwargs)

    def load_user_post(self, entity_id, token=None, **kwargs):
        """
        دریافت یک پست کاربری

        :param int entity_id: شناسه موجودیت پست
        :param str|None token: اکسس توکن کاربر - اگر ارسال نشود توکن کسب و کاری ارسال می شود

        :return: dict
        """
        kwargs["entityId"] = entity_id

        self._validate(kwargs, "loadUserPost")
        headers = self._get_headers()
        if token is not None:
            headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/loadUserPost"), params=kwargs, headers=headers,
            **kwargs)

    def search_on_user_post_by_metadata(self, meta_query, user_id, page=1, size=50, **kwargs):
        """
        جستجو در متادیتا پست کاربری

        :param dict meta_query: عبارت جستجو در متادیتا
        :param int user_id: شناسه کاربری
        :param int page: شماره صفحه
        :param int size: تعداد رکورد در هر صفحه

        :return: list
        """
        kwargs["userId"] = user_id
        kwargs["metaQuery"] = meta_query
        kwargs["page"] = page
        kwargs["size"] = size

        self._validate(kwargs, "searchOnUserPostByMetadata")
        kwargs["metaQuery"] = json.dumps(kwargs["metaQuery"])
        kwargs["orderBy"] = self.__convert_list_to_str(kwargs, "orderBy")
        kwargs["postIds"] = self.__convert_list_to_str(kwargs, "postIds")
        kwargs = self.__remove_empty_items(kwargs)

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/searchOnUserPostByMetadata"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def confirm_comment_of_user_post(self, comment_id, **kwargs):
        """
        تایید کامنت پست کاربری

        :param int comment_id: شناسه نظر

        :return: bool
        """
        kwargs["commentId"] = comment_id

        self._validate(kwargs, "confirmCommentOfUserPost")

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/confirmComment"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def un_confirm_comment_of_user_post(self, comment_id, **kwargs):
        """
        رد کامنت پست کاربری

        :param int comment_id: شناسه نظر

        :return: bool
        """
        kwargs["commentId"] = comment_id

        self._validate(kwargs, "unconfirmCommentOfUserPost")

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/unconfirmComment"), params=kwargs,
            headers=self._get_headers(), **kwargs)

    def share_user_post(self, forwarded_post_id, token, can_comment=True, can_like=True, can_rate=True, enable=True,
                        confirmation=False, **kwargs):
        """
        به اشتراک گذاری پست

        :param int forwarded_post_id: شناسه نظر
        :param str token: اکسس توکن کاربر
        :param bool can_comment: آیا امکان ثبت نظر وجود دارد؟
        :param bool can_like: آیا امکان ثبت لایک وجود دارد؟
        :param bool can_rate: آیا امکان امتیازدهی وجود دارد؟
        :param bool enable: آیا پست فعال است؟
        :param bool confirmation: آیا پست های جواب نیاز به تایید صاحب پست دارند؟

        :return: bool
        """
        kwargs["forwardedPostId"] = forwarded_post_id
        kwargs["canComment"] = can_comment
        kwargs["canLike"] = can_like
        kwargs["canRate"] = can_rate
        kwargs["enable"] = enable
        kwargs["confirmation"] = confirmation

        self._validate(kwargs, "shareUserPost")
        headers = self._get_headers()
        headers["_token_"] = token

        return self._request.call(
            super(PodSocial, self)._get_sc_product_settings("/nzh/shareUserPost"), params=kwargs, headers=headers,
            **kwargs)
