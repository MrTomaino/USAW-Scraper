# USAW Scraper
# Copyright 2024 B. Michael Tomaino
# This program scrapes arena.flowrestling.org for wrestlers' registrations and placements in USAW qualifiers this year

from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Style, Fore

# ---- CUSTOMIZE VALUES BELOW ----

curYear = "2025"  # Modify for current year
featuredEvent = "Randolph"  # Modify to highlight an event in output
curDivision = "Novice 75"

# IDs for wrestlers
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
  ,"Leonidas Dunbar":"61a6e728-3790-4191-ac64-be37e9c4d352"
  ,"Daniel Dugan":"c09c010a-8ed0-4a0a-ac63-f8a2047c3dc3"
  ,"Lucas Thompson":"03325efb-8f2a-4244-96e2-51c168073773"
  ,"Gennarro Melia":"1d56d01e-8822-47b1-867d-7ef4c5d7bfe9"
  ,"Logan Yuhas":"831a700b-39f8-4161-9ff3-17772916dc94"
  ,"Sebastian Franco":"571a6d94-098c-4653-9fcd-72f859540b34"
  ,"Jaxon Perruso":"64e8123d-117e-43d7-812a-243728fc15de"
  ,"Emilian Norgaard":"9c3c3fef-d59f-427a-859c-872b00ef81a2"
  ,"Ayden Godfrey":"d13c7e38-8463-4b0f-a20b-c7848d3afc8b"
  ,"Joey Ferrante":"9a2cc9aa-93a6-4d16-9f84-21ba34071052"
  ,"Anthony Miano":"e38ab979-0c65-477a-b3fb-c3a211663f74"
  ,"Luis Rabelo":"41db3ddd-bf87-485a-88fa-bb6ce4fea46b"
  ,"Nicholas Petruzzi":"ecaa6f2a-e5a5-4853-a6b6-70daa3825bdd"
  ,"Kenny Zapantis":"6ef402ea-7bb0-44b5-8459-22225b76c9bb"
  ,"Michael Layton":"b2f4d6dd-a22f-4dad-afda-920df81c2b10"
  #,"":""
}


# Generate filename based on current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"featured_event_records_{current_time}.txt"

# Create and initialize the output file
with open(output_filename, "w") as file:
    file.write(f"Featured Event Records - {featuredEvent}\n")
    file.write("=" * 50 + "\n\n")


def is_date_in_past(date_string):
    """Check if the date in the string is in the past."""
    date_clean = " ".join(date_string.split(" ")[0:3])
    date_object = datetime.strptime(date_clean, "%b %d, %Y")
    current_date = datetime.now()
    return date_object < current_date


def output_record(file, name, events, last_year_performance, to_console=False):
    """Output the wrestler's record to both the console and the file."""
    header = f"Wrestler: {name}\n"
    separator = "=" * 50

    if to_console:
        print("\n", Style.BRIGHT, Fore.CYAN, header.strip(), Style.NORMAL, Fore.WHITE, sep="")
    else:
        file.write(header)

    for event in events:
        if featuredEvent in event:
            line = f"  Featured Event: {event}\n"
            if to_console:
                print(Fore.LIGHTYELLOW_EX, line.strip(), Fore.WHITE, sep="")
            else:
                file.write(line)
        else:
            line = f"  Other Event: {event}\n"
            if to_console:
                print(Fore.LIGHTMAGENTA_EX, line.strip(), Fore.WHITE, sep="")
            else:
                file.write(line)

    if last_year_performance:
        line = f"  Last Year's Performance: {last_year_performance}\n"
        if to_console:
            print(Fore.LIGHTBLACK_EX, line.strip(), Fore.WHITE, sep="")
        else:
            file.write(line)

    if not to_console:
        file.write("\n")


searchedWrestlers = []
for wrestler_name, wrestler_id in ids.items():
    url = f"https://www.flowrestling.org/athletes/{wrestler_id}/placements"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    name = soup.find("div", attrs={"data-test": "athlete-header-title"}).get_text()
    searchedWrestlers.append(name)

    li_tags = soup.find_all("li")
    events = []  # To store all relevant event appearances
    in_featured_event = False
    last_year_performance = None

    for li_tag in li_tags:
        event_text = li_tag.text.strip()

        # Check for current year and division events
        if curYear in event_text and "USAW-NJ Qualifier" in event_text and curDivision in event_text:
            events.append(event_text)
            if featuredEvent in event_text:
                in_featured_event = True

        # Check for last year's performance at championships
        if "USAW-NJ Kids Scholastic State Championships" in event_text:
            last_year_performance = event_text

    # Output both to the console and the file
    if in_featured_event:
        with open(output_filename, "a") as file:
            output_record(file, name, events, last_year_performance, to_console=False)
        output_record(None, name, events, last_year_performance, to_console=True)

#print(Fore.LIGHTBLACK_EX, "\nTracked wrestlers not listed:", Fore.WHITE)
#for oneName in searchedWrestlers[:-1]:
#    print(oneName, end=", ")
#print(searchedWrestlers[-1])

print(Fore.LIGHTBLACK_EX, end="")
print("\nOperation complete...")
