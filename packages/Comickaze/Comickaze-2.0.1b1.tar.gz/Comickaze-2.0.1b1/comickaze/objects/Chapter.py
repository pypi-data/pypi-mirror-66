from .Comic import Comic


class Chapter:
    def __init__(self, comickaze, title: str, link: str, comic: Comic, date=None):
        """Chapter of a {Comic}

        Arguments:
            comickaze {Comickaze} -- Comickaze instance
            title {str} -- Title
            link {str} -- Link
            comic {Comic} -- Comic that contains this {Chapter}

        Keyword Arguments:
            date {datetime|str} -- Date published (default: {None})
        """

        self.comickaze = comickaze
        self.title = title
        self.link = link
        self.comic = comic
        self.date = date
        self.pages = []

    def get_pages(self):
        return self.comickaze.get_chapter_pages(self)

    def __str__(self):
        return self.title
