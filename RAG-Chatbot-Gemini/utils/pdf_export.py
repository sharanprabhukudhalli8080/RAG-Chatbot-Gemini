from fpdf import FPDF


def export_chat_to_pdf(history):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.cell(
        200,
        10,
        txt="Chat History",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    for chat in history:

        pdf.multi_cell(
            0,
            10,
            f"Question:\n{chat['question']}"
        )

        pdf.multi_cell(
            0,
            10,
            f"Answer:\n{chat['answer']}"
        )

        pdf.ln(5)

    output_path = "chat_history.pdf"

    pdf.output(
        output_path
    )

    return output_path