# LegalPilot

AI-powered legal consulting SaaS - 法務コンサルAI

## Features

1. **契約書レビューAI** - 契約テキスト入力からリスク条項検出、修正提案（30+リスクパターン）
2. **コンプライアンスチェック** - 業種別の法令遵守チェックリスト（15+法令対応）
3. **利用規約・プライバシーポリシー自動生成** - サービス情報からテンプレート生成
4. **契約テンプレートライブラリ** - NDA/業務委託/売買/ライセンス等10種類
5. **法改正アラート** - 業種に影響する法改正の検知とインパクト分析

## Tech Stack

- **Backend**: Python / FastAPI
- **Frontend**: Streamlit
- **Testing**: pytest (50+ tests)

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
streamlit run ui/streamlit_app.py
```

## Test

```bash
python3 -m pytest tests/ -q
```

## PilotStack

Part of the [PilotStack](https://github.com/mattyopon) suite of AI-powered consulting tools.

**Landing Page**: https://mattyopon.github.io/legalpilot/

---

(c) 2026 PilotStack
