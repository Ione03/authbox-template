'''
    Convert to django
    for covert output bs_get_all_text : res.html and src.html to django template
    django template: 
        src.html ->
            [code]-base.html
            [code]-base-index.html
            [code]-index.html
        code = hexadesimal uniq

        res.html ->
            [code]-base.html
            [code]-base-index.html
            [code]-index.html
'''

# import re
# import json
from bs4 import BeautifulSoup

def replace_title(input_file):    
    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    text_elements = soup.find('title')
    
    # add include id base.html
    tmp = "{{ title }}"
    # m_include = BeautifulSoup(tmp, "html.parser")
    text_elements.string.replace_with(tmp)

    # Add extra head dan extra body di bagian akhir tag penutup
    tmp = "{% block extra_head %} {% endblock %}"
    m_include = BeautifulSoup(tmp, "html.parser")
    soup.head.append(m_include)

    tmp = "{% block extra_body %} {% endblock %}"
    m_include = BeautifulSoup(tmp, "html.parser")
    soup.body.append(m_include)

    with open('base.html', 'w', encoding='utf-8') as file:        
        file.write(soup.prettify())

    # remove all link element from source html
    print("Replace Title Done...")
    return soup

    # with open('extracted_texts.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(texts, json_file, ensure_ascii=False, indent=4)
    
    # with open('snippets/style.html', 'r', encoding='utf-8') as file:
    #     for i in locals
    #     file.write(soup.prettify())
    # print("Extract Link Done...")

def extract_tag_name(soup, folder_name, tag_name, m_index=0):        
    # find all tag
    tag_elements = soup.find_all(tag_name)
    
    # add static to target html except for meta
    link_element = ""
    if tag_name!="meta":
        link_element = "{% load static %}"

    # proses all finding tag
    m_parent_tag = None
    for i in range(len(tag_elements)):
        # print('parent name', tag_elements[i].parent.name)
        if not m_parent_tag:
            m_parent_tag = tag_elements[i].parent

        if tag_elements[i].has_attr('href'):
            if not("https://" in tag_elements[i]["href"]):            
                tag_elements[i]["href"] = "{% static '" + folder_name + "/" + \
                                            tag_elements[i]["href"] + "' %}"
        link_element += tag_elements[i].prettify()
        # hapus element link dari soup
        tag_elements[i].decompose()
        
    # write to file tag link or meta (tag_name)
    m_link = BeautifulSoup(link_element, 'html.parser')    
    with open('snippets/'+ tag_name +'.html', 'w', encoding='utf-8') as file:        
        file.write(m_link.prettify())

    # add include to base.html
    tmp = "{% include '"+ folder_name +"/snippets/"+ tag_name +".html' %}"
    m_include = BeautifulSoup(tmp, "html.parser")
    m_parent_tag.insert(m_index, m_include)
    
    # soup.head.append(m_include)

    with open('base.html', 'w', encoding='utf-8') as file:        
        file.write(soup.prettify())

    # remove all link element from source html
    print(f"Extract {tag_name} Done...")
    return soup

    # with open('extracted_texts.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(texts, json_file, ensure_ascii=False, indent=4)
    
    # with open('snippets/style.html', 'r', encoding='utf-8') as file:
    #     for i in locals
    #     file.write(soup.prettify())
    # print("Extract Link Done...")

# def extract_link(folder_name, soup):    
#     # with open(input_file, 'r', encoding='utf-8') as file:
#     #     html_content = file.read()
    
#     # soup = BeautifulSoup(html_content, 'html.parser')
#     text_elements = soup.find_all('link')
    
#     # texts = [element.strip() for element in text_elements if element.strip()]
#     link_element = "{% load static %}"
#     for i in range(len(text_elements)):
#         if not("https://" in text_elements[i]["href"]):
#             text_elements[i]["href"] = "{% static '" + folder_name + "/" + \
#                                         text_elements[i]["href"] + "' %}"
#         link_element += text_elements[i].prettify()
#         # hapus element link dari soup
#         text_elements[i].decompose()
        
#     m_link = BeautifulSoup(link_element, 'html.parser')    

#     with open('snippets/style.html', 'w', encoding='utf-8') as file:        
#         file.write(m_link.prettify())

#     # add include id base.html
#     tmp = "{% include '"+ folder_name +"/snippets/style.html' %}"
#     m_include = BeautifulSoup(tmp, "html.parser")
#     soup.head.append(m_include)

#     with open('base.html', 'w', encoding='utf-8') as file:        
#         file.write(soup.prettify())

#     # remove all link element from source html
#     print("Extract Link Done...")
#     return soup

#     # with open('extracted_texts.json', 'w', encoding='utf-8') as json_file:
#     #     json.dump(texts, json_file, ensure_ascii=False, indent=4)
    
#     # with open('snippets/style.html', 'r', encoding='utf-8') as file:
#     #     for i in locals
#     #     file.write(soup.prettify())
#     # print("Extract Link Done...")

# def extract_meta(folder_name, soup):    
#     # with open(input_file, 'r', encoding='utf-8') as file:
#     #     html_content = file.read()
    
#     # soup = BeautifulSoup(html_content, 'html.parser')
#     text_elements = soup.find_all('meta')
    
#     # texts = [element.strip() for element in text_elements if element.strip()]
#     link_element = ""
#     for i in range(len(text_elements)):        
#         link_element += text_elements[i].prettify()
#         # hapus element link dari soup
#         text_elements[i].decompose()
        
#     m_link = BeautifulSoup(link_element, 'html.parser')    

#     with open('snippets/meta.html', 'w', encoding='utf-8') as file:        
#         file.write(m_link.prettify())


#     # add include id base.html
#     tmp = "{% include '"+ folder_name +"/snippets/meta.html' %}"
#     m_include = BeautifulSoup(tmp, "html.parser")
#     soup.head.append(m_include)

#     with open('base.html', 'w', encoding='utf-8') as file:        
#         file.write(soup.prettify())

#     print("Extract Meta Done...")
#     return soup
#     # remove all link element from source html
#     # with open('extracted_texts.json', 'w', encoding='utf-8') as json_file:
#     #     json.dump(texts, json_file, ensure_ascii=False, indent=4)
    
#     # with open('snippets/style.html', 'r', encoding='utf-8') as file:
#     #     for i in locals
#     #     file.write(soup.prettify())

#     # print("Extract Meta Done...")

def extract_body(folder_name, soup):
    body_tag = soup.body

    first_tag = body_tag.find_next()
    # if tag = header, or footer
    print('first_tag.name', first_tag.name)

    
    


    # Find all elements after body
    # elements_after_body = []
    # current = body_tag.next_sibling

    # while current:
    #     if current.name is not None: # This is a tag
    #         elements_after_body.append(current)
    #     current = current.next_sibling

    # # Display results
    # print(f"Found {len(elements_after_body)} tags after the body:")
    # for i, element in enumerate(elements_after_body, 1):
    #     print(f"{i}. {element.name}: {element}")

    # all_tags_after_body = body_tag.find_all_next(limit=5)
    # # print('ALL NEXT', all_tags_after_body)
    # for i in all_tags_after_body:
    #     print('--->', i)

    return

    # Find the first tag after <body>
    first_tag_after_body = body_tag.find_next()
    print('first_tag_after_body', first_tag_after_body)

    first_tag_after_body = first_tag_after_body.find_next()
    print('second_tag_after_body', first_tag_after_body)

def scrape_tag():
    folder_name = "ilanding"
    input_file = 'res.html'

    soup = replace_title(input_file)
    soup = extract_tag_name(soup, folder_name, 'link')
    soup = extract_tag_name(soup, folder_name, 'meta', m_index=1)
    # soup = extract_body(folder_name, soup)

    soup = extract_tag_name(soup, folder_name, 'header')
    soup = extract_tag_name(soup, folder_name, 'main', m_index=1)
    soup = extract_tag_name(soup, folder_name, 'footer', m_index=2)

    # append (insert to the last position)
    soup = extract_tag_name(soup, folder_name, 'script', m_index=3)

    print("All Done...")
    