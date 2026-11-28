import httpx

DICTIONARY_API_URL="https://api.dictionaryapi.dev/api/v2/entries/en"

async def fetch_word_from_api(word:str):
    url=f"{DICTIONARY_API_URL}/{word}"


    async with httpx.AsyncClient() as client:
        response=await client.get(url)

    if response.status_code==404:
        return None


    response.raise_for_status()
    return response.json()