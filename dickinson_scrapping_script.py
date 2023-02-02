import json
import pandas as pd
import numpy as np
import re

import requests
from bs4 import BeautifulSoup
import unicodedata
import csv



paragraph_list = list()
alphabet_list = list()



# function to scrap data from a given url
def scrappData(url):
    URL=url
    cnt = requests.get(URL)
    htmlContent=cnt.content
    # soup = BeautifulSoup(htmlContent, 'html5lib')
    soup = BeautifulSoup(htmlContent, 'html.parser')

    article = soup.find('div', {'class': "view-mode-full"}).findAll('p')
    print(article[0:10])

    # print(article[0].text)
    alphabet_list = article[0].text.split('|')
    alphabet_list = [x.strip() for x in alphabet_list]
    # print(alphabet_list)

    article.pop(0)

    for element in article:
        paragraph_list.append(element)
        # print(element)
        # print

    # print(paragraph_list)

    scrapped_main_data_dict = dict()
    scrapped_entries_and_subentries_list = list()

    for alphabet in alphabet_list:
        scrapped_main_data_dict[alphabet] = dict()

    print(scrapped_main_data_dict)

    alphabet_counter = -1


    for paragraph_item in paragraph_list:
        print("processing . .. "+str(paragraph_item))
        print
        if any(alphabet == paragraph_item.text for alphabet in alphabet_list):
            # print(paragraph_item.text)
            print
            if(alphabet_counter>-1):
                print("\n\nadding in main list . ..at ..."+alphabet_list[alphabet_counter]+"\n\n" )
                scrapped_main_data_dict[alphabet_list[alphabet_counter]] = list(scrapped_entries_and_subentries_list)
                scrapped_entries_and_subentries_list.clear()
            alphabet_counter = alphabet_counter+1
            # if(alphabet_counter==10):
            #     break

            # print("alphabet_counter is incremented to ...",alphabet_counter)
        else:
            # print(paragraph_item)
            # print(paragraph_item.text)
            print

            temp_dictionary = dict()
            description = unicodedata.normalize("NFKD",str(paragraph_item.get_text(strip=True)))

            paragraph_item_style = paragraph_item.get('style')

            if(paragraph_item_style  is None):      #Entry
                # print("This is Entry")
                index_entry = paragraph_item.find('b')  # "<b>A</b>"
                index_entry_bold = paragraph_item.find('span', {
                    'class': "foreign"})  # "strong><span class="foreign" style="font-style: italic;">ă</span></strong>"

                if(index_entry is not None):
                    temp_dictionary['index_entry'] = unicodedata.normalize("NFKD",str(index_entry.string))
                    description = description.replace(str(index_entry.string), '')
                    # print(index_entry.string)
                elif(index_entry_bold is not None):
                    temp_dictionary['index_entry'] = unicodedata.normalize("NFKD",str(index_entry_bold.string))
                    description = description.replace(str(index_entry_bold.string), '')
                    # print(index_entry_bold.string)
                else:
                    temp_dictionary['index_entry'] = ''

                links_with_text_dictionary_list = list()
                for link in paragraph_item.find_all('a'):
                    links_with_text_dictionary = dict()
                    # print(link.text)
                    # print(link.get('href'))
                    section_number_text = link.get_text(strip=True)
                    links_with_text_dictionary['section_number'] = unicodedata.normalize("NFKD",section_number_text)
                    links_with_text_dictionary['section_number_link'] = link.get('href')
                    description = description.replace(str(link.get_text(strip=True)), '')
                    links_with_text_dictionary_list.append(links_with_text_dictionary)

                temp_dictionary['section_number_and_link'] = links_with_text_dictionary_list

                description = description.replace(';','')

                # print("description==>"+description)
                temp_dictionary['description'] = unicodedata.normalize("NFKD",description)

                # text_nodes = [e.strip() for e in paragraph_item if not e.name and e.strip()]
                # print("text_nodes ==> ",text_nodes)

            elif(paragraph_item_style is not None and paragraph_item_style=="padding-left: 30px;"): #Sub-Entry
                # print("This is Subentry")
                temp_dictionary['index_entry'] = ''

                links_with_text_dictionary_list = list()
                for link in paragraph_item.find_all('a'):
                    links_with_text_dictionary = dict()
                    # print(link.text)
                    # print(link.get('href'))
                    section_number_text = link.get_text(strip=True)
                    links_with_text_dictionary['section_number'] = unicodedata.normalize("NFKD",section_number_text)
                    links_with_text_dictionary['section_number_link'] = link.get('href')
                    description = description.replace(str(link.get_text(strip=True)), '')
                    links_with_text_dictionary_list.append(links_with_text_dictionary)


                temp_dictionary['section_number_and_link'] = links_with_text_dictionary_list

                description = description.replace(';','')

                # print("description==>"+description)
                temp_dictionary['description'] = unicodedata.normalize("NFKD",description)


            latin_words_list = list()
            for latin_word in paragraph_item.find_all('span', {'class': "foreign"}):
                latin_words_list.append(unicodedata.normalize("NFKD",str(latin_word.string)))

            temp_dictionary['latin_words'] =    ' '.join([str(word) for word in latin_words_list])


            scrapped_entries_and_subentries_list.append(temp_dictionary)

    if(alphabet_counter>0):
        print("\n\nadding in main list . ..at ..." + alphabet_list[alphabet_counter] + "\n\n")
        scrapped_main_data_dict[alphabet_list[alphabet_counter]] = scrapped_entries_and_subentries_list

    print("Printing Final Scrapped Data\n")

    # print(scrapped_main_data_dict)


    # with open('dickinson.json', 'w',encoding='utf-8') as fp:
    #     json.dump(scrapped_main_data_dict, fp, ensure_ascii=False)
    #
    # print("JSON dumped . . .")
    #
    # print(scrapped_main_data_dict['A'][0].keys())
    #
    # keys = scrapped_main_data_dict['A'][0].keys()
    # with open('dickinson.csv', 'w', newline='',encoding='utf_8_sig')  as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     for key in scrapped_main_data_dict:
    #         # print(scrapped_main_data_dict[key])
    #         for item in scrapped_main_data_dict[key]:
    #             print(item)
    #             dict_writer.writerow(item)
    #
    # print("CSV dumped . . .")





if __name__ == '__main__':
    dickinson_index_page_URL="http://dcc.dickinson.edu/grammar/latin/index#XYZ"

    dickinson_index_page=scrappData(dickinson_index_page_URL)

