import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

plt.switch_backend('Agg')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

FILE_NAME = "Employee_cleaned.csv"
OUTPUT_PNG_FILE = "bieu_do_bac_luong_kinh_nghiem.png"
OUTPUT_HTML_FILE = "bao_cao_bieu_do_tuan3.html"


def create_and_export_bar_chart(filename: str):
    try:
        # 1. Đọc và Xử lý Dữ liệu
        df = pd.read_csv(filename)

        # Tạo bảng tần suất chéo (Crosstab) giữa PaymentTier và Experience
        crosstab = pd.crosstab(
            df['PaymentTier'],
            df['ExperienceInCurrentDomain'],
            normalize='index'
        ) * 100

        # Sắp xếp các cột (kinh nghiệm) theo thứ tự tăng dần
        crosstab = crosstab.sort_index(axis=1)

        # 2. Trực quan hóa (Vẽ Biểu đồ Cột Chồng)
        plt.figure(figsize=(10, 7))

        # Vẽ biểu đồ cột
        crosstab.plot(kind='bar', stacked=True, ax=plt.gca(), cmap='coolwarm')

        # Cấu hình biểu đồ (Việt hóa)
        plt.title('Phân Bố Kinh Nghiệm Làm Việc theo Bậc Lương', fontsize=14, fontweight='bold')
        plt.xlabel('Bậc Lương (Payment Tier)', fontsize=12)
        plt.ylabel('Tỷ Lệ Nhân Viên (%)', fontsize=12)

        # === KHẮC PHỤC LỖI TRỤC X ===
        tier_labels = [str(tier) for tier in crosstab.index]
        plt.xticks(ticks=range(len(tier_labels)), labels=tier_labels, rotation=0)

        # Việt hóa và đặt chú giải ra ngoài
        legend_labels = [f"{col} Năm" for col in crosstab.columns]
        plt.legend(crosstab.columns, title='Kinh Nghiệm', bbox_to_anchor=(1.02, 1), loc='upper left')

        # Thêm lưới (grid)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Điều chỉnh bố cục
        plt.tight_layout()

        # Lưu hình ảnh
        plt.savefig(OUTPUT_PNG_FILE)
        plt.close()

        # 3. Xuất ra file HTML tĩnh (ĐÃ SỬA LỖI MÃ HÓA)
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8"> <title>Báo Cáo Biểu Đồ - Tuần 3</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                img {{ border: 1px solid #ccc; max-width: 100%; height: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                p {{ color: #555; }}
            </style>
        </head>
        <body>
            <h1>Biểu Đồ Cột: Phân Bố Kinh Nghiệm theo Bậc Lương</h1>
            <p>Biểu đồ cột chồng thể hiện tỷ lệ phần trăm nhân viên có số năm kinh nghiệm khác nhau trong từng Bậc Lương (1, 2, 3).</p>
            <img src="{OUTPUT_PNG_FILE}" alt="Bar Chart - Tier vs Experience"><br>
        </body>
        </html>
        """

        with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Đã tạo biểu đồ cột thành công tại: {OUTPUT_HTML_FILE}")

    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file {filename}.")
    except Exception as e:
        print(f"LỖI XẢY RA: {e}")


if __name__ == "__main__":
    create_and_export_bar_chart(FILE_NAME)
    print(f"\n=> Vui lòng mở file {OUTPUT_HTML_FILE} trong trình duyệt để xem kết quả.")