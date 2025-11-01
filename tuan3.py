from flask import Flask, render_template_string
import csv
from typing import Dict, List, Any

app = Flask(__name__)
FILE_NAME = 'Employee_cleaned.csv'


# --- 1. CẤU TRÚC DỮ LIỆU: ĐỒ THỊ (DANH SÁCH KỀ) ---

class AdjacencyGraph:
    def __init__(self):
        self.adj_list: Dict[str, Dict[str, int]] = {}
        self.vertices: set = set()

    def add_edge(self, source: str, destination: str, weight: int = 1):
        """Trọng số = Số lượng nhân viên có mối quan hệ này."""
        self.vertices.add(source)
        if source not in self.adj_list:
            self.adj_list[source] = {}
        self.adj_list[source][destination] = self.adj_list[source].get(destination, 0) + weight

    def get_grouped_adjacencies(self) -> Dict[str, List[Dict[str, Any]]]:
        grouped_data = {}
        for source, neighbors in self.adj_list.items():
            if "Bậc lương" in source:
                # Đổi tên khóa 'Weight' thành 'Count' trong từ điển
                sorted_neighbors = sorted(
                    [{'Destination': dest, 'Count': weight} for dest, weight in neighbors.items()],
                    key=lambda x: x['Count'],
                    reverse=True
                )
                grouped_data[source] = sorted_neighbors
        return grouped_data


# --- 2. HÀM XÂY DỰNG ĐỒ THỊ TỪ CSV (ROBUST) ---

def build_employee_graph(filename: str) -> AdjacencyGraph:
    graph = AdjacencyGraph()
    RELATIONSHIP_FIELDS = ['PaymentTier', 'ExperienceInCurrentDomain']

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    source_val = row.get(RELATIONSHIP_FIELDS[0])
                    dest_val = row.get(RELATIONSHIP_FIELDS[1])

                    if source_val and dest_val and source_val.strip() and dest_val.strip():
                        source_label = f"Bậc lương {source_val}"
                        dest_label = f"{dest_val} Năm"
                        graph.add_edge(source_label, dest_label, weight=1)

                except Exception:
                    continue

    except FileNotFoundError:
        return None
    except Exception:
        return None

    return graph


# --- ROUTE CHÍNH: HIỂN THỊ HTML ---

@app.route('/')
def index():
    graph = build_employee_graph(FILE_NAME)

    if graph is None:
        return f"Lỗi: Không tìm thấy file {FILE_NAME} hoặc lỗi trong quá trình đọc.", 404

    grouped_adjacencies = graph.get_grouped_adjacencies()

    # Template HTML (Đã thay 'Trọng số' bằng 'Số lượng')
    html_output = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Cấu Trúc Đồ Thị Trực Quan</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 40px; 
                background-color: #f4f7f6;
            }
            h1 { 
                color: #2c3e50; 
                border-bottom: 3px solid #3498db; 
                padding-bottom: 15px; 
                margin-bottom: 30px;
            }
            .graph-container { 
                list-style: none; padding: 0; 
            }
            .source-node { 
                margin-bottom: 35px; 
                display: flex; 
                align-items: center; 
                border: 1px solid #ddd;
                padding: 15px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .source-label { 
                font-weight: bold; 
                color: #ffffff; 
                background-color: #e74c3c; 
                padding: 10px 20px; 
                border-radius: 6px;
                min-width: 120px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            .adj-list { 
                list-style: none; 
                padding: 0; 
                margin-left: 30px; 
                display: flex;
                flex-wrap: wrap; 
                gap: 15px; 
            }
            .arrow-symbol {
                font-size: 2em;
                color: #3498db;
                margin: 0 20px;
            }
            .neighbor-node {
                display: flex;
                align-items: center;
            }
            .dest-label {
                padding: 8px 15px; 
                background-color: #ecf0f1; 
                border-radius: 6px; 
                border: 1px solid #bdc3c7;
                transition: background-color 0.3s;
            }
            .dest-label:hover {
                background-color: #dcdfe1;
            }
            .weight { 
                font-weight: bold; 
                color: #27ae60; 
                margin-left: 5px; 
            }
        </style>
    </head>
    <body>
        <h1>Danh Sách Kề (Bậc Lương → Kinh nghiệm làm việc)</h1>

        <ul class="graph-container">
        {% for source_vertex, neighbors in grouped_adjacencies.items() %}
            <li class="source-node">
                <div class="source-label">{{ source_vertex }}</div>
                <div class="arrow-symbol">→</div> 

                <ul class="adj-list">
                {% for neighbor in neighbors %}
                    <li class="neighbor-node">
                        {# Sử dụng khóa 'Count' thay vì 'Weight' #}
                        <span class="dest-label">
                            {{ neighbor.Destination }} (Số lượng: <span class="weight">{{ neighbor.Count }}</span>)
                        </span>
                    </li>
                {% endfor %}
                </ul>
            </li>
        {% endfor %}
        </ul>

    </body>
    </html>
    """

    return render_template_string(
        html_output,
        grouped_adjacencies=grouped_adjacencies
    )


if __name__ == '__main__':
    print("Ứng dụng Flask đang chạy tại: http://127.0.0.1:5000/")
    app.run(debug=True)
