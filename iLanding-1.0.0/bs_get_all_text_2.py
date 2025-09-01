import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import re

def get_root_parent(target, contain_tag_name):
    # Traverse to the root parent
    # cek apakah mengandung tag tertentu misalnya NAV (jika iya return true)
    root_parent = target
    while root_parent.parent is not None:
        root_parent = root_parent.parent
        if root_parent.name == contain_tag_name:
            return True 
    return False

def replace_parent_tag(parent_tag, parent_parent_tag):
    res = ""

    # 1. Proses parent_parent_tag
    mclass = parent_parent_tag.get('class')    
    if mclass:
        mclass.append('hover-dropdown')
    else:
        mclass = ['hover-dropdown']       

    # print('m_class', mclass)
    tmp_str = " ".join(mclass)
    res += f' <div class="{tmp_str}"> '

    # 2. Proses parent_tag    
    if parent_tag.has_attr('class'):
        parent_tag['class'].append('hover-text')
    else:
        parent_tag['class'] = ['hover-text']

    res += f'{parent_tag}'        

    # 3. Add drop down menu
    mdropdown_menu = '<div class="dropdown-content"> ' \
        '<a href="#" class="modal-trigger" ' \
            'data-user-uuid="4d445669-4d32466c-4f444574-4d7a637a-4e693035-5a6a6b79-5a6d5668-4e513d3d"  ' \
            'data-user-type="CharField"> ' \
            '<i class="fas fa-edit icon"></i> &nbsp;Edit Data ' \
        '</a> ' \
        '<a href="#"><i class="fas fa-home icon"></i> Option 2</a> ' \
        '<a href="#"><i class="fas fa-home icon"></i> Option 3</a> ' \
        '</div>'
    res += mdropdown_menu
    res += ' </div> ' # tambah tag penutup (pengganti tag a)    
    parent_parent_tag.replace_with(BeautifulSoup(res, "html.parser"))    

def replace_parent_tag_direct(parent_tag, text_element):
    '''
        without anchor link
    '''
    res = ""

    # 1. Proses parent_parent_tag
    mclass = parent_tag.get('class')    
    print('get class', mclass)
    if mclass:
        mclass.append('hover-dropdown')
    else:
        mclass = ['hover-dropdown']       

    # print('m_class', mclass)
    tmp_str = " ".join(mclass)
    res += f' <div class="{tmp_str}"> '

    # print('res', res)

    # 2. Proses direct text, replace langusung dengan hover-text tag div
    # tmp = f'{parent_tag}'.replace(text_to_find,'THIS IS ME')    
    # if parent_tag.has_attr('class'):
    #     parent_tag['class'].append('hover-text')
    # else:
    #     parent_tag['class'] = ['hover-text']
    tmp = f'<div class="hover-text">{text_element}</div>'
    tmp = f'{parent_tag}'.replace(text_element, tmp)    
    res += f'{tmp}'        
    print('res 1', res)

    # 3. Add drop down menu
    mdropdown_menu = '<div class="dropdown-content"> ' \
        '<a href="#" class="modal-trigger" ' \
            'data-user-uuid="4d445669-4d32466c-4f444574-4d7a637a-4e693035-5a6a6b79-5a6d5668-4e513d3d"  ' \
            'data-user-type="CharField"> ' \
            '<i class="fas fa-edit icon"></i> &nbsp;Edit Data ' \
        '</a> ' \
        '<a href="#"><i class="fas fa-home icon"></i> Option 2</a> ' \
        '<a href="#"><i class="fas fa-home icon"></i> Option 3</a> ' \
        '</div>'
    res += mdropdown_menu
    res += ' </div> ' # tambah tag penutup (pengganti tag a)    
    # print('res 2', res)

    parent_tag.replace_with(BeautifulSoup(res, "html.parser"))      

def add_dropdown(soup, text_to_find):
    print('text to find:', text_to_find)
    
    text_element = soup.find(string=re.compile(text_to_find))
    parent_tag = text_element.find_parent() if text_element else None
    parent_parent_tag = parent_tag.find_parent() if parent_tag else None

    # print('text_element', text_element)
    # print('parent', parent_tag)
    # print('parent_parent', parent_parent_tag)

    # tmp = f'{parent_tag}'.replace(text_to_find,'THIS IS ME')
    # print('THIS IS ME', tmp)

    # !!1 Jika tag parent ke dua itu a, maka perlakuan berbeda dengan jika selain a
    
    # Output the parent tag\
    if parent_parent_tag:
        if parent_parent_tag.name == 'a':
            print('replace_parent_tag')
            replace_parent_tag(parent_tag, parent_parent_tag)                        
        else:
            # print("Not anchor in parent_parent & no")
            print('replace_parent_tag_direct')
            replace_parent_tag_direct(parent_tag, text_element)

    # elif parent_tag:
    #     mdropdown_menu = '<div class="dropdown-content"> ' \
    #             '<a href="#" class="modal-trigger" ' \
    #                 'data-user-uuid="4d445669-4d32466c-4f444574-4d7a637a-4e693035-5a6a6b79-5a6d5668-4e513d3d"  ' \
    #                 'data-user-type="CharField"> ' \
    #                 '<i class="fas fa-edit icon"></i> &nbsp;Edit Data ' \
    #             '</a> ' \
    #             '<a href="#"><i class="fas fa-home icon"></i> Option 2</a> ' \
    #             '<a href="#"><i class="fas fa-home icon"></i> Option 3</a> ' \
    #             '</div>'     
    else:
        if parent_tag:
            print('ada parent_tag')
        else:
            if text_element:
                print('ada text_element')
            else:
                print("Nothing parent_parent, parent, and text element")

def scrape_text():
    # URL of the webpage to scrape
    # url = "./index.html"
    # Membuka file HTML lokal
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()

    # remove all space, tab, new lines
    content = content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # remove all multiple spaces with single space
    cleaned_text = re.sub(r'\s+', ' ', content).strip()

    # print('content', content[:5000])  # Print first 1000 characters of the content
    # return

    # Membuat objek BeautifulSoup "lxml" "html5lib"
    soup = BeautifulSoup(cleaned_text, "html.parser")

    # Contoh: Mencetak judul halaman
    # print("Judul Halaman:", soup.title.string)
    
    # Fetch the webpage content
    # response = requests.get(url)
    # print('res', response)
    # if response.status_code == 200:
    # text_nodes = soup.body.find_all(text=True)
    # visible_text = [text.strip() for text in text_nodes if text.strip()]
    # all_text = ' '.join(visible_text)
    # print('all_text', all_text)
    # return

    # text = soup.body.get_text(separator='\u0001', strip=True)  # Use temporary separator
    # print(text.replace('\u0001', ' '))



    # Parse the HTML content
    # soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all visible text from the body tag

    # OKE FIND ALL TEXT
    # -----------------
    # get all text with new line separator
    body_text = soup.body.get_text(separator="\n", strip=True)    
    # print(body_text)
    # for i in body_text:
    #     print('i', i)

    # split by new line
    tmp = body_text.split('\n')
    # tmp = re.sub(r'\s+', ' ', body_text).strip()
    # tmp = tmp.split('\n')

    for i in range(len(tmp)):
        print('Proses', tmp[i])        
        print('------')
        do_replace(soup, tmp[i])
        # add_dropdown(soup, tmp[i])
        # if i>20: break


    # FIND parent tag from text
    # -------------------------
    # mtext_to_find = "iLanding"
    # add_dropdown(soup, mtext_to_find)

    # with open("res.html", "w", encoding="utf-8") as file:
    #     file.write(soup.prettify())

    # for text_node in soup.find_all(text=True)[:5]:
    #     if text_node.strip():  # Skip empty text nodes
    #         parent_tag = text_node.parent
    #         print(f"Text: '{text_node.strip()}'")
    #         print(f"Parent Tag: {parent_tag.name}")
    #         print("---")

    # Return the text as a JSON response
    # return JsonResponse({"text": body_text})
    # else:
    #     return JsonResponse({"error": "Failed to fetch the webpage"}, status=400)
