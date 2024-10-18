# Pix-Chan
PixAIというサイトのPython用APIラッパー、すぐ対策されそう
## インストール
```py
pip install pix-chan
```
必須：requests
## 使い方
#### example.py  
```py
from Pix_Chan import PixAI

pix=PixAI("メールアドレス","パスワード",login=False,proxy=None)#login=Falseでアカウント生成される、生成されたアカウントには3000クオータがついてくる
print(pix.token)
print(pix.user_id)#ユーザーIDはアンケート以外に用途なしな上に自動入力
pix.claim_daily_quota()#デイリー報酬の10000クオータを手に入れる、すでに受け取っていたらエラーになる
pix.claim_questionnaire_quota()#アンケートに答えて15000クオータを手に入れる、これもすでに受け取っていたらエラーになる
#アカウント生成したら合計で28000クオータ手に入る

pix=PixAI("メールアドレス","パスワード",proxy=None)#loginはデフォルトでTrue、トークンログインもあるけどべつにしなくていい
print(pix.get_quota())#ゆいいつintで数字だけ返ってくる
query_id=pix.generate_image("プロンプト")
#プロンプトは, で区切る、例えば 1girl, pinkなど
#widthとheightをintで指定できる、なんと課金しなくても課金専用の解像度でリクエストしてもちゃんと生成される...
#x4=Trueにして4枚同時生成、後述するメディアIDのリストに4つIDが格納されるようになる
#エロは規制されることがけっこうある (特にloliや固有名詞 + nakedみたいな)
#直接的な表現を控えると通ったりする (loli, nakedは生成されないけど、loli, no clothは生成される)
#query_idがクエリーIDになる、これはstr
media_ids=pix.get_task_by_id(query_id)#クエリーIDからメディアIDを取得する、リストが返ってくる
for media_id in media_ids:
    print(pix.get_media(media_id))#メディアIDを使って、生成された画像のURLを取得してお仕事完了

media_ids=pix.get_latest_task()#クエリーIDがわからなくても1番最後にリクエストしたタスクを取得する、これもリストでメディアIDが返ってくる
media_ids=pix.get_all_tasks()#すべてのタスクを取得する、リストにリストが格納される -> [["メディアID","メディアID","メディアID","メディアID"],["メディアID"],["メディアID"]] 的な
```
#コメントで書いてあるのが全部、悪用したら対策されるのが早くなりそう  
## もう少し知る
### ログイン / アカウント生成
```py
pix=PixAI("メールアドレス","パスワード",login=False,proxy=None)
```  
login=Trueがデフォルトで、Falseにしたら入力したメールアドレスとパスワードでアカウントを作成する  
レート制限は思ったより緩いけどちゃんとかかる  
アカウント生成にメールアドレス認証は不用 (2024/10/18) なのでテキトーなメールアドレスを入力してOK  
これだけで3000クオータ (PixAIの通貨で、デフォルト設定で1枚生成するのに2200クオータ消費する) 入ったアカウントが手に入る  
### 無料ゲットQuota  
```py
pix.claim_daily_quota()#デイリー報酬の10000クオータを手に入れる、すでに受け取っていたらエラーになる
pix.claim_questionnaire_quota()#アンケートに答えて15000クオータを手に入れる、これもすでに受け取っていたらエラーになる
```
1日1回ログインボーナスで10000クオータもらえる、デフォルト設定なら2200クオータ / 1枚 なので4つ生成できる  
アンケート報酬のクオータはアカウントごとに1回、15000クオータもらえる  
アンケートはGoogleFormsにユーザーIDを入れて回答されたものを送信するとクオータ入手クエストのとこから申請できるようになる  
```pix.claim_questionnaire_quota()```はフォーム送信と申請を自動化している  
これでアカウント生成すると28000クオータチャージされたアカウントが手に入るということ...  
クオータが尽きたら次のアカウントを生成してまた画像生成すればOK、**__対策されるまでは遊べる__**  
### 画像生成をリクエスト
```py
query_id=pix.generate_image("プロンプト")
#プロンプトは, で区切る、例えば 1girl, pinkなど
#widthとheightをintで指定できる、なんと課金しなくても課金専用の解像度でリクエストしてもちゃんと生成される...
#x4=Trueにして4枚同時生成、後述するメディアIDのリストに4つIDが格納されるようになる
#エロは規制されることがけっこうある (特にloliや固有名詞 + nakedみたいな)
#直接的な表現を控えると通ったりする (loli, nakedは生成されないけど、loli, no clothは生成される)
#query_idがクエリーIDになる、これはstr
```
コメントに書いてある通り、プロンプトと必要あれば横幅・高さをintで指定したり、x4=Trueで4枚同時に生成したりできる  
この時、課金アカウント限定の解像度を指定してもふつうに生成できてしまう...  
AI画像生成を使う人のほとんどはえっちな絵を生成したくて使っていると思うけど、けっこう厳しくてプロンプトに趣味を盛り込むとことごとく弾かれる  
どういう判定かはよくわからない -> ```nsfw``` は弾かれないけど ```naked``` は弾かれる、```loli, nsfw``` は弾かれるけど ```loli, no cloth``` は弾かれない し、なんか別のプロンプトまぜてるとうまくいったりいかなかったり  
ただ裸でいいなら無難に ```欲しい特徴, no cloth``` だけ書いて4枚生成ガチャしてお気に入りを探そう  
ソースコードには ```samplingSteps``` ```samplingMethod``` ```cfgScale``` ```seed``` ```modelId``` ...など生成に使える引数は1通りあるけどこだわるならそこだけ自分で修正してください...  
###### 本当にこだわるならStableDiffusionとか使った方がいいけど、VRAM 4GBあってもろくに生成できないからハードル高いよ(泣)
### 生成された画像を確認
```py
media_ids=pix.get_task_by_id(query_id)#クエリーIDからメディアIDを取得する、リストが返ってくる
for media_id in media_ids:
    print(pix.get_media(media_id))#メディアIDを使って、生成された画像のURLを取得してお仕事完了
```
example.pyにはクエリーIDがわからない時用の ```pix.get_latest_task()``` や全取得の ```pix.get_all_tasks()``` も書いてあるけど画像生成をリクエストする際にクエリーIDが返されるので基本的にはIDからタスクをゲットすると思う  
あたりまえだけど生成が終わってないのに画像URLを取得することはできない -> なので生成が終わってないタスクに関しては ```None``` を返すようにしてる  
ようするに  
```py
while True:
    media_ids=pix.get_task_by_id(query_id)
    if media_ids:
        break
    sleep(10)
#ここから生成された画像のURLを取得する処理を書いたり
```
いずれメディアIDの入ったリストが返ってくるのでそれまでWhileで無限ループでOK
```py
for media_id in media_ids:
    print(pix.get_media(media_id))#メディアIDを使って、生成された画像のURLを取得してお仕事完了
```
```pix.get_media(media_id)``` は画像URLだけを返すのでブラウザーで開くなりなにかに埋め込むなりで画像ゲット、これで全部完了
## 余談
こんなのでいいの？って思うほどアカウントを作りまくって28000クオータ使って無限に画像を生成できる  
その気になればいつでもすぐに対策できそうな内容ばかりなので動作は保証できません  
いちおうアカウント生成 / ログインにinvisible reCaptchaのレスポンスを要求されるけどふつうに入手できるのでBot検知という面ではあんまり役に立ってなかったりする  
VRAM 12GB以上のGPU、買いませんか？(買えない)  
## コンタクト
Discord サーバー / https://discord.gg/aSyaAK7Ktm  
Discord ユーザー名 / .taka.
