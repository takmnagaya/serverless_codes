# 参考
> [Serverless FrameworkでAWS Lamda関数を作成する](https://qiita.com/Esfahan/items/736d09f732fa619d2410)

# Dockerでの開発環境の構築

~~~
$ docker build . -t serverless_codes
$ docker run -v /path/to/serverless_codes:/myapp -it serverless_codes
# dockerコンテナにログイン!
~~~

## AWS認証設定
IAMユーザのアクセスキー、シークレットキーを用意し、コンテナ内で下記コマンド実行
~~~
$ serverless config credentials --provider aws --key xxxxxxxxxxxxxx --secret xxxxxxxxxxxxx
~~~

Macで使用しているアクセスキー、シークレットキーをそのまま使う場合は、
~~~
$ cp ~/.aws/* /path/to/serverless_codes/.aws
~~~

## デプロイ
コンテナ内で下記コマンド実行
~~~
$ cd path/to/function
$ sls deploy
~~~

# lambda関数管理

## /auto-scaling-lifecycle-hook
Auto Scalingライフサイクルフックイベントで実行される関数を管理する。

- インスタンス起動時にCloudWatchメトリクスを作成する。
- インスタンス終了時にCloudWatchメトリクスを削除する。

## /deploy-notification-to-slack
CodeDeployの完了時に通知されるSNSで実行される関数を管理する。

- SlackにCodeDeployの実行結果を通知する。

:warning: 環境変数`SLACK_WEBHOOK_URL`を各自設定してください。
