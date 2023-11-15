import fitz  # PyMuPDF
import re
import os
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    # Remove spaces (you can replace spaces with an empty string or any character you prefer)
    text = text.replace(" ", "")

    return text


def split_pdf_by_document_names(pdf_path, excel_file, output_directory, image_path):
    pdf_document = fitz.open(pdf_path)

    # Load the Excel file containing document names



    df = pd.read_excel(excel_file)
    split_list = []
    pdf_name = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        page_text = text  # Remove spaces from the extracted text
        # Rest of your code for processing the page_text


        for index, row in df.iterrows():
            document_name = row['Document Name']
            if document_name in page_text:
                new_pdf_document = fitz.open()
                new_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

                # Get the coordinates to place the image
                x, y, width, height = 320, 670, 100, 100  # Adjust as needed
                image_rect = fitz.Rect(x, y, x + width, y + height)

                # Add the image to the current page
                new_pdf_document[0].insert_image(image_rect, filename=image_path)

                # Save the new PDF document with the document name and page number
                output_pdf_name = os.path.join(output_directory, f"{page_num}_{document_name}.pdf")
                new_pdf_document.save(output_pdf_name)
                new_pdf_document.close()
                split_list.append(f"{page_num}_{document_name}")
                pdf_name.append(document_name)
                #print(pdf_name)

                #original_df = pd.read_excel(excel_file)



    pdf_document.close()
    split_df = pd.DataFrame({'PDF Name': split_list})



    for index, row in df.iterrows():
        document_name = row['Document Name']
        email_address = str(row['Email Address'])  # Explicitly convert to string
        split_df.loc[split_df['PDF Name'].str.contains(document_name), 'Email Address'] = email_address


    # Save the new DataFrame to a new Excel file
    new_excel_file = 'split_emails.xlsx'
    split_df.to_excel(os.path.join(output_directory, new_excel_file), index=False)

    # Create a list to store document names that were found in the PDF but not split
    not_split_document_names = []

    for index, row in df.iterrows():
        document_name = row['Document Name'] # Convert to string
        if document_name not in pdf_name and document_name not in os.listdir(output_directory):
            not_split_document_names.append(document_name)

    # Print the list of document names that were not found in the PDF
    print("Document Names Not Found in PDF:")
    for name in not_split_document_names:
        print(name)



if __name__ == '__main__':
    pdf_path = r'E:\10-2023.pdf'
    excel_file = 'E:\listemail2.xlsx'
    output_directory = r'E:\output'
    image_path = r'E:\cache.png'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    split_pdf_by_document_names(pdf_path, excel_file, output_directory, image_path)




print("Image added successfully")
