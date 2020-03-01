import requests
import bs4
import collections

BlockZakaz = collections.namedtuple(
    'Block',
    (
        'name,'
        'value,'
        'stavk,'
        'url,'
    )
)

class Block(BlockZakaz):

    def __str__(self):
        return f'{self.name}            {self.value}         {self.stavk}     {self.url}'

class FreeLan:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }

    def error_code(self):
        url = "https://freelancehunt.com/projects?name=%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3"
        r = self.session.get(url)
        code = r.status_code
        if code == 200:
            print("[log] Подключение к сайту выполненно успешно")
        if 200 != code:
            print(f'[log] Неизвесная ошибка {code}')

    def get_page(self):
        url = "https://freelancehunt.com/projects?name=%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3"
        r = self.session.get(url)
        r.raise_for_status()
        return r.text

    def parse_block(self, item):
        # Парсим название
        name_block = item.select_one('a.bigger.visitable')
        name = name_block.string.strip()

        # Парсим ссылку
        href = name_block.get('href')

        # Парсим цены
        value_block = item.select_one('span')
        value = value_block.text.strip()

        stavk_block = item.select_one('a.text-orange.price')
        stavk = stavk_block.text.strip()

        return Block(
            name=name,
            value=value,
            stavk=stavk,
            url=href,
        )

    def get_block(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, "lxml")

        conteiner = soup.select('tr')
        for item in conteiner:
            block = self.parse_block(item = item)
            print(block)


    def run(self):
        self.get_block()



def main():
    pars = FreeLan()
    pars.run()



if __name__ == '__main__':
    main()
