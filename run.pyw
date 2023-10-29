import re
import os
import pyperclip
from tkinter import *

def main():
  def result(event):
    output, changes = get_input()
    input.delete('1.0', END)
    if changes != "":
      input.insert('1.0', changes)
    else:
      input.insert('1.0', output)
    pyperclip.copy(output)
      
    
  # get text from ui textbox
  def get_input():
    user_input = input.get("1.0", "end-1c")
    user_input = user_input.strip()
    out = analayze(user_input)
    return out
  
  # analayze user input to pick what program to run
  def analayze(user_input):
    if '<?xml version="1.0" encoding="utf-8"?>' in user_input:
      out = epub(user_input)
    elif "funding" in user_input or "ethics" in user_input or "ack" in user_input or "contrib" in user_input or "supp" in user_input or "data" in user_input or "coi" in user_input:
      out = section(user_input)
    elif "loop" in user_input:
      out = looplink(user_input)
    elif "doi:" in user_input or "#doi:" in user_input or "#DOI:" in user_input:
      out = doi(user_input)
    elif "-" in user_input:
      print('1')
      out = page(user_input, "-")
    elif "—" in user_input:
      out = page(user_input, "—")
    
    else:
      print('error')
    return out
  
  # process user input with the right tagging for looplink
  def looplink(user_input):
    out = '<uri xlink:href="' + str(user_input) + '"/>'
    changes = ""
    return out, changes
  
  # process user input with the right tagging for doi
  def doi(user_input):
    user_input = user_input.split(": ")
    user_input.pop(0)
    doi = "".join(user_input)
    out = 'doi:&nbsp;<pub-id pub-id-type="doi">' + str(doi) + '</pub-id>'
    changes = ""
    return out, changes
  
  # process user input with the right tagging for page
  def page(user_input, separator):
    remotepc = r'D:\000_GetJob\WorkHere' 
    path = "/Users/angel/OneDrive/Documents/AutoTag"
    articles = ["fimmu", "fendo", "fcdhc", "fviro", "fruro", "fitd", "fsoi", "fsci", "fopht", "fonc", "fneph", "finsc", "frhem", "fgstr", ]
    entries = os.listdir(path)
    entries = "".join(entries)
    pages = user_input.split(separator)
    numbered = False
    value = []
    check = True
    
    for x in range(len(articles)):
      if articles[x] in entries:
        numbered = True
        if len(pages[0]) == len(pages[1]) and pages[0] != pages[1]:
          for i in range(len(pages[0])):
            if pages[0][i] == pages[1][i] and check == True:
              value.append(pages[1][i])
            else:
              check = False
    
    if numbered == True:
      value = "".join(value)
      value = pages[1].replace(value, "")
      out = "<page-range>" + pages[0] + "&ndash;" + value + "</page-range>"
    else:
      out = '<first-page>' + str(pages[0]) + '</first-page>&ndash;<last-page>' + str(pages[1]) + '</last-page>'
    changes = ""
    return out, changes

  def section(user_input):
    user_input = user_input.split(":")
    paragraph = user_input[1].strip()
    match user_input[0]:
      case "funding":
        out = '<sec id="sx" sec-type="funding-information"><title>Funding</title><p><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
      case "ethics":
        out = '<sec id="sx" sec-type="ethics-statement"><title>Ethics statement</title><p><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
      case "ack":
        out = '<ack><title>Acknowledgments</title><p><?A3B2 tlsb pt?>' + paragraph + '</p></ack>'
      case "contrib":
        out = '<sec id="sx" sec-type="author-contributions"><title>Author contributions</title><p><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
      case "supp":
        out = '<sec id="SM1" sec-type="supplementary-material"><title>Supplementary material</title><p><?A3B2 tpb pt?><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
      case "data":
        out = '<sec id="sx" sec-type="data-availability"><title>Data Availability statement</title><p><?A3B2 tpb pt?><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
      case "coi":
        out = '<sec id="sx" sec-type="COI-statement"><title>Conflict of interest</title><p><?A3B2 tpb pt?><?A3B2 tlsb pt?>' + paragraph + '</p></sec>'
    changes = ""
    return out, changes
  
  def epub(user_input):
    changes_list = ["EPUB Changes:\n"]
    aff = True
    id = 1
    while aff == True:
        if user_input.find('<a id="aff' + str(id) + '"></a><sup>' + str(id) + '</sup>') > 0:
            user_input = user_input.replace('<a id="aff' + str(id) + '"></a><sup>' + str(id) + '</sup>', '<a id="aff' + str(id) + '"></a><sup>' + str(id) + '</sup>&#160;')
            id += 1
        else:
            changes_list.append('Affiliation count: ' + str(id - 1) + '\n')
            aff = False
    author_notes = True
    while author_notes == True:
        if user_input.find('<a class="author-notes" href="#fn002"><sup>†</sup>') > 0:
            user_input = user_input.replace('<a class="author-notes" href="#fn002"><sup>†</sup>', '<a class="author-notes" href="#fn003"><sup>†</sup>')
        elif user_input.find('<p class="other"><strong>†</strong>') > 0:
            user_input = user_input.replace('<p class="other"><strong>†</strong>', '<p class="other" id="fn003"><strong><sup>†</sup></strong>') 
        elif user_input.find('<sup>,</sup><a class="author-notes" href="#fn003">') > 0:
            user_input = user_input.replace('<sup>,</sup><a class="author-notes" href="#fn003">', '<a class="author-notes" href="#fn003">')
        elif user_input.find('<sup>,</sup><a class="author-notes" href="#fn001">') > 0:
            user_input = user_input.replace('<sup>,</sup><a class="author-notes" href="#fn001">', '<a class="author-notes" href="#fn001">')
        else:
            author_notes = False
            
    #fix correspoding id        
    if user_input.find('<p class="corresp">') > 0:
      user_input = user_input.replace('<p class="corresp">', '<p class="corresp" id="fn001">')
    corresponding_start = user_input.find('<p class="corresp"')
    corresponding_end = user_input.find('</p>', corresponding_start)
    old_corresponding_section = user_input[corresponding_start:corresponding_end + 4]
    new_corresponding_section = user_input[corresponding_start:corresponding_end + 4]
    print(old_corresponding_section)
    checklooplink = TRUE
    looplink_count = 0
    while checklooplink:
      if new_corresponding_section.find('<a class="profileLink" href') > 0:
        looplink_start = new_corresponding_section.find('<a class="profileLink" href')
        looplink_end = new_corresponding_section.find('</a>, <a href="mailto', looplink_start)
        looplink_tag = new_corresponding_section[looplink_start:looplink_end + 5]
        looplink_tag_split = re.split('">|</a', looplink_tag)
        auname = looplink_tag_split[1]
        new_corresponding_section = new_corresponding_section.replace(looplink_tag, auname + '<br/>')
        looplink_count += 1
      else:
        user_input = user_input.replace(old_corresponding_section, new_corresponding_section)
        if looplink_count > 1:
          out_string = 'looplinks '
        else:
          out_string = 'looplink '
        changes_list.append('Fix corresonding id and removed ' + str(looplink_count) + ' ' + out_string + '\n')
        checklooplink = False
    
    
    #fix dagger with no taggings
    # if user_input.find('†These authors share first authorship') > 0:
    #   user_input = user_input.replace('†These authors share first authorship', '<p class="other" id="fn003"><sup>†</sup>These authors share first authorship</p>')
    #   changes_list.append('Fixed dagger with no taggings\n')
    # if user_input.find('‡These authors share first authorship') > 0:
    #   user_input = user_input.replace('‡These authors share first authorship', '<p class="other" id="fn004"><sup>‡</sup>These authors share first authorship</p>')
    #   changes_list.append('Fixed double dagger with no taggings\n')
    # fix orcid id
    # if user_input.find('<p class="other"><strong>†ORCID:</strong>') > 0:
    #   user_input = user_input.replace('<p class="other"><strong>†ORCID:</strong>', '<p class="other" id="fn003"><strong><sup>†</sup>ORCID:</strong>')
    # orcid_start = user_input.find('<p class="other" id="fn003"><strong><sup>†</sup>ORCID:</strong>')
    # orcid_end = user_input.find('</a></p>', orcid_start)
    # orcid_section = user_input[orcid_start:orcid_end + 8]
    # print(orcid_section)
    
    test = '†These authors have contributed equally to this work and share first authorship‡These authors have contributed equally to this work and share last authorship'
    
    corresponding_start = user_input.find('<p class="corresp"')
    corresponding_end = user_input.find('</p>', corresponding_start)
    dagger_end = user_input.find('<!-- HISTORY DATES -->')
    dagger = '\n†'
    Dagger = '\n‡'
    old_daggersec = ''
    if user_input.find(dagger, corresponding_end) > 0:
      daggersec = user_input[user_input.find(dagger, corresponding_end):dagger_end]
      old_daggersec = daggersec
      daggersec = daggersec.replace(dagger, '')
    elif user_input.find(Dagger, corresponding_end) > 0:
      daggersec = user_input[user_input.find(Dagger, corresponding_end):dagger_end]
      old_daggersec = daggersec
      daggersec = daggersec.replace(Dagger, '')
    print(daggersec)
    
    
    
      
    table = True
    num = 1
    while table == True:
        if user_input.find('img src="../Images/table_t' + str(num) + '.jpg"') > 0:
            user_input = user_input.replace('img src="../Images/table_t' + str(num) + '.jpg"', 'img src="../Images/table' + str(num) + '.jpg"')
            changes_list.append('Table ' + str(num) + ' image\n')
            num += 1
        else:
            table = False
            
    # fix footnote and abbrev<h2 class="Heads_1">Footnote</h2>'
    if user_input.find('<section title="Footnote">') > 0:
      footnote_start = user_input.find('<section title="Footnote">')
      footnote_end = user_input.find('</h2>', footnote_start)
      footnote_section = user_input[footnote_start:footnote_end + 5]
      user_input = user_input.replace(footnote_section, '')
      changes_list.append('Fixed Footnote\n')
      
    find_id = True
    sec_id = 1
    sec_id_list = []
    while find_id:
      if user_input.find('<h2 class="Heads_1" id="s'+str(sec_id)+'">') > 0:
        sec_id += 1
      else:
        find_id = False
        sec_id_list.append(sec_id)
    if user_input.find('Abbreviations\n<p class="fn" id="">') > 0:
      user_input = user_input.replace('Abbreviations\n<p class="fn" id="">', '<section title="Abbreviations">\n<h2 class="Heads_1" id="s'+str(sec_id)+'">Abbreviations</h2>\n<p class="Text_T1">')
      changes_list.append('Fixed Abbreviations\n')
    
    
    changes_list = "".join(changes_list)
    return user_input, changes_list
  

# load ui binding enter key
  ui = Tk()
  ui.geometry("1000x250")
  ui.resizable(False, False)
  ui.title("Tagging")
  var = StringVar()
  label = Label(ui, textvariable=var, font="TimesNewRoman 10")
  var.set("Section codes:\ncoi: = Conflict of interest | data: = Data availability | supp: = Supplementay material | contrib: = Author contributions | ethics: = Ethics statement | funding: = Funding")
  label.pack()
  input = Text(ui, font="TimesNewRoman 20", height = 500, width = 350)
  button = Button(ui)
  input.pack()
  button.pack()
  ui.bind('<Return>', result)
  ui.mainloop()
main()



