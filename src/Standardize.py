from fuzzywuzzy import fuzz, process

# TODO: Create a better map for fuzzy finding
__temporary_mapping = {
	"US DOLLARS": "USD",
	"EURO": "EUR",
	"STERLING POUNDS": "GBP",
	"JAPANESE YEN": "JPY",
	"SINGAPORE DOLLARS": "SGD",
	"AUSTRALIAN DOLLARS": "AUD",
	"SWISS FRANCS": "CHF",
	"KUWAITI DINARS": "KWD",
	"OMANI RIYALS": "OMR",
	"SAUDI ARABIAN RIYALS": "SAR",
	"UAE DIRHAMS": "AED",
	"QATAR RIYALS": "QAR",
	"JORDANIAN DINARS": "JOD",
	"BAHRAIN DINARS": "BHD",
	"INDIAN RUPEES": "INR",
	"CANADIAN DOLLAR": "CAD",
	"NEW ZEALAND DOLLARS": "NZD",
}

def __getBestMatch(query):
	best_match = process.extractOne(query, __temporary_mapping.keys(), scorer=fuzz.ratio)
	if best_match and best_match[1] >= 80:  # Adjust the similarity threshold as needed
		return best_match[0]
	return None

def convertToISO4217(currencyName: str):
	matching_currency_name = __getBestMatch(currencyName)
	if matching_currency_name:
		return __temporary_mapping[matching_currency_name]
	return None