"""利用規約・プライバシーポリシー自動生成サービス.

サービス情報を入力し、利用規約とプライバシーポリシーのテンプレートを生成する。
"""

from __future__ import annotations

from app.models import GeneratedTerms, ServiceInfo, ServiceType


def _generate_terms_of_service(info: ServiceInfo) -> str:
    """利用規約を生成."""
    sections = []
    sections.append(f"# {info.service_name} 利用規約")
    sections.append("")
    sections.append(f"本利用規約（以下「本規約」）は、{info.company_name}（以下「当社」）が提供する")
    sections.append(f"「{info.service_name}」（以下「本サービス」）の利用条件を定めるものです。")
    sections.append("")

    # 第1条 適用
    sections.append("## 第1条（適用）")
    sections.append("本規約は、ユーザーと当社との間の本サービスの利用に関わる一切の関係に適用されるものとします。")
    sections.append("")

    # 第2条 利用登録
    sections.append("## 第2条（利用登録）")
    sections.append("登録希望者が当社の定める方法によって利用登録を申請し、当社がこれを承認することによって、利用登録が完了するものとします。")
    sections.append("")

    # 第3条 禁止事項
    sections.append("## 第3条（禁止事項）")
    sections.append("ユーザーは、本サービスの利用にあたり、以下の行為をしてはなりません。")
    sections.append("1. 法令または公序良俗に違反する行為")
    sections.append("2. 犯罪行為に関連する行為")
    sections.append("3. 当社のサーバーまたはネットワークの機能を破壊したり、妨害したりする行為")
    sections.append("4. 当社のサービスの運営を妨害するおそれのある行為")
    sections.append("5. 他のユーザーに関する個人情報等を収集または蓄積する行為")
    sections.append("6. 不正アクセスをし、またはこれを試みる行為")
    sections.append("7. 他のユーザーに成りすます行為")
    sections.append("")

    # 第4条 サービスの提供停止
    sections.append("## 第4条（本サービスの提供の停止等）")
    sections.append("当社は、以下のいずれかの事由があると判断した場合、ユーザーに事前に通知することなく本サービスの全部または一部の提供を停止または中断することができるものとします。")
    sections.append("1. 本サービスにかかるコンピュータシステムの保守点検または更新を行う場合")
    sections.append("2. 地震、落雷、火災、停電または天災などの不可抗力により、本サービスの提供が困難となった場合")
    sections.append("3. その他、当社が本サービスの提供が困難と判断した場合")
    sections.append("")

    # 有料サービス
    if info.has_paid_features:
        sections.append("## 第5条（有料サービス）")
        sections.append("1. 有料サービスの利用料金は、当社が別途定める料金表に従うものとします。")
        sections.append("2. ユーザーは、当社が定める方法により利用料金を支払うものとします。")
        sections.append("3. 理由の如何を問わず、すでに支払われた利用料金は返金しないものとします。")
        sections.append("")

    # 未成年
    if info.target_minors:
        sections.append("## 第6条（未成年者の利用）")
        sections.append("未成年者が本サービスを利用する場合は、法定代理人の同意を得た上でご利用ください。")
        sections.append("")

    # 免責事項
    sections.append("## 第7条（免責事項）")
    sections.append("1. 当社は、本サービスに事実上または法律上の瑕疵がないことを明示的にも黙示的にも保証しておりません。")
    sections.append("2. 当社は、本サービスに起因してユーザーに生じたあらゆる損害について、当社の故意又は重過失による場合を除き、一切の責任を負いません。")
    sections.append("")

    # 準拠法・管轄
    sections.append("## 第8条（準拠法・裁判管轄）")
    sections.append("本規約の解釈にあたっては、日本法を準拠法とします。")
    sections.append("本サービスに関して紛争が生じた場合には、当社の本店所在地を管轄する裁判所を専属的合意管轄とします。")
    sections.append("")

    sections.append("制定日: [日付]")
    sections.append(f"{info.company_name}")

    return "\n".join(sections)


def _generate_privacy_policy(info: ServiceInfo) -> str:
    """プライバシーポリシーを生成."""
    sections = []
    sections.append(f"# {info.service_name} プライバシーポリシー")
    sections.append("")
    sections.append(f"{info.company_name}（以下「当社」）は、{info.service_name}（以下「本サービス」）における")
    sections.append("ユーザーの個人情報の取扱いについて、以下のとおりプライバシーポリシーを定めます。")
    sections.append("")

    # 収集する情報
    sections.append("## 第1条（収集する個人情報）")
    sections.append("当社は、以下の個人情報を収集することがあります。")
    sections.append("1. 氏名、メールアドレス等の登録情報")
    if info.has_paid_features:
        sections.append("2. クレジットカード情報等の決済情報")
    sections.append(f"{'3' if info.has_paid_features else '2'}. アクセスログ、IPアドレス等の利用情報")
    sections.append("")

    # 利用目的
    sections.append("## 第2条（個人情報の利用目的）")
    sections.append("当社は、収集した個人情報を以下の目的で利用します。")
    sections.append("1. 本サービスの提供・運営のため")
    sections.append("2. ユーザーからのお問い合わせに対応するため")
    sections.append("3. 利用規約に違反したユーザーに対して、利用の停止を通知するため")
    sections.append("4. サービスの改善、新サービスの開発のため")
    if info.has_paid_features:
        sections.append("5. 有料サービスにおいて、利用料金を請求するため")
    sections.append("")

    # 第三者提供
    sections.append("## 第3条（個人情報の第三者提供）")
    sections.append("当社は、次に掲げる場合を除いて、あらかじめユーザーの同意を得ることなく、第三者に個人情報を提供することはありません。")
    sections.append("1. 法令に基づく場合")
    sections.append("2. 人の生命、身体又は財産の保護のために必要がある場合")
    sections.append("3. 公衆衛生の向上又は児童の健全な育成の推進のために特に必要がある場合")
    sections.append("")

    # Cookie
    if info.uses_cookies:
        sections.append("## 第4条（Cookieの使用）")
        sections.append("本サービスは、サービス向上のためにCookieを使用することがあります。")
        sections.append("ユーザーはブラウザの設定によりCookieの受け入れを拒否することができますが、一部の機能が利用できなくなる場合があります。")
        sections.append("")

    # 安全管理
    sections.append("## 第5条（個人情報の安全管理）")
    sections.append("当社は、個人情報の漏洩、滅失またはき損の防止その他の個人情報の安全管理のために必要かつ適切な措置を講じます。")
    sections.append("")

    # 開示・訂正・削除
    sections.append("## 第6条（個人情報の開示・訂正・削除）")
    sections.append("ユーザーは、当社に対して個人情報の開示、訂正、追加、削除、利用停止を請求することができます。")
    sections.append("")

    # 国際
    if info.international:
        sections.append("## 第7条（国際的なデータ移転）")
        sections.append("本サービスの提供にあたり、個人情報を日本国外のサーバーに保存する場合があります。")
        sections.append("その場合、当社は適切な安全管理措置を講じます。")
        sections.append("")

    sections.append("## 第8条（プライバシーポリシーの変更）")
    sections.append("当社は、必要に応じて本プライバシーポリシーを変更することがあります。")
    sections.append("変更後のプライバシーポリシーは、本サービス上に掲載した時点で効力を生じるものとします。")
    sections.append("")

    sections.append("制定日: [日付]")
    sections.append(f"{info.company_name}")

    return "\n".join(sections)


def generate_terms(info: ServiceInfo) -> GeneratedTerms:
    """利用規約とプライバシーポリシーを生成する.

    Args:
        info: サービス情報

    Returns:
        GeneratedTerms
    """
    tos = _generate_terms_of_service(info)
    pp = _generate_privacy_policy(info)

    service_type_label = {
        ServiceType.WEB_SERVICE: "Webサービス",
        ServiceType.MOBILE_APP: "モバイルアプリ",
        ServiceType.EC_SITE: "ECサイト",
        ServiceType.SAAS: "SaaS",
        ServiceType.PLATFORM: "プラットフォーム",
        ServiceType.OTHER: "その他",
    }.get(info.service_type, "サービス")

    summary = f"{info.service_name}（{service_type_label}）の利用規約とプライバシーポリシーを生成しました。"

    return GeneratedTerms(
        service_info=info,
        terms_of_service=tos,
        privacy_policy=pp,
        summary=summary,
    )
