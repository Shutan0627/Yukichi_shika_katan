# 諭吉しか勝たん！
- プレゼンの発表練習を収録して、総合評価を行うアプリケーション

## for frontend
- app.pyに主に２関数あります。
  - コメントを保持するcsvファイルの作成と、フィードバックの生成を一度に行うapp
  - timeを指定するとそのタイム以下の上位４つを近い順に返す関数
  - Yukichi_shika_katan配下に.env置いてね（OPENAI_API_KEY="your-api-key"）
- demo.pyはgradioで、現在の出力がどんな感じになるかがわかるよ
- 使う時はpip install -r requirments.txtしてね
  - 一部できないやつあるので、ないよって言われたら入れ方調べて下さい
  - **仮想環境作ってやることを強くお勧めします** （Python仮想環境作り方とか、pyenv, virtualenvsについて調べてみて）
