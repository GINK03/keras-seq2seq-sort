# seq2seq sort

## 並び順がなくなった文字列から、文字のもとの列を復元します
- seq2seqのタスクの一つであるソートを自然言語に拡張します

- キャラクタレベル（文字粒度）で順序情報を失ったベクトル情報に対してベクトルを入力として、並び順が残っているもとの文章を構築しようと試みます

　もともとの想定していたユースケースとしては、アイディアを出し合うようなブレインストーミングなどで、よく付箋などを使ってキーワードをポスイットなどで張って、それから最終的に言いたいことを構築するようなことを私はよくやるのですが、そういったキーワード群を投入することで、自然に導きたい情報を帰結させることもできるなとか思いました。
 
 　データセットとネットワークサイズの限界で文字の並び替えのタスクを今回は与えてみようと思います。

## 先行研究
- [ORDER MATTERS: SEQUENCE TO SEQUENCE FOR SETS](https://arxiv.org/pdf/1511.06391.pdf)

## 文字列を破壊して並びなおす
- 東洋経済さんのオンラインコンテンツの記事タイトルを利用します
- char粒度で分解してBag of Wordsのようなベクトル表現に変換します
- Encoderの入力を行いベクトル化して、Decoderで元の並びを推定します

## ネットワーク
なんどか試してうまくいったモデルを使用したいと思います
```python
enc = input_tensor
enc = Flatten()(enc)
enc = RepeatVector(30)(enc)
enc = GRU(256, return_sequences=True)(enc)

dec = Bi(GRU(512, dropout=0.30, recurrent_dropout=0.25, return_sequences=True))(enc)
dec = TD(Dense(3000, activation='relu'))(dec)
dec = Dropout(0.5)(dec)
dec = TD(Dense(3000, activation='relu'))(dec)
dec = Dropout(0.1)(dec)
decode  = TD(Dense(3135, activation='softmax'))(dec)

model = Model(inputs=input_tensor, outputs=decode)
model.compile(loss='categorical_crossentropy', optimizer='adam')
```

## 前処理
**東洋経済さんのコンテンツをスクレイピングします**
```console
$ python3 12-scan.py
```

**スクレイピングしたhtml情報を解析してテキスト情報を取り出します**
```console
$ python3 16-parse-html.py
```

**テキスト情報とベクトル情報のペアを作ります**
```console
$ python3 19-make_title_boc_pair.py 
```

**機械学習できる数字のベクトル情報に変換します**
```console
$ python3 23-make_vector.py 
```

## 学習
**学習を行います**
（データサイズが巨大なので、128GByte程度のメインメモリが必要になります）
```console
$ python3 24-train.py --train
...
```
categorical_crossentropyの損失が0.3程度に下がると、ある程度の予想が可能にまります  

## 評価

## 終わりに
