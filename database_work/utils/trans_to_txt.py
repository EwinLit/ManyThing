#pip install PyMuPDF
#pip install python-docx
#pip install Spire.Doc
import fitz
import os
from docx import Document
from spire.doc import Document, FileFormat
def pdf2txt(pdf_folder):
    """Convert all .pdf files in the specified folder and its subfolders to .txt files."""
    
    if not os.path.exists(pdf_folder):
        print("指定的文件夹不存在。")
        return
    
    #print("开始转换 PDF 文件...")
    
    # 使用 os.walk 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(pdf_folder):
        for pdf_filename in files:
            if pdf_filename.endswith('.pdf'):
                pdf_path = os.path.join(root, pdf_filename)
                
                try:
                    # 打开 PDF 文件
                    pdf_document = fitz.open(pdf_path)
                    
                    # 获取 PDF 中的所有页面并将它们合并为一个字符串
                    pdf_text = ""
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document.load_page(page_num)
                        pdf_text += page.get_text()
                    
                    # 创建一个 TXT 文件并将 PDF 内容写入其中
                    txt_filename = os.path.splitext(pdf_filename)[0] + '.txt'
                    txt_path = os.path.join(root, txt_filename)
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(pdf_text)
                    
                    pdf_document.close()
                    
                    #print(f"成功转换 {pdf_path} 到 {txt_path}")
                
                except Exception as e:
                    print(f"转换 {pdf_path} 时出错: {e}")
    
    #print("所有 PDF 文件已成功转换为 UTF-8 编码的 TXT 文件。")

def convert_docx_to_txt(input_dir):
    """遍历文件夹及子文件夹，将所有 .docx 文件转换为 .txt 文件"""
    
    if not os.path.exists(input_dir):
        print("指定的文件夹不存在。")
        return
    
    #dprint("开始转换 DOCX 文件...")
    
    # 使用 os.walk 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.docx'):
                # 构造 .docx 文件路径
                docx_file = os.path.join(root, file)
                
                # 构造对应的 .txt 文件路径
                txt_file = os.path.join(root, file.replace('.docx', '.txt'))
                
                try:
                    # 打开 .docx 文件并提取文本
                    doc = Document(docx_file)
                    
                    # 将提取的文本写入 .txt 文件
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        for para in doc.paragraphs:
                            f.write(para.text + '\n')
                    
                    #print(f"成功转换 {docx_file} 为 {txt_file}")
                
                except Exception as e:
                    print(f"转换 {docx_file} 时出错: {e}")

def remove_evaluation_warning(text):
    '''移除水印'''
    lines=text.splitlines()
    if "Evaluation Warning: "in lines[0]:
        return "\n".join(lines[1:])
    return text
def doc2txt(input_dir):
    '''包含水印'''
    if not os.path.exists(input_dir):
        print("no exist ")
        return 
    #print("start transfering")

    for root,dirs,files in os.walk(input_dir):
        for file in files :
            if file.lower().endswith('doc'):
                doc_file=os.path.join(root,file)
                txt_file=os.path.join(root,file.replace('doc','txt'))

                try:
                    doc = Document()
                    doc.LoadFromFile(doc_file)
                    doc.SaveToFile(txt_file,FileFormat.Txt)
                    doc.Close()
                    '''处理水印'''
                    with open(txt_file,'r',encoding='utf-8')as f:
                        content=f.read()
                    clean_content=remove_evaluation_warning(content)
                    with open(txt_file,'w',encoding='utf-8')as f:
                        f.write(clean_content)
                    #print(f"success trans{doc_file}to{txt_file}")
                except Exception as e:
                    print(f"make fault in trans {doc_file}:{e}") 

    
if __name__=="__main__":
    INPUTDIR="/home/ubuntu/jiah/workspace/file_manager/file_manager/utils"
    pdf2txt(INPUTDIR)
    convert_docx_to_txt(INPUTDIR)
    doc2txt(INPUTDIR)
