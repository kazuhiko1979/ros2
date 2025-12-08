# Repository Guidelines

## プロジェクト構成とモジュール配置
- `ros2_ws/src` を起点にパッケージを管理。`my_cpp_pkg/` は C++ ノード群、`my_py_pkg/` は Python ノード群、`my_robot_interfaces/` が共通メッセージ・サービスを提供。
- `my_robot_bringup/` の `launch/` と `config/` が代表的なデモ構成を束ね、`my_robot_description/` 以下に URDF/Xacro と RViz 設定を配置。`turtlesim_catch_them_all/` はゲーム系ユーティリティを切り出した Python パッケージ。
- `build/` `install/` `log/` は colcon が生成する成果物ディレクトリ。リポジトリにはコミットしない。

## ビルド・テスト・開発コマンド
- `colcon build --packages-select <pkg>` で対象パッケージのみビルド。全体ビルド時はセレクタ不要。
- `. install/setup.bash` をシェルで読み込み、`ros2 run` や `ros2 launch` で最新ノードを解決可能にする。
- `colcon test --packages-select my_py_pkg` で pytest と ament lint を実行し、`colcon test-result --verbose` で結果を確認。
- 動作例: `ros2 launch my_robot_bringup number_app.launch.py` で数値配信デモ、`ros2 launch my_robot_description display.launch.py` で URDF を RViz 表示。

## コーディングスタイルと命名
- C++ は ament_cmake + C++14 前提。インデント 2 スペース、トピック・サービス名はスネークケース、クラスは CamelCase。既存の `src/` ノード実装をベースに統一。
- Python は rclpy + 4 スペースインデント、モジュール・関数・変数はスネークケース。エントリポイントは `setup.py` の console_scripts に登録。
- パラメータキーは小文字スネークケース (`catch_closest_turtle_first`) に揃え、launch 名称と実行可能名は極力一致させる。

## テスト指針
- `test/test_flake8.py` と `test/test_pep257.py` が Python 向け静的チェックを実行。新規モジュールは flake8 / docstring 規約を満たすこと。
- 仕様が複雑化する際は Python なら `my_py_pkg/tests/`、C++ なら gtest を追加して `colcon test` に統合。
- メッセージ・サービス連携は関連 launch を起動し `ros2 topic echo` や `rqt_graph` で疎通確認。

## コミットと PR ガイドライン
- コミットは命令形で短く (`Add turtle spawn cooldown`)、1 つの論理変更に限定。必要に応じてパッケージ名を添える。
- PR では目的、実行したテストコマンド、影響する launch/設定ファイルを明記し、挙動が変わる場合はログ抜粋やスクリーンショットを添付。
- レビュー前に `colcon test` を通し、インターフェース変更時は関連ドキュメントや YAML コメントを更新する。

## Launch・シミュレーション Tips
- トラブルシュート時は `ros2 param dump <node>` で実行中のパラメータを記録。
- コミット前に `__pycache__/` など生成物を削除。lint や CI 失敗の原因になりやすい。

## 日本語で回答して
codexのチャット及び、ファイル内のコメントを含め、基本すべて日本語で表記してください。