# Container Manager
DNNツール等を用いた実験の環境構築〜モデル学習をサポートするツールです．

## Requirement
* nvidia-driver
* docker
* docker-py
* nvidia-docker

## Install
以下のコマンドで`coctl`コマンドがインストールされます．
```
pip install container_manager
```

## GetStart
`example`ディレクトリに最も簡単なサンプルがあります．
`example`ディレクトリのある場所で`coctl`コマンドを使うことでタスクを実行することができます．
### run
`run`コマンドでディレクトリを指定しタスクを作成，実行することができます．
```
$ coctl run example
```
上記のコマンドでpytorch1.4がインストールされた環境で`タスク名/main.py`が実行されます(例では`example/main.py`)．
指定したディレクトリ名のタスクが作成されます．
`coctl`コマンドは実行したいタスクのディレクトリのある場所で実行してください．
`$ coctl run xxx/example`や`$ coctl run ../example`のような指定はできないことに注意してください．
個別に必要なライブラリ等がある場合は`example/Dockerfile`に記載されているように適宜必要なライブラリを追加してください．
`main.py`が実行される環境は起動時に毎回新規に環境が作られるため，必ず`Dockerfile`に`pip install`などを記載し，指定するディレクトリの中に配置してください．
runの実行後はmain.pyのログが表示されます．`Ctr-C` などでログの表示を止めることができますが，タスクのプロセス自体は終了しません．
現在走っているタスクを止めるには下記の`rm`コマンドでタスクを削除するか，同名のタスクを`run`することで削除した後新しいタスクが作成されます．

#### 実行時引数
実行したいタスクの`main.py`が実行時引数を必要とする場合には`-o`オプションで引数を渡すことができます．
```
$ coctl run example -o args1:hoge args2:baa arg3
```
とした場合
```
$ main.py --args1=hoge --args2=baa --arg3
```
のように解釈されます．

#### タスクの入出力
学習データなどの入力データは`training_input/タスク名`以下に配置してください．
出力データは`training_output/タスク名`に出力されます．
タスクの実行される環境では`training_input/タスク名`は`/input`に，`training_output/タスク名`は`/output`として認識されるのでタスクの`main.py`では`/input`以下からデータを読み込み，`/output`へデータを書き込みようにしてください．


### list

`list`コマンドで実行中及び完了済みのタスクが表示できます．
```
$ coctl list
task_name       | status
 example        | running
 test   | exited
 ```
 上記の例ではタスク名`test`が完了済み，`example`が実行中であることを示します．

 ### logs
 実行中のタスクのログを確認するには`list`コマンドを利用します．
```
$ coctl logs example
arg3=default arg
main is run!!!
count 0
count 1
count 2
count 3
```
`-f`オプションをつけるとログをストリームで監視します．

### rm
`rm`コマンドでタスクの削除を行うことができます．
```
$ coctl rm example
Task example is deleted
```

### clean
タスクの生成を繰り返すと不要なデータが蓄積することがあります．
ディスク容量が圧迫される場合は`clean`コマンドで不要なデータを削除してください．
```
$ coctl clean
```

### GCPで学習を行う場合の例
以下のコマンドでGPUを持つインスタンスを確保します．

```
gcloud beta compute \
	--accelerator=type=nvidia-tesla-v100,count=1 \
	--image-project=ml-images \
	--boot-disk-size=50GB \
	--zone=us-central1-a \
	--machine-type=n1-standard-1 \
	--subnet=default \
	--network-tier=PREMIUM \
	--maintenance-policy=TERMINATE \
	--service-account=770963190637-compute@developer.gserviceaccount.com \
	--scopes=https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/trace.append,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/devstorage.read_write \
	--image=c3-deeplearning-tf-ent-2-1-cu100-20200131 \
	--boot-disk-type=pd-standard \
	--boot-disk-device-name=gpu-test \
	--reservation-affinity=any
```

`gpt-test`がインスタンス名なので適宜修正してください．
`accelerator`を`nvidia-tesla-k80`にしたり，`count`を増やしたりすることができます．
また，`boot-disk-size`を変えることでディスク容量が変えられます．
インスタンスの作成が完了し，サーバが起動すると以下のコマンドでログインできます．
```
gcloud compute ssh インスタcoンス名
```
*ログイン時にnvidiaドライバのインストールを行うか聞かれるので`y`を選択してください．
ContainerManagerの手順に従い，`coctl`をインストールします．
上記の手順で作成したインスタンスはContainerManagerのrequirementを満たしているのでそのまま`pip install`が可能です．
