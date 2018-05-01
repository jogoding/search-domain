import requests
import xml.etree.ElementTree as ET
import time

sess = requests.Session()
sess.headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML,  like Gecko) Chrome/50.0.2661.87 Safari/537.36'


def verify(length, typ, suffix):
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
    pinyin = ["a", "ai", "an", "ang", "ao", "ba", "bai", "ban", "bang", "bao", "bei", "ben", "beng", "bi", "bian",
              "biao", "bie", "bin", "bing", "bo", "bu", "ca", "cai", "can", "cang", "cao", "ce", "ceng", "cha", "chai",
              "chan", "chang", "chao", "che", "chen", "cheng", "chi", "chong", "chou", "chu", "chuai", "chuan",
              "chuang", "chui", "chun", "chuo", "ci", "cong", "cou", "cu", "", "cuan", "cui", "cun", "cuo", "da", "dai",
              "dan", "dang", "dao", "de", "deng", "di", "dian", "diao", "die", "ding", "diu", "dong", "dou", "du",
              "duan", "dui", "dun", "duo", "e", "en", "er", "fa", "fan", "fang", "fei", "fen", "feng", "fo", "fou",
              "fu", "ga", "gai", "gan", "gang", "gao", "ge", "gei", "gen", "geng", "gong", "gou", "gu", "gua", "guai",
              "guan", "guang", "gui", "gun", "guo", "ha", "hai", "han", "hang", "hao", "he", "hei", "hen", "heng",
              "hong", "hou", "hu", "hua", "huai", "huan", "huang", "hui", "hun", "huo", "ji", "jia", "jian", "jiang",
              "jiao", "jie", "jin", "jing", "jiong", "jiu", "ju", "juan", "jue", "jun", "ka", "kai", "kan", "kang",
              "kao", "ke", "ken", "keng", "kong", "kou", "ku", "kua", "kuai", "kuan", "kuang", "kui", "kun", "kuo",
              "la", "lai", "lan", "lang", "lao", "le", "lei", "leng", "li", "lia", "lian", "liang", "liao", "lie",
              "lin", "ling", "liu", "long", "lou", "lu", "lv", "luan", "lue", "lun", "luo", "ma", "mai", "man", "mang",
              "mao", "me", "mei", "men", "meng", "mi", "mian", "miao", "mie", "min", "ming", "miu", "mo", "mou", "mu",
              "na", "nai", "nan", "nang", "nao", "ne", "nei", "nen", "neng", "ni", "nian", "niang", "niao", "nie",
              "nin", "ning", "niu", "nong", "nu", "nv", "nuan", "nue", "nuo", "o", "ou", "pa", "pai", "pan", "pang",
              "pao", "pei", "pen", "peng", "pi", "pian", "piao", "pie", "pin", "ping", "po", "pu", "qi", "qia", "qian",
              "qiang", "qiao", "qie", "qin", "qing", "qiong", "qiu", "qu", "quan", "que", "qun", "ran", "rang", "rao",
              "re", "ren", "reng", "ri", "rong", "rou", "ru", "ruan", "rui", "run", "ruo", "sa", "sai", "san", "sang",
              "sao", "se", "sen", "seng", "sha", "shai", "shan", "shang", "shao", "she", "shen", "sheng", "shi", "shou",
              "shu", "shua", "shuai", "shuan", "shuang", "shui", "shun", "shuo", "si", "song", "sou", "su", "suan",
              "sui", "sun", "suo", "ta", "tai", "tan", "tang", "tao", "te", "teng", "ti", "tian", "tiao", "tie", "ting",
              "tong", "tou", "tu", "tuan", "tui", "tun", "tuo", "wa", "wai", "wan", "wang", "wei", "wen", "weng", "wo",
              "wu", "xi", "xia", "xian", "xiang", "xiao", "xie", "xin", "xing", "xiong", "xiu", "xu", "xuan", "xue",
              "xun", "ya", "yan", "yang", "yao", "ye", "yi", "yin", "ying", "yo", "yong", "you", "yu", "yuan", "yue",
              "yun", "za", "zai", "zan", "zang", "zao", "ze", "zei", "zen", "zeng", "zha", "zhai", "zhan", "zhang",
              "zhao", "zhe", "zhen", "zheng", "zhi", "zhong  ", "zhou", "zhu", "zhua", "zhuai", "zhuan", "zhuang",
              "zhui", "zhun", "zhuo", "zi", "zong", "zou", "zu", "zuan", "zui", "zun", "zuo"]
    special = ["code", "tech", "cell", "work", "man", "best"]

    if typ == 1:
        bas = len(num)
        cur = num
    elif typ == 2:
        bas = len(char)
        cur = char
    elif typ == 3:
        bas = len(pinyin)
        cur = pinyin
    elif typ == 4:
        bas = len(num + char)
        cur = num + char

    special_len = len(special)
    compose_len = bas ** length

    u = open('unregistered.txt', 'w')
    r = open('registered_or_failed.txt', 'w')

    for s in range(special_len):
        for x in range(compose_len):
            n = x
            chr0 = cur[n % bas]
            composed_chars = chr0
            for y in range(length - 1):
                n //= bas
                composed_chars += cur[n % bas]
                special_domain = composed_chars + special[s]
                full_domain = special_domain + '.' + suffix
                search(full_domain, u, r)

    u.close()
    r.close()


def search(domain, available, unusable):
    lookup_url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='

    try:
        time.sleep(0.1)
        resp = sess.get(lookup_url + domain, timeout=30)
        et = ET.fromstring(resp.content.decode())
        res = et.find('./original').text[:3]
        if res == '210':
            print(domain + ' domain name is available')
            available.write(domain + '\n')
            available.flush()
        elif res == '211':
            print(domain + ' domain name is not available')
        else:
            print(domain + ' verify timeout')
            unusable.write(domain + '\n')
            unusable.flush()
    except Exception as e:
        print(domain + '\ttimeout')
        unusable.write(domain + '\n')
        unusable.flush()


if __name__ == '__main__':
    verify(2, 2, 'com')
    sess.close()
