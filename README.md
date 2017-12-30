> [Serverless FrameworkでAWS Lamda関数を作成する](https://qiita.com/Esfahan/items/736d09f732fa619d2410)

~~~
npm install
npm bin serverless
~~~

# Dockerでの開発環境の構築

~~~
$ docker build . -t serverless_codes
$ docker run -it serverless_codes
# dockerコンテナにログイン!
~~~

## AWS認証設定
IAMユーザのアクセスキー、シークレットキーを用意し、コンテナ内で下記コマンド実行
~~~
$ serverless config credentials --provider aws --key xxxxxxxxxxxxxx --secret xxxxxxxxxxxxx
~~~

## デプロイ
コンテナ内で下記コマンド実行
~~~
$ cd path/to/function
$ sls deploy
~~~
