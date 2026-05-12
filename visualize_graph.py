from app.graph.youth_graph import build_graph


def main():
    graph = build_graph()

    png_data = graph.get_graph().draw_mermaid_png()

    with open("langgraph_flow.png", "wb") as f:
        f.write(png_data)

    print("그래프 이미지 저장 완료: langgraph_flow.png")


if __name__ == "__main__":
    main()