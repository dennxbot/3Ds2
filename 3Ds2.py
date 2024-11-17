from serpapi import GoogleSearch
import random
import ctypes

# ASCII Banner
BANNER = """
\033[1;32m

██████╗ ██████╗ ███████╗██████╗      ██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗    ██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗██████╗ 
╚════██╗██╔══██╗██╔════╝╚════██╗    ██╔════╝ ██╔═══██╗██╔═══██╗██╔════╝ ██║     ██╔════╝    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
 █████╔╝██║  ██║███████╗ █████╔╝    ██║  ███╗██║   ██║██║   ██║██║  ███╗██║     █████╗      ██║  ██║██║   ██║██████╔╝█████╔╝ █████╗  ██████╔╝
 ╚═══██╗██║  ██║╚════██║██╔═══╝     ██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝      ██║  ██║██║   ██║██╔══██╗██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝██████╔╝███████║███████╗    ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗    ██████╔╝╚██████╔╝██║  ██║██║  ██╗███████╗██║  ██║
╚═════╝ ╚═════╝ ╚══════╝╚══════╝     ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝


\033[0m
"""

# Embedded SerpAPI keys
API_KEYS = [
    "d2e42bb059244b6172549e1275a3e1a8456e9015ffb977489a0f33b165a89a7d",
    "bb2afb740b6b3843a7a9dee1ce6c48f59f2bb12217dc73c6689392658542799c",
    "557d7a2d169ed0ba5292eff9546c359dcddf25f203f570aa351356414d04b09a",
    "60026f1ab05c25d5c6f413165b6c4804b52168ad03ffcb2b358de1fa0055ed48",
    "ec6a2fc54cb2410d841eaca7a85737195416b500ecd47ef6781b240b390be16a",
    "6976f506d93be3d5e48978eb31bc5cff15dd6a01661997720fa95f1b566d0804",
    "79d34d191555dca28e0e063595b0d74363054ee0530976f27e0db5516875ffc1",
    "25f3e50404d940a8fd0dc30fcf9511e2160b04c6ebcfbda3edf3c2ea77dcb4b7",
]

# Randomly choose one API key for this session
chosen_api_key = random.choice(API_KEYS)
chosen_key_index = API_KEYS.index(chosen_api_key) + 1  # Get the index of the key for display


def enable_fullscreen():
    """
    Set the console window to fullscreen mode (Windows).
    """
    try:
        # Windows-specific fullscreen
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 3)
    except Exception as e:
        print(f"[ERROR] Failed to enable fullscreen: {e}")


def print_author_info():
    """
    Prints the author and motto section in a centered, styled format.
    """
    # Author and Motto
    author = "Author: Mark Angelo Doctolero"
    motto = "Simplicity is the ultimate hack."

    # Define the border width
    border_width = 60
    border = "*" * border_width

    # Center the text within the border
    author_line = f"* {author.center(border_width - 4)} *"
    motto_line = f"* {motto.center(border_width - 4)} *"

    # Print the styled section
    print(f"\033[1;34m{border}\033[0m")
    print(f"\033[1;32m{author_line}\033[0m")
    print(f"\033[1;33m{motto_line}\033[0m")
    print(f"\033[1;34m{border}\033[0m\n")


def search_dork(dork_query, total_results, location):
    """
    Perform a Google Dork search using a single API key to fetch up to `total_results` results.
    """
    print(f"[INFO] Searching with dork: {dork_query} in location: {location}")
    results = []  # Store results

    while len(results) < total_results:
        # Parameters for the SerpAPI request
        params = {
            "engine": "google",
            "q": dork_query,
            "num": 10,
            "location": location,
            "hl": "en",
            "api_key": chosen_api_key,
        }

        try:
            search = GoogleSearch(params)
            response = search.get_dict()
            for result in response.get("organic_results", []):
                link = result.get("link")
                if link:
                    results.append(link)
        except Exception as e:
            print(f"[ERROR] Failed to perform search: {e}")
            break

        print(f"[INFO] Collected {len(results)} results so far.")

    return results[:total_results]


def main():
    """
    Main function to handle user input and perform the dork search.
    """
    enable_fullscreen()  # Enable fullscreen mode

    print(BANNER)

    # Call the author info function
    print_author_info()

    print(f"[INFO] Using GEMINI ApiKey:#{chosen_key_index} for this session.")

    dork_query = input("Enter your Google Dork query (e.g., inurl:shop): ").strip()
    if not dork_query:
        print("[ERROR] Dork query cannot be empty!")
        return

    print("Select the target location:")
    print("1. United States (USA)")
    print("2. Australia (AU)")
    print("3. Canada (CA)")
    location_choice = input("Enter your choice (1/2/3): ").strip()

    if location_choice == "1":
        location = "United States"
    elif location_choice == "2":
        location = "Australia"
    elif location_choice == "3":
        location = "Canada"
    else:
        print("[ERROR] Invalid location choice. Please select 1, 2, or 3.")
        return

    try:
        total_results = int(input("Enter the number of results you want (max 100): ").strip())
        if total_results < 1 or total_results > 100:
            raise ValueError
    except ValueError:
        print("[ERROR] Please enter a valid number between 1 and 100.")
        return

    results = search_dork(dork_query, total_results, location)

    if results:
        print("\n[INFO] Found the following results:")
        for i, result in enumerate(results, start=1):
            print(f"{i}. \033[1;31m{result}\033[0m")
        with open("dork_results.txt", "w") as file:
            for result in results:
                file.write(result + "\n")
        print("\n[INFO] Results saved to dork_results.txt")
    else:
        print("[INFO] No results found.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Exiting... Goodbye!")
