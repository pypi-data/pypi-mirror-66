from requests import get
from time import sleep
import re


class Std:
    _vol_fill = False

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        self._vol_fill = True
        return self.normal_arc_name({'vol': idx.split('-')})

    def _elements(self, selector, content=None) -> list:
        if not content:
            content = self.content
        return self.document_fromstring(content, selector)

    def _cover_from_content(self, selector, attr='src') -> str:
        image = self._elements(selector)
        if image is not None and len(image):
            return self.http().normalize_uri(image[0].get(attr))

    @staticmethod
    def _first_select_options(parser, selector, skip_first=True) -> list:
        options = 'option'
        if skip_first:
            options = 'option + option'
        select = parser.cssselect(selector)
        if select:
            return select[0].cssselect(options)
        return []

    @classmethod
    def _images_helper(cls, parser, selector, attr='src', alternative_attr='data-src') -> list:
        image = parser.cssselect(selector)
        images = []
        for i in image:
            src = i.get(attr) or i.get(alternative_attr)
            images.append(src.strip(' \r\n\t\0'))
        return images

    @classmethod
    def _idx_to_x2(cls, idx, default=0) -> list:
        return [
            str(idx[0]),
            str(default if len(idx) < 2 or not idx[1] else idx[1])
        ]

    @staticmethod
    def _join_groups(idx, glue='-') -> str:
        result = []
        for i in idx:
            if i:
                result.append(i)
        return glue.join(result)

    def _get_name(self, selector, url=None) -> str:
        if url is None:
            url = self.get_url()
        return re.search(selector, url).group(1)

    def _get_content(self, tpl) -> str:
        return self.http_get(tpl.format(self.domain, self.manga_name))

    def _base_cookies(self, url=None):
        if url is None:
            url = self.get_url()
        cookies = self.http().get_base_cookies(url)
        self._storage['cookies'] = cookies.get_dict()

    def parse_background(self, image) -> str:
        url = re.search(
            r'background.+?url\([\'"]?([^\s]+?)[\'"]?\)',
            image.get('style')
        )
        return self.http().normalize_uri(url.group(1))

    @property
    def manga_name(self) -> str:
        name = self._storage.get('manga_name', None)
        if name is None:
            name = self.get_manga_name()
        return name

    def normal_arc_name(self, idx):
        if isinstance(idx, str):
            idx = [idx]
        if isinstance(idx, list):
            self._vol_fill = True
            return self.__normal_name_list(idx)
        if isinstance(idx, dict):
            return self.__normal_name_dict(idx)
        raise DeprecationWarning('Wrong arc name type: %s' % type(idx))

    @staticmethod
    def __fill(var, fmt: str = '-{}'):
        if isinstance(var, str):
            var = [var]
        return (fmt * len(var)).format(*var).lstrip('-')

    def __normal_name_list(self, idx: list):
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}' * (len(idx) - 1)
        elif self._vol_fill and self._zero_fill:
            idx.append('0')
            fmt += '-{}'
        return fmt.format(*idx)

    def __normal_name_dict(self, idx: dict):
        vol = idx.get('vol', None)
        ch = idx.get('ch', None)
        result = ''
        if vol:
            if isinstance(vol, str):
                vol = [vol]
            result = self.__normal_name_list(vol)
        if ch:
            result += '-ch_' + self.__fill(ch)

        if self._with_manga_name:
            name = self._params.get('name', '')
            if not len(name):
                name = self.manga_name

            result = '%s-%s' % (name, result)

        return result

    def text_content(self, content, selector, idx: int = 0, strip: bool = True):
        doc = self.document_fromstring(content, selector)
        if not doc:
            return None
        text = doc[idx].text_content()
        if strip:
            text = text.strip()
        return text

    def _download(self, file_name, url, method):
        # clean file downloader
        now_try_count = 0
        while now_try_count < 5:
            with open(file_name, 'wb') as out_file:
                now_try_count += 1
                response = get(url, timeout=60, allow_redirects=True)
                if response.status_code >= 400:
                    self.http().debug and self.log('ERROR! Code {}\nUrl: {}'.format(
                        response.status_code,
                        url,
                    ))
                    sleep(2)
                    continue
                out_file.write(response.content)
                response.close()
                out_file.close()
                break

    @staticmethod
    def _test_url(url: str, path: str = None) -> bool:
        _path = r'https?://.+?\.\w{2,7}'
        if path is not None:
            _path += path
        _re = re.compile(_path)
        return _re.search(url) is not None
