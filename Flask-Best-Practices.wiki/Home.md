# Flask-Best-Practices
このリポジトリはFlaskのベストプラクティス、実施的なテクニックを紹介するリポジトリです。

## Overview
FlaskはpythonのWebフレームワークで、基本的にSinatraライクな
軽量フレームワークです。しかしながら、要件に応じて、MTVパターンにしたがって拡張が出来ます。
MTV (Model Template View)です。名前は実際はどうでもよいですが、
RailsでいうところのMVCです。すなわち

* Models -> Models
* Templates -> Views
* Views -> Controllers

といった対応関係があります。

近年機械学習、解析系アプリケーションの需要が
高まるにつれてpythonの利用者が増えてきています。
pythonの優れた書籍は日本語で大体読めるようになってきていますが、
最近人気が高まってきているFlaskの日本語書籍は未だ皆無です。

本リポジトリではFlaskのベストな利用法、便利なプラグイン、ベスト・プラクティス
などを紹介していきます。
(なお、本稿は筆者が独断と偏見と経験に基いて作られたもので、本稿で紹介された
設計技法を用いてアプリケーションがカオスになっても何ら責任は負いません)