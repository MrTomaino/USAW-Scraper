#USAW Scraper
#Copyright 2024 B. Michael Tomaino
#This program scrapes arena.flowrestling.org for wrestlers' registrations and placementsin USAW qualifiers this year

from datetime import datetime
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from colorama import Style, Fore

# ---- CUSTOMIZE VALUES BELOW ----

curYear="2025" # modify for current year
featuredEvent="Randolph" # modify to highlight an event in output
curDivision="Novice 75"

ids={ # add names and IDs here... the name field is disregarded and is useful only for the coder
  "Desmond Tomaino":"450ada6f-8fd9-4c6b-9e06-85cd36427893"
  ,"Braden Smigler":"e89a71a6-ac86-429e-b6c5-094449b64523"
  ,"Parker Won":"0135a9e6-b537-4132-a382-ff6313b11ee6"
  ,"Carter Meng":"116e82b7-985a-4306-bfce-3d9cf060ec7e"
  ,"Lucas Harris":"c4516d34-3bc9-4d9a-beaf-9d6bb85d54c0"
  ,"Jonathan Moscato":"caa2024e-7d9c-4412-863c-2dc3271c6fe8"
  ,"Declan Sharkey":"7d06e349-b87a-449d-b9a5-011aa1768ebc"
  #,"Keir Devlin":"817a94c6-762c-4845-8327-7635701a53ae"
  ,"Joseph Bibro":"67f8c116-c50a-4b12-bfc9-481039e7812c"
  ,"Noah Hein":"bb230315-58c1-439a-8df5-29aa3d952ade"
  ,"Anthony D Libecci":"69cccc0b-1dd8-4f7b-8eb2-7f29d8d524e9"
  ,"Brody Winkel":"a26b24c6-174a-4456-b6ec-7573aa24eb68"
  ,"Matthew Amelio":"6aa1847d-060c-4989-aae1-473e9e088776"
  ,"Jason Roy":"9291fd77-26b5-4380-8956-216da7f5e428"
  ,"bert Dhiman":"f378b1b3-8b87-430d-8629-44a19735140e"
  ,"Jaxson James":"f8fcf0a2-aa21-4c52-8e80-c102ed9a760b"
  ,"Travis Butenewicz":"6d7718d1-4e24-424b-82d4-e09f64903d6f"
  ,"Jack Lauer":"fba26286-dedb-4e58-a19a-a180388bac5f"
  ,"Gianni Belluardo":"cecc7d17-1aa1-497c-8f5f-0da12109bc67"
  ,"Kruize Pawlus":"a9516867-debc-4530-926f-79f46d0508b7"
  ,"Dennis Gendel":"3177fd41-a9eb-4f21-854a-f3e838df87ff"
  ,"Anthony Messina Jr.":"2cf38ab4-6c34-4147-be46-7a8ca8e1fcb2"
  ,"Patrick McGorty":"1a08c16a-158f-4f0b-b516-e9fa3c9b4f9e"
  ,"JJ Gieger":"54995aef-fbe9-411a-b8b3-d2d7ca4c619f"
  ,"Parker Clancy":"0902abcf-ed56-498e-bf97-bc6e2f8bbb72"
  ,"Ethan Guzman":"3b805c59-5f53-4573-9034-337fe7bbb9d9"
  ,"Andrew Lopera":"a4f02af7-c1aa-4dd0-8e9c-df64bfb2de50"
  ,"Kieren McEllen":"6e119a10-028c-42c5-bd69-230013ef883d"
  ,"Kevin Wojcik":"1aed3886-593f-4eaa-8e4f-4f5e8b9d7cb3"
  ,"AJ Guercio":"05624784-dab1-4dc3-8c1b-5018844a9a92"
  ,"Mason Sawyer":"fd2a6b74-9c02-482a-a5ab-27d2c6523ad0"
  ,"Jayce Bird":"9bf9f041-83de-4ad7-b835-582e60599073"
  #,"Leonidas Dunbar":"61a6e728-3790-4191-ac64-be37e9c4d352"
  ,"Daniel Dugan":"c09c010a-8ed0-4a0a-ac63-f8a2047c3dc3"
  #,"Lucas Thompson":"03325efb-8f2a-4244-96e2-51c168073773"
  #,"Gennarro Melia":"1d56d01e-8822-47b1-867d-7ef4c5d7bfe9"
  #,"":""
  #,"":""
}

# ---- END CUSTOMIZATION SECTION ----

def is_date_in_past(date_string):
  # isolate first three tokens in date string
  date_clean = ' '.join(date_string.split(' ')[0:3])
  
  date_object = datetime.strptime(date_clean, "%b %d, %Y")
  # Get the current date and time
  current_date = datetime.now()

  # Compare the dates
  return date_object < current_date


searchedWrestlers=[];
for id in ids.values():
  url = "https://www.flowrestling.org/athletes/"+id+"/placements"
  page = urlopen(url)
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")
  
  soup=BeautifulSoup(html,'html.parser')
  name=soup.find('div', attrs={'data-test':'athlete-header-title'}).get_text()
  searchedWrestlers.append(name)
  
  li_tags=soup.find_all("li")
  in_qual=False
  for li_tag in li_tags:
    if curYear in li_tag.text  and "USAW-NJ Qualifier" in li_tag.text and curDivision in li_tag.text:
      in_qual=True
      print('\n',Style.BRIGHT,Fore.CYAN)
      print(name,Style.NORMAL,Fore.WHITE)
      searchedWrestlers.remove(name)
      break

  if in_qual:
    for li_tag in li_tags:
      if curYear in li_tag.text  and "USAW-NJ Qualifier" in li_tag.text and curDivision in li_tag.text:
        if is_date_in_past(li_tag.text.strip()):
          print(Fore.LIGHTBLACK_EX,end='')
        elif featuredEvent in li_tag.text:
          print(Fore.LIGHTYELLOW_EX,end='')
        else:
          print(Fore.LIGHTMAGENTA_EX,end='')
        print(li_tag.text.strip(),Fore.WHITE)
  
    for li_tag in li_tags:
      if "USAW-NJ Kids Scholastic State Championships" in li_tag.text:
        print(Fore.LIGHTBLACK_EX,end='')
        print("Previous year:",li_tag.text.strip(),Fore.WHITE)

print(Fore.LIGHTBLACK_EX,"\nTracked wrestlers not listed:",Fore.WHITE);
for oneName in searchedWrestlers[:-1]:
    print(oneName, end=", ")
print(searchedWrestlers[-1])

print(Fore.LIGHTBLACK_EX,end='')
print("\nOperation complete...")
