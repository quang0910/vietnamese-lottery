import requests
import bs4
import sys


class ServerError(Exception):
    pass


def ketqua():
    resp = requests.get('http://ketqua.net')
    if resp.status_code // 100 == 5:
        raise ServerError('Cannot connect to server!')
    tree = bs4.BeautifulSoup(resp.text, features="lxml")
    date = tree.find(attrs={'id': 'result_date'}).text
    prizes = {}
    prizes['Đặc biệt'] = [tree.find(attrs={'id': 'rs_0_0'}).text]
    prizes['Giải nhất'] = [tree.find(attrs={'id': 'rs_1_0'}).text]
    prizes['Giải nhì'] = [tree.find(attrs={'id': 'rs_2_{}'.format(i)}).text
                          for i in range(2)]
    prizes['Giải ba'] = [tree.find(attrs={'id': 'rs_3_{}'.format(i)}).text
                         for i in range(6)]
    prizes['Giải tư'] = [tree.find(attrs={'id': 'rs_4_{}'.format(i)}).text
                         for i in range(4)]
    prizes['Giải năm'] = [tree.find(attrs={'id': 'rs_5_{}'.format(i)}).text
                          for i in range(6)]
    prizes['Giải sáu'] = [tree.find(attrs={'id': 'rs_6_{}'.format(i)}).text
                          for i in range(3)]
    prizes['Giải bảy'] = [tree.find(attrs={'id': 'rs_7_{}'.format(i)}).text
                          for i in range(4)]
    return prizes, date


def check_ketqua(*args):
    prizes, date = ketqua()
    list_prizes = [i[-2:] for j in prizes for i in prizes[j]]
    count = 0
    print(date)
    for num in args:
        if num in list_prizes:
            count += 1
            cnt = list_prizes.count(num)
            print('Bạn đã trúng lô x{1} với số {0}'.format(num, cnt))
    if count == 0:
        print('Rất tiếc bạn không trúng lô\nDanh sách giải:')
        for prize in prizes:
            print(prize, ':', prizes[prize])
    return None


def main():
    for arg in sys.argv[1:]:
        if len(arg) != 2:
            raise ValueError('Nhập sai số lô')
    check_ketqua(*sys.argv[1:])


if __name__ == "__main__":
    main()
