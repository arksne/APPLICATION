#!/usr/bin/env python3
"""Generate a traditional Japanese 履歴書 PDF (rirekisho) with Davran's data."""

from fpdf import FPDF
import os

class RirekishoPDF(FPDF):
    def header(self):
        pass  # Handled in page 1

    def footer(self):
        pass

    def format_label(self, text):
        self.set_font('MSGo', 'B', 12)
        self.cell(40, 10, text, new_x='LMARGIN', new_y='NEXT', align='L')
        self.ln(2)

    def add_kanji_cell(self, text, row_height=6, is_label=False, align='C'):
        self.set_font('MSGo', 'B' if is_label else '', 12)
        self.cell(0, row_height, text, new_x='LMARGIN', new_y='NEXT', align=align)

    def add_en_cell(self, text, row_height=5, is_label=False, align='L'):
        self.set_font('MSGo', 'B' if is_label else '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, row_height, text, new_x='LMARGIN', new_y='NEXT', align=align)
        self.set_text_color(0, 0, 0)


def generate_rirekisho(output_path):
    pdf = RirekishoPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    # Font loading (msgothic.ttc is a TrueType Collection, fpdf2 supports it)
    pdf.add_font('MSGo', '', r'C:\Windows\Fonts\msgothic.ttc')
    pdf.set_font('MSGo', '', 12)
    pdf.add_page()

    # ─── Title in header ───
    pdf.set_font('MSGo', '', 22)
    pdf.cell(0, 12, '履 歴 書', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.set_line_width(0.4)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    # ─── 1. Name with Furigana ───
    pdf.set_font('MSGo', '', 16)
    pdf.add_kanji_cell('ダフラン・エルガシェフ')
    pdf.add_kanji_cell('（だふらん・えるがしぇふ）')
    pdf.add_en_cell('Davran Ergashev (Developer & Music Producer)')
    pdf.ln(8)

    # ─── 2. Basic Info ───
    pdf.set_font('MSGo', '', 12)
    info_lines = [
        '生年月日：2001年2月9日（満25歳）',
        '性別：男',
        '住所：キルギス共和国 ビシュケク市',
        '電話番号：+996 553 205 855',
        'メール：W.lowlight@gmail.com',
    ]
    for line in info_lines:
        pdf.cell(0, 8, line, new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.ln(8)

    # ─── 3. Education ───
    pdf.set_font('MSGo', '', 14)
    pdf.cell(0, 10, '学 歴', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('MSGo', '', 12)

    edu = [
        {'period': '20xx年4月～20xx年3月', 'name': 'ギムナジウム第4校', 'detail': '9学年卒業（ビシュケク）'},
        {'period': '20xx年4月～20xx年3月', 'name': 'I.ラザコフ記念KSTU短大', 'detail': '機械工学技術学科 — テクニシャン（マナサ通り66、ビシュケク）'},
        {'period': '2024年', 'name': 'NAT N5', 'detail': '日本語能力試験 N5認定'},
        {'period': '現在', 'name': '学習中', 'detail': '日本語 N3/N4レベル、ITスキルも学習中'},
    ]

    for item in edu:
        pdf.cell(0, 6, f'{item["period"]} — {item["name"]}', new_x='LMARGIN', new_y='NEXT', align='L')
        pdf.cell(0, 6, f'{item["detail"]}', new_x='LMARGIN', new_y='NEXT', align='L')
        pdf.ln(4)

    # ─── 4. Work History ───
    pdf.ln(2)
    pdf.set_font('MSGo', '', 14)
    pdf.cell(0, 10, '職 歴', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('MSGo', '', 12)

    work = [
        {'period': '20xx年〜現在', 'title': 'アパレル製造販売（家業手伝い）', 'desc': '両親のアパレルビジネスに従事。製造工程の管理、販売、在庫管理、仕入れ交渉、顧客対応まで実務全般を担当。仕事の流れを理解し、責任を持って業務を遂行。'},
        {'period': '20xx年〜現在', 'title': '音楽制作（フリーランス）', 'desc': 'レコーディング、ミキシング、マスタリング、ビートメイキング。W.Lowlight名義で作品制作。'},
    ]

    for item in work:
        pdf.cell(0, 6, f'{item["period"]} — {item["title"]}', new_x='LMARGIN', new_y='NEXT', align='L')
        pdf.set_text_color(80, 80, 80)
        pdf.set_font('MSGo', '', 11)
        pdf.multi_cell(0, 6, item['desc'], align='L')
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('MSGo', '', 12)
        pdf.ln(4)

    # ─── 5. Skills ───
    pdf.ln(2)
    pdf.set_font('MSGo', '', 14)
    pdf.cell(0, 10, '資格・免許', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('MSGo', '', 12)

    skills = [
        '• NAT N5（日本語能力試験）— 2024年',
        '• 日本語 N3/N4 レベル（現在学習中）',
        '• 普通自動車免許（キルギス）',
    ]

    for s in skills:
        pdf.cell(0, 6, s, new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.ln(8)

    # ─── 6. Motivation ───
    pdf.ln(2)
    pdf.set_font('MSGo', '', 14)
    pdf.cell(0, 10, '志望動機', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('MSGo', '', 12)

    motivation = '私は両親のアパレルビジネスを長年手伝い、ものづくりとお客様対応の大切さを身をもって学びました。また、音楽制作を通じて、目標に向かってコツコツと積み上げる習慣が身についています。'
    motivation += '日本語学習を1年半前から開始し、現在も継続して勉強中です。日本で働きながら、さらに日本語力とスキルを向上させたいと考えています。'
    motivation += '未経験の分野でも、すぐに学び、戦力になれる自信があります。まずは日本で働く機会をいただき、成長しながら貢献したいです。'

    pdf.set_font('MSGo', '', 11)
    pdf.multi_cell(0, 6, motivation, align='L')
    pdf.ln(6)

    # ─── 7. Self-PR ───
    pdf.set_font('MSGo', '', 14)
    pdf.cell(0, 10, '自己PR', new_x='LMARGIN', new_y='NEXT', align='L')
    pdf.set_font('MSGo', '', 12)

    self_pr = '【実務経験とビジネス感覚】家族のアパレル事業で製造・販売・在庫管理・顧客対応を経験。売上やコストを意識した仕事ができ、責任感があります。'
    self_pr += '【学習意欲と適応力】新しいことへの抵抗がなく、必要なことはすぐに吸収します。日本語も独学でN3レベルまで習得。ITスキルも独学で学び始め、実践的な作業ができるようになりました。'
    self_pr += '【真面目で誠実】与えられた仕事は最後までやり遂げます。日本での就労を真剣に考えており、長期的に働ける環境を望んでいます。'

    pdf.set_font('MSGo', '', 10)
    pdf.multi_cell(0, 6, self_pr, align='L')
    pdf.ln(6)

    # ─── Footer ───
    pdf.set_font('MSGo', '', 10)
    pdf.cell(0, 6, '2026年6月23日 作成', new_x='LMARGIN', new_y='NEXT', align='R')
    pdf.ln(8)
    pdf.cell(0, 6, '___ダフラン・エルガシェフ___', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(4)

    # ─── Output ───
    pdf.output(output_path)
    print(f'OK - Rirekisho PDF saved: {output_path}')


if __name__ == '__main__':
    generate_rirekisho(r'C:\Users\ARK\resume-site\rirekisho.pdf')