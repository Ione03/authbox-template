import requests
from bs4 import BeautifulSoup, Comment
# from django.http import JsonResponse
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

def get_root_parent_id(target, contain_tag_name):
    # Traverse to the root parent
    # cek apakah mengandung tag tertentu misalnya NAV (jika iya return true)
    root_parent = target
    while root_parent.parent is not None:
        root_parent = root_parent.parent
        if root_parent.name == contain_tag_name:
            if root_parent.has_attr('id'):
                mid = root_parent.get('id')    
                return mid 
    return None 

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

def add_dropdown(soup, text_to_find, m_section_array):
    # print('text to find:', text_to_find)
    # replace <!-- Standard Plan --> too
        
    # Error jika ada karakter +
    if text_to_find[0] == '+':
        text_to_find = text_to_find.replace('+','')

    text_element = soup.body.find_all(string=re.compile(text_to_find))
    
    for i in range(len(text_element)):
        # print('text parent', text_element[i].parent)

        if not text_element[i]:
            print('Ubah data index.html jika ini masih muncul!!! (Hilangkan karakter ? + dll)')
            print('text to find:', text_to_find)
            print('found text_element:', text_element[i])
            print('fix this first')
            return 

        m_continue = True
        if get_root_parent(text_element[i], 'nav'):
            # print('Text is inside nav, skip it:', text_to_find)
            m_continue = False 

        if m_continue and get_root_parent(text_element[i], 'ul'):
            # print('Text is inside ul, skip it:', text_to_find)
            m_continue = False 

        if m_continue and get_root_parent(text_element[i], 'form'):
            # print('Text is inside form, skip it:', text_to_find)
            m_continue = False 

        # get section id
        m_section = {}
        if m_continue:
            # print('section', get_root_parent_id(text_element[i], 'section'))
            # print('Text is inside form, skip it:', text_to_find)
            tmp = get_root_parent_id(text_element[i], 'section')
            # print('SECTION', tmp)
            # print('m_section_array', m_section_array)
            if tmp:
                # Reset code mulai dari 1 jika name berubah
                mfound = False
                for j in range(len(m_section_array)):
                    if m_section_array[j]['name'] == tmp:
                        # print('found', tmp)
                        m_section_array[j]['code'] += 1
                        m_section = m_section_array[j]
                        mfound = True
                        break
                    # else:
                    #     # m_section_array[j]['name'] = tmp
                    #     # m_section_array[j]['code'] = 1
                    #     print('not found', tmp)
                    #     m_section = {'name': tmp, 'code': 1}                        
                    #     m_section_array.append(m_section)        
                        # print('append', m_section)                
                if not mfound:
                    m_section = {'name': tmp, 'code': 1}                        
                    m_section_array.append(m_section)        

                # if m_section['name'] == tmp:
                #     m_section['code'] += 1
                # else:
                #     m_section['code'] = 1
                #     m_section['name'] = tmp
            else: 
                # m_section['code'] += 1
                mfound = False
                for j in range(len(m_section_array)):                    
                    if m_section_array[j]['name'] == 'main':
                        # print('found', 'main')
                        m_section_array[j]['code'] += 1
                        m_section = m_section_array[j]
                        # print('append', m_section)                
                        mfound = True
                        break
                    # else:                        
                    #     # m_section_array.append(m_section)     
                    #     # m_section_array[j]['name'] = tmp
                    #     # m_section_array[j]['code'] = 1
                    #     # m_section = {'name': tmp, 'code': 1}                        
                    #     m_section = {'name': tmp, 'code': 1}                        
                    #     m_section_array.append(m_section)                                           

                if not mfound:
                    m_section = {'name': tmp, 'code': 1}                        
                    m_section_array.append(m_section)              

                # m_section['code'] = text_to_find
                # print('m_section', m_section)
            # m_continue = True


        # agar tidak 2 kali penulisan hoverable ini
        if text_element[i].parent.has_attr('class'):
            mclass = text_element[i].parent.get('class')    
            for j in mclass:
                # print('jj', j)
                if j=='hoverable':
                    m_continue = False
                    break
                elif j=='close':
                    m_continue = False
                    break
            

        if m_continue:
            m_code = f"{m_section['name']}-{m_section['code']}"     
            print('m_code', m_code)
            m_type = 'text'

            tmp = """
                    <span class="hoverable" id='""" + m_code + """'
                        data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
                        data-modal-title='""" + text_to_find + """'
                        data-modal-code='""" + m_code + """'
                        data-modal-type='""" + m_type + """'
                        >
                    """ + text_to_find + """
                        </span> 
                    """
            # print('---', tmp)
            replacement_soup = BeautifulSoup(tmp, 'html.parser')

            # print('text elemet', text_element)
            text_element[i].string.replace_with(replacement_soup)
            # soup = str(soup).replace('#REPLACE-ME#', tmp)
            # print(soup[:2500])
            # print('fff', text_element.string)


        # text_element.string.replace_with('tmp')  # replace text element with the original text

    # source = source.replace(text_to_find,'REPLACE_ME')
    # print('found text_element:', text_element)
    # if not text_element:
    #     print('text to find:', text_to_find)
    #     print('not found text_element:', text_element)

    # text_element = soup.find(string=re.compile(text_to_find))
    # parent_tag = text_element.find_parent() if text_element else None
    # parent_parent_tag = parent_tag.find_parent() if parent_tag else None

    # print('text_element', text_element)
    # print('parent', parent_tag)
    # print('parent_parent', parent_parent_tag)

    # tmp = f'{parent_tag}'.replace(text_to_find,'THIS IS ME')
    # print('THIS IS ME', tmp)

    # !!1 Jika tag parent ke dua itu a, maka perlakuan berbeda dengan jika selain a
    
    # Output the parent tag\
    # if parent_parent_tag:
    #     if parent_parent_tag.name == 'a':
    #         print('replace_parent_tag')
    #         replace_parent_tag(parent_tag, parent_parent_tag)                        
    #     else:
    #         # print("Not anchor in parent_parent & no")
    #         print('replace_parent_tag_direct')
    #         replace_parent_tag_direct(parent_tag, text_element)

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
    # else:
    #     if parent_tag:
    #         print('ada parent_tag')
    #     else:
    #         if text_element:
    #             print('ada text_element')
    #         else:
    #             print("Nothing parent_parent, parent, and text element")

def replace_icon(soup, class_name):
    bi_icons = soup.find_all('i', class_=class_name)
    # bi_icons = soup.find_all('i', class_=lambda x: x and any(cls.startswith('bi-') for cls in x))
    idx = 0
    m_type = 'icon'

    # Print results
    for icon in bi_icons:
        if icon:            
            m_continue = True
            if get_root_parent(icon, 'nav'):
                # print('Text is inside nav, skip it:', text_to_find)
                m_continue = False 

            if m_continue and get_root_parent(icon, 'ul'):
                # print('Text is inside ul, skip it:', text_to_find)
                m_continue = False 

            if m_continue:
                idx += 1
                m_code = f'bi-icon-{idx}'
                # print(m_code, m_code)

                icon_name = ""
                for j in icon.get('class', []):
                    # print('class', j)
                    if j.startswith('bi-'):
                        icon_name = j
                        # print('m_code', m_code)
                        break

                print(icon)        
                tmp = f"""
                    <span class="hoverable" 
                        data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
                        data-modal-title='{icon_name}'
                        data-modal-code='{m_code}'
                        data-modal-type='{m_type}'>
                        {icon}
                    </span> 
                """

                # print('---', tmp)
                replacement_soup = BeautifulSoup(tmp, 'html.parser')

                # print('text elemet', text_element)
                icon.replace_with(replacement_soup)
                # print(f"Full tag: {icon}")
                # print(f"Classes: {icon.get('class', [])}")
                # print("---")

def replace_img(soup):
    imgs = soup.find_all('img')
    # bi_icons = soup.find_all('i', class_=lambda x: x and any(cls.startswith('bi-') for cls in x))
    idx = 0
    m_type = 'image'
    

    for img in imgs:
        # print('img PARENT', img.parent)
        # print('-----------------------')
        if img:
            idx += 1
            m_code = f'image-{idx}'
            print('image', m_code, img)
            tmp = f"""
                <span class="hoverable" 
                    data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
                    data-modal-title='{img}'
                    data-modal-code='{m_code}'
                    data-modal-type='{m_type}'>
                    {img}
                </span> 
            """

            # print('---', tmp)
            replacement_soup = BeautifulSoup(tmp, 'html.parser')

            # print('text elemet', text_element)
            img.replace_with(replacement_soup)


    # Print results
    # for icon in bi_icons:
    #     if icon:            
    #         m_continue = True
    #         if get_root_parent(icon, 'nav'):
    #             # print('Text is inside nav, skip it:', text_to_find)
    #             m_continue = False 

    #         if m_continue:
    #             idx += 1
    #             m_code = f'bi-icon-{idx}'
    #             # print(m_code, m_code)

    #             icon_name = ""
    #             for j in icon.get('class', []):
    #                 # print('class', j)
    #                 if j.startswith('bi-'):
    #                     icon_name = j
    #                     # print('m_code', m_code)
    #                     break

    #             print(icon)        
    #             tmp = f"""
    #                 <span class="hoverable" 
    #                     data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
    #                     data-modal-title='{icon_name}'
    #                     data-modal-code='{m_code}'
    #                     data-modal-type='{m_type}'>
    #                     {icon}
    #                 </span> 
    #             """

    #             # print('---', tmp)
    #             replacement_soup = BeautifulSoup(tmp, 'html.parser')

    #             # print('text elemet', text_element)
    #             icon.replace_with(replacement_soup)
    #             # print(f"Full tag: {icon}")
    #             # print(f"Classes: {icon.get('class', [])}")
    #             # print("---")

def replace_ul(soup):
    items = soup.find_all('ul')
    # bi_icons = soup.find_all('i', class_=lambda x: x and any(cls.startswith('bi-') for cls in x))
    idx = 0
    m_type = 'unordered-list'

    for item in items:
        # print('item PARENT', item.parent)
        # print('-----------------------')        
        if item:            
            m_continue = True
            if get_root_parent(item, 'nav'):
                # print('Text is inside nav, skip it:', text_to_find)
                m_continue = False 

            if m_continue:
                idx += 1
                m_code = f'unordered-list-{idx}'
            
                print('unordered-list', m_code, item)
                print('------------------------------------')

                tmp = f"""
                    <span class="hoverable" 
                        data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
                        data-modal-title='{item.get_text(separator=', ', strip=True)}'
                        data-modal-code='{m_code}'
                        data-modal-type='{m_type}'>
                        {item}
                    </span> 
                """

                # print('---', tmp)
                replacement_soup = BeautifulSoup(tmp, 'html.parser')

                # print('text elemet', text_element)
                item.replace_with(replacement_soup)

def replace_nav(soup):
    items = soup.find_all('nav')
    # bi_icons = soup.find_all('i', class_=lambda x: x and any(cls.startswith('bi-') for cls in x))
    idx = 0
    m_type = 'nav-bar'

    for item in items:
        # print('item PARENT', item.parent)
        # print('-----------------------')        
        if item:            
        
            idx += 1
            m_code = f'nav-bar-{idx}'
        
            print('nav-bar', m_code, item)
            print('------------------------------------')

            tmp = f"""
                <span class="hoverable" 
                    data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!" 
                    data-modal-title='{item.get_text(separator=', ', strip=True)}'
                    data-modal-code='{m_code}'
                    data-modal-type='{m_type}'>
                    {item}
                </span> 
            """

            # print('---', tmp)
            replacement_soup = BeautifulSoup(tmp, 'html.parser')

            # print('text elemet', text_element)
            item.replace_with(replacement_soup)



def scrape_text():
    # URL of the webpage to scrape
    # url = "./index.html"
    # Membuka file HTML lokal
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()

    # remove all space, tab, new lines
    content = content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('$','Rp')

    # remove all multiple spaces with single space
    cleaned_text = re.sub(r'\s+', ' ', content).strip()

    # print('content', content[:5000])  # Print first 1000 characters of the content
    # return

    # Membuat objek BeautifulSoup "lxml" "html5lib"
    soup = BeautifulSoup(cleaned_text, "html.parser")
    # html_string = """
    #     <div class="container bc">
    #         <a href="#" class="bc1">
    #             <span class="bc2">Content inside anchor</span>
    #             <p class="bc3">Some text here</p>
    #         </a>
    #         <a href="#" class="bc4">
    #             <img src="image.jpg" alt="Example" class="bc45">
    #         </a>
    #     </div>
    #     """
    # soup = BeautifulSoup(html_string, 'html.parser')    

    # Remove all script and style elements
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        # print('comment', comment)
        comment.extract()

    # Find all <a> replace with <div> tags
    # Find all <a> tags with href="#"
    # for a_tag in soup.find_all('a'):
    #     # Create a new div tag
    #     new_div = soup.new_tag('div')
        
    #     # Copy all attributes (except href) from the a tag to div
    #     for attr, value in a_tag.attrs.items():
    #         if attr != 'href':  # Don't copy href attribute
    #             new_div[attr] = value
        
    #     # Move all children from a tag to div
    #     # print('tag', a_tag.contents)
    #     # print('length', len(a_tag.contents))
    #     # for i in range(len(a_tag.contents)-1):
    #     #     # print('child', a_tag.contents[child])
    #     #     print('i', i, 'child', a_tag.contents[i])
    #     #     new_div.append(a_tag.contents[i])
    #     # Move contents
    #     # Create a copy of contents to avoid modification during iteration
    #     children = list(a_tag.contents)  # Make a copy!
        
    #     # Move all children from a tag to div
    #     for child in children:
    #         new_div.append(child)
        
    #     # Replace the a tag with the new div
    #     a_tag.replace_with(new_div)

    # Remove href from all <a> tags
    for a_tag in soup.find_all('a'):
        if 'href' in a_tag.attrs:
            del a_tag.attrs['href']

    # print('soup', soup.prettify())  # Print first 1000 characters of the soup
    # return
    # Replace simbol ? dan +
    # !!!!

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
    # print(soup)
    # j=0
    m_section_array = []
    # m_section = { 'name': 'main', 'code': 0 }
    m_section_array.append({ 'name': 'main', 'code': 0 })

    for i in range(len(tmp)):
        # print('Proses', tmp[i])        
        # print('------')
        # do_replace(soup, tmp[i])
        
        add_dropdown(soup, tmp[i], m_section_array)
    
    replace_icon(soup, 'bi')
    replace_img(soup)
    replace_ul(soup)
    replace_nav(soup)

        # break
        # j+=1
        # if j==130:
        # Karena tanda $ ternyata, ke replace  <!DOCTYPE html>
            
        # if j>131:
        #     print(i, f'{tmp[i]}')
        #     break
        # if tmp[i][0] == '+':
        #     tmp[i] = tmp[i].replace('+','')

        # cleaned_text = cleaned_text.replace(tmp[i],' REPLACE_ME ')
        # if i>20: break


    # FIND parent tag from text
    # -------------------------
    # mtext_to_find = "iLanding"
    # add_dropdown(soup, mtext_to_find)

    # Koreksi awal dokumen
    # <!DOCTYPE html>
    
    # print(f'{soup}'[:100])

    with open("res.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    # .prettify()

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
