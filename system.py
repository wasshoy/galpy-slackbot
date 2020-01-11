# ----------------------------
# gal for python (galpy)
# 2019.10.05 Sat. by A.Arimura
# ----------------------------
import random
import yaml
import re
import MeCab

tagger = MeCab.Tagger('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')

class GalPy:
    def __init__(self): 
        with open('./vocab/brain.yaml', mode='r') as f:
            b = yaml.load(f, Loader=yaml.SafeLoader)
            # 反応する言葉のリスト(正規表現)
            self.keys = list(map(lambda x: re.compile(x[0]), b))
            # 返答する言葉のリスト
            self.values = list(map(lambda x: x[1], b))
# ----------------------------------------
# translate(str, dict):
# strの中からdict(gReflects)のkeyと一致する言葉があればそのvalueを返す
# ----------------------------------------
    def translate(self, str, dict):
        '''
        translate(str, dict):
        strを形態素解析し、dictのkeyと一致する言葉があればそのvalueに変換する\n
        最終的に変換した文字列を返す
        '''
        # 形態素解析
        node = tagger.parseToNode(str)
        ws = ''
        while node:
            ws += node.surface + ' '
            node = node.next
        words = ws.split()
        keys = dict.keys()
        for i in range(0, len(words)):
            # 1単語ずつkeyと比較し、dictにあればそのvalueに変換
            if words[i] in keys:
                words[i] = dict[words[i]]
        return ''.join(words)

# ----------------------------------------
# respond:
# 会話の言葉(str)に対する返答を返答リストから選んで返す
# ----------------------------------------
    def respond(self, str):
        '''
        返答システム部分
        '''
        # 返答リストにある文体がきたら一致する返答パターンリストから乱択して返す
        # リストのはじめからみていくので先に一致したものが優先される
        for i in range(0, len(self.keys)):
            # re.compile('反応パターンの正規表現').match(str) で一致結果格納(matchオブジェクト)
            match_obj = self.keys[i].match(str)
            # 一致あり
            if match_obj:
                resp = random.choice(self.values[i])
                # resp内の%がある位置(=変換する文字)の初めのindexを返す(ない場合-1を返す)
                pos = resp.find('%')
                while pos > -1:
                    # resp内の最後の%までrespを更新
                    # (%の横の数字がnum)
                    # num は match.group(num) として使う
                    num = int(resp[pos+1:pos+2])
                    # ねえ、きみはだれ -> ねえ、あーしはだれ
                    resp = resp[:pos] + \
                            self.translate(match_obj.group(num), gReflections) + \
                            resp[pos+2:]
                    
                    pos = resp.find('%')
                return resp

# ------------------------------------------
# 「君」に対して「あーし」で返すやつのペア 
# ------------------------------------------
gReflections = {
                'きみ' : 'あーし',
                '君' : 'あーし',
                'おまえ': 'あーし',
                'お前': 'あーし'
               }

def interface(text):
    gal = GalPy()
    return gal.respond(text)